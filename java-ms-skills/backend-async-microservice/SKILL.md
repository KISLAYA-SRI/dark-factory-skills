---
name: backend-async-microservice
description: Use when implementing, reviewing, or fixing Spring Boot asynchronous backend microservices that consume or publish Kafka messages or platform events through listeners/handlers, delegate to service interfaces and ServiceImpl orchestration, handle idempotency, retries, DLQ, correlation metadata. Triggers include async backend, Kafka listener, event listener, @KafkaListener, @EventHandler, @HandleEvent, listener-service-serviceimpl, event-driven workflow, or platform-events consumption.
---

# Backend Async Microservice

Build asynchronous backend microservices as listener-based Spring Boot services that consume Kafka messages or platform events, validate and map payloads, and orchestrate business behavior through services and adapter/shared libraries. The JIRA, event contract, schema, topic, and acceptance criteria context should already be present in the task context; use that provided context as the source of truth.

## Expected Repository Shape

Treat the repo as a Maven Java 25 Spring Boot service.

```text
pom.xml
.gitlab-ci.yml
src/main/java/<root-package>/<service>/
  <Service>Application.java
  listener/         Kafka listeners, platform event handlers, or message consumers
  service/          service interfaces
  service/impl/     business orchestration, adapter calls, and event publication
  config/           Kafka/event config, error handling, validators, security/context
  dto/              inbound event DTOs and internal domain DTOs
  event/            platform events or outbound event models when used locally
  exception/        canonical exceptions and listener/global handlers
  mapper/           MapStruct or local mappers when present
src/main/resources/
  application.yml
src/test/java/<root-package>/<service>/
  listener/
  service/
  config/
  exception/
src/test/resources/
  application-test.yaml
```

Follow existing package names first. Some projects use `consumer/`, `handler/`, or `messaging/` instead of `listener/`; extend the local convention.

## Layering Rules

Use this call path:

```text
Listener/EventHandler -> Service interface -> ServiceImpl -> adapter/shared-lib client and/or API call and/or event publisher
```

- Add listeners or handlers to an existing listener class for the same topic/resource.
- Add methods to the existing service interface and `service/impl` implementation.
- Only `ServiceImpl` owns orchestration, downstream adapter calls, event publishing, and status updates.
- Listeners validate, extract metadata, log receive/complete/failure, and delegate. They do not call downstream clients directly.
- Reuse adapter/shared-lib clients from `pom.xml` and existing imports. Add local downstream code only when the needed symbol is genuinely absent.
- Reuse `$platform-events` when the project uses FAB platform events. Do not introduce raw Kafka wrapper logic when the shared event library is already present.

## Listener Pattern

- Put topic names, group IDs, container factories, retry counts, and DLQ topics in configuration using the existing property style. Do not hardcode environment-specific values.
- Deserialize to the existing event DTO or `PlatformEvent` type. Do not pass raw JSON strings through the service layer unless the repo already does that.
- Validate required payload fields and message headers before delegation with `jakarta.validation` or the local validator.
- Propagate correlation ID, event ID, request ID, source system, channel, and trace metadata through existing context utilities.
- Keep listener methods small. Use private helper methods only for repeated metadata extraction or validation that is already too noisy inline.

## Service Pattern

- Put domain orchestration, idempotency checks, adapter invocation, status persistence, and outbound event publication in `ServiceImpl`.
- Inject adapter/shared-lib clients, event publishers, repositories, mappers, and helpers through constructor injection.
- Use MapStruct for repeated DTO mapping; use builders or the project's existing mapper style for small mappings.
- In reactive code, return `Mono<Void>`, `Mono<T>`, or `Flux<T>`, keep the chain non-blocking, and use `doOnSuccess`/`doOnError` for logs.
- Do not call `block()`, `subscribe()` for business flow control, or create unmanaged threads/executors.
- Preserve idempotency semantics from the contract and existing code. Use event IDs or business keys when the contract requires duplicate detection.

## Error, Retry, and DLQ Model

- Use existing listener error handlers, retry templates, dead-letter publishing recoverers, or platform-events retry/DLQ annotations.
- Map validation and business failures to the local non-retryable exception style when present.
- Let transient downstream failures follow the configured retry/DLQ path instead of swallowing errors.
- Do not log full event payloads or downstream response bodies when they may contain sensitive data.
- Include correlation/event identifiers in failure logs using existing structured logging conventions.

## Event Publishing

- Publish follow-up events through the existing project mechanism or `$platform-events`.
- Keep outbound event payloads stable, versionable, and free of unnecessary internal DTO structure.
- Include business references and correlation metadata. Avoid sensitive raw data.
- Use acknowledged publishing for workflows where the contract requires delivery confirmation.

## Headers and Metadata

Common metadata in the sample services includes `correlationId`, `senderId`, `transactionDateTime`, `timeZoneOffset`, `timeZone`, `X-Channel`, `X-Source-System`, event ID, topic, partition, and offset. Use the exact provided contract and existing local utilities for the current event.
