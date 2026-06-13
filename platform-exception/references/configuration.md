# Configuration And Behavior

Use this reference only when configuring or diagnosing `platform-exception`.

## Response Shape

The global handler returns a standardized response similar to:

```json
{
  "statusCode": 400,
  "message": "Validation failed",
  "errorDetails": {
    "field": "Invalid value",
    "correlationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  },
  "timestamp": "2026-04-02T10:15:30.123",
  "path": "/api/users"
}
```

Do not create another response format in controllers.

## Configuration

```yaml
platform:
  exception:
    logging:
      enabled: true
      include-stack-trace: false
      log-client-errors: true
      log-server-errors: true
    security:
      expose-stack-trace: false
      mask-sensitive-data: true
      environment: production
      sensitive-fields:
        - password
        - token
        - ssn
        - creditCard
    correlation:
      enabled: true
      auto-generate: true
      header-name: X-Correlation-ID
```

## Correlation ID

The library can extract `X-Correlation-ID`, generate one when missing, propagate it through reactive context, include it in error responses, and log it with exceptions.

Manual use exists through:

```java
import com.fab.common.lib.exception.util.CorrelationIdHolder;
```

Prefer automatic request correlation. Use `CorrelationIdHolder` only when the existing codebase already manages non-request workflows this way.

## Troubleshooting

- Stack traces exposed in production: set `platform.exception.security.environment=production` and `expose-stack-trace=false`.
- Correlation IDs missing: check `platform.exception.correlation.enabled=true` and `auto-generate=true`.
- Validation errors not caught: add `@Valid` to controller parameters and Bean Validation annotations to DTOs.
- Custom exceptions not handled: extend `BusinessException` or use an existing project-level handler extension.

