---
name: execute-sonar-analysis
description: Use when running, triggering, or executing a SonarQube analysis for a Java Maven backend microservice/adapter library, or a Node.js/React/TypeScript frontend or backend project. Triggers include run sonar, execute sonar analysis, sonar scan, mvn sonar, sonar:sonar, sonar-scanner, npx sonar-scanner, trigger quality gate analysis, or publish analysis results to SonarQube.
---

# Execute SonarQube Analysis

Run a SonarQube analysis for a project and publish results to the configured SonarQube server. This skill supports two project families — **Maven (Java)** and **Node/React (npm/yarn/pnpm)** — and only executes the analysis; use the `fix-sonar-issues` skill to triage and remediate reported findings afterward.

## STEP 0: Detect Project Type (MANDATORY — Run First)

Determine which project family the target repository belongs to before choosing a command:

| Signal | Project Family | Reference Folder |
|---|---|---|
| `pom.xml` at the repo/module root | **Maven (Java)** | [`references/maven.md`](references/maven.md) |
| `package.json` at the repo root, no `pom.xml` at that level | **Node/React** | [`references/node.md`](references/node.md) |
| Both present (e.g., Java backend with an embedded frontend module) | **Mixed** | Run each command scoped to its own module: `references/maven.md` from the Maven module root, `references/node.md` from the Node module root |

If detection is ambiguous (e.g., a monorepo with multiple modules and no clear target), ask which module/path to analyze before proceeding rather than guessing.

Once the project family is confirmed, load only the matching reference file(s) below for the exact command and flags — do not load both upfront.

## Required Values

The following values must be supplied before running the analysis for either project family. Never hardcode, guess, or reuse values from a different project/environment:

- **`SONAR_PROJECT_ID`** — the SonarQube project key to publish results under.
- **`SONAR_URL`** — the base URL of the SonarQube server.
- **`SONAR_TOKEN`** — the authentication token/login used to publish results.

If any of these values is missing from the current task context, ask for it explicitly before running the command. Do not fabricate placeholder values in the actual command execution.

## Execution Steps

1. Confirm the project family using STEP 0 (Maven, Node/React, or Mixed).
2. Confirm `SONAR_PROJECT_ID`, `SONAR_URL`, and `SONAR_TOKEN` are available. If any is missing, request it before proceeding.
3. Load the matching reference file (`references/maven.md` or `references/node.md`) for the exact command, required prerequisites, and flags for that project family.
4. Run the command from the correct project/module root.
5. Stream/monitor the build/scan output.
6. Wait for the quality gate result (both reference commands include the flag that blocks until the quality gate outcome is known).
7. Capture and report the outcome.

For **Mixed** repositories, repeat steps 3–6 once per module, using the reference and command appropriate to that module's project family.

## Interpreting the Result

- **Success (exit code 0):** the analysis completed and the quality gate passed. Report the SonarQube dashboard link if printed in the output, along with a brief pass summary.
- **Failure due to quality gate:** the analysis published successfully but the quality gate failed. Report this clearly and distinguish it from a build/compile/lint failure. Do not attempt to fix findings as part of this skill — hand off to the `fix-sonar-issues` skill for triage and remediation.
- **Failure before the Sonar step runs (compile/test/lint failure):** the analysis did not run. Report the underlying build failure (compilation error, failing test, lint error, etc.) since that must be resolved first.
- **Failure at the Sonar step itself (connectivity/auth):** check `SONAR_URL` reachability and validity of `SONAR_TOKEN`/`SONAR_PROJECT_ID` before retrying.

## Rules

- Do not modify source code, tests, or configuration as part of running the analysis — this skill only triggers and reports the analysis.
- Do not hardcode `SONAR_PROJECT_ID`, `SONAR_URL`, or `SONAR_TOKEN` values into `pom.xml`, `package.json`, `sonar-project.properties`, scripts, or committed files. Pass them as command-line properties/flags as shown in the matching reference file, or via the mechanism already used by the project's CI pipeline (e.g., CI/CD variables) if one exists.
- Do not remove or alter any of the required flags in the reference command for the detected project family unless the user explicitly requests a change.
- For multi-module Maven projects, run the command from the aggregator/root POM unless the task specifies a single module to analyze.
- For npm/yarn/pnpm monorepos (workspaces), run the scan from the workspace/package root that owns the relevant `sonar-project.properties`, unless the task specifies a different scope.
- If the project's existing CI pipeline (e.g., `.gitlab-ci.yml`, GitHub Actions workflow) already defines an equivalent Sonar stage, prefer aligning with its parameters and only run locally when explicitly asked to.

## Result

Report:

- Detected project family (Maven, Node/React, or Mixed).
- The exact command executed (with sensitive values like the token masked in the report, e.g., `-Dsonar.login=****` or `-Dsonar.token=****`).
- Build/scan outcome (success/failure) and which phase failed, if any.
- Quality gate status (PASSED/FAILED) when available.
- Link to the SonarQube analysis/dashboard if present in the output.
- Next step recommendation: proceed if passed, or hand off to `fix-sonar-issues` if the quality gate failed.
