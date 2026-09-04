---
name: configure-mock-server
description: Use when configuring, enabling, or toggling consumption of an external mock service in a Spring Boot BFF microservice. Triggers include mock service, mock consumer, mock toggle, features.mock.enabled, mock server URL, mock downstream, mock vs real, profile-based mock, external mock, shared mock service, dev mock, staging real, CI/CD mock override, or switching downstream calls between the shared mock service and real downstream systems per environment.
---

# Configure Mock Service Consumer

Configure togglable consumption of an **external shared mock service** in Spring Boot BFF microservices so that downstream HTTP calls can be switched between the shared mock service and real downstream systems per environment. The mock service is already provisioned and its URL is available in the JIRA ticket or provided as code-context. Mocks from the mock service behave exactly like downstream APIs — same request/response contracts, same HTTP paths.

> **Important:** This skill does NOT create mock implementations, MockResponseService classes, or in-process mock data. The service always makes real HTTP calls; only the base URL changes based on the toggle.

---

## Code-Context Check (Perform Before Any Tool Calls)

Before executing any steps, **check whether the required information is already present in the provided code-context**.

The following values are needed to configure the mock service consumer:

| Variable | Description |
|---|---|
| `jira_id` | JIRA ticket identifier |
| `mock_server_base_url` | Base URL of the shared external mock service |
| `openapi_spec` | OpenAPI specification for the downstream API |
| Endpoint details | HTTP method, path, request/response schemas |

**Decision Logic:**

```
IF code-context already contains:
  - mock_server_base_url (or mock_service_url or mock_base_url)
  - AND endpoint details (paths, methods, schemas)
THEN:
  → SKIP Step 0 and Step 1 entirely
  → Proceed directly to Step 2 (Repository Inspection)
ELSE:
  → Execute Step 0 (fetch JIRA ticket)
  → Execute Step 1 (extract mock server URL and OpenAPI spec)
  → Then proceed to Step 2
```

> **Note:** When the agent is invoked with a JIRA ticket pre-loaded as code-context.md (or via the `code-context-retrieval` skill), all JIRA fields including the mock server URL, OpenAPI spec, and endpoint details are already available. In this case, Steps 0 and 1 are skipped automatically.

---

## Step 0 — [OPTIONAL] Fetch JIRA Ticket Details

> **Skip this step if** `mock_server_base_url` and endpoint details are already present in the provided code-context.

Fetch the JIRA ticket details using the JIRA MCP tool and extract the mock service base URL and OpenAPI spec.

1. Use the JIRA MCP tool (`jira_get_issue`) to fetch the full ticket details using the `[JIRA_ID]` from the task context.
2. Search the ticket **description**, **custom fields**, and **comments** for any of the following:
   - Field named `mock_server_url`, `mock_service_url`, or `mock_base_url`
   - Text containing `mock service`, `mock server`, `mock URL`
   - Attachment or linked OpenAPI spec that references the mock host
3. Also extract:
   - The downstream API base URL (real downstream)
   - The OpenAPI spec or endpoint definitions (paths, methods, request/response schemas)
4. If no mock URL is found in the ticket, request clarification or use the value provided by the project team.

---

## Step 1 — [OPTIONAL] Extract Mock Server URL and Verify Path Mapping

> **Skip this step if** `mock_server_base_url` and endpoint details are already present in the provided code-context.

Using the information retrieved in Step 0:

1. **Set `[MOCK_SERVER_BASE_URL]`** to the URL extracted from the JIRA ticket.
2. **Verify path mapping**: The mock service endpoints mirror the downstream API paths exactly.
   - Check the OpenAPI spec attached to the JIRA ticket, or
   - Check the mock service repository for registered stub paths.
3. **Example**: if the real downstream endpoint is `POST /api/v1/resource/action`, the mock service endpoint is also `POST /api/v1/resource/action` at the mock base URL.

---

## Step 2 — Inspect the Repository

Inspect the existing project structure before writing any code:

1. Read `pom.xml` to identify:
   - Root package name
   - Existing dependencies (WebClient vs RestClient)
   - Spring Boot version
2. Scan `src/main/java` to identify:
   - Existing `config/` package location
   - Existing `WebClient` or `RestClient` bean definitions
   - Existing `application.yml` and profile-specific YAML files
3. Treat existing package names and conventions as the source of truth.

---

## Expected Repository Shape

Treat the repo as a Maven Java Spring Boot BFF service.

```text
pom.xml
src/main/java/<root-package>/<service>/
  config/
    DownstreamConfig.java         resolves effective base URL (mock or real) based on toggle
    MockServiceProperties.java    mock service URL and toggle configuration properties
src/main/resources/
  application.yml                 base config; features.mock.enabled defaults to false
  application-dev.yml             mock enabled = true + mock service base URL
  application-local.yml           mock enabled = true + mock service base URL
  application-staging.yml         mock enabled = false + real downstream base URL
  application-prod.yml            mock enabled = false + real downstream base URL
```

Follow existing package names first. If the project already has a `config/` package, place new config classes there.

---

## Configuration Properties

### application.yml (base — defaults off)

```yaml
features:
  mock:
    enabled: ${MOCK_ENABLED:false}          # master toggle; true = route to mock service

downstream:
  base-url: ${DOWNSTREAM_BASE_URL:[DOWNSTREAM_API_BASE_URL]}

mock:
  service:
    base-url: ${MOCK_SERVICE_BASE_URL:[MOCK_SERVER_BASE_URL]}
```

- `features.mock.enabled` — master toggle. `false` by default in base config.
- `downstream.base-url` — real downstream base URL used when mock is disabled. Replace `[DOWNSTREAM_API_BASE_URL]` with the actual downstream URL from the JIRA ticket or code-context.
- `mock.service.base-url` — shared mock service base URL used when mock is enabled. Replace `[MOCK_SERVER_BASE_URL]` with the URL extracted from the JIRA ticket or code-context.

### application-dev.yml

```yaml
features:
  mock:
    enabled: true

mock:
  service:
    base-url: [MOCK_SERVER_BASE_URL]   # URL from JIRA ticket or code-context
```

### application-local.yml

```yaml
features:
  mock:
    enabled: true

mock:
  service:
    base-url: [MOCK_SERVER_BASE_URL]   # URL from JIRA ticket or code-context
```

### application-staging.yml

```yaml
features:
  mock:
    enabled: false

downstream:
  base-url: [DOWNSTREAM_API_BASE_URL]   # real staging downstream URL
```

### application-prod.yml

```yaml
features:
  mock:
    enabled: false

downstream:
  base-url: [DOWNSTREAM_API_BASE_URL]   # real production downstream URL
```

---

## Profile-Based Toggle Rules

- `dev` and `local` profiles: `features.mock.enabled=true` — routes all downstream calls to the shared mock service.
- `staging`, `uat`, `prod` profiles: `features.mock.enabled=false` — routes all downstream calls to the real downstream system.
- CI/CD pipelines may override via environment variables regardless of active profile (see [Environment Variable Override](#environment-variable-override-for-cicd)).
- **Never** hard-code `true` in `application.yml` (the base config); always default to `false` and enable only in dev/local profile files.
- Do **not** use `@Profile` annotations to conditionally register beans — keep all beans always available and switch URLs at runtime based on the property.

---

## MockServiceProperties — Configuration Class

Create `MockServiceProperties.java` under `config/`:

```java
package [ROOT_PACKAGE].config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;
import jakarta.validation.constraints.NotBlank;

@ConfigurationProperties(prefix = "mock.service")
@Validated
public class MockServiceProperties {

    /**
     * Base URL of the shared external mock service.
     * Extracted from JIRA ticket or code-context.
     */
    @NotBlank
    private String baseUrl;

    public String getBaseUrl() { return baseUrl; }
    public void setBaseUrl(String baseUrl) { this.baseUrl = baseUrl; }
}
```

Enable it in the main application class or a `@Configuration` class:

```java
@EnableConfigurationProperties(MockServiceProperties.class)
```

---

## DownstreamConfig — Effective Base URL Resolution

Create `DownstreamConfig.java` under `config/`. This class resolves the correct base URL at runtime based on the mock toggle:

```java
package [ROOT_PACKAGE].config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import lombok.extern.slf4j.Slf4j;

@Configuration
@Slf4j
public class DownstreamConfig {

    @Value("${features.mock.enabled:false}")
    private boolean mockEnabled;

    @Value("${mock.service.base-url}")
    private String mockServiceBaseUrl;

    @Value("${downstream.base-url}")
    private String downstreamBaseUrl;

    /**
     * Returns the effective base URL for downstream HTTP calls.
     * When mock is enabled, returns the shared mock service URL.
     * When mock is disabled, returns the real downstream URL.
     */
    public String getEffectiveBaseUrl() {
        String effectiveUrl = mockEnabled ? mockServiceBaseUrl : downstreamBaseUrl;
        log.info("[DownstreamConfig] Mock enabled={}, effective base URL={}",
                 mockEnabled, effectiveUrl);
        return effectiveUrl;
    }

    /**
     * Primary WebClient bean configured with the effective base URL.
     * Routes to mock service when features.mock.enabled=true,
     * routes to real downstream when features.mock.enabled=false.
     */
    @Bean
    public WebClient downstreamWebClient(WebClient.Builder builder) {
        String baseUrl = getEffectiveBaseUrl();
        log.info("[DownstreamConfig] Configuring WebClient with base URL: {}", baseUrl);
        return builder
                .baseUrl(baseUrl)
                .build();
    }
}
```

> **Note:** If the project uses `RestClient` instead of `WebClient`, replace the `WebClient.Builder` with `RestClient.Builder` and adapt accordingly. The URL resolution logic (`getEffectiveBaseUrl()`) remains identical.

---

## RestClient Variant (if project uses RestClient)

If the project uses Spring 6 `RestClient` instead of WebFlux `WebClient`:

```java
@Configuration
@Slf4j
public class DownstreamConfig {

    @Value("${features.mock.enabled:false}")
    private boolean mockEnabled;

    @Value("${mock.service.base-url}")
    private String mockServiceBaseUrl;

    @Value("${downstream.base-url}")
    private String downstreamBaseUrl;

    public String getEffectiveBaseUrl() {
        return mockEnabled ? mockServiceBaseUrl : downstreamBaseUrl;
    }

    @Bean
    public RestClient downstreamRestClient(RestClient.Builder builder) {
        String baseUrl = getEffectiveBaseUrl();
        log.info("[DownstreamConfig] Configuring RestClient with base URL: {}", baseUrl);
        return builder
                .baseUrl(baseUrl)
                .build();
    }
}
```

---

## Service Implementation Pattern

The service implementation **always calls an HTTP endpoint** — there is no in-process mock branching. The URL is already resolved to either the mock service or the real downstream by `DownstreamConfig`. No `if (mockEnabled)` branching is needed in the service layer:

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class [SERVICE_NAME]ServiceImpl implements [SERVICE_NAME]Service {

    private final WebClient downstreamWebClient;   // injected — already points to correct URL
    private final [SERVICE_NAME]Transformer transformer;

    @Override
    public Mono<[RESPONSE_TYPE]> execute([REQUEST_TYPE] request, ApiRequestContext context) {
        log.debug("[[SERVICE_NAME]Service] Calling downstream, correlationId={}",
                  context.getCorrelationId());
        return downstreamWebClient
                .post()
                .uri("/api/v1/[resource]/[action]")   // same path for both mock and real
                .bodyValue(request)
                .retrieve()
                .bodyToMono([BACKEND_RESPONSE_TYPE].class)
                .map(transformer::toResponse);
    }
}
```

- The `downstreamWebClient` bean already has the correct base URL (mock or real) injected by `DownstreamConfig`.
- The URI path is **identical** for both mock and real downstream — the mock service mirrors the same path structure.
- No `MockResponseService`, no `if (mockEnabled)` branch, no in-process mock data.

---

## Environment Variable Override for CI/CD

Spring Boot maps environment variables to properties via relaxed binding automatically.

| Environment Variable | Maps To | Purpose |
|---|---|---|
| `MOCK_ENABLED` | `features.mock.enabled` | Master toggle override |
| `MOCK_SERVICE_BASE_URL` | `mock.service.base-url` | Mock service URL override |
| `DOWNSTREAM_BASE_URL` | `downstream.base-url` | Real downstream URL override |

### CI Pipeline Example — Integration Tests (mock enabled)

```yaml
# .gitlab-ci.yml or equivalent CI config — integration test stage with mock enabled
variables:
  MOCK_ENABLED: "true"
  MOCK_SERVICE_BASE_URL: "[MOCK_SERVER_BASE_URL]"
  SPRING_PROFILES_ACTIVE: "dev"
```

### CI Pipeline Example — Staging (mock disabled)

```yaml
variables:
  MOCK_ENABLED: "false"
  DOWNSTREAM_BASE_URL: "[DOWNSTREAM_API_BASE_URL]"
  SPRING_PROFILES_ACTIVE: "staging"
```

Document all supported environment variables in the service `README.md` under a **"Mock Service Configuration"** section.

---

## Validation — Connectivity Check

After configuring the mock service consumer, verify connectivity by making a test call to the mock service.

### Option 1 — Health Endpoint

If the mock service exposes a health endpoint, call it:

```bash
curl -v [MOCK_SERVER_BASE_URL]/actuator/health
# or
curl -v [MOCK_SERVER_BASE_URL]/health
```

Expected: HTTP 200 with a JSON body indicating the service is UP.

### Option 2 — Mock Endpoint Test Call

Make a test call to one of the mock endpoints to verify the path mapping and response contract:

```bash
curl -v -X POST [MOCK_SERVER_BASE_URL]/api/v1/[resource]/[action] \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

Expected: HTTP 200 (or the mock-configured status) with a response body matching the downstream API contract.

### Option 3 — Application Startup Verification

Start the Spring Boot application with the `dev` profile and check the startup logs:

```bash
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

Expected log output:
```
[DownstreamConfig] Mock enabled=true, effective base URL=[MOCK_SERVER_BASE_URL]
[DownstreamConfig] Configuring WebClient with base URL: [MOCK_SERVER_BASE_URL]
```

---

## Adding Support for a New Downstream Endpoint

When a new downstream endpoint is added to the BFF service:

1. **No new mock configuration is needed** — the mock service already mirrors all downstream API paths.
2. Implement the service method using the injected `downstreamWebClient` (or `downstreamRestClient`) with the correct URI path.
3. Verify the path exists in the mock service by checking the JIRA ticket or the mock service repository.
4. Test locally with `dev` profile to confirm the mock service returns the expected response for the new path.

---

## Prerequisites

Before running this skill:

- [ ] JIRA ticket ID is available in the task context **OR** mock server details are already provided as code-context.
- [ ] The Spring Boot project compiles and starts successfully.
- [ ] The project uses `WebClient` or `RestClient` for downstream HTTP calls.
- [ ] Network access to `[MOCK_SERVER_BASE_URL]` is available from the development environment.
- [ ] The mock service repository is accessible for path verification (URL from JIRA ticket or project team).

---

## Result

Report the following after completing the configuration:

1. **Mock server URL used** — the URL extracted from JIRA ticket or code-context.
2. **Toggle state per profile** — which profiles have mock enabled and which have it disabled.
3. **Effective base URL at startup** — confirm the log output shows the correct URL for each profile.
4. **Connectivity verification result** — whether the health check or test call to the mock service succeeded.
5. **Files modified** — list of configuration files and Java classes created or updated.

If blocked by a missing or inaccessible mock service URL, report the JIRA ticket fields checked (or code-context fields inspected) and request the correct URL before proceeding.
