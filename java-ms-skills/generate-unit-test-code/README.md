# Generate Unit Test Code

`generate-unit-test-code` is an agent skill for generating or updating focused Java unit tests for newly changed business behavior in Spring Boot backend API microservices or adapter libraries. It guides the agent to mirror the production package structure, follow JUnit 5/Mockito/`StepVerifier` conventions, and cover success, validation, and error-propagation paths for changed code only.

Use this skill after a code-generation change (from `generate-api-code`, `generate-async-code`, or `generate-adapter-lib-code`) to add test coverage for the newly changed behavior. The skill expects the agent to use the repository's existing test fixtures, builders, and conventions rather than inventing a new test style.

## Applies To

- Generating controller, service/`ServiceImpl`, and adapter client tests for newly changed behavior.
- Mirroring the production package under `src/test/java` for both domain service and adapter library shapes.
- Following naming conventions: `*Test` for unit tests, `*IT`/`*IntegrationTest` for integration tests, `*KarateTest`/`*KarateIT` for Karate tests.
- Covering success, validation failure, and error propagation for changed service/controller/client behavior.
- Reusing existing test fixtures, builders, constants, object mappers, and security setup from nearby tests.

## Output Expectations

The agent should produce focused, behavior-driven tests scoped only to the changed production code — not a broad test-suite rewrite.

Generated output should:

- Modify or add test code only; do not touch unrelated production code.
- Prefer one focused test class per changed production class, with no more than 3 test classes per run.
- Use JUnit 5, Mockito for isolated tests, and `reactor-test` `StepVerifier` for `Mono`/`Flux` behavior.
- Follow Arrange-Act-Assert structure with behavior-focused, not implementation-detail-focused, assertions.
- Skip passive DTO getters/setters, configuration property binding, and auto-configuration tests unless the changed behavior specifically requires them.
- Target at least 80% coverage of changed business logic without expanding scope.

## When Not To Use

Do not use this skill for running or stabilizing tests (`execute-unit-tests`), implementing new business features (`generate-api-code`, `generate-async-code`, `generate-adapter-lib-code`), compiling the project (`validate-project-compile`), or code-quality/architecture review (`clean-code-architecture`). Use this skill immediately after implementation, then hand off to `execute-unit-tests` to run the created tests.

See [SKILL.md](./SKILL.md) for the full execution rules.
