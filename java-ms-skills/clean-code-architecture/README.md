# Clean Code and Software Architecture Design

`clean-code-architecture` is an agent skill for reviewing, refactoring, and designing Java Spring Boot backend API microservices, async microservices, and adapter libraries with clean-code and software-architecture principles. It guides the agent to apply SOLID, dependency-direction, cohesion/coupling, and naming/readability standards within the repository's existing layered conventions.

Use this skill when the task includes a design/architecture review request, a refactor request, a code-smell fix, or general code-quality feedback on Java microservice or adapter-library code. The skill expects the agent to inspect the target code first and treat existing layering, naming, and package conventions as the baseline to improve rather than replace.

**No human-in-the-loop:** this skill is designed to run unattended as a step in an agentic pipeline (for example, immediately after `backend-api-microservice`, `backend-async-microservice`, or `adapter-lib` code generation). It never pauses for approval. Scope resolution and fix-vs-report decisions are driven by a deterministic severity model and a fixed, standard-industry-practice review checklist (aligned with common SonarQube/Checkstyle/PMD and OWASP baseline categories) that the agent works through to completion for the target scope.

## Applies To

- Reviewing controllers, services, `ServiceImpl`, listeners, mappers, and adapter clients for clean-code and architecture issues.
- Refactoring a class or package for single responsibility, reduced coupling, or improved cohesion without changing public contracts.
- Enforcing dependency direction across `Controller/Listener -> Service interface -> ServiceImpl -> adapter/shared-lib client`.
- Applying SOLID principles to service interfaces, adapter client ports, and orchestration classes.
- Removing duplication, magic values, and unclear naming while preserving existing conventions.
- Flagging blocking calls, swallowed exceptions, and testability gaps in reactive code.

## Output Expectations

The agent should produce either:

- A **review report** grouped by naming/readability, responsibility/cohesion, coupling/dependency direction, duplication, error handling/reactive correctness, and testability, each with a file/class reference and a concrete minimal fix; or
- A **refactor** that applies one or more small, verifiable structural changes (extract method/class, introduce interface, move method, replace magic value) while preserving public API contracts, event contracts, and method signatures used elsewhere.

Generated output should:

- Stay within the existing layered architecture; it does not introduce a new package layout or framework.
- Preserve behavior; refactors should be verifiable with existing or newly suggested tests.
- Avoid large-scale rewrites in a single pass — prefer a sequence of small, verifiable changes.
- Call out any case where a requested change would need to break an existing boundary or contract instead of silently doing so.

## When Not To Use

Do not use this skill for implementing new business features (`backend-api-microservice`, `backend-async-microservice`, `adapter-lib`), test generation (`unit-testing`), test execution (`test-project`), build validation (`build-project`), or mock-service configuration (`configure-mock-server`). Use this skill alongside those, typically after implementation or when a design/architecture concern is raised.

See [SKILL.md](./SKILL.md) for the full execution rules.
