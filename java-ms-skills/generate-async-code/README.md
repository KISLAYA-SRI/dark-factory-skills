# Generate Async Code

`generate-async-code` is an agent skill for implementing, reviewing, or fixing Spring Boot asynchronous backend microservices that consume or publish Kafka messages or platform events. It guides the agent to build listener/handler-based services that validate and map payloads, orchestrate business behavior through services and adapter/shared libraries, and handle idempotency, retries, DLQ, and correlation metadata using the repository's existing conventions.

Use this skill when the task includes a JIRA story, event contract, schema, topic, or acceptance criteria for a Spring Boot event-driven/Kafka microservice. The skill expects the agent to inspect the local project first and treat the provided event contract, headers/metadata, and existing code conventions as the source of truth.

## Applies To

- Adding or extending Kafka listeners, platform event handlers, or message consumers.
- Wiring `Listener/EventHandler -> Service interface -> ServiceImpl -> adapter/shared-lib client and/or event publisher`.
- Reusing adapter/shared-lib clients and `$platform-events` from the current `pom.xml`.
- Deserializing inbound events to existing DTO/`PlatformEvent` types with `jakarta.validation`.
- Preserving idempotency, retry, and DLQ semantics from the contract and existing code.
- Publishing follow-up events with stable, versionable payloads and correlation metadata.

## Output Expectations

The agent should produce code that fits the current repository structure instead of introducing a new architecture. Typical output includes listener methods, service interface methods, `ServiceImpl` orchestration, DTOs, mapper updates, and configuration changes only when the event actually requires them.

Generated output should:

- Keep listeners focused on validation, metadata extraction, and delegation; downstream calls and event publication stay inside `ServiceImpl`.
- Keep reactive chains (`Mono<Void>`, `Mono<T>`, `Flux<T>`) non-blocking; never call `block()`, `subscribe()` for control flow, or spawn unmanaged threads.
- Route failures through existing listener error handlers, retry templates, or platform-events retry/DLQ mechanisms instead of swallowing errors.
- Avoid logging full event payloads or downstream response bodies that may contain sensitive data.
- Use the exact provided event contract, topic, and metadata fields for the current event.

## When Not To Use

Do not use this skill for synchronous REST API implementation (`generate-api-code`), shared adapter library implementation (`generate-adapter-lib-code`), unit-test-only generation (`generate-unit-test-code`), or generic Java clean-code/architecture review (`clean-code-architecture`). Use the corresponding skill for those cases.

See [SKILL.md](./SKILL.md) for the full execution rules.
