# Configuration

Use this reference only when configuring `platform-security`.

```yaml
security:
  api:
    tokens:
      user:
        enabled: true
        expiration: 3600s
        refresh-expiration: 86400s
        clock-skew: 30s
        issuer: my-service
        audience: my-app
        signing-algorithm: RS256
      service:
        enabled: true
        expiration: 3600s
        cache-size: 1000
        cache-ttl: 50m
        mtls-enabled: false
    acr:
      enabled: true
      propagate-in-service-calls: true
      levels:
        basic: 1
        mfa: 2
        biometric: 3
    stepup:
      enabled: true
      max-levels: 3
      token-expiration: 10m
      session-timeout: 15m
      preserve-request-context: true
    cors:
      enabled: true
      allowed-origins:
        - https://app.example.com
      allowed-methods:
        - GET
        - POST
        - PUT
        - DELETE
      allowed-headers:
        - Authorization
        - Content-Type
      allow-credentials: true
      max-age: 3600
    security-headers:
      enabled: true
      content-security-policy: true
      strict-transport-security: true
      x-content-type-options: true
      x-frame-options: true
      x-frame-options-value: DENY
    rate-limiting:
      enabled: true
      max-requests-per-minute: 60
      max-auth-attempts-per-minute: 5
      block-on-exceed: true
    keys:
      private-key-path: /path/to/private-key.pem
      public-key-path: /path/to/public-key.pem
      use-external-key-store: false
```

Use project secret management for private keys, client secrets, and signing material.

## ACR Levels

- `AcrLevel.LEVEL_0`: public/no authentication.
- `AcrLevel.LEVEL_1`: username/password or basic authentication.
- `AcrLevel.LEVEL_2`: MFA, OTP, SMS, or email verification.
- `AcrLevel.LEVEL_3`: biometric or hardware-backed authentication.
- `AcrLevel.LEVEL_4`: maximum assurance for critical operations.

