---
name: platform-security
description: Use when implementing, reviewing, or refactoring authentication and authorization in Java/Spring WebFlux services with FAB's platform-security common library. Triggers include platform security, UserTokenService, ServiceTokenService, StepupTokenService, TokenRequest, TokenResponse, AuthenticationContext, AcrLevel, @RequireAcr, @RequireScope, JWT validation, service tokens, stepup authentication, scopes, or reactive security context.
---

# Platform Security

Use FAB `platform-security` for token generation/validation, ACR enforcement, service tokens, stepup authentication, and reactive security context handling.

## Core Rule

Follow the service's existing security pattern first. Do not hand-roll JWT parsing, token validation, ACR checks, service-token caches, or custom WebFlux filters when `platform-security` already provides them.

## Dependency

Add only if missing:

```xml
<dependency>
    <groupId>com.bankfab.ksa.middleware</groupId>
    <artifactId>platform-security</artifactId>
    <version>1.0.4-SNAPSHOT</version>
</dependency>
```

## API Selection

- `UserTokenService`: end-user token generation, validation, refresh, revoke.
- `ServiceTokenService`: machine-to-machine service tokens and scope validation.
- `StepupTokenService`: short-lived elevated-authentication tokens.
- `AcrValidator` / `@RequireAcr`: authentication assurance enforcement.
- `SecurityContextUtils`: read current subject/context in reactive flows.

## User Token

```java
TokenRequest request = TokenRequest.builder()
    .subject(username)
    .acrLevel(AcrLevel.LEVEL_1)
    .roles(Set.of("USER"))
    .permissions(Set.of("READ_PROFILE"))
    .sessionId(sessionId)
    .build();

return userTokenService.generateUserToken(request);
```

Validation:

```java
return userTokenService.validateToken(token)
    .map(AuthenticationContext::getSubject);
```

Refresh:

```java
return userTokenService.refreshToken(refreshToken);
```

## Service Token

```java
TokenRequest request = TokenRequest.builder()
    .subject("order-service")
    .scopes(Set.of("payment:read", "payment:write"))
    .audience("payment-service")
    .build();

return serviceTokenService.generateServiceToken(request);
```

Scope validation:

```java
return serviceTokenService.validateServiceToken(token, "payment:read");
```

## ACR Enforcement

Use annotations at API or service methods when the project uses method security:

```java
@RequireAcr(AcrLevel.LEVEL_2)
public Mono<TransferResponse> transferFunds(TransferRequest request) {
    return SecurityContextUtils.getCurrentContext()
        .flatMap(context -> paymentService.transfer(request, context));
}
```

Trigger stepup for sensitive operations:

```java
@RequireAcr(value = AcrLevel.LEVEL_2, triggerStepup = true)
public Mono<TransferResponse> transferFunds(TransferRequest request) {
    return transferService.transfer(request);
}
```

## Implementation Guidance

- Use reactive APIs and return `Mono`/`Flux`; do not block.
- Read the subject/context from `SecurityContextUtils` instead of reparsing tokens.
- Use scopes for service-to-service authorization.
- Use ACR levels for user authentication strength, not roles.
- Never log tokens, refresh tokens, OTPs, passwords, private keys, or authorization headers.
- Configure keys and secrets through secure configuration, not source code.

## Optional Details

Read these only when needed:

- `references/configuration.md`: token, ACR, stepup, CORS, security headers, rate limiting, and key configuration.
- `references/stepup-and-troubleshooting.md`: stepup flow, metrics, and common failures.
