# Stepup And Troubleshooting

Use this reference only for elevated authentication flows or diagnosis.

## Stepup Token

```java
TokenRequest stepupRequest = TokenRequest.builder()
    .acrLevel(AcrLevel.LEVEL_2)
    .customClaims(Map.of(
        "mfa_method", "totp",
        "mfa_timestamp", Instant.now().toString()
    ))
    .build();

return stepupTokenService.generateStepupToken(originalToken, stepupRequest);
```

Validate:

```java
return stepupTokenService.validateStepupToken(stepupToken, AcrLevel.LEVEL_2);
```

Revoke:

```java
return stepupTokenService.revokeToken(stepupToken);
```

## Programmatic ACR Validation

```java
return SecurityContextUtils.getCurrentContext()
    .flatMap(context -> acrValidator.validateAcrLevel(context, AcrLevel.LEVEL_2))
    .flatMap(context -> executePayment(request))
    .onErrorResume(InsufficientAcrLevelException.class,
        error -> Mono.error(new StepupRequiredException(AcrLevel.LEVEL_2, "executePayment")));
```

## Troubleshooting

- Token validation fails: check expiration, issuer, audience, signing key, algorithm, and JWT format.
- ACR validation fails: verify token claims and required ACR level; trigger stepup when appropriate.
- Service token cache misses: check `security.api.tokens.service.cache-size` and `cache-ttl`.
- Rate limiting blocks valid traffic: tune request/auth attempt limits and client retry behavior.
- Never solve SSL/key issues by hard-coding keys or disabling validation in production.

