---
name: adapter-lib
description: Use when implementing, extending, reviewing, or fixing a shared Spring Boot adapter library JAR that wraps a third-party REST/HTTP API behind reactive client ports, Spring Boot auto-configuration, configuration properties, DTOs, token handling, common-lib WebClient transport, and Maven build validation. Triggers include adapter-lib, shared adapter library, NI adapter, T24 adapter, client port, AutoConfiguration.imports, HeaderObject, RequestContext, token retry, or downstream API wrapper.
---

# Adapter Library

Build adapter libraries as reusable protocol adapters consumed by domain services. The JIRA and OpenAPI/spec context should already be present in the task context; use that provided context for endpoint paths, methods, headers, schemas, and acceptance criteria.

## Expected Repository Shape

Treat the repo as a Maven Java 25 Spring Boot library JAR 

```text
pom.xml
sonar-project.properties
.gitlab-ci.yml
devops-config/
src/main/java/<root-package>/<adapter>/
  client/                  port interfaces consumed by domain services
  client/impl/             final reactive implementations
  config/                  AutoConfiguration, properties, WebClient/circuit config
  constants/               shared message, validation, path, and header constants
  context/                 Reactor request context for header propagation
  dto/<domain>/            upstream request/response DTOs
  exception/               adapter-specific exceptions, only if already used
  helper/                  header and pure helper utilities
  port/                    extra/backward-compatible ports such as token ports
  service/, service/impl/  internal token/cache/mapping services
src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
src/test/java/<root-package>/<adapter>/...
src/test/resources/application-test.yml
```

The sample adapter is a Maven `jar` with Spring WebFlux, configuration processor, Resilience4j, and `common-lib`. CI uses a Java Maven library archetype.

## Implementation Rules

1. Add or extend the port interface under `client/`.
2. Implement it under `client/impl/` as `final class XClientImpl implements XClient`.
3. Constructor-inject transport, properties, token service, helpers, and mappers.
4. Wire beans through the existing `*AdapterAutoConfiguration` with `@ConditionalOnMissingBean`.
5. Extend `*AdapterProperties` for base URLs, timeouts, credentials, retry/circuit options, and cache durations.
6. Add `AutoConfiguration.imports` only when a genuinely new auto-configuration class is added.
7. Keep business orchestration out of client implementations. Adapter clients validate inputs, build URI/headers, call transport, apply timeout/token handling, log, and return typed responses.

## Transport Rule

Use the in-house `common-lib` `WebClient` already present in the repo as the only outbound HTTP transport. Do not create raw Spring `WebClient.builder()`, `RestTemplate`, Apache clients, or a new transport wrapper inside client implementations.

Call shape:

```java
restClient.invokeApi(
    uri,
    HttpMethod.POST,
    headers,
    request,
    new ParameterizedTypeReference<ResponseDto>() {}
)
```

Compose `timeout(...)`, token retry, logging, and circuit breaker behavior around that call.

## Client Pattern

- Return `Mono<T>` or `Flux<T>`.
- Validate constructor args and method args with `Objects.requireNonNull(...)`, using existing constants where available.
- Build URIs from `*AdapterProperties`; never hard-code hostnames.
- Use private URI builders for path variables.
- Use `ParameterizedTypeReference<T>` for generic responses.
- Apply `timeout(properties.getTimeout())`.
- Log outbound URI at `INFO`, payload/response at `DEBUG`, failures at `ERROR`.
- Do not place controller concerns, public API mapping, or domain business branching in the adapter.

## Headers And Context

Prefer existing helpers:

- `HeaderHelper` for `HttpHeaders` creation from maps or propagated header objects.
- `HeaderObject` for explicit propagated headers.
- `RequestContext` in Reactor Context when the repo uses request-scoped propagation.

Common propagated headers include `traceparent`, `Source-App-Code`, `Source-App-Name`, `Ext-User-Id`, `Idempotency-Key`, and `RequestId`. Preserve exact local casing when constants or helpers already exist.

## Token And Error Rules

- Get tokens through the existing `TokenService`.
- Add `Authorization: Bearer <token>` only when the upstream requires auth.
- On 401, invalidate token and retry according to the existing helper. Avoid broad retries for all 4xx responses.
- Let 400, 403, 404, 409, and 422 propagate unless local code already maps them.
- Propagate 5xx and timeouts to consuming services unless the adapter already has a matching exception policy.
- Never call `block()` inside the library.

## DTO Rules

- Put DTOs under `dto/<domain>`.
- Match local DTO style: Lombok mutable DTOs or immutable final DTOs.
- Use `BigDecimal` for money and `LocalDate`, `Instant`, or `OffsetDateTime` for dates/timestamps.
- Use `@JsonProperty` when wire names differ from Java names.
- Add `jakarta.validation` annotations for required fields.
- Mask sensitive fields from logs and `toString`.

## Build

Run `mvn -q compile` after implementation and repeat until clean. Use `maven-quality` for test, coverage, CI, or Sonar work.
