# Authentication, Caching, And Configuration

Use this reference only when adding or changing auth, cache, or platform REST client configuration.

## Authentication

Imports:

```java
import com.fab.common.lib.restclient.auth.AuthConfig;
import com.fab.common.lib.restclient.auth.AuthType;
```

Basic auth:

```java
AuthConfig authConfig = AuthConfig.builder()
    .authType(AuthType.BASIC)
    .username(username)
    .password(password)
    .build();
```

Bearer token:

```java
AuthConfig authConfig = AuthConfig.builder()
    .authType(AuthType.BEARER_TOKEN)
    .bearerToken(token)
    .build();
```

API key in a header:

```java
AuthConfig authConfig = AuthConfig.builder()
    .authType(AuthType.API_KEY)
    .apiKeyHeader("X-API-Key")
    .apiKeyValue(apiKey)
    .apiKeyInQuery(false)
    .build();
```

OAuth2:

```java
AuthConfig authConfig = AuthConfig.builder()
    .authType(AuthType.OAUTH2)
    .clientId(clientId)
    .clientSecret(clientSecret)
    .tokenUrl(tokenUrl)
    .scope(scope)
    .build();
```

Attach auth to a request:

```java
return reactiveHttpService.request()
    .url(baseUrl + "/resource")
    .auth(authConfig)
    .get(Response.class);
```

Do not hard-code secrets. Read credentials from project configuration, secret providers, or the existing credential helper.

## Credential Vault

If the project already uses the vault, reuse it:

```java
import com.fab.common.lib.restclient.auth.CredentialVault;
```

Use `credentialVault.store(key, value)` and `credentialVault.retrieve(key)` through an application service. Do not introduce vault usage into unrelated code paths just because the library supports it.

## Caching

Enable cache only when the downstream operation is safe to cache and the project requirement calls for it:

```yaml
restclient:
  cache:
    enabled: true
    ttlSeconds: 300
    maxSize: 1000
    respectCacheHeaders: true
```

Bypass cache for write or freshness-sensitive calls:

```java
return httpService.request()
    .url(baseUrl + "/users/{userId}")
    .uriParam("userId", userId)
    .cacheBypass(true)
    .put(UserResponse.class, request);
```

If cache invalidation is required and the project already wires it, use:

```java
import com.fab.common.lib.restclient.cache.CacheInvalidationService;
```

Available operations include `invalidateByUrl(...)`, `invalidateByResource(...)`, and `clearAll()`.

## Common Configuration Keys

Use existing application configuration style. These keys are supported by the library:

```yaml
restclient:
  http:
    connectTimeout: 5000
    readTimeout: 30000
    writeTimeout: 30000
    followRedirects: false
    maxConnections: 100
    maxConnectionsPerRoute: 20
    connectionTimeToLive: 60000
    idleConnectionTimeout: 30000
  retry:
    enabled: true
    maxAttempts: 3
    initialInterval: 1000
    multiplier: 2.0
    maxInterval: 10000
  circuitbreaker:
    enabled: true
    slidingWindowSize: 10
    failureRateThreshold: 50.0
    waitDurationInOpenState: 30
    permittedCallsInHalfOpenState: 5
```

