# Execute SonarQube Analysis

`execute-sonar-analysis` is an agent skill for triggering a SonarQube analysis and publishing results to a configured SonarQube server. It supports two project families — **Java Maven** backend microservices/adapter libraries, and **Node.js/React/TypeScript** frontend or backend projects — and detects which one applies before choosing the analysis command.

Use this skill when the task is to run, trigger, or execute a SonarQube scan — for example, after a set of code changes, before opening a pull request, or as an explicit "run sonar analysis" request. This skill only executes the analysis; it does not fetch, triage, or fix findings.

## Applies To

- Running a SonarQube analysis for a Maven-based Java microservice or adapter library (`mvn verify sonar:sonar`).
- Running a SonarQube analysis for a Node.js/React/TypeScript project (`sonar-scanner` via `npx` or an existing npm script).
- Publishing analysis results to a SonarQube server using project-specific credentials.
- Waiting on and reporting the SonarQube quality gate result for the current analysis.
- Multi-module Maven projects and npm/yarn/pnpm workspaces, when run from the appropriate module/workspace root.
- Mixed repositories containing both a Maven module and a Node/React module, analyzed per module.

## Project Type Detection

Before running any command, the agent detects the project family:

| Signal | Project Family | Reference |
|---|---|---|
| `pom.xml` present | Maven (Java) | [`references/maven.md`](./references/maven.md) |
| `package.json` present, no `pom.xml` | Node/React | [`references/node.md`](./references/node.md) |
| Both present | Mixed | Both references, run per module |

Only the reference file matching the detected project family is loaded — this keeps the skill's context usage lean.

## Output Expectations

The agent runs the analysis command with the required project-specific values substituted in, then reports:

- The detected project family.
- The command executed, with the authentication token masked.
- Whether the build/scan succeeded or failed, and at which phase.
- The SonarQube quality gate status (PASSED/FAILED) once available.
- The SonarQube dashboard/analysis link, when present in the output.
- A recommendation to hand off to the `fix-sonar-issues` skill if the quality gate failed.

The agent does not modify source code, tests, `pom.xml`, `package.json`, or `sonar-project.properties` as part of this skill — this is strictly an analysis-trigger skill.

## Required Values

The agent must have these three values before running the analysis, regardless of project family. Never hardcode or guess them:

- `SONAR_PROJECT_ID` — the SonarQube project key.
- `SONAR_URL` — the SonarQube server base URL.
- `SONAR_TOKEN` — the authentication token/login used to publish results.

## When Not To Use

Do not use this skill to interpret, triage, or fix reported SonarQube findings — use `fix-sonar-issues` for that. Do not use this skill for plain unit test execution without a Sonar analysis — use `execute-unit-tests` for that.

See [SKILL.md](./SKILL.md) for the full execution rules, and `references/maven.md` / `references/node.md` for the exact commands per project family.
