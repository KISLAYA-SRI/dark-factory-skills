---
name: test-project
description: Use when running, fixing, or stabilizing Java Maven tests for backend API microservices or adapter libraries. Triggers include run tests, fix tests, mvn test, mvn verify, unit test failure, integration test failure, Karate, Surefire, Failsafe, JaCoCo coverage failure, or keep testing until success.
---

# Test Project

Use this skill for executing and stabilizing tests. Test generation belongs to `unit-testing`; compile/package-only validation belongs to `build-project`.

## Commands

Prefer the quietest class-level Maven command that validates the changed behavior:

```bash
mvn -q -Dstyle.color=never -DtrimStackTrace=true -Dtest=ClassNameTest test
```

- Use `-Dtest=ClassNameTest` by default for every changed or failing test class.
- Do not use method-level targeting. Keep runs at test-class level so setup, related scenarios, and class-level fixtures are validated together.
- Use full `mvn test` or `mvn verify` only when explicitly requested, required by integration/coverage gates, or after class-level runs pass and broader confirmation is necessary.
- Keep output quiet with `-q`, `-Dstyle.color=never`, and `-DtrimStackTrace=true`.
- Avoid `-X`, verbose logging, dependency trees, and repeated full-suite execution unless a plugin/environment failure cannot be understood from targeted quiet output.

## Test Loop

1. Run the narrowest class-level test command that validates the changed behavior.
2. Fix production or test code according to the actual failure.
3. Re-run the same command.
4. Continue until the requested test command succeeds or the failure is clearly blocked by external infrastructure, unavailable dependencies, credentials, or environment setup.

Do not stop after creating tests if the requested command still fails and the failure is fixable.

## Failure Triage

- Compilation failure: fix imports, constructor signatures, mocks, generated mapper references, or incompatibilities first.
- Assertion failure: verify expected behavior against the provided contract and changed production code.
- Reactive test failure: use `StepVerifier`, avoid `block()`, and assert success/error completion explicitly.
- Spring context failure: minimize context usage, prefer slice tests when nearby tests use them, and mock downstream clients.
- Karate/Failsafe failure: check feature file paths, profile config, server port, and test resource setup.
- Coverage failure: add focused tests for changed business branches; do not lower thresholds unless explicitly requested.

## Result

Report the exact command that passed. If blocked, report the command, failing test class/method, concise root failure, and whether the failure is code, test, or environment related.
