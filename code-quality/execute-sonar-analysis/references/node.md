# Execute SonarQube Analysis — Node.js / React

## Prerequisites

- The target project must be a Node-based project (a `package.json` must exist at the project root or workspace/package root). This reference does not apply to Java/Maven projects — see `maven.md` for those.
- A `sonar-project.properties` file (or equivalent scanner configuration) should already define `sonar.sources`, `sonar.tests`, and any `sonar.exclusions`/`sonar.coverage.exclusions` for the project. If it does not exist, do not invent broad defaults — confirm the intended source/test paths first.
- For coverage to be included in the analysis, the project's test runner (Jest/Vitest) must already be configured to emit an LCOV report (see the `fix-sonar-issues` Coverage reference for setup details); this skill does not configure the test runner, only runs the scan.
- `SONAR_PROJECT_ID`, `SONAR_URL`, and `SONAR_TOKEN` must be available as environment variables (see the main `SKILL.md` for how to obtain these).

## Preferred: Run via the script

Do not invoke `npx sonar-scanner` directly by default — `npx` re-resolves and can re-download the `sonar-scanner` npm package on every invocation unless it is already cached, which makes the run non-deterministic and slower than necessary. Instead, use [`../scripts/execute-sonar.sh`](../scripts/execute-sonar.sh), which encodes a deterministic resolution order and only falls back to `npx` when nothing else is available:

```bash
SONAR_PROJECT_ID=<<SONAR_PROJECT_ID>> \
SONAR_URL=<<SONAR_URL>> \
SONAR_TOKEN=<<SONAR_TOKEN>> \
../scripts/execute-sonar.sh <<NODE_PROJECT_ROOT>>
```

## Scanner Resolution Order (what the script does)

For a Node/React project (`package.json` present, no `pom.xml`), the script resolves the `sonar-scanner` binary in this order, from most to least deterministic:

1. **`sonar-scanner` on `PATH`** — a scanner CLI already installed globally or provisioned by the CI runner/base image. No download, fully deterministic across runs.
2. **`node_modules/.bin/sonar-scanner`** — a scanner CLI installed as a project devDependency (e.g., `sonarqube-scanner` or `@sonar/scan` in `package.json`). No download at run time; the version is pinned by the repo's lockfile, which is the preferred way to make this reproducible for a specific project.
3. **`npx --yes sonar-scanner`** — last-resort fallback only, used when neither of the above is found. This may fetch the package from the npm registry on every run if it is not already cached locally, and its resolved version can drift over time unless a version is pinned inline (e.g., `npx --yes sonar-scanner@x.y.z`). The script prints an explicit warning whenever this path is taken so the non-determinism is visible in the run log.

If a project is expected to run this analysis repeatedly (CI, frequent local runs), add `sonar-scanner`-compatible tooling as a devDependency or ensure it is present on the execution image's `PATH` so resolution steps 1–2 apply instead of the `npx` fallback.

## Underlying Command (what the script runs, once a scanner binary is resolved)

```bash
<resolved-scanner-binary> \
  -Dsonar.projectKey=<<SONAR_PROJECT_ID>> \
  -Dsonar.host.url=<<SONAR_URL>> \
  -Dsonar.token=<<SONAR_TOKEN>> \
  -Dsonar.qualitygate.wait=true
```

Where `<resolved-scanner-binary>` is `sonar-scanner`, `node_modules/.bin/sonar-scanner`, or `npx --yes sonar-scanner`, per the resolution order above.

- `-Dsonar.projectKey` identifies the project on the SonarQube server (`SONAR_PROJECT_ID`).
- `-Dsonar.host.url` points the analysis at the correct SonarQube server instance (`SONAR_URL`).
- `-Dsonar.token` authenticates the analysis publish call (`SONAR_TOKEN`). This is the current recommended flag name for the SonarScanner CLI; some older setups may still use `-Dsonar.login` — follow the project's existing convention if one is already established, and update the script rather than diverging between the script and this document.
- `-Dsonar.qualitygate.wait=true` makes the scanner block until the quality gate result is available and exit non-zero if the quality gate does not pass.

## Alternative: via an existing npm script

If the project already wraps the scanner in an npm script (commonly `sonar` or `sonar-scan` in `package.json`) that itself resolves a locally installed CLI, prefer running that script instead of calling `scripts/execute-sonar.sh`, passing the same required values through environment variables or CLI arguments consistent with how the script is defined:

```bash
npm run sonar -- \
  -Dsonar.projectKey=<<SONAR_PROJECT_ID>> \
  -Dsonar.host.url=<<SONAR_URL>> \
  -Dsonar.token=<<SONAR_TOKEN>> \
  -Dsonar.qualitygate.wait=true
```

Do not create a new npm script for this unless explicitly asked; use the existing one if present, or use `scripts/execute-sonar.sh` otherwise.

## Notes

- For yarn/pnpm workspaces, run the script from the workspace/package root that owns the `sonar-project.properties` for the target package, not necessarily the monorepo root, unless the analysis is intentionally configured at the monorepo level.
- If no `sonar-project.properties` exists and the project instead configures the scanner via `package.json` (`sonar` key) or CI pipeline flags, use that existing configuration source instead of introducing a new one.
- `SONAR_URL` reachability and `SONAR_TOKEN`/`SONAR_PROJECT_ID` validity are the first things to check if the scan step itself fails (as opposed to a prior lint/build/test failure in the project's own pipeline, if the scan is chained after those steps).
- `SONAR_EXTRA_ARGS` can be exported before running the script to append additional `-D` flags without editing the script.
