# Execute SonarQube Analysis — Node.js / React

## Prerequisites

- The target project must be a Node-based project (a `package.json` must exist at the project root or workspace/package root).
- The SonarQube/SonarCloud scanner CLI must be resolvable — either as a dev dependency (`sonarqube-scanner` / `@sonar/scan`) with an npm script, or invokable directly via `npx sonar-scanner` / `npx @sonar/scan` if the SonarScanner CLI is installed or fetchable.
- A `sonar-project.properties` file (or equivalent scanner configuration) should already define `sonar.sources`, `sonar.tests`, and any `sonar.exclusions`/`sonar.coverage.exclusions` for the project. If it does not exist, do not invent broad defaults — confirm the intended source/test paths first.
- For coverage to be included in the analysis, the project's test runner (Jest/Vitest) must already be configured to emit an LCOV report (see the `fix-sonar-issues` Coverage reference for setup details); this skill does not configure the test runner, only runs the scan.
- `SONAR_PROJECT_ID`, `SONAR_URL`, and `SONAR_TOKEN` must be available (see the main `SKILL.md` for how to obtain these).

## Command

Run the analysis from the project/workspace root (the directory containing the relevant `package.json` and `sonar-project.properties`) using the SonarScanner CLI via `npx`:

```bash
npx sonar-scanner \
  -Dsonar.projectKey=<<SONAR_PROJECT_ID>> \
  -Dsonar.host.url=<<SONAR_URL>> \
  -Dsonar.token=<<SONAR_TOKEN>> \
  -Dsonar.qualitygate.wait=true
```

Substitute `<<SONAR_PROJECT_ID>>`, `<<SONAR_URL>>`, and `<<SONAR_TOKEN>>` with the actual values provided for the task.

- `npx sonar-scanner` runs the SonarScanner CLI, resolving it from the project's dev dependencies if present, or fetching it on demand otherwise.
- `-Dsonar.projectKey` identifies the project on the SonarQube server (`SONAR_PROJECT_ID`).
- `-Dsonar.host.url` points the analysis at the correct SonarQube server instance (`SONAR_URL`).
- `-Dsonar.token` authenticates the analysis publish call (`SONAR_TOKEN`). This is the current recommended flag name for the SonarScanner CLI; some older setups may still use `-Dsonar.login` — follow the project's existing convention if one is already established.
- `-Dsonar.qualitygate.wait=true` makes the scanner block until the quality gate result is available and exit non-zero if the quality gate does not pass.

## Alternative: via an npm script

If the project already wraps the scanner in an npm script (commonly `sonar` or `sonar-scan` in `package.json`), prefer running that script instead of invoking `npx sonar-scanner` directly, passing the same required values through environment variables or CLI arguments consistent with how the script is defined:

```bash
npm run sonar -- \
  -Dsonar.projectKey=<<SONAR_PROJECT_ID>> \
  -Dsonar.host.url=<<SONAR_URL>> \
  -Dsonar.token=<<SONAR_TOKEN>> \
  -Dsonar.qualitygate.wait=true
```

Do not create a new npm script for this unless explicitly asked; use the existing one if present, or fall back to the direct `npx sonar-scanner` command above.

## Notes

- For yarn/pnpm workspaces, run the command from the workspace/package root that owns the `sonar-project.properties` for the target package, not necessarily the monorepo root, unless the analysis is intentionally configured at the monorepo level.
- If no `sonar-project.properties` exists and the project instead configures the scanner via `package.json` (`sonar` key) or CI pipeline flags, use that existing configuration source instead of introducing a new one.
- `SONAR_URL` reachability and `SONAR_TOKEN`/`SONAR_PROJECT_ID` validity are the first things to check if the scan step itself fails (as opposed to a prior lint/build/test failure in the project's own pipeline, if the scan is chained after those steps).
