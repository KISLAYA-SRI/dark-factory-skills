# Configuration

Use this reference only when configuring `platform-logging`.

## Basic Structured Logging

```yaml
platform:
  logging:
    default-level: INFO
    structured:
      enabled: true
      format: json
      pretty-print: false
      include-stack-trace: true
    context:
      enabled: true
      auto-generate-correlation-id: true
      correlation-id-header: X-Correlation-ID
    security:
      mask-sensitive-data: true
      mask-pattern: "***REDACTED***"
```

## Sensitive Fields

```yaml
platform:
  logging:
    sensitive-fields:
      - password
      - passwd
      - pwd
      - token
      - secret
      - apikey
      - api-key
      - authorization
      - bearer
      - creditcard
      - credit-card
      - ssn
      - social-security
      - email
```

Production should keep masking enabled.

## Environment Defaults

Development:

```yaml
platform:
  logging:
    default-level: DEBUG
    structured:
      enabled: true
      pretty-print: true
```

Production:

```yaml
platform:
  logging:
    default-level: INFO
    structured:
      enabled: true
      pretty-print: false
    async:
      enabled: true
    security:
      mask-sensitive-data: true
```

## Troubleshooting

- `LoggerProvider not initialized`: verify the dependency is present and Spring Boot auto-configuration is active.
- Missing correlation ID: ensure `platform.logging.context.enabled=true` and the WebFlux filter is active.
- Sensitive data not masked: verify `platform.logging.security.mask-sensitive-data=true` and the field name is listed in `sensitive-fields`.
- Logs too noisy: tune `platform.logging.default-level` and `platform.logging.logger-levels`.

