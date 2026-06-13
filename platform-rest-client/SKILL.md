---
name: platform-rest-client
description: Use when implementing, reviewing, or refactoring Java/Spring outbound HTTP calls that should use FAB's platform-rest-client common library. Triggers include platform REST client, HttpService, ReactiveHttpService, RequestAttributes, common-lib REST calls, outbound adapter HTTP clients, replacing raw Spring WebClient/RestTemplate usage, or adding authentication/caching/timeout behavior through the shared REST client.
---

# Platform REST Client

Use FAB `platform-rest-client` for outbound HTTP calls when the codebase has this dependency or the user asks for common-lib REST client usage.

## Core Rule

Prefer the existing project pattern first. If the module already injects `HttpService` or `ReactiveHttpService`, extend that style. Do not introduce raw `RestTemplate`, `WebClient.builder()`, Apache HTTP clients, or a new transport abstraction for downstream REST calls.

## Dependency

For Maven projects, add the dependency only if it is missing:

```xml
<dependency>
    <groupId>com.bankfab.ksa.middleware</groupId>
    <artifactId>platform-rest-client</artifactId>
    <version>1.0.4-SNAPSHOT</version>
</dependency>
```

## Choose The API

- Use `com.fab.common.lib.restclient.ReactiveHttpService` in WebFlux/reactive flows and return `Mono<T>` / `Flux<T>` without blocking.
- Use `com.fab.common.lib.restclient.HttpService` in blocking Spring MVC or synchronous service code.
- Keep the selected style consistent with the surrounding module. Do not mix blocking and reactive calls in the same call path.

## Standard Fluent Usage

Blocking:

```java
UserResponse response = httpService.request()
    .url(baseUrl + "/users/{userId}")
    .uriParam("userId", userId)
    .header("Authorization", "Bearer " + token)
    .header("Accept", "application/json")
    .queryParam("include", "profile")
    .timeout(10)
    .get(UserResponse.class);
```

Reactive:

```java
Mono<UserResponse> response = reactiveHttpService.request()
    .url(baseUrl + "/users/{userId}")
    .uriParam("userId", userId)
    .header("Authorization", "Bearer " + token)
    .header("Accept", "application/json")
    .timeout(10)
    .get(UserResponse.class);
```

For generic response types, use `ParameterizedTypeReference`:

```java
Mono<List<UserResponse>> users = reactiveHttpService.request()
    .url(baseUrl + "/users")
    .getList(new ParameterizedTypeReference<List<UserResponse>>() {});
```

## Implementation Guidance

- Inject the service through constructor injection.
- Build URLs from configuration properties, not hard-coded hostnames.
- Use `uriParam(...)` for path variables and `queryParam(...)` for query strings.
- Set request headers through the fluent API or existing header helper.
- Set a timeout per call when the downstream contract requires one.
- Keep authentication, correlation IDs, and source/destination tracing consistent with the local project helpers.
- Do not log secrets, bearer tokens, API keys, PAN, CVV, PIN, OTP, or full card numbers.
- Let project-level exception handling translate client/server exceptions unless the module already has a specific wrapper pattern.

## Optional Details

Read these only when the task needs them:

- `references/auth-cache-config.md`: authentication modes, caching, configuration keys, and credential handling.
- `references/advanced-operations.md`: POST/PUT/PATCH/DELETE, ResponseEntity, file upload/download, tracing, and circuit breaker examples.
- `references/troubleshooting.md`: timeout, pool, cache, OAuth refresh, SSL, debug logging, and performance tuning notes.
