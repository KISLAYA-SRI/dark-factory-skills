---
name: platform-logging
description: Use when implementing, reviewing, or refactoring Java/Spring logging with FAB's platform-logging common library. Triggers include platform logging, StructuredLogger, LogContext, LogContextHolder, ReactiveLogContextOperator, correlation ID logging, structured JSON logs, sensitive data masking, @Loggable, replacing SLF4J/Log4j direct usage, or standardizing service logs.
---

# Platform Logging

Use FAB `platform-logging` when a service should use the shared structured logger, context propagation, and masking behavior.

## Core Rule

Follow the existing project logging style first. If the module uses `StructuredLogger`, continue it. Do not mix raw SLF4J/Log4j logging into classes that already use platform logging.

## Dependency

Add only if missing:

```xml
<dependency>
    <groupId>com.bankfab.ksa.middleware</groupId>
    <artifactId>platform-logging</artifactId>
    <version>1.0.4-SNAPSHOT</version>
</dependency>
```

Gradle:

```gradle
implementation 'com.bankfab.ksa.middleware:platform-logging:1.0.4-SNAPSHOT'
```

## Standard Logger

```java
import com.fab.common.lib.logging.core.LoggerFactory;
import com.fab.common.lib.logging.core.StructuredLogger;

public class OrderService {
    private static final StructuredLogger logger = LoggerFactory.getLogger(OrderService.class);
}
```

Use parameterized messages:

```java
logger.info("Order {} submitted successfully", orderId);
logger.warn("Retry attempt {} failed", attemptNumber);
logger.error("Failed to process payment for order {}", orderId, exception);
```

## Structured Fields

Use structured fields when values are useful for search, metrics, audit, or troubleshooting:

```java
import com.fab.common.lib.logging.config.LogLevel;

Map<String, Object> fields = Map.of(
    "orderId", order.getId(),
    "customerId", order.getCustomerId(),
    "currency", order.getCurrency(),
    "status", "submitted"
);

logger.log(LogLevel.INFO, "Order submitted", fields);
```

## Reactive Logging

Use reactive side-effect operators without blocking:

```java
return userRepository.save(user)
    .doOnSuccess(saved -> logger.info("User created: {}", saved.getId()))
    .doOnError(error -> logger.error("Failed to create user", error));
```

## Implementation Guidance

- Prefer `private static final StructuredLogger logger`.
- Use `ERROR` for failed operations, `WARN` for recoverable or retryable conditions, `INFO` for important business milestones, and `DEBUG` for diagnostic details.
- Include the throwable in error logs.
- Use supplier/lazy logging for expensive debug message construction.
- Never log raw passwords, tokens, API keys, authorization headers, PAN, CVV, PIN, OTP, SSN, or full card numbers.
- Prefer structured fields over string concatenation when adding multiple data points.

## Optional Details

Read these only when needed:

- `references/configuration.md`: structured logging, masking, async logging, and environment configuration.
- `references/context-and-reactive.md`: `LogContext`, `LogContextHolder`, `ReactiveLogContextOperator`, and `@Loggable`.
