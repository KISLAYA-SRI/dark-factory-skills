#!/usr/bin/env bash
#
# run-quality-gate.sh — run ONE root package.json script and return a parsed verdict.
#
# One script for every non-test gate. The command is a parameter.
#
#   bash run-quality-gate.sh format      # pnpm run format
#   bash run-quality-gate.sh lint:fix    # pnpm run lint:fix
#   bash run-quality-gate.sh lint        # pnpm run lint
#   bash run-quality-gate.sh build       # pnpm run build
#   bash run-quality-gate.sh <any root script>
#
# Tests are NOT run here — use the run-test-cases skill, which returns per-test
# detail and flaky detection a generic wrapper cannot.
#
# OPTIONS
#   --label <name>     Output folder name        (default: the gate name)
#   --timeout <secs>   Per-run timeout           (default: 900)
#   --repo-root <dir>  Override root detection
#   --quiet            Suppress the error list on stdout (still written to disk)
#
# OUTPUT
#   stdout    VERDICT line, counts, and up to 40 errors as: file:line  rule  message
#   files     .SS_WF/Agent/QUALITY_RUNS/<label>-<timestamp>/
#               raw.log       full command output
#               errors.txt    parsed errors only    (file<TAB>line<TAB>rule<TAB>message)
#               warnings.txt  parsed warnings only
#               summary.txt   key=value verdict block
#
# VERDICTS
#   PASS                 exit 0   clean
#   PASS_WITH_WARNINGS   exit 0   warnings only — ignore per project policy
#   FAIL                 exit 1   errors present, or non-zero exit with no parsed errors
#   SCRIPT_NOT_FOUND     exit 4   not in root package.json (lists what is available)
#   ENV_ERROR            exit 4   pnpm missing / repo root not found
#   TIMEOUT              exit 5

set -uo pipefail

EXIT_OK=0; EXIT_FAIL=1; EXIT_USAGE=2; EXIT_ENV=4; EXIT_TIMEOUT=5

GATE=""; LABEL=""; TIMEOUT=900; REPO_ROOT=""; QUIET=0

while [ $# -gt 0 ]; do
  case "$1" in
    --label)     LABEL="${2:-}"; shift 2 ;;
    --timeout)   TIMEOUT="${2:-900}"; shift 2 ;;
    --repo-root) REPO_ROOT="${2:-}"; shift 2 ;;
    --quiet)     QUIET=1; shift ;;
    -h|--help)   sed -n '2,40p' "$0"; exit $EXIT_OK ;;
    -*)          echo "ERROR: unknown option: $1" >&2; exit $EXIT_USAGE ;;
    *)           [ -z "$GATE" ] && GATE="$1" || { echo "ERROR: unexpected arg: $1" >&2; exit $EXIT_USAGE; }; shift ;;
  esac
done

if [ -z "$GATE" ]; then
  echo "ERROR: no gate given." >&2
  echo "Usage: bash run-quality-gate.sh <script-name> [--label X] [--timeout N]" >&2
  exit $EXIT_USAGE
fi
[ -z "$LABEL" ] && LABEL="$(printf '%s' "$GATE" | tr ':/ ' '-')"

# ── Repo root ───────────────────────────────────────────────────────────────
is_root() { [ -f "$1/pnpm-workspace.yaml" ] || [ -f "$1/turbo.json" ]; }

# Search upward from cwd, and at each level also look one level down into common
# workspace sub-folders — the repo root is often <workspace>/src, not <workspace>.
find_root() {
  local dir="$1" nested c
  while :; do
    if is_root "$dir"; then printf '%s' "$dir"; return 0; fi
    for nested in src Src repo app; do
      c="$dir/$nested"
      if [ -d "$c" ] && is_root "$c"; then printf '%s' "$c"; return 0; fi
    done
    [ "$dir" = "/" ] && return 1
    dir="$(dirname "$dir")"
  done
}

if [ -n "$REPO_ROOT" ]; then
  [ -d "$REPO_ROOT" ] || { echo "ERROR: --repo-root not a directory: $REPO_ROOT" >&2; exit $EXIT_ENV; }
  ROOT="$(cd "$REPO_ROOT" && pwd)"
else
  ROOT="$(find_root "$(pwd)")" || {
    echo "VERDICT=ENV_ERROR"
    echo "REASON=Repository root not found (no pnpm-workspace.yaml or turbo.json). Pass --repo-root."
    exit $EXIT_ENV
  }
fi

command -v pnpm >/dev/null 2>&1 || { echo "VERDICT=ENV_ERROR"; echo "REASON=pnpm not on PATH"; exit $EXIT_ENV; }
[ -f "$ROOT/package.json" ] || { echo "VERDICT=ENV_ERROR"; echo "REASON=No package.json at $ROOT"; exit $EXIT_ENV; }

# ── Script must exist ───────────────────────────────────────────────────────
HAS_SCRIPT=$(node -e '
  const fs=require("fs");
  const p=JSON.parse(fs.readFileSync(process.argv[1],"utf8")).scripts||{};
  process.stdout.write(p[process.argv[2]]?"yes":"no");
' "$ROOT/package.json" "$GATE" 2>/dev/null || echo "unknown")

if [ "$HAS_SCRIPT" = "no" ]; then
  AVAILABLE=$(node -e '
    const fs=require("fs");
    const p=JSON.parse(fs.readFileSync(process.argv[1],"utf8")).scripts||{};
    process.stdout.write(Object.keys(p).join(", "));
  ' "$ROOT/package.json" 2>/dev/null)
  echo "VERDICT=SCRIPT_NOT_FOUND"
  echo "REASON=Root package.json has no '$GATE' script"
  echo "AVAILABLE=$AVAILABLE"
  exit $EXIT_ENV
fi

# ── Output location ─────────────────────────────────────────────────────────
STAMP="$(date +%Y%m%d-%H%M%S)"
if [ -d "$ROOT/.SS_WF" ]; then
  OUT="$ROOT/.SS_WF/Agent/QUALITY_RUNS/${LABEL}-${STAMP}"
else
  OUT="$(mktemp -d "${TMPDIR:-/tmp}/quality-${LABEL}-XXXXXX")"
fi
mkdir -p "$OUT" || { echo "VERDICT=ENV_ERROR"; echo "REASON=Cannot create $OUT"; exit $EXIT_ENV; }
RAW="$OUT/raw.log"; ERRORS="$OUT/errors.txt"; WARNINGS="$OUT/warnings.txt"; SUMMARY="$OUT/summary.txt"
: > "$ERRORS"; : > "$WARNINGS"

# ── Run ─────────────────────────────────────────────────────────────────────
START=$(date +%s)
if command -v timeout >/dev/null 2>&1; then
  ( cd "$ROOT" && CI=true FORCE_COLOR=0 NO_COLOR=1 TURBO_UI=false \
      timeout "$TIMEOUT" pnpm run "$GATE" ) >"$RAW" 2>&1
  STATUS=$?
else
  ( cd "$ROOT" && CI=true FORCE_COLOR=0 NO_COLOR=1 TURBO_UI=false \
      pnpm run "$GATE" ) >"$RAW" 2>&1
  STATUS=$?
fi
DURATION=$(( $(date +%s) - START ))

# Strip ANSI so the parser sees clean text
if command -v perl >/dev/null 2>&1; then
  perl -pe 's/\e\[[0-9;?]*[A-Za-z]//g' "$RAW" > "$RAW.clean" && mv "$RAW.clean" "$RAW"
else
  sed -i'' -e 's/\x1b\[[0-9;?]*[A-Za-z]//g' "$RAW" 2>/dev/null || true
fi

if [ "$STATUS" -eq 124 ]; then
  { echo "VERDICT=TIMEOUT"; echo "GATE=$GATE"; echo "TIMEOUT_S=$TIMEOUT"; echo "LOG=$RAW"; } | tee "$SUMMARY"
  exit $EXIT_TIMEOUT
fi

# ── Parse ───────────────────────────────────────────────────────────────────
# Normalises ESLint stylish, tsc, Next.js and generic compiler output into:
#   file <TAB> line <TAB> rule <TAB> message        (severity routed to two files)
node - "$RAW" "$ERRORS" "$WARNINGS" <<'NODE'
const fs = require("fs");
const [, , rawPath, errPath, warnPath] = process.argv;
const lines = fs.readFileSync(rawPath, "utf8").split(/\r?\n/);

const errors = [], warnings = [];
const seen = new Set();
let currentFile = null;

const push = (sev, file, line, rule, msg) => {
  file = (file || "").trim().replace(/^\.\//, ""); msg = (msg || "").trim();
  if (!msg) return;
  // Ignore summary/footer noise that is not a real diagnostic
  if (/^(✖|✓|√|×)?\s*\d+\s+problems?\b/.test(msg)) return;
  if (/^(Found \d+ error|Lint|Done in|ELIFECYCLE|Command failed)/i.test(msg)) return;
  const key = `${sev}|${file}|${line}|${rule}|${msg}`;
  if (seen.has(key)) return;
  seen.add(key);
  (sev === "error" ? errors : warnings).push([file, line || "", rule || "", msg].join("\t"));
};

for (const raw of lines) {
  const line = raw.replace(/\s+$/, "");
  if (!line.trim()) { continue; }

  // ESLint stylish: a bare path line starts a file block
  const fileHeader = line.match(/^(?:\s*)((?:\/|\.{0,2}\/|[A-Za-z]:\\)?[\w.@\-/\\]+\.(?:ts|tsx|js|jsx|mjs|cjs|json|css|scss|md))\s*$/);
  if (fileHeader) { currentFile = fileHeader[1]; continue; }

  // ESLint stylish body:  12:5  error  Message  rule/name
  const stylish = line.match(/^\s*(\d+):(\d+)\s+(error|warning)\s+(.*?)(?:\s\s+([\w@/\-.]+))?\s*$/);
  if (stylish && currentFile) {
    push(stylish[3], currentFile, stylish[1], stylish[5] || "", stylish[4]);
    continue;
  }

  // Compact / tsc / Next:  path(12,5): error TS2345: Message
  //                        path:12:5: error: Message
  const compact = line.match(
    /^\s*(?:\[\d+\/\d+\]\s*)?([^\s(:][^(:]*\.(?:ts|tsx|js|jsx|mjs|cjs))[(:](\d+)[,:](\d+)\)?:?\s*(error|warning)\s*(TS\d+)?:?\s*(.*)$/i
  );
  if (compact) {
    push(compact[4].toLowerCase(), compact[1], compact[2], compact[5] || "", compact[6]);
    continue;
  }

  // Next.js / webpack block:  ./path/file.tsx  then  Type error: ...
  const nextFile = line.match(/^\s*\.?\/([\w.@\-/\\]+\.(?:ts|tsx|js|jsx))\s*$/);
  if (nextFile) { currentFile = nextFile[1]; continue; }
  const typeErr = line.match(/^\s*(Type error|Syntax error|Error):\s*(.*)$/i);
  if (typeErr) { push("error", currentFile || "", "", "", typeErr[2]); continue; }

  // Bare "error ..." / "warning ..." lines with no file context
  const bare = line.match(/^\s*(error|warning)\b[:\s]+(.*)$/i);
  if (bare && bare[2].length > 3) { push(bare[1].toLowerCase(), currentFile || "", "", "", bare[2]); }
}

fs.writeFileSync(errPath, errors.join("\n") + (errors.length ? "\n" : ""));
fs.writeFileSync(warnPath, warnings.join("\n") + (warnings.length ? "\n" : ""));
NODE

count_lines() { [ -s "$1" ] && grep -c . "$1" 2>/dev/null | head -1 | tr -d ' \n' || printf '0'; }
ERR_COUNT=$(count_lines "$ERRORS");  ERR_COUNT=${ERR_COUNT:-0}
WARN_COUNT=$(count_lines "$WARNINGS"); WARN_COUNT=${WARN_COUNT:-0}
ERR_FILES=$(cut -f1 "$ERRORS" 2>/dev/null | grep -v '^$' | sort -u | wc -l | tr -d ' \n')
ERR_FILES=${ERR_FILES:-0}

# ── Verdict ─────────────────────────────────────────────────────────────────
if [ "$ERR_COUNT" -gt 0 ]; then
  VERDICT="FAIL"; REASON="$ERR_COUNT error(s) in $ERR_FILES file(s)"; CODE=$EXIT_FAIL
elif [ "$STATUS" -ne 0 ]; then
  VERDICT="FAIL"
  REASON="Command exited $STATUS but no errors were parsed — read raw.log (tooling or config failure)"
  CODE=$EXIT_FAIL
elif [ "$WARN_COUNT" -gt 0 ]; then
  VERDICT="PASS_WITH_WARNINGS"; REASON="$WARN_COUNT warning(s) — ignored per policy"; CODE=$EXIT_OK
else
  VERDICT="PASS"; REASON="Clean"; CODE=$EXIT_OK
fi

{
  echo "VERDICT=$VERDICT"
  echo "GATE=$GATE"
  echo "COMMAND=pnpm run $GATE"
  echo "REPO_ROOT=$ROOT"
  echo "EXIT_CODE=$STATUS"
  echo "DURATION_S=$DURATION"
  echo "ERRORS=$ERR_COUNT"
  echo "WARNINGS=$WARN_COUNT"
  echo "ERROR_FILES=$ERR_FILES"
  echo "REASON=$REASON"
  echo "OUTPUT_DIR=$OUT"
} | tee "$SUMMARY"

if [ "$ERR_COUNT" -gt 0 ] && [ "$QUIET" -eq 0 ]; then
  echo "ERRORS_START"
  awk -F'\t' 'NR<=40 { printf "%s:%s  %s  %s\n", ($1==""?"?":$1), ($2==""?"?":$2), ($3==""?"-":$3), $4 }' "$ERRORS"
  [ "$ERR_COUNT" -gt 40 ] && echo "... $((ERR_COUNT - 40)) more — see $ERRORS"
  echo "ERRORS_END"
fi

exit $CODE
