---
name: maven-quality
description: Use when running, fixing, or reviewing Maven build, compile, unit tests, integration tests, JaCoCo coverage, Karate tests, GitLab CI Java archetypes, or Sonar/SonarQube validation for Java 25 Spring Boot services and adapter libraries. Triggers include mvn compile, mvn test, mvn verify, coverage threshold, sonar-project.properties, sonar:sonar, JaCoCo, Surefire, Failsafe, Karate, build failure, or CI failure.
---

# Maven Quality

Use this for build, test execution, coverage, CI, and Sonar work in Java Maven repos.

## Expected Tooling

Domain service sample:

- Java 25: `java.version`, compiler source/target, and compiler `<release>25</release>`.
- Spring Boot parent `4.0.0`.
- Surefire includes `**/*Test.java`, `**/*Tests.java`, and `**/*KarateTest.java`.
- Failsafe includes `**/*IT.java`, `**/*IntegrationTest.java`, and `**/*KarateIT.java`.
- JaCoCo version `0.8.14`.
- JaCoCo line coverage minimum `0.95`.
- Sonar Maven plugin configured by `sonar.version`.
- Karate dependencies for API tests.

Adapter library sample:

- Maven `jar` packaging.
- Central library parent.
- Spring WebFlux, Resilience4j, Spring Boot configuration processor, and `common-lib`.
- `sonar-project.properties` may define sources and exclusions.
- GitLab Java Maven library archetype.

## Command Selection

```bash
mvn -q compile
mvn test
mvn verify
mvn -Dtest=ClassNameTest test
mvn -DskipTests compile
mvn sonar:sonar -Dsonar.host.url=<url> -Dsonar.token=<token>
```

- Implementation sanity check: `mvn -q compile`.
- Unit tests: `mvn test` or `mvn -Dtest=ClassNameTest test`.
- Integration tests and coverage gates: `mvn verify`.
- Use `-DskipTests` only when the task is explicitly compile-only or when isolating compile errors. Do not use it to claim tests pass.
- For Sonar Maven plugin projects, use the repo's documented `mvn sonar:sonar` command with required host/token/project properties.
- For standalone Sonar scanner projects, use `sonar-project.properties` and the configured scanner only when available.

## Build Loop

Run the narrowest command that validates the change, fix relevant compile/test failures, then rerun. Do not mark implementation done until `mvn -q compile` is clean. If tests or coverage are part of the request, do not stop before the requested command is clean or clearly blocked by environment/dependency access.

## Test Execution Standards

- Keep tests close to changed behavior.
- Use JUnit 5 and Mockito/Spring test support already present in the repo.
- Use `reactor-test`/`StepVerifier` for reactive flows.
- Use Karate only where the repo already has Karate feature/API tests or the request explicitly targets API integration coverage.
- Avoid brittle tests that only assert implementation details.

## Sonar And Coverage

- Respect exclusions already configured in `pom.xml` or `sonar-project.properties`.
- Do not "fix" Sonar by deleting behavior, weakening validation, or adding broad exclusions unless explicitly requested.
- Prefer targeted code-quality fixes: remove dead code, simplify duplication, close resource leaks, strengthen null handling, and add missing assertions around changed behavior.

## Failure Handling

- Compile errors: fix imports, package mismatches, Java 25 compatibility, annotation processor issues, and missing bean signatures first.
- Test errors: identify whether the failure is due to changed behavior, stale mocks, Spring context config, or external environment.
- Coverage failures: add meaningful tests for changed branches; do not lower thresholds without explicit approval.
- Sonar failures: prefer targeted code fixes over exclusions.
