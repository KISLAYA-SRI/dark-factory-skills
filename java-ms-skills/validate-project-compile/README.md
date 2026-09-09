# Validate Project Compile

`validate-project-compile` is an agent skill for compiling a Java Maven backend API microservice or adapter library after code changes. It guides the agent to run quiet, targeted Maven build commands, triage compiler and annotation-processing failures, and keep iterating until the build succeeds or hits a genuine environment blocker.

Use this skill immediately after code changes to confirm the project still compiles, before moving on to test execution or a code-quality pass. The skill expects the agent to run the narrowest build command that proves the change compiles and to fix every relevant compiler, dependency, or bean-wiring error it finds.

## Applies To

- Compiling a Spring Boot backend API microservice or adapter library after implementation or refactor changes.
- Diagnosing and fixing Maven compile failures: missing symbols/imports, annotation processor (Lombok/MapStruct) errors, dependency resolution failures, and Spring bean signature mismatches.
- Keeping build output quiet and targeted so only relevant errors reach the task context.
- Iterating on a build loop until it passes or is genuinely blocked by environment/credential/network issues.

## Output Expectations

The agent should run the narrowest applicable Maven command (`mvn -q -Dstyle.color=never compile` by default), fix the underlying cause of any failure, and re-run the same command until it succeeds.

Generated output should:

- Prefer quiet, targeted commands over verbose/full-debug builds.
- Avoid `mvn clean` unless stale/generated files are clearly the cause.
- Fix the actual compile-time cause rather than papering over it (e.g., do not delete failing code to make the build pass).
- Report the exact command that succeeded, or the concise blocker and smallest relevant error excerpt if the build cannot be completed.

## When Not To Use

Do not use this skill for running or stabilizing tests (`execute-unit-tests`), generating test code (`generate-unit-test-code`), implementing new business features (`generate-api-code`, `generate-async-code`, `generate-adapter-lib-code`), or code-quality/architecture review (`clean-code-architecture`). Use this skill as the compile-validation step in the pipeline, typically right after implementation and before test execution.

See [SKILL.md](./SKILL.md) for the full execution rules.
