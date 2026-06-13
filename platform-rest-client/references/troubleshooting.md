# Troubleshooting

Use this reference only when diagnosing or tuning platform REST client behavior.

## Timeouts

If requests time out frequently, inspect per-call `.timeout(...)` values and application configuration:

```yaml
restclient:
  http:
    connectTimeout: 10000
    readTimeout: 60000
```

## Connection Pool Exhaustion

For too many open files, pending acquire failures, or pool exhaustion, inspect:

```yaml
appconfig:
  web-client-max-connections: 2000
  web-client-max-idle-time-in-seconds: 300
  web-client-pending-acquire-max-count: 1000
  web-client-max-pending-acquire-timeout-in-seconds: 60
  web-client-max-life-time-in-seconds: 1800
```

## Cache Misses

If cache is expected but not used:

```yaml
restclient:
  cache:
    enabled: true
    respectCacheHeaders: false
```

Confirm the request is cacheable and not using `.cacheBypass(true)`.

## OAuth Refresh Failures

For repeated 401 after token expiry, confirm OAuth config includes the required refresh inputs for the project's token flow:

```java
AuthConfig authConfig = AuthConfig.builder()
    .authType(AuthType.OAUTH2)
    .clientId(clientId)
    .clientSecret(clientSecret)
    .tokenUrl(tokenUrl)
    .refreshToken(refreshToken)
    .build();
```

## Debug Logging

Enable temporarily while diagnosing. Do not leave noisy debug logging enabled by default unless the project standard requires it.

```yaml
logging:
  level:
    com.fab.common.lib.restclient: DEBUG
    reactor.netty.http.client: DEBUG
    org.springframework.web.reactive.function.client: DEBUG
```

## SSL Problems

For `PKIX path building failed` or SSL handshake errors, prefer installing the correct CA certificate or configuring the project truststore. Do not add trust-all SSL code to production paths.

## High-Throughput Tuning

Tune only with evidence from load tests or runtime metrics:

```yaml
appconfig:
  web-client-max-connections: 5000
  web-client-max-connections-per-route: 500
  web-client-pending-acquire-max-count: 2000
  web-client-max-idle-time-in-seconds: 300

restclient:
  cache:
    enabled: true
    maxSize: 10000
    ttlSeconds: 600
```

