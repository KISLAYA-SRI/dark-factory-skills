---
name: configure-mock-server
description: Use when configuring, enabling, disabling, or extending the mock server integration in a Spring Boot BFF microservice. Triggers include mock server, mock toggle, features.mock.enabled, MockResponseService, mock downstream, mock vs real, profile-based mock, WireMock, mock endpoint, mock configuration, dev mock, staging real, CI/CD mock override, or toggling downstream calls between mock and live.
---

# Configure Mock Server

Configure togglable mock server integration in Spring Boot BFF microservices so that downstream endpoint calls can be switched between static mock responses and real downstream systems per environment. The JIRA and API spec context should already be present in the task context; use the provided mock scenario tables, trigger conditions, and response payloads as the source of truth for mock data.

## Expected Repository Shape

Treat the repo as a Maven Java 25 Spring Boot BFF service.

```text
pom.xml
src/main/java/<root-package>/<service>/
  config/
    MockServerProperties.java     feature-flag and per-endpoint mock URL config
    MockServerConfig.java         optional WireMock bean wiring
  mock/
    MockResponseService.java      interface for serving static mock responses
    impl/
      MockResponseServiceImpl.java  returns predefined payloads per endpoint/scenario
  service/impl/
    <Domain>ServiceImpl.java      branches on features.mock.enabled before calling downstream
src/main/resources/
  application.yml                 base config; features.mock.enabled default
  application-dev.yml             mock enabled = true
  application-local.yml           mock enabled = true (optional)
  application-staging.yml         mock enabled = false
  application-prod.yml            mock enabled = false
  mock/
    <domain>-<scenario>.json      optional static JSON payloads loaded by MockResponseServiceImpl
src/test/java/<root-package>/<service>/
  mock/
    MockResponseServiceImplTest.java
  service/
    <Domain>ServiceImplMockTest.java
```

Follow existing package names first. Some projects place mock classes directly under `service/mock/` or `config/mock/`; extend the local convention.

## Configuration Properties

Add or extend `MockServerProperties` under `config/`:

```java
@ConfigurationProperties(prefix = "features.mock")
@Validated
public class MockServerProperties {
    /** Master toggle — true = serve mock responses, false = call real downstream. */
    private boolean enabled;

    /** Per-endpoint mock base URLs when using WireMock or a shared mock server. */
    private Map<String, String> endpoints = new LinkedHashMap<>();

    // getters / setters
}
```

Register in `application.yml`:

```yaml
features:
  mock:
    enabled: false          # default off; overridden per profile
    endpoints:
      login: ${MOCK_LOGIN_URL:http://localhost:8089}
      sendOtp: ${MOCK_SEND_OTP_URL:http://localhost:8089}
      verifyOtp: ${MOCK_VERIFY_OTP_URL:http://localhost:8089}
```

Profile overrides:

```yaml
# application-dev.yml
features:
  mock:
    enabled: true

# application-staging.yml
features:
  mock:
    enabled: false

# application-prod.yml
features:
  mock:
    enabled: false
```

Environment variable override for CI/CD:

```bash
FEATURES_MOCK_ENABLED=true   # enables mock in any environment without profile change
```

## Profile-Based Toggle Rules

- `dev` and `local` profiles: `features.mock.enabled=true` by default.
- `staging`, `uat`, `prod` profiles: `features.mock.enabled=false` by default.
- CI/CD pipelines may override via `FEATURES_MOCK_ENABLED` environment variable regardless of active profile.
- Never hard-code `true` in `application.yml` (the base config); always default to `false` and enable only in dev/local profile files.
- Do not use `@Profile` annotations on `MockResponseService` beans — keep the bean always available and branch on the property at runtime.

## ServiceImpl Branching Pattern

In each `<Domain>ServiceImpl`, inject `MockServerProperties` and `MockResponseService`, then branch before the downstream call:

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class LoginServiceImpl implements LoginService {

    private final LoginClient loginClient;
    private final MockServerProperties mockProperties;
    private final MockResponseService mockResponseService;
    private final LoginTransformer transformer;

    @Override
    public Mono<LoginResponse> login(LoginRequest request, ApiRequestContext context) {
        if (mockProperties.isEnabled()) {
            log.info("[MOCK] Returning mock response for login, correlationId={}",
                     context.getCorrelationId());
            return mockResponseService.getLoginResponse(request);
        }
        return loginClient.login(request, context)
                          .map(transformer::toLoginResponse);
    }
}
```

- Always log at `INFO` when serving a mock response, including the endpoint name and correlation ID.
- Do not call `block()` inside the service.
- Keep the branch as the first statement in the method so mock short-circuits before any downstream setup.

## MockResponseService Pattern

Define an interface under `mock/`:

```java
public interface MockResponseService {
    Mono<LoginResponse> getLoginResponse(LoginRequest request);
    Mono<SendOtpResponse> getSendOtpResponse(SendOtpRequest request);
    Mono<VerifyOtpResponse> getVerifyOtpResponse(VerifyOtpRequest request);
    // add one method per endpoint that has mock support
}
```

Implement under `mock/impl/`:

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class MockResponseServiceImpl implements MockResponseService {

    private final ObjectMapper objectMapper;

    @Override
    public Mono<LoginResponse> getLoginResponse(LoginRequest request) {
        // Scenario routing based on trigger conditions from JIRA mock scenario tables
        if ("user123".equals(request.getUsername())) {
            return Mono.just(buildSuccessLoginResponse(request));
        }
        return Mono.error(new DomainClientException("AUTH_INVALID_CREDENTIALS",
                                                    "Invalid credentials", 401));
    }

    private LoginResponse buildSuccessLoginResponse(LoginRequest request) {
        return LoginResponse.builder()
                .success(true)
                .data(LoginData.builder()
                        .custId("CUST123456")
                        .resultCode("SUCCESS")
                        .resultMessage("Login successful")
                        .build())
                .build();
    }

    // implement remaining methods following the same pattern
}
```

- Route mock scenarios using the trigger conditions from the JIRA mock scenario tables (e.g., specific username, OTP value, or request field).
- Return `Mono.error(...)` for error scenarios using the same exception types the real downstream path uses so the `GlobalExceptionHandler` handles them identically.
- Load static JSON payloads from `src/main/resources/mock/` using `objectMapper.readValue(...)` when the payload is large or reused across tests.
- Do not hard-code sensitive data (real tokens, real credentials) in mock payloads.

## WireMock Integration (Optional)

Use WireMock when the project requires a running HTTP mock server rather than in-process static responses. Add the dependency only when the project already uses WireMock or when the JIRA specifies a shared mock server URL.

```xml
<!-- pom.xml — test scope only for embedded WireMock -->
<dependency>
    <groupId>org.wiremock</groupId>
    <artifactId>wiremock-standalone</artifactId>
    <version>${wiremock.version}</version>
    <scope>test</scope>
</dependency>
```

For integration tests against the shared mock server at `https://dev.internal.tw.publicislabs.net/mock-service`, configure the mock base URL via `features.mock.endpoints.<name>` and point the downstream `WebClient` at it when `features.mock.enabled=true`:

```yaml
# application-dev.yml
features:
  mock:
    enabled: true
    endpoints:
      login: https://dev.internal.tw.publicislabs.net/mock-service
      sendOtp: https://dev.internal.tw.publicislabs.net/mock-service
      verifyOtp: https://dev.internal.tw.publicislabs.net/mock-service
```

In `MockServerConfig`, create a conditional `WebClient` bean that targets the mock URL:

```java
@Configuration
@ConditionalOnProperty(name = "features.mock.enabled", havingValue = "true")
@RequiredArgsConstructor
public class MockServerConfig {

    private final MockServerProperties mockProperties;

    @Bean
    @Primary
    public WebClient mockLoginWebClient(WebClient.Builder builder) {
        return builder
                .baseUrl(mockProperties.getEndpoints().getOrDefault("login", ""))
                .build();
    }
}
```

Only add `MockServerConfig` when the project routes to a real HTTP mock server. Omit it when using the in-process `MockResponseService` pattern.

## Adding a New Mock Endpoint

1. Add the endpoint name and default mock URL to `features.mock.endpoints` in `application.yml`.
2. Add the corresponding profile overrides in `application-dev.yml` if the URL differs per environment.
3. Add a new method to the `MockResponseService` interface.
4. Implement the method in `MockResponseServiceImpl` using the trigger conditions from the JIRA mock scenario table for that endpoint.
5. Inject `MockResponseService` into the relevant `ServiceImpl` and add the `if (mockProperties.isEnabled())` branch.
6. Add unit tests in `MockResponseServiceImplTest` covering success and at least one error scenario.
7. Add a unit test in `<Domain>ServiceImplMockTest` verifying the branch is taken when `features.mock.enabled=true`.

## Testing the Mock Toggle

Unit test the branch in `ServiceImpl`:

```java
@ExtendWith(MockitoExtension.class)
class LoginServiceImplMockTest {

    @Mock LoginClient loginClient;
    @Mock MockResponseService mockResponseService;
    @Mock LoginTransformer transformer;

    MockServerProperties mockProperties = new MockServerProperties();
    LoginServiceImpl service;

    @BeforeEach
    void setUp() {
        service = new LoginServiceImpl(loginClient, mockProperties,
                                       mockResponseService, transformer);
    }

    @Test
    void whenMockEnabled_thenMockResponseServiceIsCalled() {
        mockProperties.setEnabled(true);
        LoginRequest request = LoginRequest.builder().username("user123").build();
        LoginResponse expected = LoginResponse.builder().success(true).build();
        when(mockResponseService.getLoginResponse(request)).thenReturn(Mono.just(expected));

        StepVerifier.create(service.login(request, mockContext()))
                    .expectNext(expected)
                    .verifyComplete();

        verify(loginClient, never()).login(any(), any());
    }

    @Test
    void whenMockDisabled_thenRealClientIsCalled() {
        mockProperties.setEnabled(false);
        LoginRequest request = LoginRequest.builder().username("user123").build();
        LoginResponse expected = LoginResponse.builder().success(true).build();
        when(loginClient.login(eq(request), any())).thenReturn(Mono.just(new BackendLoginResponse()));
        when(transformer.toLoginResponse(any())).thenReturn(expected);

        StepVerifier.create(service.login(request, mockContext()))
                    .expectNext(expected)
                    .verifyComplete();

        verify(mockResponseService, never()).getLoginResponse(any());
    }
}
```

Unit test `MockResponseServiceImpl` scenarios:

```java
@ExtendWith(MockitoExtension.class)
class MockResponseServiceImplTest {

    MockResponseServiceImpl service = new MockResponseServiceImpl(new ObjectMapper());

    @Test
    void getLoginResponse_validUser_returnsSuccess() {
        LoginRequest request = LoginRequest.builder().username("user123").build();
        StepVerifier.create(service.getLoginResponse(request))
                    .assertNext(r -> {
                        assertThat(r.isSuccess()).isTrue();
                        assertThat(r.getData().getResultCode()).isEqualTo("SUCCESS");
                    })
                    .verifyComplete();
    }

    @Test
    void getLoginResponse_invalidUser_returnsError() {
        LoginRequest request = LoginRequest.builder().username("baduser").build();
        StepVerifier.create(service.getLoginResponse(request))
                    .expectErrorMatches(e -> e instanceof DomainClientException
                            && ((DomainClientException) e).getErrorCode()
                                                          .equals("AUTH_INVALID_CREDENTIALS"))
                    .verify();
    }
}
```

- Use `StepVerifier` for all `Mono`/`Flux` assertions.
- Cover at least one success scenario and one error scenario per endpoint.
- Use `@SpringBootTest(properties = "features.mock.enabled=true")` for integration tests that verify the full BFF stack routes through mock.

## Mock Scenario Routing Rules

Route mock scenarios using the trigger conditions from the JIRA mock scenario tables. Common patterns:

| Trigger Type | Example | Routing Logic |
|---|---|---|
| Username match | `username="user123"` | `if ("user123".equals(request.getUsername()))` |
| OTP value match | `otp="1234"` | `if ("1234".equals(request.getOtp()))` |
| OTP type match | `otpType="M"` | `if ("M".equals(request.getOtpType()))` |
| Empty/null field | `otp=""` | `if (StringUtils.isBlank(request.getOtp()))` |
| Error simulation | `username="error500"` | `if ("error500".equals(request.getUsername()))` |

For stateful mock scenarios (e.g., failed-attempt counters, OTP expiry), maintain an in-memory `ConcurrentHashMap` keyed by username or session ID. Reset state on application restart. Do not use persistent storage in mock mode.

## Stateful Mock State Management

When the JIRA mock scenario table defines stateful/sequence-dependent behavior:

```java
@Service
public class MockResponseServiceImpl implements MockResponseService {

    // In-memory state — reset on restart, never persisted
    private final ConcurrentHashMap<String, AtomicInteger> failedAttempts =
            new ConcurrentHashMap<>();

    @Override
    public Mono<LoginResponse> getLoginResponse(LoginRequest request) {
        int attempts = failedAttempts
                .computeIfAbsent(request.getUsername(), k -> new AtomicInteger(0))
                .get();

        if (attempts >= 3) {
            return Mono.error(new DomainClientException("AUTH_ACCOUNT_LOCKED",
                                                        "Account locked", 423));
        }
        if (!"P@ssw0rd123".equals(request.getPassword())) {
            failedAttempts.get(request.getUsername()).incrementAndGet();
            return Mono.error(new DomainClientException("AUTH_INVALID_CREDENTIALS",
                                                        "Invalid credentials", 401));
        }
        failedAttempts.remove(request.getUsername());
        return Mono.just(buildSuccessLoginResponse(request));
    }
}
```

- Keep state in `ConcurrentHashMap` or `ConcurrentHashMap<String, AtomicInteger>` for thread safety.
- Document the reset mechanism (application restart or explicit reset endpoint) in a `README.md` note.
- Do not implement state reset endpoints in production code; add them only in a `@Profile("dev")` controller if needed.

## Environment Variable Override for CI/CD

Spring Boot maps `FEATURES_MOCK_ENABLED=true` to `features.mock.enabled=true` automatically via relaxed binding. In CI/CD pipelines:

```yaml
# GitLab CI example
variables:
  FEATURES_MOCK_ENABLED: "true"   # enables mock for integration test stage
  SPRING_PROFILES_ACTIVE: "dev"
```

For per-endpoint URL overrides:

```yaml
variables:
  FEATURES_MOCK_ENDPOINTS_LOGIN: "https://dev.internal.tw.publicislabs.net/mock-service"
  FEATURES_MOCK_ENDPOINTS_SENDOTP: "https://dev.internal.tw.publicislabs.net/mock-service"
```

Document all supported environment variables in the service `README.md` under a "Mock Server Configuration" section.

## Result

Report which endpoints now have mock support, the active toggle state per profile, and whether in-process `MockResponseService` or external WireMock/shared mock server routing was configured. If blocked by missing JIRA mock scenario data, report the missing endpoint names and request the scenario table before proceeding.
