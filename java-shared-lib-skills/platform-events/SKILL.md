---
name: platform-events
description: Use when implementing, reviewing, or refactoring event-driven Java/Spring code with FAB's platform-events common library. Triggers include platform events, PlatformEvent, EventPublisherService, @PublishEvent, @EventHandler, @HandleEvent, event publishing, event consumption, DLQ, retry, event topics, reactive event handlers, or replacing custom event bus/Kafka wrapper logic.
---

# Platform Events

Use FAB `platform-events` for domain event publishing and consumption when the service uses the shared event library.

## Core Rule

Model events explicitly, publish through `EventPublisherService` or `@PublishEvent`, and consume with `@EventHandler` / `@HandleEvent`. Do not introduce a raw Kafka/Rabbit/WebClient event wrapper when `platform-events` is available.

## Dependency

Add only if missing:

```xml
<dependency>
    <groupId>com.bankfab.ksa.middleware</groupId>
    <artifactId>platform-events</artifactId>
    <version>1.0.4-SNAPSHOT</version>
</dependency>
```

## Minimal Configuration

```yaml
spring:
  application:
    name: order-service

platform:
  events:
    enabled: true
    source: ${spring.application.name}
    default-topic: platform.events
```

## Define Events

Extend `PlatformEvent` and validate required payload fields:

```java
import com.fab.common.events.domain.model.PlatformEvent;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.SuperBuilder;

@Data
@SuperBuilder
@EqualsAndHashCode(callSuper = true)
public class OrderPlacedEvent extends PlatformEvent {
    @NotBlank
    private String orderId;

    @NotBlank
    private String customerId;
}
```

## Publish Events

Prefer programmatic publishing when event creation depends on business logic:

```java
import com.fab.common.events.application.service.EventPublisherService;

return orderRepository.save(order)
    .flatMap(saved -> {
        OrderPlacedEvent event = OrderPlacedEvent.builder()
            .orderId(saved.getId())
            .customerId(saved.getCustomerId())
            .build();

        return eventPublisher.publish(event).thenReturn(saved);
    });
```

Use acknowledged publishing for critical workflows:

```java
return eventPublisher.publishWithAck(event)
    .thenReturn(result);
```

Use annotation publishing only for simple method-result events:

```java
import com.fab.common.events.application.annotation.PublishEvent;

@PublishEvent(
    topic = "order.events",
    eventType = OrderPlacedEvent.class,
    eventExpression = "#result"
)
public Mono<OrderPlacedEvent> placeOrder(OrderRequest request) {
    return orderService.place(request).map(this::toEvent);
}
```

## Consume Events

```java
import com.fab.common.events.application.annotation.EventHandler;
import com.fab.common.events.application.annotation.HandleEvent;

@EventHandler(topics = {"order.events"})
@RequiredArgsConstructor
public class OrderEventHandler {
    private final InventoryService inventoryService;

    @HandleEvent(eventType = OrderPlacedEvent.class, maxRetries = 3, timeout = 30000)
    public Mono<Void> handleOrderPlaced(OrderPlacedEvent event) {
        return inventoryService.reserveItems(event.getOrderId()).then();
    }
}
```

## Implementation Guidance

- Keep event payloads stable, versionable, and free of unnecessary internal DTO structure.
- Include IDs and business references, not sensitive raw data.
- Use `publishBatch(...)` only for true bulk/high-throughput operations.
- Use SpEL conditions only for simple filtering; keep complex routing in services.
- Handler methods should return `Mono<Void>` for async work and should not block.
- Configure retries and DLQ through the library or annotations, not ad hoc retry loops.

## Optional Details

Read `references/advanced-usage.md` only for batch publishing, topic-specific publishing, conditional handlers, sagas, monitoring, or troubleshooting.
