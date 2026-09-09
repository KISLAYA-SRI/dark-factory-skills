#!/usr/bin/env bash
#
# execute-sonar.sh
#
# Deterministic SonarQube analysis runner for both Maven (Java) and
# Node.js/React projects. Detects the project type from the target
# directory and invokes the correct, pinned analysis command.
#
# Detection / resolution order:
#   1. Maven project  -> pom.xml present at TARGET_DIR         -> `mvn verify sonar:sonar`
#   2. Node project    -> package.json present at TARGET_DIR    -> resolve a scanner binary in this order:
#        a. Locally installed CLI on PATH           (`command -v sonar-scanner`)
#        b. Project-local devDependency binary       (`node_modules/.bin/sonar-scanner`)
#        c. Fallback: `npx --yes sonar-scanner`      (downloads on demand; last resort only)
#   3. Neither found   -> fail with a clear error instead of guessing.
#
# Required environment variables (never hardcode these):
#   SONAR_PROJECT_ID  - SonarQube project key
#   SONAR_URL         - SonarQube server base URL
#   SONAR_TOKEN       - SonarQube authentication token
#
# Optional environment variables:
#   TARGET_DIR        - project/module root to analyze (default: current directory)
#   SONAR_EXTRA_ARGS  - additional space-separated -D flags appended to the command
#
# Usage:
#   SONAR_PROJECT_ID=my-service \
#   SONAR_URL=https://sonar.example.com \
#   SONAR_TOKEN=xxxx \
#   ./execute-sonar.sh [target_dir]
#
# Exit codes:
#   0  - analysis ran and the quality gate passed
#   1  - missing prerequisite (env var, project type, tool)
#   2  - build/analysis failed (compile/test/lint failure or quality gate failure)
#
set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve target directory
# ---------------------------------------------------------------------------
TARGET_DIR="${1:-${TARGET_DIR:-$(pwd)}}"

if [[ ! -d "${TARGET_DIR}" ]]; then
  echo "[execute-sonar] ERROR: target directory does not exist: ${TARGET_DIR}" >&2
  exit 1
fi

cd "${TARGET_DIR}"
echo "[execute-sonar] Target directory: $(pwd)"

# ---------------------------------------------------------------------------
# Validate required environment variables
# ---------------------------------------------------------------------------
missing_vars=()
[[ -z "${SONAR_PROJECT_ID:-}" ]] && missing_vars+=("SONAR_PROJECT_ID")
[[ -z "${SONAR_URL:-}" ]] && missing_vars+=("SONAR_URL")
[[ -z "${SONAR_TOKEN:-}" ]] && missing_vars+=("SONAR_TOKEN")

if [[ ${#missing_vars[@]} -gt 0 ]]; then
  echo "[execute-sonar] ERROR: missing required environment variable(s): ${missing_vars[*]}" >&2
  echo "[execute-sonar] Set SONAR_PROJECT_ID, SONAR_URL, and SONAR_TOKEN before running this script." >&2
  exit 1
fi

# Never print the token itself.
echo "[execute-sonar] SONAR_PROJECT_ID=${SONAR_PROJECT_ID}"
echo "[execute-sonar] SONAR_URL=${SONAR_URL}"
echo "[execute-sonar] SONAR_TOKEN=****"

EXTRA_ARGS="${SONAR_EXTRA_ARGS:-}"

# ---------------------------------------------------------------------------
# 1. Maven (Java) project
# ---------------------------------------------------------------------------
if [[ -f "pom.xml" ]]; then
  echo "[execute-sonar] Detected project type: Maven (pom.xml found)"

  if ! command -v mvn >/dev/null 2>&1; then
    echo "[execute-sonar] ERROR: pom.xml found but 'mvn' is not on PATH." >&2
    exit 1
  fi

  echo "[execute-sonar] Running: mvn verify sonar:sonar ..."
  # shellcheck disable=SC2086
  mvn verify sonar:sonar \
    -Dsonar.projectKey="${SONAR_PROJECT_ID}" \
    -Dsonar.host.url="${SONAR_URL}" \
    -Dsonar.login="${SONAR_TOKEN}" \
    -DargLine="-XX:+EnableDynamicAgentLoading" \
    -Dsonar.qualitygate.wait=true \
    ${EXTRA_ARGS} \
  || { echo "[execute-sonar] Maven build/analysis failed or quality gate did not pass." >&2; exit 2; }

  echo "[execute-sonar] Maven analysis completed and quality gate passed."
  exit 0
fi

# ---------------------------------------------------------------------------
# 2. Node.js / React project
# ---------------------------------------------------------------------------
if [[ -f "package.json" ]]; then
  echo "[execute-sonar] Detected project type: Node/React (package.json found)"

  SCANNER_CMD=()

  # 2a. Prefer a scanner already available on PATH (deterministic, no download).
  if command -v sonar-scanner >/dev/null 2>&1; then
    echo "[execute-sonar] Using globally installed sonar-scanner CLI on PATH."
    SCANNER_CMD=("sonar-scanner")

  # 2b. Prefer a project-local devDependency binary (deterministic, version-pinned by the repo).
  elif [[ -x "node_modules/.bin/sonar-scanner" ]]; then
    echo "[execute-sonar] Using project-local node_modules/.bin/sonar-scanner."
    SCANNER_CMD=("node_modules/.bin/sonar-scanner")

  # 2c. Last resort: npx, which may download the package on demand.
  else
    if ! command -v npx >/dev/null 2>&1; then
      echo "[execute-sonar] ERROR: no sonar-scanner CLI found on PATH or in node_modules/.bin, and 'npx' is not available." >&2
      exit 1
    fi
    echo "[execute-sonar] WARNING: no local/global sonar-scanner CLI found. Falling back to 'npx --yes sonar-scanner'."
    echo "[execute-sonar] WARNING: this fallback may download the sonar-scanner package on every run. Install it as a devDependency or on PATH for a deterministic, repeatable run."
    SCANNER_CMD=("npx" "--yes" "sonar-scanner")
  fi

  echo "[execute-sonar] Running: ${SCANNER_CMD[*]} ..."
  # shellcheck disable=SC2086
  "${SCANNER_CMD[@]}" \
    -Dsonar.projectKey="${SONAR_PROJECT_ID}" \
    -Dsonar.host.url="${SONAR_URL}" \
    -Dsonar.token="${SONAR_TOKEN}" \
    -Dsonar.qualitygate.wait=true \
    ${EXTRA_ARGS} \
  || { echo "[execute-sonar] Sonar scan failed or quality gate did not pass." >&2; exit 2; }

  echo "[execute-sonar] Node/React analysis completed and quality gate passed."
  exit 0
fi

# ---------------------------------------------------------------------------
# 3. Neither Maven nor Node project detected
# ---------------------------------------------------------------------------
echo "[execute-sonar] ERROR: no pom.xml or package.json found in ${TARGET_DIR}." >&2
echo "[execute-sonar] This script supports Maven (Java) and Node.js/React projects only." >&2
exit 1
