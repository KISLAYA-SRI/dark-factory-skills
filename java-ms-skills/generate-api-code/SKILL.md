---
name: generate-api-code
description: Use when implementing, extending, reviewing, or fixing Spring Boot backend API microservice that exposes REST endpoints, controllers, service interfaces, ServiceImpl orchestration, adapter-lib/shared-lib client consumption, DTO mapping, validation, OpenAPI annotations, global exception handling, and security headers. Triggers include backend API, Java microservice, Spring Boot endpoint, controller-service-serviceimpl, customer accounts style service, or downstream adapter client reuse.
---

# Backend API Microservice

Build backend API microservices as REST services that orchestrate business behavior and consume adapter/shared libraries for downstream systems. The JIRA and OpenAPI/spec context should already be present in the task context; use that provided context for endpoint contracts, headers, schemas, error matrix, and acceptance criteria.

## Expected Repository Shape

Treat the repo as a Maven Java 25 Spring Boot service

```text
pom.xml
.gitlab-ci.yml
src/main/java/<root-package>/<service>/
  <Service>Application.java
  controller/       REST controllers and endpoint validation
  service/          service interfaces
  service/impl/     business orchestration and adapter calls
  client/           reactive/HTTP clients invoking downstream/adapter services
  transformer/      MapStruct or local mappers between public DTOs and downstream DTOs
  model/            internal carrier objects (e.g., grouped headers) passed across layers
  constant/         header names, paths, regex patterns, and shared literal values
  config/           security, Jackson, downstream service properties, WebClient/client config, validators
  dto/              request/response DTOs, split into public API DTOs and downstream/adapter DTOs
  exception/        canonical exceptions and global handler
  mapper/           MapStruct or local mappers when present (use transformer/ when mapping public <-> downstream DTOs)
src/main/resources/
  application.yml
  application-local.yml
src/test/java/<root-package>/<service>/
  controller/
  service/
  service/impl/
  client/
  transformer/
  config/
  constant/
  exception/
  integration/
  karate/
src/test/resources/
  application-test.yaml
  feature/
```

The sample backend API uses Spring Boot 4.x, Java 25, validation, security, actuator, springdoc, Resilience4j, adapter-library dependencies, JUnit 5, reactor-test, Karate, JaCoCo, Surefire, Failsafe, and Sonar Maven plugin.

## Layering Rules

Use this call path:

```text
Controller -> Service interface -> ServiceImpl -> adapter/shared-lib client
```

- Add endpoints to an existing controller for the same resource.
- Add methods to the existing service interface and `service/impl` implementation.
- Only `ServiceImpl` talks to adapter/shared-lib clients.
- Controllers validate and delegate; they do not call downstream clients directly.
- Reuse imported adapter/shared-lib clients from `pom.xml` and existing imports. Add local downstream code only when the needed symbol is genuinely absent.

## Controller Pattern

- Use the existing class-level `@RequestMapping` base path.
- Typical annotations: `@RestController`, `@Validated`, `@RequiredArgsConstructor`, `@Slf4j`.
- Add springdoc annotations when the project uses them: `@Operation`, `@ApiResponse`/`@ApiResponses`, `@Parameter`, and `@Schema(example = "...")`.
- Validate path, query, body, and headers with `jakarta.validation` such as `@NotBlank`, `@Min`, `@Size`, and `@Valid`.
- Extract required headers exactly as the provided contract and local project expect.
- Build or map request DTOs in the style already used by nearby controller methods.
- Return the existing response envelope/type. Do not invent a new public response or error structure.

## Service Pattern

- Put orchestration, adapter invocation, and domain mapping in `ServiceImpl`.
- Inject adapter/shared-lib clients, mappers, and helpers through constructor injection.
- Use MapStruct for repeated DTO mapping; use builders or the project's existing mapper style for small mappings.
- In reactive code, return `Mono<T>`/`Flux<T>`, keep the chain non-blocking, and use `doOnSuccess`/`doOnError` for logs.
- Use `Mono.defer(...)` or the existing reactive validation style when validation must be deferred until subscription.
- Do not call `block()` inside the service.

## Client Pattern

- Place downstream/adapter HTTP calls in dedicated `client/` classes, one client per downstream resource or capability.
- Clients accept request DTOs/values and a headers map (or the internal headers carrier model), and return the downstream response type.
- Read base URL, paths, and timeouts from typed configuration properties in `config/`; do not hardcode downstream URLs or paths in the client.
- In reactive services, clients return `Mono<T>`/`Flux<T>` and stay non-blocking; do not call `block()` inside a client.
- Apply timeouts and retry policies consistently across clients using the project's existing resilience approach (e.g., Resilience4j, reactor retry).
- Map 4xx responses to client-side exceptions and 5xx/connectivity failures to service-side exceptions; do not leak raw downstream error bodies that may contain sensitive data.
- Reuse an existing client for a downstream resource instead of creating a duplicate; only add a new client class when a genuinely new downstream resource or capability is introduced.

## Transformer Pattern

- Place mapping logic between public API DTOs and downstream/adapter DTOs in `transformer/`, one transformer per resource/domain area.
- Prefer MapStruct interfaces for structural request/response mapping; use `@Mapping` to reconcile field name or shape differences between layers.
- Use a local/manual transformer implementation only when mapping logic is conditional, derived, or otherwise unsuitable for declarative MapStruct mapping.
- Transformers must not perform I/O, call clients, or contain business/orchestration logic — that belongs in `ServiceImpl`.
- Keep transformer methods pure and one-directional per method (request mapping and response mapping as separate methods) so they remain independently testable.
- Reuse an existing transformer for a resource instead of duplicating mapping logic in a controller or service.

## Model Pattern

- Use `model/` for internal carrier objects that group related values (e.g., a set of headers or context fields) passed between Controller, Service, and Client layers.
- Model classes exist to avoid long method signatures and are not part of the public API contract; do not expose them directly as request/response bodies.
- Keep model classes immutable where practical (builder pattern or similar) and free of business logic.
- Populate model objects from incoming request data (headers, path/query values) at the controller or service boundary, not deep inside client code.

## Constant Pattern

- Centralize header names, downstream/internal path literals, regex/validation patterns, and repeated literal values in a `constant/` class (or a small set of them grouped by concern).
- Declare constants as `public static final` on a non-instantiable utility class (private constructor).
- Reference constants from controllers, services, clients, and transformers instead of duplicating literal strings; add a new constant when a literal is used in more than one place or represents a contract value (header name, path, error message key).
- Do not put environment-specific values (URLs, credentials, timeouts) in `constant/`; those belong in typed configuration properties under `config/` and `application*.yml`.

## Error Model

- Use existing exceptions and the global `@RestControllerAdvice`.
- Keep public error response shape stable.
- Map adapter/downstream errors through the existing handler, such as `DownstreamErrorHandler`.
- Map downstream status codes consistently with local policy: validation/business errors to 400/422-style exceptions, auth to 401/403, missing resources to 404, conflicts to 409, and service/system failures to 5xx.
- Do not log full downstream response bodies if they may contain sensitive data.

## Headers

Common required headers in the sample include `Content-Type`, `Accept`, `correlationId`, `senderId`, `transactionDateTime`, `timeZoneOffset`, `timeZone`, `X-Channel`, `X-Source-System`, and `Authorization`. Use the exact provided contract for the current endpoint and existing local utilities.
