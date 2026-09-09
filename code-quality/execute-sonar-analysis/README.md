# Execute SonarQube Analysis

`execute-sonar-analysis` is an agent skill for triggering a SonarQube analysis and publishing results to a configured SonarQube server. It supports two project families — **Java Maven** backend microservices/adapter libraries, and **Node.js/React/TypeScript** frontend or backend projects — and detects which one applies before choosing the analysis command.

Use this skill when the task is to run, trigger, or execute a SonarQube scan — for example, after a set of code changes, before opening a pull request, or as an explicit "run sonar analysis" request. This skill only executes the analysis; it does not fetch, triage, or fix findings.

## Applies To

- Running a SonarQube analysis for a Maven-based Java microservice or adapter library (`mvn verify sonar:sonar`).
- Running a SonarQube analysis for a Node.js/React/TypeScript project (a resolved `sonar-scanner` binary, falling back to `npx` only as a last resort).
- Publishing analysis results to a SonarQube server using project-specific credentials.
- Waiting on and reporting the SonarQube quality gate result for the current analysis.
- Multi-module Maven projects and npm/yarn/pnpm workspaces, when run from the appropriate module/workspace root.
- Mixed repositories containing both a Maven module and a Node/React module, analyzed per module.

## Deterministic Execution via Script

This skill ships [`scripts/execute-sonar.sh`](./scripts/execute-sonar.sh), a single script that performs project-type detection and tool resolution itself, so the same invocation behaves the same way every run:

```bash
SONAR_PROJECT_ID=<<SONAR_PROJECT_ID>> \
SONAR_URL=<<SONAR_URL>> \
SONAR_TOKEN=<<SONAR_TOKEN>> \
./scripts/execute-sonar.sh <<TARGET_DIR>>
```

The script:

- Detects Maven (`pom.xml`) vs Node/React (`package.json`) automatically.
- For Node/React, resolves the scanner binary in order: `sonar-scanner` on `PATH` -> `node_modules/.bin/sonar-scanner` -> `npx --yes sonar-scanner` (last resort, with an explicit warning since `npx` can re-download the package on every run).
- Fails fast with a clear message if required environment variables or tools are missing.

The agent prefers running this script over hand-assembling the Maven/npx command; the `references/maven.md` and `references/node.md` files exist mainly to document what the script does, and as a manual fallback if script execution is not available in the current environment.

## Project Type Detection

The script (and the manual fallback path) detect the project family the same way:

| Signal | Project Family | Reference |
|---|---|---|
| `pom.xml` present | Maven (Java) | [`references/maven.md`](./references/maven.md) |
| `package.json` present, no `pom.xml` | Node/React | [`references/node.md`](./references/node.md) |
| Both present | Mixed | Both references, run the script once per module |

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

See [SKILL.md](./SKILL.md) for the full execution rules, [`scripts/execute-sonar.sh`](./scripts/execute-sonar.sh) for the deterministic runner, and `references/maven.md` / `references/node.md` for the exact commands and tool-resolution logic per project family.
