# Generate Adapter Lib Code

`generate-adapter-lib-code` is an agent skill for implementing, extending, reviewing, or fixing a shared Spring Boot adapter library JAR that wraps a third-party REST/HTTP API. It guides the agent to build reactive client ports, Spring Boot auto-configuration, configuration properties, DTOs, token handling, and transport calls using the repository's existing `common-lib` `WebClient` conventions.

Use this skill when the task includes a JIRA story, OpenAPI/spec contract, or acceptance criteria for a new or changed downstream API wrapper in a shared adapter library. The skill expects the agent to inspect the local project first and treat the provided contract, headers, request/response schemas, and existing code conventions as the source of truth.

## Applies To

- Adding or extending client port interfaces and their `client/impl/` implementations.
- Wiring beans through the existing `*AdapterAutoConfiguration` and extending `*AdapterProperties`.
- Using the in-house `common-lib` `WebClient` as the only outbound HTTP transport (`restClient.invokeApi(...)`).
- Adding upstream request/response DTOs under `dto/<domain>` with correct types, `@JsonProperty`, and validation.
- Implementing token retrieval, `Authorization` header handling, and 401 invalidate/retry logic through the existing `TokenService`.
- Propagating headers and request context through `HeaderHelper`, `HeaderObject`, or `RequestContext`.

## Output Expectations

The agent should produce code that fits the current repository structure instead of introducing a new architecture. Typical output includes port interfaces, `client/impl/` classes, DTOs, `AutoConfiguration`/properties updates, and header/token handling only when the endpoint actually requires them.

Generated output should:

- Keep business orchestration out of client implementations; clients validate inputs, build URI/headers, call transport, apply timeout/token handling, and return typed responses.
- Never introduce raw `WebClient.builder()`, `RestTemplate`, or a new transport wrapper; reuse `common-lib` transport.
- Return `Mono<T>`/`Flux<T>` and never call `block()`.
- Build URIs from `*AdapterProperties`; never hard-code hostnames.
- Preserve exact local header casing and propagate `traceparent`, `Source-App-Code`, `Source-App-Name`, `Ext-User-Id`, `Idempotency-Key`, and `RequestId` when applicable.

## When Not To Use

Do not use this skill for implementing REST controllers/services (`generate-api-code`), asynchronous Kafka/event-handler services (`generate-async-code`), unit-test-only generation (`generate-unit-test-code`), or generic Java clean-code/architecture review (`clean-code-architecture`). Use the corresponding skill for those cases.

See [SKILL.md](./SKILL.md) for the full execution rules.
