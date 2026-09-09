# Execute Unit Tests

`execute-unit-tests` is an agent skill for running, fixing, and stabilizing Java Maven tests for backend API microservices and adapter libraries. It guides the agent to use quiet, class-level Maven test commands, triage failures by category (compilation, assertion, reactive, Spring context, Karate/Failsafe, coverage), and keep iterating until the requested test command passes.

Use this skill after code or test changes to confirm the affected behavior is verified. The skill expects the agent to run the narrowest class-level test command that validates the changed behavior and to keep fixing production or test code until that command succeeds or is genuinely blocked by environment/infrastructure issues.

## Applies To

- Running and stabilizing JUnit 5, Mockito, and `reactor-test`/`StepVerifier` tests for changed behavior.
- Fixing unit test, integration test, Karate, Surefire, and Failsafe failures.
- Diagnosing JaCoCo coverage failures for changed business logic.
- Iterating on a test loop until the requested command passes or hits a real blocker.

## Output Expectations

The agent should run the quietest class-level Maven command for every changed or failing test class (`mvn -q -Dstyle.color=never -DtrimStackTrace=true -Dtest=ClassNameTest test`), fix the actual failure, and re-run the same command until it passes.

Generated output should:

- Target test classes, not individual methods, so setup and related scenarios are validated together.
- Use full `mvn test`/`mvn verify` only when explicitly requested or required by coverage/integration gates.
- Fix the real cause of a failure (compilation, assertion, reactive completion, Spring context, or coverage) rather than weakening assertions or lowering thresholds without explicit request.
- Report the exact command that passed, or the failing test class/method and concise root cause if blocked.

## When Not To Use

Do not use this skill for generating new test code (`generate-unit-test-code`), compiling without running tests (`validate-project-compile`), implementing new business features (`generate-api-code`, `generate-async-code`, `generate-adapter-lib-code`), or code-quality/architecture review (`clean-code-architecture`). Use this skill as the test-execution step in the pipeline, typically after `generate-unit-test-code` or any implementation change.

See [SKILL.md](./SKILL.md) for the full execution rules.
