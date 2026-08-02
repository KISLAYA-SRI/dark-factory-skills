---
name: platform-exception
description: Use when implementing, reviewing, or refactoring standardized exception handling in Java/Spring services with FAB's platform-exception common library. Triggers include platform exception, common exception handling, BusinessException, ResourceNotFoundException, ValidationException, ConflictException, standardized error response, correlation ID errors, replacing custom ControllerAdvice, or mapping service failures to common error contracts.
---

# Platform Exception

Use FAB `platform-exception` when a Spring service should rely on the shared exception hierarchy and global handler instead of local error envelopes or custom controller advice.

## Core Rule

Prefer the existing project error style first. If `platform-exception` is already present, throw its specific exception types and let auto-configuration/global handling produce the response. Do not create duplicate error DTOs, inline error bodies, or new `@ControllerAdvice` classes unless the project already has a required extension point.

## Dependency

Add only if missing:

```xml
<dependency>
    <groupId>com.bankfab.ksa.middleware</groupId>
    <artifactId>platform-exception</artifactId>
    <version>1.0.4-SNAPSHOT</version>
</dependency>
```

## Exception Selection

- `ValidationException`: invalid request or business validation failure, HTTP 400.
- `UnauthorizedException`: unauthenticated or invalid credentials, HTTP 401.
- `ForbiddenException`: authenticated but insufficient permission, HTTP 403.
- `ResourceNotFoundException`: missing domain resource, HTTP 404.
- `ConflictException`: duplicate or conflicting state, HTTP 409.
- `InternalServerException`: unexpected server failure, HTTP 500.
- `ServiceUnavailableException`: downstream/service temporarily unavailable, HTTP 503.
- `BusinessException`: custom business error when no specific type fits.

## Standard Usage

```java
throw ResourceNotFoundException.builder()
    .message("Order not found")
    .resourceType("Order")
    .resourceId(orderId)
    .build();
```

```java
throw ConflictException.builder()
    .message("Email already exists")
    .conflictingField("email")
    .conflictingValue(request.getEmail())
    .build();
```

Reactive:

```java
return orderRepository.findById(orderId)
    .switchIfEmpty(Mono.error(ResourceNotFoundException.builder()
        .message("Order not found")
        .resourceType("Order")
        .resourceId(orderId)
        .build()));
```

Mapping a known persistence error:

```java
return service.create(request)
    .onErrorMap(DuplicateKeyException.class, ex -> ConflictException.builder()
        .message("Resource already exists")
        .cause(ex)
        .build());
```

## Implementation Guidance

- Use Bean Validation annotations such as `@Valid`, `@NotBlank`, `@NotNull`, `@Size`, and `@Email` at API boundaries.
- Add useful context through builder fields; avoid dumping whole request objects.
- Do not include secrets, PAN, CVV, PIN, OTP, bearer tokens, passwords, or raw credentials in messages or context data.
- Let the library handle exception logging. Do not log and rethrow the same exception unless local project standards require it.
- Preserve correlation ID behavior from the framework unless the existing project explicitly manages it.

## Optional Details

Read `references/configuration.md` only when configuring responses, correlation IDs, masking, or troubleshooting.
