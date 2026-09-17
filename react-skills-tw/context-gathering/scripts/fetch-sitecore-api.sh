#!/usr/bin/env bash
#
# fetch-sitecore-api.sh
#
# Fetches the Sitecore Layout/API JSON for a story and writes it to the canonical
# context path. Used by the Context Gathering phase of the FE Story Analysis Agent.
#
# The Sitecore endpoint uses a self-signed / internal certificate, so -k is applied
# INSIDE this script. Callers must not pass TLS flags.
#
# USAGE
#   bash scripts/fetch-sitecore-api.sh "<complete-endpoint-url>" [output-path]
#
# ARGUMENTS
#   $1  Complete Sitecore endpoint URL (required) — must be the full endpoint,
#       including scheme, host, path and any query string.
#   $2  Output file path (optional) — defaults to ./.SC_API_SPEC/sitecore-api.json
#
# EXIT CODES
#   0  Success — valid JSON written to the output path
#   1  Usage error — missing or malformed endpoint argument
#   2  Network/transport failure — host unreachable, DNS failure, timeout
#   3  HTTP error — non-2xx status returned by the endpoint
#   4  Invalid payload — response was empty or not parseable JSON
#   5  Filesystem error — could not create directory or write the output file
#
# GUARANTEE
#   On ANY failure the output file is NOT created or modified. A partial, empty,
#   or error-payload file is never left behind. The Context Validation phase treats
#   an unreadable or empty artefact as "not materialised", so this script must fail
#   cleanly rather than write junk.

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration — TLS and transport flags live here, not in the caller
# ---------------------------------------------------------------------------
readonly CURL_INSECURE="-k"          # endpoint uses an internal/self-signed cert
readonly CURL_SILENT="-sS"           # silent, but still surface errors
readonly CONNECT_TIMEOUT=15          # seconds to establish a connection
readonly MAX_TIME=60                 # seconds for the whole transfer
readonly MAX_REDIRECTS=5

readonly DEFAULT_OUTPUT="./.SC_API_SPEC/sitecore-api.json"

# ---------------------------------------------------------------------------
# Arguments
# ---------------------------------------------------------------------------
if [[ $# -lt 1 || -z "${1:-}" ]]; then
  echo "ERROR: Sitecore endpoint URL is required." >&2
  echo "Usage: bash scripts/fetch-sitecore-api.sh \"<complete-endpoint-url>\" [output-path]" >&2
  exit 1
fi

ENDPOINT="$1"
OUTPUT_PATH="${2:-$DEFAULT_OUTPUT}"

if [[ ! "$ENDPOINT" =~ ^https?:// ]]; then
  echo "ERROR: Endpoint must be a complete URL starting with http:// or https://" >&2
  echo "       Received: $ENDPOINT" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Prepare output directory
# ---------------------------------------------------------------------------
OUTPUT_DIR="$(dirname "$OUTPUT_PATH")"
if ! mkdir -p "$OUTPUT_DIR" 2>/dev/null; then
  echo "ERROR: Could not create output directory: $OUTPUT_DIR" >&2
  exit 5
fi

# Stage into a temp file so the final path is only written on full success
TMP_BODY="$(mktemp 2>/dev/null)" || {
  echo "ERROR: Could not create temporary file." >&2
  exit 5
}
cleanup() { rm -f "$TMP_BODY" 2>/dev/null || true; }
trap cleanup EXIT

# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------
echo "Fetching Sitecore API..."
echo "  Endpoint: $ENDPOINT"
echo "  Output:   $OUTPUT_PATH"

set +e
HTTP_STATUS="$(
  curl $CURL_INSECURE $CURL_SILENT \
    --location \
    --max-redirs "$MAX_REDIRECTS" \
    --connect-timeout "$CONNECT_TIMEOUT" \
    --max-time "$MAX_TIME" \
    --header "Accept: application/json" \
    --output "$TMP_BODY" \
    --write-out "%{http_code}" \
    "$ENDPOINT" 2>/dev/null
)"
CURL_EXIT=$?
set -e

if [[ $CURL_EXIT -ne 0 ]]; then
  echo "ERROR: Transport failure contacting the Sitecore endpoint (curl exit $CURL_EXIT)." >&2
  case $CURL_EXIT in
     6) echo "       Could not resolve host." >&2 ;;
     7) echo "       Failed to connect to host." >&2 ;;
    28) echo "       Operation timed out." >&2 ;;
    35) echo "       TLS handshake failed." >&2 ;;
    *)  echo "       See curl exit code $CURL_EXIT for detail." >&2 ;;
  esac
  echo "       No artefact written." >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Validate HTTP status
# ---------------------------------------------------------------------------
if [[ ! "$HTTP_STATUS" =~ ^2[0-9][0-9]$ ]]; then
  echo "ERROR: Sitecore endpoint returned HTTP $HTTP_STATUS." >&2
  echo "       Expected a 2xx response. No artefact written." >&2
  exit 3
fi

# ---------------------------------------------------------------------------
# Validate payload is non-empty, parseable JSON
# ---------------------------------------------------------------------------
if [[ ! -s "$TMP_BODY" ]]; then
  echo "ERROR: Sitecore endpoint returned an empty body. No artefact written." >&2
  exit 4
fi

JSON_VALID=0
if command -v python3 >/dev/null 2>&1; then
  python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$TMP_BODY" >/dev/null 2>&1 && JSON_VALID=1
elif command -v python >/dev/null 2>&1; then
  python -c "import json,sys; json.load(open(sys.argv[1]))" "$TMP_BODY" >/dev/null 2>&1 && JSON_VALID=1
elif command -v jq >/dev/null 2>&1; then
  jq empty "$TMP_BODY" >/dev/null 2>&1 && JSON_VALID=1
else
  # No validator available — accept only if the body looks like JSON
  FIRST_CHAR="$(head -c 1 "$TMP_BODY")"
  [[ "$FIRST_CHAR" == "{" || "$FIRST_CHAR" == "[" ]] && JSON_VALID=1
  echo "WARNING: No JSON validator found (python3/python/jq). Shape-checked only." >&2
fi

if [[ $JSON_VALID -ne 1 ]]; then
  echo "ERROR: Response was not valid JSON. No artefact written." >&2
  echo "       First 200 bytes of the response:" >&2
  head -c 200 "$TMP_BODY" >&2 || true
  echo "" >&2
  exit 4
fi

# ---------------------------------------------------------------------------
# Commit — only now is the canonical path written
# ---------------------------------------------------------------------------
if ! cp "$TMP_BODY" "$OUTPUT_PATH" 2>/dev/null; then
  echo "ERROR: Could not write output file: $OUTPUT_PATH" >&2
  exit 5
fi

BYTES="$(wc -c < "$OUTPUT_PATH" | tr -d ' ')"
echo "SUCCESS: Sitecore API JSON written."
echo "  HTTP status: $HTTP_STATUS"
echo "  File:        $OUTPUT_PATH"
echo "  Size:        ${BYTES} bytes"
exit 0
