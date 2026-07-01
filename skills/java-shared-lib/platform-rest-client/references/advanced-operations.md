# Advanced Operations

Use this reference only when the task needs methods beyond simple GET calls.

## POST

```java
UserResponse response = httpService.request()
    .url(baseUrl + "/users")
    .header("Content-Type", "application/json")
    .timeout(10)
    .post(UserResponse.class, request);
```

Reactive:

```java
Mono<UserResponse> response = reactiveHttpService.request()
    .url(baseUrl + "/users")
    .header("Content-Type", "application/json")
    .timeout(10)
    .post(UserResponse.class, request);
```

## ResponseEntity

Use when the code needs status or response headers:

```java
ResponseEntity<UserResponse> entity = httpService.request()
    .url(baseUrl + "/users")
    .postForEntity(new ParameterizedTypeReference<UserResponse>() {}, request);
```

## Collections

Use `ParameterizedTypeReference` for collections and maps:

```java
List<OrderResponse> orders = httpService.request()
    .url(baseUrl + "/orders")
    .getList(new ParameterizedTypeReference<List<OrderResponse>>() {});
```

```java
Mono<Map<String, List<OrderResponse>>> grouped = reactiveHttpService.request()
    .url(baseUrl + "/orders/grouped")
    .get(new ParameterizedTypeReference<Map<String, List<OrderResponse>>>() {});
```

## PUT, PATCH, DELETE

```java
UserResponse updated = httpService.request()
    .url(baseUrl + "/users/{userId}")
    .uriParam("userId", userId)
    .put(UserResponse.class, request);
```

```java
UserResponse patched = httpService.request()
    .url(baseUrl + "/users/{userId}")
    .uriParam("userId", userId)
    .patch(UserResponse.class, patchRequest);
```

```java
DeleteResponse deleted = httpService.request()
    .url(baseUrl + "/users/{userId}")
    .uriParam("userId", userId)
    .delete(DeleteResponse.class);
```

## File Download

```java
ByteArrayResource file = httpService.request()
    .url(baseUrl + "/files/{fileId}")
    .uriParam("fileId", fileId)
    .timeout(60)
    .downloadFile();
```

Use project file-storage helpers for persistence. Do not write downloaded files to arbitrary local paths from production code.

## File Upload

```java
MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
body.add("file", new FileSystemResource(file));

UploadResponse response = httpService.request()
    .url(baseUrl + "/files/upload")
    .header("Content-Type", MediaType.MULTIPART_FORM_DATA_VALUE)
    .timeout(120)
    .post(UploadResponse.class, body);
```

## Tracing

Use project correlation/header helpers first. If the module uses the client fluent tracing fields, set them like this:

```java
return reactiveHttpService.request()
    .url(baseUrl + "/orders/{orderId}")
    .uriParam("orderId", orderId)
    .origination("order-service")
    .destination("orders-api")
    .throughEvent(false)
    .header("X-Correlation-ID", correlationId)
    .get(OrderResponse.class);
```

## Circuit Breaker

Only add direct circuit breaker wrapping if the project already uses Resilience4j this way. Otherwise prefer the library and application configuration.

```java
return circuitBreaker.executeSupplier(() ->
    httpService.request()
        .url(baseUrl + "/users/{userId}")
        .uriParam("userId", userId)
        .get(UserResponse.class)
);
```

