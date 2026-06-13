# Advanced Usage

Use this reference only for non-basic event publishing/consumption.

## Batch Publishing

```java
List<OrderPlacedEvent> events = orders.stream()
    .map(this::toEvent)
    .toList();

return eventPublisher.publishBatch(events);
```

## Topic-Specific Publishing

```java
return eventPublisher.publishToTopic("fraud.alerts", highRiskPaymentEvent);
```

## Conditional Handlers

```java
@HandleEvent(
    eventType = PaymentProcessedEvent.class,
    condition = "#event.amount > 500",
    maxRetries = 5
)
public Mono<Void> checkLargePayment(PaymentProcessedEvent event) {
    return fraudService.calculateRiskScore(event).then();
}
```

## Ordered Handling

Use ordered processing only when business correctness requires per-key ordering:

```java
@HandleEvent(
    eventType = OrderPlacedEvent.class,
    condition = "#event.customerId.startsWith('VIP-')",
    ordered = true
)
public Mono<Void> handleVipOrder(OrderPlacedEvent event) {
    return vipService.process(event).then();
}
```

## Saga Pattern

Use event handlers to move the saga state forward and publish command events. Persist saga state before publishing the next command when the workflow must recover after failures.

```java
@HandleEvent(eventType = InventoryReservedEvent.class)
public Mono<Void> onInventoryReserved(InventoryReservedEvent event) {
    return sagaStateRepository.updateState(event.getOrderId(), "INVENTORY_RESERVED")
        .then(eventPublisher.publishToTopic("payment.commands",
            new ProcessPaymentCommand(event.getOrderId())));
}
```

## Troubleshooting

- Event not published: verify `platform.events.enabled=true`, source, default topic, and publisher bean wiring.
- Handler not invoked: verify `@EventHandler(topics=...)`, event type, broker/topic configuration, and package scanning.
- Repeated failures: inspect handler exceptions, retry settings, and DLQ entries.
- Correlation missing: verify tracing/monitoring options and upstream correlation propagation.

