---
name: domain-service
description: Use when implementing, extending, reviewing, or fixing a Java 25 Spring Boot domain microservice/API that exposes REST endpoints, controllers, service interfaces, ServiceImpl orchestration, adapter-lib/shared-lib client consumption, DTO mapping, validation, OpenAPI annotations, global exception handling, security headers, and Maven build validation. Triggers include domain service, microservice endpoint, controller-service-serviceimpl, customer accounts style service, downstream adapter client reuse, or ss_code_gen.md for domain code.
---

# Domain Service

Build domain services as REST APIs that orchestrate business behavior and consume adapter/shared libraries for downstream systems. The JIRA and OpenAPI/spec context should already be present in the task context; use that provided context for endpoint contracts, headers, schemas, error matrix, and acceptance criteria.

## Expected Repository Shape

Treat the repo as a Maven Java 25 Spring Boot service unless `pom.xml` says otherwise.

```text
pom.xml
.gitlab-ci.yml
src/main/java/<root-package>/<service>/
  <Service>Application.java
  controller/       REST controllers and endpoint validation
  service/          service interfaces
  service/impl/     business orchestration and adapter calls
  config/           security, Jackson, downstream error mapping, validators
  dto/              public API request/response DTOs
  exception/        canonical exceptions and global handler
  mapper/           MapStruct or local mappers when present
src/main/resources/
  application.yml
  application-local.yml
src/test/java/<root-package>/<service>/
  controller/
  service/
  config/
  exception/
  karate/
src/test/resources/
  application-test.yaml
  feature/
```

The sample domain service uses Spring Boot 4.x, Java 25, validation, security, actuator, springdoc, Resilience4j, adapter-library dependencies, JUnit 5, reactor-test, Karate, JaCoCo, Surefire, Failsafe, and Sonar Maven plugin.

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

## Error Model

- Use existing exceptions and the global `@RestControllerAdvice`.
- Keep public error response shape stable.
- Map adapter/downstream errors through the existing handler, such as `DownstreamErrorHandler`.
- Map downstream status codes consistently with local policy: validation/business errors to 400/422-style exceptions, auth to 401/403, missing resources to 404, conflicts to 409, and service/system failures to 5xx.
- Do not log full downstream response bodies if they may contain sensitive data.

## Headers

Common required headers in the sample include `Content-Type`, `Accept`, `correlationId`, `senderId`, `transactionDateTime`, `timeZoneOffset`, `timeZone`, `X-Channel`, `X-Source-System`, and `Authorization`. Use the exact provided contract for the current endpoint and existing local utilities.

## Build And Handoff

Run `mvn -q compile` after implementation and repeat until clean. Create or replace `ss_code_gen.md` in the workspace root, outside the Java repo, with:

```text
## Functionality Implemented
## Files Changed
## Key Technical Notes
## Build Result
```

Keep the handoff factual and concise. Use `unit-testing` for test generation and `maven-quality` for coverage, CI, or Sonar work.
