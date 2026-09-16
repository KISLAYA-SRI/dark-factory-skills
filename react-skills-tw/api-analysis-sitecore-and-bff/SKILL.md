---
name: api-analysis-sitecore-and-bff
description: Use this Skill to analyse already-fetched Sitecore API JSON and BFF API specs. Performs deep contract analysis of all request/response scenarios, identifies data the frontend needs but the API does not provide, and produces the Data Fetching Pattern per endpoint. Reads specs from disk; performs no fetching. Triggers include API analysis, Sitecore contract, BFF contract, API spec analysis, contract gaps, or data fetching pattern.
---

## API Analysis — Sitecore and BFF

### Purpose

This skill is for **contract analysis only** on Sitecore and BFF API specs already fetched.

- ✅ Read the fetched spec files and analyse their contracts in full
- ✅ **Identify every gap** — data the frontend needs that the API does not provide
- ✅ Produce the FE-relevant slice for ANALYSIS_PLAN.md Section 11
- ✅ Produce the Data Fetching Pattern per BFF endpoint
- ❌ **No fetching.** Never call `curl`, the http tool, or the open-api-spec MCP tool.
- ❌ **No JIRA re-scanning** for endpoints or operationIds — the CONTEXT_MANIFEST lists them.

---

### Inputs

| Input                  | Source                               | Required?                            |
| ---------------------- | ------------------------------------ | ------------------------------------ |
| CONTEXT_MANIFEST       | Phase 2                              | **Mandatory**                        |
| Classification         | Phase 3                              | **Mandatory**                        |
| Provisional prop model | Phase 3 Step 7.2                     | **Mandatory** — drives gap detection |
| Acceptance Criteria    | Phase 3 Step 4                       | **Mandatory** — drives gap detection |
| Figma findings         | Phase 5                              | **Mandatory** — drives gap detection |
| Sitecore API JSON      | `./.SC_API_SPEC/sitecore-api.json`   | Per classification                   |
| BFF API specs          | `./.BFF_API_SPEC/{operationId}.json` | Per classification                   |

⚠️ **Pure Presentational stories have no BFF specs by design.** Mark the BFF section `NOT REQUIRED` and skip BFF analysis — this is correct, not a gap.

---

### ⚠️ ANALYSIS DEPTH vs OUTPUT WIDTH — READ FIRST

```text
ANALYSIS DEPTH  →  UNCHANGED. Read the complete spec file.
                   Extract EVERY request scenario, EVERY response scenario,
                   EVERY error code, EVERY conditional/nullable field,
                   EVERY example payload. This is how gaps and edge cases are found.

OUTPUT WIDTH    →  COMPRESSED. Emit only the FE-relevant slice into
                   ANALYSIS_PLAN.md Section 11 — plus ALL gaps, which are
                   never compressed away.
```

| Work Performed (always, in full)           | Emitted To                                                          |
| ------------------------------------------ | ------------------------------------------------------------------- |
| Read complete spec file                    | Internal                                                            |
| Extract ALL request scenarios              | Internal → distil to request shape                                  |
| Extract ALL response scenarios             | Internal → distil to rendered fields + error mapping                |
| Extract ALL error codes and messages       | Internal → emit only those with distinct UI treatment               |
| Extract ALL conditional / nullable fields  | **§11.2** — these drive mapper defaults                             |
| Extract ALL example payloads               | Internal — validate contract understanding only                     |
| **Contract gap detection**                 | **DEV_REVIEW.md §5 (dedicated section)** + brief inline note in §11 |
| Sitecore rendering → FE component mapping  | **§11.1**                                                           |
| Resolve provisional `Source Detail` values | **§12** — replaces `To be resolved in API analysis`                 |
| Data Fetching Pattern per endpoint         | **§11.2**                                                           |
| State rendering rules per endpoint         | **§10** — not duplicated in §11                                     |

⚠️ **Gaps are never compressed, summarised, or omitted.** Every gap is reported in full. A missing field discovered here but not reported becomes a runtime defect the Coding Agent cannot foresee.

---

## ⚠️ CONTRACT GAP ANALYSIS (MANDATORY)

This is a **first-class output of this phase**, not a footnote.

### What a Gap Is

A gap exists when the **frontend needs a piece of data** to satisfy the design, the acceptance criteria, or the prop model — and the **API contract does not provide it**.

### Gap Detection Method

Compare what the FE requires against what the contract delivers:

```text
FE REQUIREMENTS                          API CONTRACT
├── Provisional prop model (§12)   ──┐
├── Acceptance criteria (§4)       ──┼──►  Sitecore fields available
├── Figma-identified content       ──┤     BFF response fields available
└── States requiring data (§10)    ──┘
                                          ↓
                              Anything required but NOT available = GAP
```

For **every** prop in the provisional model marked `Sitecore` or `BFF API`, locate its source field in the contract. If it cannot be located, that is a gap — record it. Do **not** silently leave the prop as `Unknown` without recording why.

### Gap Categories

| Category                          | Definition                                                       | Example                                                          |
| --------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Missing field**                 | FE needs a field the response does not contain                   | UI shows policy end date; response has only start date           |
| **Missing endpoint**              | A required capability has no endpoint at all                     | AC requires cancelling a request; no cancel operation exists     |
| **Insufficient detail**           | Field exists but lacks needed granularity                        | Response returns a status code but no display message            |
| **Missing error semantics**       | UI must distinguish failure types the contract does not separate | All failures return generic 500; UI needs "expired" vs "invalid" |
| **Missing pagination / metadata** | List UI needs totals or cursors not provided                     | Pager needs total count; response has only the page array        |
| **Type / format mismatch**        | Field exists but in an unusable form                             | Date as free-text string where UI needs an ISO timestamp         |
| **Missing CMS field**             | Sitecore rendering lacks an authored field the design requires   | Design shows a subtitle; rendering has no subtitle field         |

### Gap Output → DEV_REVIEW.md §5

Assign each gap a stable ID and record it in the dedicated section:

```markdown
## 5. API Contract Gaps

> Data the frontend requires that the API contract does not currently provide.
> Each gap blocks or degrades a specific piece of functionality and requires
> a backend/CMS decision before implementation can be completed.

| Gap ID  | Category      | What FE Needs | Needed For                  | Expected Source                  | Contract Evidence                     | Impact if Unresolved      | Recommended Action         |
| ------- | ------------- | ------------- | --------------------------- | -------------------------------- | ------------------------------------- | ------------------------- | -------------------------- |
| GAP-001 | Missing field | [field/data]  | [AC-00x / component / prop] | [endpoint or Sitecore rendering] | [what the contract actually contains] | [what breaks or degrades] | [specific backend/CMS ask] |
```

**Every column is mandatory:**

- **What FE Needs** — the concrete data item, named precisely.
- **Needed For** — the AC ID, component, or prop that requires it. A gap with no consumer is not a gap.
- **Expected Source** — which endpoint or Sitecore rendering should own it.
- **Contract Evidence** — what the spec actually contains, proving absence. Never assert absence without checking.
- **Impact if Unresolved** — what the user sees or loses.
- **Recommended Action** — a specific, actionable ask, not "clarify with backend".

⚠️ If there are no gaps, write: `No API contract gaps identified. All frontend data requirements are satisfied by the available contracts.` **Never leave this section blank** — a blank section is indistinguishable from "not checked".

### Gap Handling Elsewhere

| Location                         | What to record                                                            |
| -------------------------------- | ------------------------------------------------------------------------- |
| **§11.1 / §11.2 — Gaps line**    | Brief factual note: `Gaps: [field] not present in response (GAP-001)`     |
| **§12 — Prop model**             | Mark the affected prop `Unknown — source contract not provided`           |
| **§10 — States**                 | If a gap forces a fallback/degraded state, record that state              |
| **§8 — Things NOT to Implement** | If a gap makes a feature unbuildable this sprint, list it with the reason |

⚠️ ANALYSIS_PLAN.md must remain decisive. State the gap as **fact** and the chosen fallback as a **decision**. Never write "needs developer confirmation" or reference DEV_REVIEW.md in the plan.

---

### ⚠️ TASK-LEVEL FAIL-STOP RULE

Sitecore analysis and BFF analysis are **independent tasks**.

> If a spec file is missing or unreadable despite passing validation, **stop that task only**. Do not invent API fields, endpoints, or properties. Do not abort the other task, the phase, or the agent.

---

## 6.1 Sitecore API Analysis

The Sitecore API JSON is at `./.SC_API_SPEC/sitecore-api.json`.

**Step 1 — If NO Sitecore API details are found:**

Do not invent API fields or endpoints. Mark the section:

```text
SITECORE API NOT FOUND / NOT REQUIRED
```

**Step 2 — If Sitecore API details ARE found:**

Use this file as the source of truth for the Sitecore integration response contracts.

> ⚠️ **STRICT LOOKUP RULE — MANDATORY:**
>
> - Read **only** `./.SC_API_SPEC/sitecore-api.json`. Do NOT browse the folder, list directory contents, or scan other JSON files.
> - If the contract cannot be located within it, mark: `SITECORE API CONTRACT NOT FOUND — endpoint [name] could not be located. Developer must confirm the endpoint.` and proceed without inventing fields.

**Analyse (in full):**

- Which CMS rendering maps to which FE component
- Which props are CMS-authored
- Which props are passed from Sitecore to FE
- Placeholder key, datasource and template
- **Missing fields** — every design/AC-required authored field absent from the rendering → **GAP**
- Unclear rendering, unknown datasource
- How the Sitecore API will be consumed in frontend development

**Step 3 — Resolve provisional prop sources.** For every §12 prop marked `Sitecore` with `To be resolved in API analysis`, substitute the actual field name. If no field exists → record a GAP and mark the prop `Unknown — source contract not provided`.

**Step 4 — Distil to §11.1:**

```markdown
### 11.1 Sitecore Contract

| Rendering | FE Entry Component | Field Name | Field Type | Maps To Prop |
| --------- | ------------------ | ---------- | ---------- | ------------ |
|           |                    |            |            |              |

- **Placeholder:** [key, or: None]
- **Datasource / Template:** [name, or: Not Provided]
- **Gaps:** [brief note per gap with GAP ID, or: None]
```

⚠️ Do **not** emit separate "Sitecore Endpoints Identified", "CMS Rendering to Component Mapping", "Sitecore-Authored Props", or "How Sitecore API Will Be Used in Development" sections.

---

## 6.2 BFF API Specification Analysis

**Step 1 — Identify BFF/Backend Endpoints:** read the operationIds from the **CONTEXT_MANIFEST**. Do not re-scan the JIRA story.

**Step 2 — If NO BFF API details are found:**

For a presentational component, or when no BFF details exist, do not invent API fields or endpoints. Define the expected frontend prop model and mark backend mapping as pending. Mark the section:

```text
BFF API NOT FOUND / NOT REQUIRED
```

**Step 3 — If BFF API details ARE found:**

Each operation's spec is at `./.BFF_API_SPEC/{operationId}.json`. Use these as the source of truth for request/response contracts.

> ⚠️ **STRICT LOOKUP RULE — MANDATORY:**
>
> - Open **only** the `{operationId}.json` files named in the CONTEXT_MANIFEST. Do NOT browse the folder, list directory contents, or scan other JSON files.
> - If a spec file is not found, do **NOT** fall back to a nearby, similarly-named, or related file. Do **NOT** open other files to infer the contract.
> - If the operation cannot be located, mark: `BFF API CONTRACT NOT FOUND — operation [operationId] could not be located.` and proceed without inventing fields.

**Data fetching guidance:** apply the project's approved pattern — Component → Hook → TanStack Query → Service → Java BFF API → Upstream Service. Do not deviate unless the story specifies otherwise.

**Step 4 — Deep API Spec Analysis (MANDATORY when a spec is found):**

Read and analyse the **complete** endpoint specification — do NOT skim. Extract and analyse:

- **All request scenarios**: every request variant — parameter combinations, optional vs required fields, conditional headers, different body payloads.
- **All response scenarios**: success (2xx), client error (4xx), server error (5xx), empty responses, partial data, conditional response shapes.
- **All response field details**: for every scenario — field name, data type, required/optional, purpose.
- **All error codes and messages**: every code, message, and error response shape.
- **Conditional / branching logic**: conditional fields, nullable fields, fields appearing only in certain scenarios.
- **Request/Response examples**: use to validate contract understanding.

> ⚠️ **SPEC READING RULE — MANDATORY**: You MUST NOT summarise or skip any scenario **during analysis**. Every request and response scenario MUST be individually analysed. Omitting a scenario is a critical failure.

**SCOPE FILTER:** analyse only the operations named in the CONTEXT_MANIFEST. Mark others `Not in scope for this story.`

**Analyse (in full):**

| Area                          | What to Identify                                                        |
| ----------------------------- | ----------------------------------------------------------------------- |
| Required APIs                 | Which endpoints are needed for the user story                           |
| Request method                | GET / POST / PUT / PATCH / DELETE                                       |
| Request params                | Path, query, headers, body — for ALL request scenarios                  |
| Request scenarios             | Every distinct request variant / use case                               |
| Response shape                | Fields needed by FE — for EVERY response scenario                       |
| Response scenarios            | Success (2xx), client errors (4xx), server errors (5xx), empty, partial |
| Error codes and messages      | Every code, message, and error response shape                           |
| Conditional / nullable fields | Fields appearing only in certain scenarios or nullable                  |
| Error handling                | API-specific error scenarios and expected FE behaviour                  |
| Prop impact                   | Which props/view models are populated from the API                      |
| **Missing contract gaps**     | **Required FE data not present in the spec → GAP-xxx**                  |
| Development usage             | How this BFF API will be consumed in frontend development               |

**Step 5 — Gap sweep (MANDATORY).** Walk the provisional prop model, the ACs, the Figma-identified content, and the states requiring data. For every item expected from this endpoint, confirm the field exists. Record every absence as a GAP.

**Step 6 — Resolve provisional prop sources.** Replace every `To be resolved in API analysis` with the actual field path. Unresolvable → GAP + `Unknown — source contract not provided`.

**Step 7 — Distil the FE-Relevant Slice:**

| Extracted in Step 4           | Keep for §11.2?                                 | Test                                        |
| ----------------------------- | ----------------------------------------------- | ------------------------------------------- |
| Endpoint + method             | ✅ Always                                       | —                                           |
| Request fields                | ✅ Only fields actually sent                    | Does the FE send it?                        |
| Response fields               | ✅ Only fields actually rendered                | Does any component display or branch on it? |
| Nullable / conditional fields | ✅ Always                                       | Drives mapper defaults                      |
| Error codes                   | ✅ Only those with distinct UI treatment        | Does the UI render differently?             |
| **Gaps**                      | ✅ **Always — never compressed**                | —                                           |
| Response scenarios            | ❌ Drop those never surfaced in this story's UI | Does the user ever see this state?          |
| Example payloads              | ❌ Never emit                                   | —                                           |
| Out-of-scope operations       | ❌ Never emit                                   | —                                           |

If several error codes collapse to one UI state, emit **one** row describing the collapsed mapping.

**Step 8 — Output → §11.2:**

```markdown
### 11.2 BFF Contract

- **Endpoint:** [path]
- **Method:** [GET/POST/…]

**Request shape (fields actually sent):**

| Field | In  | Type | Required? |
| ----- | --- | ---- | --------- |
|       |     |      |           |

**Response fields actually rendered:**

| Field | Type | Nullable / Conditional? | Mapper Default | Maps To Prop |
| ----- | ---- | ----------------------- | -------------- | ------------ |
|       |      |                         |                |              |

**Error → UI state mapping:**

| Error Code | UI State | Component |
| ---------- | -------- | --------- |
|            |          |           |

**Data Fetching Pattern:**

| Hook | Service | Query Key | Endpoint Constant |
| ---- | ------- | --------- | ----------------- |
|      |         |           |                   |

- **Gaps:** [brief note per gap with GAP ID, or: None]
```

⚠️ Do **not** emit the legacy tables: API Consumption Summary, Request Analysis, Request Scenarios, Response Analysis, Response Scenarios, Error Codes and Messages, Conditional/Nullable Fields (standalone), Data Transformation/Mapping, API to Component Prop Impact, API Error/Edge Case Handling, or "How BFF API Will Be Used in Development".

---

## Data Fetching Pattern (Reference — Drives the §11.2 Table)

All BFF API calls are **client-side**:

```text
Browser
  → Component                              renders UI + states
    → useHook(params)                      feature hook (Hooks/)
      → useQuery({ queryKey, queryFn })    TanStack Query
        → fetch(params, endpoint)          service function (Services/)
          → Java BFF API                   framework boundary
            → Upstream service             actual data source
```

### Layer Responsibilities

| Layer         | Folder                        | Owns                                                                 | Must NOT contain                                       |
| ------------- | ----------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------ |
| **Component** | `Features/<name>/Components/` | Rendering, loading/error/empty UI states, user interaction           | Direct `fetch()` calls, query config, endpoint strings |
| **Hook**      | `Features/<name>/Hooks/`      | `useQuery`/`useMutation` wiring, query key usage, clean return value | JSX, endpoint URLs, business formatting                |
| **Service**   | `Features/<name>/Services/`   | The actual `fetch()`/HTTP call, request/response shape               | Next.js-specific code, React hooks                     |
| **Constants** | `Features/<name>/Constants/`  | Query key factories, BFF endpoint paths, magic values                | Logic, JSX                                             |
| **Types**     | `Features/<name>/Types/`      | Request/response TypeScript interfaces                               | Implementation logic                                   |

**Key rule:** the service layer is **framework-agnostic** — no Next.js imports. Callable and testable in plain Node.js.

### Query Key Factory Pattern

```ts
export const [FEATURE_NAME]_QUERY_KEYS = {
  all: ['featureName'] as const,
  [keyName]: (param: ParamType) =>
    [[FEATURE_NAME]_QUERY_KEYS.all[0], 'keyName', param] as const,
};
```

### Endpoint Constant Pattern

```ts
export const [FEATURE_NAME]_ENDPOINTS = {
  [endpointName]: '/api/path/to/endpoint',
};
```

### State Rendering Rules (Feed §10, Not §11)

| State   | Condition                    | FE Behaviour                                  |
| ------- | ---------------------------- | --------------------------------------------- |
| Loading | `isLoading === true`         | Render skeleton / spinner / placeholder       |
| Error   | `isError === true`           | Render error message / toast / error boundary |
| Empty   | `data` is empty array / null | Render empty state UI                         |
| Partial | Some fields null/absent      | Render available data, hide absent sections   |
| Success | `data` populated             | Render full component with data               |

Also determine per endpoint: **Infinite Scroll** (Yes/No) and **Mutation Required** (Yes/No). Record in the Data Fetching Pattern row or as a §10 state row where they change UI behaviour.

⚠️ Continue STATE-xxx numbering from Phase 3/5 when adding API-driven states. Do not renumber.

---

### Guardrails

#### Do

- Read only the spec files named in the CONTEXT_MANIFEST.
- Read the **complete** spec file — do NOT skim.
- Analyse EVERY request scenario, response scenario, error code, and conditional/nullable field **in full**.
- **Run the gap sweep against the prop model, ACs, Figma content and states.**
- **Record every gap with full evidence in DEV_REVIEW.md §5.**
- Resolve every provisional `Source Detail` or record a gap explaining why it cannot be resolved.
- Emit every nullable/conditional field — they drive mapper defaults.
- Collapse error codes sharing a UI state into one mapping row.
- Produce the Data Fetching Pattern row for every in-scope operation.
- Keep Sitecore (§11.1) and BFF (§11.2) as separate subsections.
- Skip BFF analysis entirely for Pure Presentational — that is correct, not a gap.

#### Do Not

- **Never fetch** — no `curl`, no http tool, no open-api-spec MCP.
- **Never re-scan the JIRA story** for endpoints or operationIds.
- **Never invent API endpoints, fields, or properties** to fill a gap — record the gap instead.
- **Never leave a prop as `Unknown` without a corresponding GAP entry.**
- **Never leave DEV_REVIEW.md §5 blank** — state "No API contract gaps identified" if there are none.
- **Never compress, summarise, or omit a gap.**
- **Never assert a field is missing without checking the contract** — every gap needs evidence.
- Never browse, list, or scan spec folders.
- Never fall back to a nearby or similarly-named file.
- **Never skip any scenario during analysis.**
- **Never emit full example payloads into ANALYSIS_PLAN.md.**
- **Never emit response scenarios that never surface in this story's UI.**
- **Never emit a standalone Sitecore-Authored Props table** — per-prop detail belongs to §12.
- Never merge §11.1 and §11.2.
- Never renumber STATE-xxx or INT-xxx IDs from earlier phases.
- Never pass raw API responses directly to feature display components.
- Never hardcode missing backend values.
- **Never write "needs developer confirmation" into ANALYSIS_PLAN.md** — state the gap as fact and the fallback as a decision.

---

### Gate: Phase 6 Complete When

**Analysis completeness:**

- [ ] CONTEXT_MANIFEST consulted — spec files identified
- [ ] Complete spec file read for every in-scope operation — not skimmed
- [ ] Every request scenario individually analysed
- [ ] Every response scenario individually analysed (2xx/4xx/5xx/empty/partial)
- [ ] Every error code and message analysed
- [ ] Every conditional/nullable field identified
- [ ] Example payloads used to validate contract understanding
- [ ] Strict lookup rule followed — no folder browsing, no fallback files
- [ ] Out-of-scope operations marked, not analysed

**Gap analysis:**

- [ ] Gap sweep run against the provisional prop model
- [ ] Gap sweep run against the acceptance criteria
- [ ] Gap sweep run against Figma-identified content
- [ ] Gap sweep run against states requiring data
- [ ] Every gap has a GAP-xxx ID and all eight columns populated
- [ ] Every gap cites contract evidence proving absence
- [ ] Every gap names a concrete consumer (AC / component / prop)
- [ ] **DEV_REVIEW.md §5 populated — or explicitly states no gaps**
- [ ] §11.1 / §11.2 Gaps lines carry brief notes with GAP IDs
- [ ] Props that cannot be sourced are marked `Unknown` AND have a GAP entry

**Emission discipline:**

- [ ] §11.1 emitted as the Sitecore contract table + placeholder/datasource/gaps
- [ ] §11.2 emitted as: request shape, rendered response fields, error→UI mapping, Data Fetching Pattern, gaps
- [ ] Every provisional `Source Detail` in §12 resolved or gap-recorded
- [ ] Nullable/conditional fields carried with their mapper defaults
- [ ] No example payloads emitted
- [ ] No unsurfaced response scenarios emitted
- [ ] State rendering rules routed to §10, not duplicated in §11
- [ ] No invented endpoints, fields, or properties anywhere
