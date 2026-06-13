# Context And Reactive Logging

Use this reference only when adding explicit context propagation, reactive transformations, or AOP logging.

## LogContext

```java
import com.fab.common.lib.logging.context.LogContext;
import com.fab.common.lib.logging.context.LogContextHolder;

LogContext context = LogContext.builder()
    .correlationId(correlationId)
    .sessionId(sessionId)
    .userId(userId)
    .applicationName("order-service")
    .addCustomMetadata("orderId", orderId)
    .build();
```

## Imperative Context

Always clear context in a `finally` block:

```java
LogContextHolder.setContext(context);
try {
    logger.info("Starting transaction");
    processTransaction(transaction);
} finally {
    LogContextHolder.clearContext();
}
```

## Reactive Context

```java
import com.fab.common.lib.logging.reactive.ReactiveLogContextOperator;

return Mono.just(request)
    .flatMap(this::validateOrder)
    .flatMap(this::processPayment)
    .transform(ReactiveLogContextOperator.monoTransformer(context))
    .doOnSuccess(order -> logger.info("Order processed: {}", order.getId()));
```

For `Flux`:

```java
return repository.findByOrderId(orderId)
    .transform(ReactiveLogContextOperator.fluxTransformer(context))
    .doOnNext(event -> logger.debug("Order event: {}", event.getType()));
```

## AOP Logging

Use `@Loggable` only when the project has enabled and accepted method-level logging. Avoid placing it on methods that receive secrets or large payloads.

```java
import com.fab.common.lib.logging.Loggable;

@Loggable
public Mono<OrderResponse> createOrder(OrderRequest request) {
    return orderService.create(request);
}
```

