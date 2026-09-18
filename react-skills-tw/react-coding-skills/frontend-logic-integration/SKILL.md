---
name: frontend-logic-integration
description: Use to generate the transactional/integration layer over already-built presentational UI — API contract types, view models, mappers, constants/query keys, framework-agnostic services, TanStack Query hooks, containers, and loading/error/empty/partial state orchestration. For Transactional and Hybrid components only. Triggers include logic integration, API integration, data fetching, TanStack Query, container, mapper, or wire up the API for this component.
disable-model-invocation: true
---

## Frontend Logic Integration

### Purpose

Layer the complete data + business logic over the presentational components. Runs ONLY for **Transactional** or **Hybrid** components. Never runs for Presentational components (hero banner/carousel).

### Approved Data Flow

```text
Component (presentational)
  → Container
  → Hook (TanStack Query)
  → Service (framework-agnostic)
  → Java BFF API
  → Upstream Service
```

Raw API responses MUST be transformed to FE view models by a **mapper** before reaching any display component. Query keys and endpoints live in **constants**; services stay framework-agnostic (no React imports).

### Ordered Generation Steps

Generate in this exact order (each step consumes the manifest's BFF/Sitecore contracts and prop models):

```text
1. Types        — API contract types (request/response) + FE ViewModel types
2. Constants    — endpoint constants + query keys (SCREAMING_SNAKE_CASE)
3. Mapper       — raw API response → FE ViewModel (pure functions, fully typed)
4. Service      — framework-agnostic API call using the constants + parser
5. Hook         — TanStack Query useQuery/useMutation returning ViewModel + status
6. Container    — consumes the hook, orchestrates states, passes props down
7. Wire         — connect container to the presentational component(s)
8. Barrels      — export public symbols from nearest index.ts
```

### Types Layer

- Separate **API contract types** (mirror the BFF/Sitecore spec exactly) from **FE ViewModel types** (what components consume).
- No `any`. Model nullable/optional/conditional fields exactly as the contract defines.
- Enumerate response variants (2xx / 4xx / 5xx / empty / partial) as needed for the mapper and states.

### Mapper Layer

- Pure, side-effect-free functions: `mapXxxResponseToViewModel(dto): XxxViewModel`.
- Handle nullable/missing fields with explicit defaults; never leak raw DTO shapes upward.
- Centralise formatting decisions that belong to data (not presentation) here.

### Service Layer

- Framework-agnostic (no React, no hooks). Accepts params, returns typed API data via the project API client with a parser closure.
- Uses endpoint + query-key constants; never inlines URLs.
- Surfaces errors as typed results the hook can translate into UI state.

### Hook Layer (TanStack Query)

- `useQuery` for reads, `useMutation` for writes; stable query keys from constants.
- Returns `{ data: ViewModel, isLoading, isError, error, ... }` — the mapper runs inside `select` or immediately after fetch so consumers only see ViewModels.
- Configure caching/staleness per the data-fetching pattern captured in the manifest (from Analysis Plan Section 17). No arbitrary values.

### Container Layer

- The container is the ONLY place that calls the hook and decides which visual state to show.
- Maps hook status → presentational props (`isLoading`, `error`, `data`, `isEmpty`).
- Owns navigation callbacks and business-rule branching; passes plain props/callbacks down.
- Contains no markup styling decisions — that stays in presentational components.

### State Orchestration (Every Applicable State)

Handle each state the manifest lists for the component:

```text
default   → render ViewModel data
loading   → pass isLoading to the presentational shell (skeleton)
success   → pass mapped data
error     → pass typed error message (no raw error object)
empty     → pass isEmpty; render empty slot
partial   → render available data + degrade gracefully
disabled/unauthorised → per business rule / persona from the plan
```

Forms and shared cross-component state are delegated to **frontend-state-and-form-management**. Sitecore field wiring is delegated to **sitecore-rendering-integration**.

### Learnings Namespace (Resolved Conflict 6)

Load only the `# LOGIC LEARNINGS` namespace. Do not read UI/TEST/STORYBOOK namespaces.

### Output Files (typical Transactional feature)

```text
<FeatureName>/
├── Components/<Component>.tsx        # presentational (from Phase 4)
├── Components/<Component>Container.tsx
├── Hooks/use<Feature>.ts
├── Services/<Feature>Service.ts
├── Types/<Feature>Types.ts           # API + ViewModel types
├── Constants/<FEATURE>_CONSTANTS.ts
├── Mappers/<Feature>Mapper.ts
└── index.ts
```

### Gate: Complete When

```text
- [ ] Types (API + ViewModel), constants/query keys, mapper, service, hook, container generated.
- [ ] Raw API → ViewModel mapping in place; no DTO reaches a display component.
- [ ] All applicable states orchestrated in the container.
- [ ] Service is framework-agnostic; endpoints/keys from constants only.
- [ ] Caching/staleness set per the plan's data-fetching pattern.
- [ ] Barrels updated; forms/state and Sitecore delegated where relevant.
```

### Never Do

- Never run for a Presentational component.
- Never place API calls in design-system or feature display components — only in services via hooks/containers.
- Never pass raw DTOs into presentational props.
- Never inline endpoint URLs or magic query keys.
- Never put React/hook code inside a service.
