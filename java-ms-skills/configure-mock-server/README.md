# Configure Mock Server

`configure-mock-server` is an agent skill for configuring togglable consumption of an **external shared mock service** in Spring Boot BFF microservices. It guides the agent to wire profile-based mock/real downstream switching using configuration properties, without any in-process mock data or `MockResponseService` classes.

Use this skill when the task involves enabling a mock service toggle, switching downstream HTTP calls between a shared mock service and real downstream systems, or configuring environment-specific mock/real routing in a Java Spring Boot microservice.

## Applies To

- Configuring `features.mock.enabled` toggle in a Spring Boot BFF service.
- Adding `MockServiceProperties` and `DownstreamConfig` classes to resolve the effective downstream base URL at runtime.
- Setting up profile-specific YAML files (`application-dev.yml`, `application-local.yml`, `application-staging.yml`, `application-prod.yml`) with mock/real URL switching.
- Wiring a `WebClient` or `RestClient` bean that automatically routes to the mock service or real downstream based on the active profile.
- Supporting CI/CD environment variable overrides for the mock toggle and URLs.

## Purpose

This skill configures a **URL-switching pattern** — not in-process mocking. The service always makes real HTTP calls; only the base URL changes depending on whether the mock toggle is enabled. The mock service mirrors the downstream API's paths exactly, so no code changes are needed when switching between mock and real.

## Prerequisites

Before invoking this skill, ensure the following are available:

- **JIRA ticket** with mock server details (URL, downstream API base URL, endpoint paths) **OR** these details pre-loaded as **code-context** in the agent invocation.
- The Spring Boot project compiles and starts successfully.
- The project uses `WebClient` (Spring WebFlux) or `RestClient` (Spring 6 MVC) for downstream HTTP calls.
- Network access to the mock service URL from the development environment.

## Input

The skill expects **one of the following** input modes:

### Mode A — JIRA Ticket (Steps 0 and 1 will be executed)

Provide the JIRA ticket ID in the task context. The agent will:
1. Fetch the JIRA ticket using the JIRA MCP tool.
2. Extract the mock server base URL, downstream API base URL, and endpoint details.
3. Proceed with configuration.

### Mode B — Code-Context Pre-Loaded (Steps 0 and 1 are SKIPPED)

Provide the following details directly as code-context in the agent invocation:

| Field | Description |
|---|---|
| `mock_server_base_url` | Base URL of the shared external mock service |
| `downstream_api_base_url` | Base URL of the real downstream API |
| Endpoint details | HTTP method, path, request/response schemas from the OpenAPI spec |

When these fields are present in the code-context, the agent **skips JIRA tool calls** (Steps 0 and 1) and proceeds directly to repository inspection and code generation.

> **Tip:** Use the `code-context-retrieval` skill to pre-load JIRA ticket details as code-context before invoking this skill. This avoids redundant JIRA API calls and speeds up execution.

## How to Invoke

### With JIRA Ticket ID

```
Configure mock server consumer for [JIRA_ID]. 
The project is a Spring Boot BFF service at [GIT_REPO_URL].
```

### With Code-Context Pre-Loaded

```
Configure mock server consumer using the following details:
- Mock server base URL: [MOCK_SERVER_BASE_URL]
- Downstream API base URL: [DOWNSTREAM_API_BASE_URL]
- Endpoints: [list of endpoint paths and methods]
The project is a Spring Boot BFF service at [GIT_REPO_URL].
```

## Expected Output

The skill produces the following files and changes:

### New Java Classes

| File | Purpose |
|---|---|
| `config/MockServiceProperties.java` | `@ConfigurationProperties` class binding `mock.service.*` properties |
| `config/DownstreamConfig.java` | Resolves effective base URL (mock or real) and creates the `WebClient`/`RestClient` bean |

### Modified Configuration Files

| File | Change |
|---|---|
| `application.yml` | Adds `features.mock.enabled`, `downstream.base-url`, `mock.service.base-url` with env var bindings |
| `application-dev.yml` | Sets `features.mock.enabled=true` and mock service base URL |
| `application-local.yml` | Sets `features.mock.enabled=true` and mock service base URL |
| `application-staging.yml` | Sets `features.mock.enabled=false` and real downstream base URL |
| `application-prod.yml` | Sets `features.mock.enabled=false` and real downstream base URL |

### Verification Report

After configuration, the agent reports:
- Mock server URL used
- Toggle state per profile (which profiles use mock vs real)
- Effective base URL at startup (from application logs)
- Connectivity verification result (health check or test call)
- Full list of files created or modified

## Configuration

### Mock Toggle

The mock/real switch is controlled by a single property:

```yaml
features:
  mock:
    enabled: true   # true = route to mock service; false = route to real downstream
```

This can be overridden at runtime via the `MOCK_ENABLED` environment variable.

### Environment Variable Overrides

| Environment Variable | Property | Purpose |
|---|---|---|
| `MOCK_ENABLED` | `features.mock.enabled` | Master toggle |
| `MOCK_SERVICE_BASE_URL` | `mock.service.base-url` | Mock service URL |
| `DOWNSTREAM_BASE_URL` | `downstream.base-url` | Real downstream URL |

### Profile Defaults

| Profile | Mock Enabled | Routes To |
|---|---|---|
| `local` | `true` | Mock service |
| `dev` | `true` | Mock service |
| `staging` | `false` | Real downstream |
| `uat` | `false` | Real downstream |
| `prod` | `false` | Real downstream |

## Notes on Generic Usage

This skill is **completely project-agnostic** and works with any Java Spring Boot microservice:

- All URLs are sourced from the JIRA ticket or code-context — no hardcoded values.
- Package names are derived from the existing project structure.
- The `WebClient` vs `RestClient` variant is chosen based on the project's existing dependencies.
- The mock service path mapping is verified against the OpenAPI spec or mock service repository provided in the JIRA ticket.
- No project-specific identifiers, team names, or environment URLs are embedded in the skill.

See [SKILL.md](./SKILL.md) for the full execution rules and code templates.
