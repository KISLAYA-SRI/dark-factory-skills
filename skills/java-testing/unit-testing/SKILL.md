---
name: unit-testing
description: Use when generating or updating focused Java unit tests for newly changed business behavior in Java 25 Spring Boot domain services or adapter libraries. Triggers include unit test generation, test handoff, JUnit 5, Mockito, StepVerifier, controller tests, service tests, adapter client tests, targeted mvn -Dtest runs, or coverage for changed code.
---

# Unit Testing

Generate focused Java tests for newly changed behavior only. Use the repository and code-generation handoff already present in context; do not broaden scope into unrelated production code.

## Expected Test Structure

Mirror the production package under `src/test/java`.

Domain service shape:

```text
src/test/java/<root-package>/<service>/
  controller/       controller endpoint and validation tests
  service/          service and ServiceImpl tests
  config/           validator/security/Jackson/downstream handler tests when changed
  exception/        global handler and custom exception tests when changed
  karate/           API/integration entry points such as *KarateIT
src/test/resources/
  application-test.yaml
  feature/          Karate feature files
```

Adapter library shape:

```text
src/test/java/<root-package>/<adapter>/
  client/           port-level tests when present
  client/impl/      adapter implementation tests
  config/           properties, auto-config, circuit breaker tests when changed
  context/          RequestContext tests
  dto/              serialization/deserialization tests when behavior changed
  helper/           header/helper tests when changed
  service/          token/cache/mapping service tests
  service/impl/     implementation tests
src/test/resources/
  application-test.yml
```

Common naming:

- Unit test classes end with `Test`.
- Integration tests end with `IT` or `IntegrationTest`.
- Karate tests may end with `KarateTest` or `KarateIT`.

## Scope Rules

- Modify test code only.
- Create tests only for newly changed business behavior.
- Prefer one focused test class per changed production class.
- Create no more than 3 test classes.
- Cover success, validation, and error propagation for changed service/controller/client behavior.
- Skip passive DTO getters/setters, configuration property binding, auto-configuration, and duplicate error-only test classes unless the changed production behavior specifically requires them.
- Target at least 80% coverage of changed business logic without expanding scope.

## Framework Conventions

- Use JUnit 5.
- Use Mockito for isolated service/client tests.
- Use existing Spring test support for controller/context tests.
- Use `reactor-test` `StepVerifier` for `Mono`/`Flux` behavior.
- Use Arrange-Act-Assert structure.
- Keep assertions behavior-focused, not implementation-detail-focused.
- Reuse existing test fixtures, builders, constants, object mappers, and security setup from nearby tests.

## Domain Service Test Targets

Controller tests should cover:

- HTTP method/path/query/header binding for the changed endpoint.
- Required validation failures for changed inputs.
- Delegation to the service.
- Response status/body/header shape that the endpoint owns.
- Error translation only when the controller/global handler behavior changed.

Service tests should cover:

- Adapter/shared-lib client invocation.
- DTO mapping.
- Validation or guard behavior.
- Downstream error propagation or mapping through the existing handler.
- Reactive success/error completion with `StepVerifier`.

## Adapter Library Test Targets

Client implementation tests should cover:

- URI construction.
- Required argument validation.
- Header propagation through `HeaderHelper`, `HeaderObject`, or `RequestContext`.
- Token usage and 401 token invalidation/retry when changed.
- Timeout/error propagation.
- Correct `HttpMethod`, body, and `ParameterizedTypeReference` usage at the transport boundary.

Service/helper tests should cover token caching, mapping, context propagation, and helper logic only when those production classes changed.

## Targeted Runs

Run each created or modified test class exactly once:

```bash
mvn -q -Dtest=<ClassName> test
```

Do not run the full suite. Do not repeatedly rewrite or rerun failing tests. If a targeted run fails, record the concise compiler/test failure for the Test Stabilizer Agent and stop after all created/modified classes have had their single targeted run.

## Output

Report:

- Created/modified test classes.
- Targeted commands run.
- Pass/fail status for each command.
- Concise compiler/test failures for handoff.
- Coverage summary for changed business logic when available from the targeted run or obvious from tested paths.
