# Generate API Code

`generate-api-code` is an agent skill for creating or extending Java Spring Boot backend API microservices. It guides the agent to implement REST endpoints using the repository's existing controller, service, `ServiceImpl`, DTO, mapper, validation, OpenAPI, exception, and downstream adapter patterns.

Use this skill when the task includes a backend API requirement, JIRA story, OpenAPI contract, endpoint change, or acceptance criteria for a Spring Boot microservice. The skill expects the agent to inspect the local project first and treat the provided contract, headers, request and response schemas, error matrix, and existing code conventions as the source of truth.

## Applies To

- Adding new REST endpoints to an existing Java microservice.
- Extending an existing controller and service flow for a new operation.
- Wiring `Controller -> Service interface -> ServiceImpl -> adapter/shared-lib client`.
- Reusing adapter-library or shared-library clients from the current `pom.xml`.
- Adding request/response DTOs, validation annotations, OpenAPI annotations, and canonical error handling.
- Preserving reactive `Mono`/`Flux` flows without blocking calls.

## Output Expectations

The agent should produce code that fits the current repository structure instead of introducing a new architecture. Typical output includes controller methods, service interface methods, `ServiceImpl` orchestration, DTOs, mapper updates, validation rules, exception handling, and configuration changes only when the endpoint actually requires them.

Generated code should:

- Keep controllers focused on request binding, validation, and delegation.
- Keep downstream calls inside `ServiceImpl` or existing adapter/shared clients.
- Reuse existing response envelopes and public error response formats.
- Use exact header names, path variables, query parameters, and schemas from the supplied contract.
- Follow nearby logging, mapping, validation, and test conventions.

## When Not To Use

Do not use this skill for asynchronous Kafka or event-handler services, shared adapter library implementation, unit-test-only generation, generic Java refactoring, or frontend API integration. Use the corresponding async, adapter-lib, unit-testing, or frontend skills for those cases.

See [SKILL.md](./SKILL.md) for the full execution rules.
