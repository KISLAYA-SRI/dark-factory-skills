---
name: execute-sonar-analysis
description: Use when running, triggering, or executing a SonarQube analysis for a Java Maven backend microservice/adapter library, or a Node.js/React/TypeScript frontend or backend project. Triggers include run sonar, execute sonar analysis, sonar scan, mvn sonar, sonar:sonar, sonar-scanner, npx sonar-scanner, trigger quality gate analysis, or publish analysis results to SonarQube.
---

# Execute SonarQube Analysis

Run a SonarQube analysis for a project and publish results to the configured SonarQube server. This skill supports two project families — **Maven (Java)** and **Node/React (npm/yarn/pnpm)** — and only executes the analysis; use the `fix-sonar-issues` skill to triage and remediate reported findings afterward.

## Preferred Execution Path: `scripts/execute-sonar.sh`

This skill ships a single deterministic script, [`scripts/execute-sonar.sh`](scripts/execute-sonar.sh), that performs project-type detection and tool resolution itself. **Prefer invoking this script over manually assembling a command.** It:

1. Detects the project type from the target directory: Maven (`pom.xml` present) or Node/React (`package.json` present).
2. For Maven, runs `mvn verify sonar:sonar` with the required flags.
3. For Node/React, resolves a scanner binary deterministically, in this order:
   a. A `sonar-scanner` CLI already on `PATH` (no download).
   b. A project-local `node_modules/.bin/sonar-scanner` devDependency binary (no download, version-pinned by the repo).
   c. Only as a last-resort fallback: `npx --yes sonar-scanner`, which may download the package on every run — the script prints a warning when this path is used.
4. Fails fast with a clear message if neither project type is detected, or if a required environment variable or tool is missing, instead of guessing.

Run it with the required environment variables already exported (never pass secrets as inline command-line literals from chat/task context):

```bash
SONAR_PROJECT_ID=<<SONAR_PROJECT_ID>> \
SONAR_URL=<<SONAR_URL>> \
SONAR_TOKEN=<<SONAR_TOKEN>> \
./scripts/execute-sonar.sh <<TARGET_DIR>>
```

`<<TARGET_DIR>>` is optional and defaults to the current directory; pass the Maven module root or the Node/React project/workspace root when analyzing a specific module in a multi-module or monorepo layout.

Use [`references/maven.md`](references/maven.md) and [`references/node.md`](references/node.md) only to understand *what the script does* under the hood (the exact flags, why each is required, and edge cases like flag-name differences across tool versions) — do not hand-assemble the command when the script is available and executable in the current environment.

## STEP 0: Detect Project Type (MANDATORY — Run First)

If the script cannot be run in the current environment (e.g., a sandboxed context without shell execution), fall back to manually determining which project family the target repository belongs to and building the command from the matching reference:

| Signal | Project Family | Reference Folder |
|---|---|---|
| `pom.xml` at the repo/module root | **Maven (Java)** | [`references/maven.md`](references/maven.md) |
| `package.json` at the repo root, no `pom.xml` at that level | **Node/React** | [`references/node.md`](references/node.md) |
| Both present (e.g., Java backend with an embedded frontend module) | **Mixed** | Run the script (or the matching reference command) once per module: Maven module root, then Node module root |

If detection is ambiguous (e.g., a monorepo with multiple modules and no clear target), ask which module/path to analyze before proceeding rather than guessing.

Once the project family is confirmed, load only the matching reference file(s) below for the exact command and flags — do not load both upfront.

## Required Values

The following values must be supplied before running the analysis for either project family. Never hardcode, guess, or reuse values from a different project/environment:

- **`SONAR_PROJECT_ID`** — the SonarQube project key to publish results under.
- **`SONAR_URL`** — the base URL of the SonarQube server.
- **`SONAR_TOKEN`** — the authentication token/login used to publish results.

If any of these values is missing from the current task context, ask for it explicitly before running the command. Do not fabricate placeholder values in the actual command execution.

## Execution Steps

1. Confirm `SONAR_PROJECT_ID`, `SONAR_URL`, and `SONAR_TOKEN` are available. If any is missing, request it before proceeding.
2. Run [`scripts/execute-sonar.sh`](scripts/execute-sonar.sh) with those three variables exported and the target project/module directory as the argument (defaults to the current directory). The script performs its own project-type detection and tool resolution — do not re-implement that logic manually when the script can be executed.
3. If script execution is not possible in the current environment, fall back to STEP 0 and the matching reference file (`references/maven.md` or `references/node.md`) to assemble the equivalent command manually.
4. Stream/monitor the build/scan output.
5. Wait for the quality gate result (the script and both reference commands include the flag that blocks until the quality gate outcome is known).
6. Capture and report the outcome, including which resolution path was used for Node/React (PATH, `node_modules/.bin`, or the `npx` fallback) since that affects run determinism.

For **Mixed** repositories, run the script once per module (Maven module root, then Node module root).

## Interpreting the Result

- **Success (exit code 0):** the analysis completed and the quality gate passed. Report the SonarQube dashboard link if printed in the output, along with a brief pass summary.
- **Failure due to quality gate:** the analysis published successfully but the quality gate failed. Report this clearly and distinguish it from a build/compile/lint failure. Do not attempt to fix findings as part of this skill — hand off to the `fix-sonar-issues` skill for triage and remediation.
- **Failure before the Sonar step runs (compile/test/lint failure):** the analysis did not run. Report the underlying build failure (compilation error, failing test, lint error, etc.) since that must be resolved first.
- **Failure at the Sonar step itself (connectivity/auth):** check `SONAR_URL` reachability and validity of `SONAR_TOKEN`/`SONAR_PROJECT_ID` before retrying.

## Rules

- Do not modify source code, tests, or configuration as part of running the analysis — this skill only triggers and reports the analysis.
- Do not hardcode `SONAR_PROJECT_ID`, `SONAR_URL`, or `SONAR_TOKEN` values into `pom.xml`, `package.json`, `sonar-project.properties`, the script, or any committed file. Export them as environment variables before invoking `scripts/execute-sonar.sh`, or pass them via the mechanism already used by the project's CI pipeline (e.g., CI/CD variables) if one exists.
- Prefer `scripts/execute-sonar.sh` over hand-assembling the Maven/npx command — it is the deterministic, single source of truth for tool resolution and flags. Only fall back to manually building the command from the reference files when the script genuinely cannot be executed.
- For the Node/React path, never jump straight to `npx sonar-scanner` if a `sonar-scanner` binary is already resolvable on `PATH` or in `node_modules/.bin` — the script already encodes this preference order to avoid unnecessary package downloads on every run.
- Do not remove or alter any of the required flags baked into the script, or in the reference command for the detected project family, unless the user explicitly requests a change.
- For multi-module Maven projects, run the script from the aggregator/root POM directory unless the task specifies a single module to analyze.
- For npm/yarn/pnpm monorepos (workspaces), run the script from the workspace/package root that owns the relevant `sonar-project.properties`, unless the task specifies a different scope.
- If the project's existing CI pipeline (e.g., `.gitlab-ci.yml`, GitHub Actions workflow) already defines an equivalent Sonar stage, prefer aligning with its parameters and only run locally when explicitly asked to.

## Result

Report:

- Detected project family (Maven, Node/React, or Mixed), as reported by the script's log output (or by manual detection if the script was not used).
- For Node/React runs, which scanner resolution path was used (`PATH`, `node_modules/.bin`, or the `npx` fallback).
- The exact command executed (with sensitive values like the token masked in the report, e.g., `-Dsonar.login=****` or `-Dsonar.token=****`).
- Build/scan outcome (success/failure) and which phase failed, if any.
- Quality gate status (PASSED/FAILED) when available.
- Link to the SonarQube analysis/dashboard if present in the output.
- Next step recommendation: proceed if passed, or hand off to `fix-sonar-issues` if the quality gate failed.
