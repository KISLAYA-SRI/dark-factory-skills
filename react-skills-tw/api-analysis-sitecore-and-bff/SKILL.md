---
name: api-analysis-sitecore-and-bff
description: Use when performing Sitecore API and BFF API analysis for a frontend user story. Enforces strict endpoint-only lookup, deep YAML analysis for all request/response scenarios, and produces the Data Fetching Pattern per endpoint. Triggers include API analysis, Sitecore endpoint, BFF endpoint, YAML spec, API contract, or data fetching pattern.
---

# API Analysis — Sitecore and BFF

## Core Rule

This agent is responsible for performing BOTH Sitecore API analysis AND BFF API analysis directly. There is no separate API analysis agent. All analysis must be completed here as part of the analysis document.

## Inputs Available to the Agent

Before starting, confirm what inputs are available:

| Input           | Source                                         | Required?     |
| --------------- | ---------------------------------------------- | ------------- |
| JIRA User Story | `.SS_WF/{{$var[ticket_id]s}}_jira_output.json` | **Mandatory** |

---

## Sitecore API Analysis

### Step 1 — Identify Sitecore Endpoints

The Sitecore API JSON is already extracted under `{{$var[BITBUCKET_SC_CLONE_DIR]s}}`.

### Step 2 — If NO Sitecore API Details Are Found Under this folder

Do not invent API fields or endpoints. Mark the Sitecore API section as:

> `SITECORE API NOT FOUND / NOT REQUIRED`

> ⚠️ **STRICT ENDPOINT LOOKUP RULE — MANDATORY:**
>
> - You MUST look up **only** the exact endpoint(s) inside `{{$var[BITBUCKET_SC_CLONE_DIR]s}}`..
> - Do NOT browse other folder, list directory contents, or scan other JSON files.
> - If the exact endpoint file is not immediately found, do **NOT** fall back to nearby, similarly-named, or related JSON files.
> - If the exact endpoint cannot be located, mark as: `SITECORE API CONTRACT NOT FOUND — endpoint [name] could not be located. Developer must provide the correct file path or confirm the endpoint.`

### Step 3 — Analyse

- Which CMS rendering maps to which FE component
- Which props are CMS-authored
- Which props are passed from Sitecore to FE
- Missing fields, unclear rendering, unknown datasource
- How the Sitecore API will be consumed in frontend development context

---

## BFF API Analysis

### Step 1 — Identify BFF/Backend Endpoints

From the JIRA Story data, identify all backend/BFF endpoints/OperationId mentioned for integration. The BFF API JSON specs are all extracted under `{{$var[BITBUCKET_CLONE_DIR]s}}`.

### Step 2 — If NO BFF API Details Are Found

If it is only a presentational component or no BFF API details are found, do not invent API fields.
Mark it as:

> `BFF API NOT FOUND / NOT REQUIRED`

### Step 3 — If BFF API Details ARE Found

The BFF API Spec repository is cloned under `{{$var[BITBUCKET_CLONE_DIR]s}}`.

> ⚠️ **STRICT ENDPOINT LOOKUP RULE — MANDATORY:**
>
> - You MUST look up **only** the exact endpoint(s) inside `{{$var[BITBUCKET_CLONE_DIR]s}}`.
> - Do NOT browse other folder, list directory contents, or scan other JSON files.
> - If the exact endpoint file is not immediately found, do **NOT** fall back to nearby, similarly-named, or related JSON files.
> - If the exact endpoint cannot be located, mark as: `BFF API CONTRACT NOT FOUND — endpoint [name] could not be located. Developer must provide the correct file path or confirm the endpoint.`

### Step 4 — Deep YAML / Spec Analysis (MANDATORY When Endpoint/OperationId File Is Found)

Once the exact endpoint YAML/JSON file is located, you MUST read and analyse the **complete** file content — do NOT skim or partially read it. Extract and analyse:

- **All request scenarios**: Every request variant — different parameter combinations, optional vs required fields, conditional headers, different body payloads.
- **All response scenarios**: Every response case — success (2xx), client error (4xx), server error (5xx), empty responses, partial data responses, conditional response shapes.
- **All response field details**: For every response scenario, extract each field name, data type, whether required or optional, and its purpose/meaning.
- **All error codes and messages**: Every error code, error message, and error response shape.
- **Conditional / branching logic**: Any conditional fields, nullable fields, or fields that appear only in certain scenarios.
- **Request/Response examples**: Any example payloads provided — use these to validate understanding of the contract.

> **YAML/SPEC READING RULE — MANDATORY**: You MUST NOT summarise or skip any scenario. Every request scenario and every response scenario MUST be individually analysed and included in the BFF API Analysis section. Ignoring or omitting any scenario is a critical failure.
>
> **SCOPE FILTER — MANDATORY**: Only analyse the endpoints that are **directly referenced in the JIRA story**. If the YAML file contains multiple endpoints (e.g., 11 endpoints), extract and document ONLY the endpoints the story requires (e.g., `/auth/otp/send`, `/auth/otp/verify`, `/auth/user/details`). Do NOT replicate or document the full YAML for endpoints not relevant to this story. Mark all other endpoints as: `Not in scope for this story.`

### BFF Analysis Areas

| Area                          | What to Identify                                                                                   |
| ----------------------------- | -------------------------------------------------------------------------------------------------- |
| Required APIs                 | Which API endpoints are needed for the user story                                                  |
| Request method                | GET / POST / PUT / PATCH / DELETE                                                                  |
| Request params                | Path params, query params, headers, body — for ALL request scenarios                               |
| Request scenarios             | Every distinct request variant / use case defined in the spec                                      |
| Response shape                | Relevant fields needed by FE — for EVERY response scenario                                         |
| Response scenarios            | Every response case — success (2xx), client errors (4xx), server errors (5xx), empty, partial data |
| Error codes and messages      | Every error code, error message, and error response shape from the spec                            |
| Conditional / nullable fields | Fields that appear only in certain scenarios or can be null/absent                                 |
| Error handling                | API-specific error scenarios and expected FE behaviour for each                                    |
| Prop impact                   | Which props/view models are populated from the API                                                 |
| Missing contract gaps         | Required fields not present in API/spec                                                            |
| Development usage             | How this BFF API will be consumed in frontend development context                                  |

---

## Data Fetching Pattern (for BFF API Integration)

All BFF API calls are **client-side calls** (not from server). The pattern is:

```
Browser
  → Component          renders UI + states
    → useHook(params)                        feature hook (Hooks/)
      → useQuery({ queryKey, queryFn })      TanStack Query
        → fetch(params, endpoint)            service function (Services/)
          → Java BFF API                     framework boundary
            → Upstream service               actual data source
```

### Layer Responsibilities

| Layer         | Folder                        | Owns                                                                            | Must NOT contain                                              |
| ------------- | ----------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Component** | `Features/<name>/Components/` | Rendering, loading/error/empty UI states, user interaction                      | Direct `fetch()` calls, query configuration, endpoint strings |
| **Hook**      | `Features/<name>/Hooks/`      | `useQuery`/`useMutation` wiring, query key usage, exposing a clean return value | JSX, endpoint URLs, business formatting                       |
| **Service**   | `Features/<name>/Services/`   | The actual `fetch()`/HTTP call, request/response shape                          | Next.js-specific code, React hooks                            |
| **Constants** | `Features/<name>/Constants/`  | Query key factories, BFF endpoint paths, magic values                           | Logic, JSX                                                    |
| **Types**     | `Features/<name>/Types/`      | Request/response TypeScript interfaces for the feature domain                   | Implementation logic                                          |

**Key rule:** The service layer is **framework-agnostic** — no Next.js imports. It must be callable and testable in plain Node.js.

### Data Fetching Pattern Output (Mandatory — Per Endpoint)

For every BFF endpoint identified, produce the following structured output:

```
Endpoint: [HTTP Method] [endpoint path]
Consuming Component: [ComponentName]
Hook: use[FeatureName]Data (Hooks/use[FeatureName]Data.ts)
Service: [FeatureName]Service (Services/[FeatureName]Service.ts)
Query Key Factory: [FEATURE_NAME]_QUERY_KEYS.[keyName]([params])
Endpoint Constant: [FEATURE_NAME]_ENDPOINTS.[endpointName]

State Rendering Rules:
  isLoading  → [what to render: skeleton / spinner / placeholder]
  isError    → [what to render: error message / error boundary / toast]
  data       → [what to render: populated component]
  isEmpty    → [what to render: empty state UI]

Infinite Scroll: [Yes / No]
Mutation Required: [Yes / No — if Yes, use useMutation instead of useQuery]
```

### Query Key Factory Pattern

Query keys must be defined in a factory in `Constants/`:

```typescript
export const [FEATURE_NAME]_QUERY_KEYS = {
  all: ['featureName'] as const,
  [keyName]: (param: ParamType) => [[FEATURE_NAME]_QUERY_KEYS.all[0], 'keyName', param] as const,
};
```

### Endpoint Constant Pattern

BFF endpoint paths must be defined in `Constants/`:

```typescript
export const [FEATURE_NAME]_ENDPOINTS = {
  [endpointName]: '/api/path/to/endpoint',
};
```

### State Rendering Rules (Applied in Component Layer)

| State   | Condition                    | FE Behaviour                                    |
| ------- | ---------------------------- | ----------------------------------------------- |
| Loading | `isLoading === true`         | Render skeleton / spinner / loading placeholder |
| Error   | `isError === true`           | Render error message / toast / error boundary   |
| Empty   | `data` is empty array / null | Render empty state UI                           |
| Partial | Some fields null/absent      | Render available data, hide absent sections     |
| Success | `data` populated             | Render full component with data                 |

---

## Required Output Sections in ANALYSIS_PLAN.md

### Sitecore API Analysis Section

```markdown
## Sitecore API Analysis

### Sitecore Endpoints Identified

| Endpoint | Purpose | Mapped FE Component | Notes |

### CMS Rendering to Component Mapping

| CMS Rendering | FE Component | Props from Sitecore | Notes |

### Sitecore-Authored Props

| Prop | Type | Sitecore Field | Required? | Notes |

### Sitecore API Contract Gaps / Assumptions

| Gap / Assumption | Impact | Needs Developer / Sitecore Confirmation? |

### How Sitecore API Will Be Used in Development

[Narrative description]
```

### BFF API Analysis Section

```markdown
## BFF API Analysis

### API Consumption Summary

| API | Purpose | Trigger Point | Consuming Component / Hook | Required? |

### Request Analysis

| API | Method | Path / Endpoint | Params / Headers / Body | Notes |

### Request Scenarios (All scenarios from YAML spec — MUST be fully populated)

| Scenario ID | Scenario Description | Request Method | Endpoint | Request Params / Body | Optional vs Required | Notes |
| REQ-001 | [scenario name] | | | | | |

### Response Analysis

| API | Response Field | Data Type | Required? | Used For | Notes |

### Response Scenarios (All scenarios from YAML spec — MUST be fully populated)

| Scenario ID | HTTP Status | Scenario Description | Response Shape / Fields | FE Handling Required | Owner |
| RES-001 | 200 | [success scenario] | | | |
| RES-002 | 4xx | [client error] | | | |
| RES-003 | 5xx | [server error] | | | |

### Error Codes and Messages (from YAML spec)

| Error Code | HTTP Status | Error Message / Shape | Trigger Condition | FE Behaviour |

### Conditional / Nullable Fields

| Field Name | Condition for Presence | Nullable? | FE Handling |

### Data Transformation / Mapping

| Source Field | Target FE Prop / View Model Field | Transformation Required | Owner |

### API to Component Prop Impact

| Component | Props Populated from API | Mapper / Utility Required | Notes |

### API Error / Edge Case Handling

| API | Scenario | Expected FE Behaviour | Owner |

### API Contract Gaps / Assumptions

| Gap / Assumption | Impact | Needs Developer / BE Confirmation? |

### Data Fetching Pattern (Per Endpoint — Mandatory for Transactional / Hybrid Components)

[For each BFF endpoint, produce the following block:]
```

Endpoint: [HTTP Method] [endpoint path]
Consuming Component: [ComponentName]
Hook: use[FeatureName]Data (Hooks/use[FeatureName]Data.ts)
Service: [FeatureName]Service (Services/[FeatureName]Service.ts)
Query Key Factory: [FEATURE_NAME]\_QUERY_KEYS.[keyName]([params])
Endpoint Constant: [FEATURE_NAME]\_ENDPOINTS.[endpointName]

State Rendering Rules:
isLoading → [skeleton / spinner / placeholder]
isError → [error message / error boundary / toast]
data → [populated component]
isEmpty → [empty state UI]

Infinite Scroll: [Yes / No]
Mutation Required: [Yes / No]

```

### How BFF API Will Be Used in Development

[Narrative description]
```

---

## Guardrails

### Do

- Perform Sitecore API analysis directly within this agent — do not delegate.
- Perform BFF API analysis directly within this agent — do not delegate.
- Look up **only** the exact endpoint identified from the JIRA story.
- Read the **complete** BFF YAML/JSON spec file once located — do NOT skim.
- List EVERY request scenario individually in the Request Scenarios table.
- List EVERY response scenario individually in the Response Scenarios table.
- List EVERY error code and error message in the Error Codes table.
- List EVERY conditional or nullable field in the Conditional / Nullable Fields table.
- Include dedicated "How it will be used in development" narrative for each API.
- Keep Sitecore API and BFF API as **separate sections** in the output document.
- Produce the **Data Fetching Pattern block** for EVERY BFF endpoint identified — including hook name, service name, query key factory, endpoint constant, state rendering rules, and mutation/infinite scroll flags.

### Do Not

- Do not delegate Sitecore or BFF API analysis to a separate agent.
- Do not invent API endpoints or fields if not provided.
- Do not browse, list, or scan the contents of cloned repository folders.
- Do not fall back to a nearby, similarly-named, or related JSON file if the exact endpoint file is not found.
- Do not open multiple JSON files to infer or reconstruct an endpoint contract.
- Do not pass raw API response directly to feature display components.
- Do not hardcode missing backend values.
- Do not merge the Sitecore API and BFF API sections — they must remain separate.
