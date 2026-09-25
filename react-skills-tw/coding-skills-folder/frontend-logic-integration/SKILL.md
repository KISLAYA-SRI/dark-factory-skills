---
name: frontend-logic-integration
description: Use to generate the transactional/integration layer over already-built presentational UI — API contract types, view models, mappers, constants/query keys, framework-agnostic services, TanStack Query hooks, containers, and loading/error/empty/partial state orchestration. Embeds the project data-fetching pattern in full. For Transactional and Hybrid components only. Triggers include logic integration, API integration, data fetching, TanStack Query, container, mapper, BFF, or wire up the API for this component.
disable-model-invocation: true
---

## Frontend Logic Integration

### Purpose

Layer the complete data + business logic over the presentational components. Runs ONLY for **Transactional** or **Hybrid** components. Never runs for Presentational components (hero banner/carousel).

⚠️ **This skill embeds the project's complete data-fetching pattern.** No external guideline lookup required.

---

## ⚠️ WRITE FILES, NOT DESCRIPTIONS

**The PRIMARY deliverable is actual TypeScript/React source files written to disk.**

```text
✅ Every file in the manifest written with the file-write tool, at the exact path
❌ Describing what the code would be
❌ Documenting the code in the summary as a substitute for writing it
❌ Stopping after analysis or planning and producing only a plan
```

If you find yourself writing to the summary document before source files exist on disk, you have skipped the implementation and must go back and write all source files first. **The order is: write source files → verify → document.**

If a single file cannot be written (tool error), record it as a gap and **continue with the remaining files**. Do not stop the entire implementation because one file failed.

---

## The Approved Data Flow

```text
Browser
  → Component                      renders UI + states
    → useHook(params)              feature hook (Hooks/)
      → useQuery({queryKey, queryFn})   TanStack Query
        → fetch(params, endpoint)  service function (Services/)
          → Java BFF API           framework boundary
            → Upstream service     actual data source
```

Each arrow is also a **layer boundary**. Raw API responses MUST be transformed to FE view models by a **mapper** before reaching any display component.

**Reference implementation:** `Portals/Sme/Features/.example/PolicyList/` — a pattern to copy, not production code to import from.

### Layer-by-Layer Responsibilities

| Layer | Folder | Owns | Must NOT contain |
| --- | --- | --- | --- |
| **Component** | `Features/<Domain>/<Feature>/Components/` | Rendering, loading/error/empty UI states, user interaction | Direct `fetch()` calls, query config, endpoint strings |
| **Hook** | `Features/<Domain>/<Feature>/Hooks/` | `useQuery`/`useMutation` wiring, query key usage, clean return value | JSX, endpoint URLs, business formatting |
| **Service** | `Features/<Domain>/<Feature>/Services/` | The actual `fetch()`/HTTP call, request/response shape | Next.js-specific code, React hooks |
| **Constants** | `Features/<Domain>/<Feature>/Constants/` | Query key factories, BFF endpoint paths, magic values | Logic, JSX |
| **Types** | `Features/<Domain>/<Feature>/Types/` | Request/response TypeScript interfaces | Implementation logic |
| **Provider** | `Packages/Common/Providers/QueryProvider.tsx` | App-wide `QueryClientProvider`, default query options | Feature-specific query config |
| **BFF route** | api-endpoint | Talks to the upstream service | UI logic |

⚠️ **Key rule:** the **service layer is framework-agnostic** — no Next.js imports. It must be callable and testable in plain Node.js, independent of React or Next.js. This is the one rule most worth double-checking.

---

## Ordered Generation Steps

Generate in this exact order. Each step consumes the manifest's BFF/Sitecore contracts and prop models.

```text
1. Types        — API contract types (request/response) + FE ViewModel types
2. Constants    — endpoint constants + query key factory (SCREAMING_SNAKE_CASE)
3. Mapper       — raw API response → FE ViewModel (pure functions, fully typed)
4. Service      — framework-agnostic API call using the constants
5. Hook         — TanStack Query useQuery/useMutation returning ViewModel + status
6. Container    — consumes the hook, orchestrates states, passes props down
7. Wire         — connect container to the presentational component(s)
8. Barrels      — export public symbols from nearest index.ts
```

⚠️ **Types first, constants second, mapper third** — before any hook, container, or Sitecore component. Mapper output must match the target presentational component's prop interface exactly.

---

## 1. Types Layer

- Separate **API contract types** (mirror the BFF spec exactly) from **FE ViewModel types** (what components consume).
- Use `interface` for object shapes; `type` for unions, intersections, primitives aliases.
- Use `import type` for type-only imports.
- Named exports only — no default type exports.
- ❌ Never use `any` — use `unknown` and narrow with type guards.
- ❌ Never use `@ts-ignore` / `@ts-expect-error` without an explanatory comment.
- ❌ Never cast with `as` unless the shape has been validated (add a comment explaining why).

| Pattern | Rule |
| --- | --- |
| API response shapes | Always a typed interface — never `any` or `object` |
| Error objects | Always typed error interfaces (e.g. `PolicyServiceError`) |
| Event handlers | Type the event parameter (`React.ChangeEvent<HTMLInputElement>`) |
| `useQuery` generics | Always provide both data and error type params |

**Interface suffix conventions:**

| Suffix | When |
| --- | --- |
| `Props` | Component props |
| *(none)* | Domain/entity model (`Policy`, `UserProfile`) |
| `Params` | Input to a hook or service function |
| `Response` / `Request` | API/BFF payload shape |
| `State` | Internal component/reducer state |
| `Context` | React Context value |
| `Config` | Static configuration object |

⚠️ Never prefix interfaces with `I`. Never create empty interfaces — use `Record<string, never>` or omit. Extend existing interfaces rather than duplicating fields.

Enumerate response variants (2xx / 4xx / 5xx / empty / partial) as needed for the mapper and state orchestration.

---

## 2. Constants Layer

### Query Key Factory

- ✅ Define ALL query keys in a structured factory object inside `Constants/<DOMAIN>_CONSTANTS.ts`
- ✅ Use `as const` on every key tuple to preserve literal types and enable precise cache invalidation
- ✅ Structure keys hierarchically: `[entity]` → `[entity, scope]` → `[entity, scope, params]`
- ❌ **Never** use inline string arrays as query keys inside hooks

```ts
export const POLICY_QUERY_KEYS = {
  all: ['policy'] as const,
  list: (params: PolicyListParams) =>
    [POLICY_QUERY_KEYS.all[0], 'list', params] as const,
};
```

### Endpoint Constants

```ts
export const POLICY_ENDPOINTS = {
  list: '/api/policies',
};
```

⚠️ Endpoints must live in `Constants/` — never scattered across hooks or components.

---

## 3. Mapper Layer

- Pure, side-effect-free functions: `mapXxxResponseToViewModel(dto): XxxViewModel`
- Handle nullable/missing fields with **explicit defaults** — never leak raw DTO shapes upward
- Array fields with zero items → empty array output (not `null`/`undefined`)
- Centralise formatting decisions that belong to data (not presentation) here
- Mapper output must match the target component's prop interface **exactly**

⚠️ **Create mappers BEFORE wiring display components.**

---

## 4. Service Layer

### Rules

- ✅ ALL `fetch()` calls live in `Services/` — never in components or hooks
- ✅ Accept `baseUrl` as a parameter — allows reuse from both Server and Client Components
- ✅ Use `URLSearchParams` for query string construction — never string concatenation
- ✅ Throw a **typed error** on non-2xx responses
- ✅ Use `cache: 'no-store'` for transactional data
- ✅ Wrap all `fetch()` calls in try/catch; errors bubble to the hook
- ❌ **Never** import from `'next'` in service files — keep them framework-agnostic
- ❌ **Never** import `headers()`, `cookies()`, `redirect()` or any Next.js API
- ❌ **Never** add client-only directives to service files
- ❌ **Never** hardcode URLs — use `process.env.BACKEND_SERVICE_URL` (server) or the BFF endpoint constant (client)
- ❌ **Never** call upstream services directly — always call the BFF route

---

## 5. Hook Layer (TanStack Query)

### Core Rules

⚠️ **Never call `fetch()` directly inside a component or hook.** All HTTP calls go through the service layer, invoked via TanStack Query hooks.

- ✅ Every data-fetching hook lives in `Features/<Domain>/<Feature>/Hooks/` named `use<Name>.ts`
- ✅ Hook files are client-side only
- ✅ Always provide both data and error generic type params to `useQuery<TData, TError>`
- ✅ Always return a **typed result object** — never expose the raw query object to consumers
- ✅ The mapper runs inside `select` or immediately after fetch, so consumers only see ViewModels
- ❌ **Never** place `useQuery`/`useMutation` directly inside a component — always wrap in a dedicated hook

### Query Configuration

| Option | Value | Why |
| --- | --- | --- |
| `staleTime` | `0` for transactional/user-specific data | Always re-fetch on mount |
| `gcTime` | `5 * 60 * 1000` (5 min) | Keep data in memory for fast back-navigation |
| `retry` | `1` | One automatic retry; avoids silent retry storms |
| `refetchOnWindowFocus` | `false` for transactional data | Should not auto-refresh |

Apply the specific values captured in the manifest from the Analysis Plan's Data Fetching Pattern. **No arbitrary values.**

### Hook Selection

| Hook | Use case |
| --- | --- |
| `useQuery` | Read data (GET) with caching |
| `useMutation` | Write data (POST/PUT/DELETE) |
| `useInfiniteQuery` | Paginated lists with infinite scroll |

### ⚠️ Infinite Scroll — Mandatory for Lists

- ✅ Use `useInfiniteQuery` for **all** list and table data
- ✅ **Numbered pagination is not permitted**
- ✅ Use `IntersectionObserver` on a sentinel element to trigger `fetchNextPage`
- ✅ Set `initialPageParam: 1`; derive next page via `getNextPageParam` from the last page response
- ✅ Wrap the sentinel with `aria-live="polite"` for accessible loading announcements
- ❌ **Never** use `useState` + `setPage` for list pagination

### ⚠️ Hook vs Container Responsibility Split

```text
HOOK owns:
  TanStack Query logic
  API success and error handling logic

CONTAINER owns:
  UI actions — displaying an error in a toast
  Navigation — routing the user after an action
  (consumed via the hook's success/error callbacks or returned state)
```

### QueryProvider — Singleton

⚠️ `QueryProvider` is mounted **once**, at the outermost layer, in `pages/_app.tsx`:

```tsx
<QueryProvider>
  <ThemeProvider>
    <Header />
    {children}
  </ThemeProvider>
</QueryProvider>
```

**Rule:** feature hooks never create their own `QueryClient` or wrap their own provider. A new feature needs **zero** additional provider setup.

❌ **Never create a new `QueryClientProvider` inside a feature** — this creates a second, disconnected query cache and defeats app-wide caching.

---

## 6. Container Layer

- The container is the **ONLY** place that calls the hook and decides which visual state to show
- Maps hook status → presentational props (`isLoading`, `hasError`, `data`, `isEmpty`)
- Owns navigation callbacks and business-rule branching; passes plain props/callbacks down
- Contains **no** visual/layout markup — delegates to presentational components
- Owns loading, error, empty, and partial data state rendering
- Must NOT be imported into other feature containers unless explicitly approved
- Add `data-testid` to interactive and key structural elements

### State Rendering Rules

- ✅ Always handle all three states explicitly: `isLoading`, `isError`, and the data state
- ✅ Return a skeleton/loader for `isLoading`, an error component for `isError`, and handle empty data before rendering
- ❌ **Never** render data without first guarding against `isLoading` and `isError`

### State Orchestration (Every Applicable State)

```text
default    → render ViewModel data
loading    → pass isLoading to the presentational shell (skeleton)
success    → pass mapped data
error      → pass typed error message (no raw error object)
empty      → pass isEmpty; render empty slot
partial    → render available data + degrade gracefully
disabled / unauthorised → per business rule / persona from the plan
```

---

## 7. Error Handling

- ✅ Service functions wrap all `fetch()` calls in try/catch
- ✅ Errors bubble to the TanStack Query hook, which exposes `isError` and `error`
- ✅ Transactional components performing data fetching are the primary candidates for Error Boundary wrapping
- ✅ Error Boundaries go at the **feature component level** — e.g. `Portals/Sme/Features/Motor/`
- ❌ **Never** place an Error Boundary on `pages/[[...path]].tsx` — it is a thin catch-all shell
- ❌ **Never** use Error Boundaries for expected API failures — use try/catch + fallback UI
- ❌ **Never** expose technical error details to the user — show meaningful fallback UI only
- Presentational components that only render Sitecore fields do **not** require Error Boundaries

### Toast Message Mapping (API Error Code → Sitecore Message)

```text
1. API Error Response          → contains error code (e.g. AUTH_INVALID_CREDENTIALS)
2. Sitecore ApiResponseMessages → maps error code → display message + severity
3. Error Handler                → finds Sitecore message, replaces placeholders, maps severity to ToastType
```

| Sitecore Severity | ToastType |
| --- | --- |
| "Error" | `error` |
| "Warning" | `warning` |
| "Info" | `info` |
| "Success" | `success` |
| Unknown/Missing | `error` (default) |

⚠️ Error message copy comes from Sitecore — never hardcode it.

---

## 8. Prop-Driven Wiring Rules

All data passed to presentational components flows through typed props:

- Map API ViewModel fields to the **exact prop names** in the presentational component's interface
- Map Sitecore field values to the exact prop names in that interface
- Pass loading state as `isLoading`; error as `hasError`; empty as `isEmpty`
- Pass all interaction callbacks (`onSubmit`, `onClick`, `onChange`) from container to component
- ❌ **Never** pass raw API response objects as props
- ❌ **Never** add new props to presentational components unless absolutely required for wiring; if needed, record it as a gap and add the minimal prop

---

## 9. Component Layering — This Skill's Role

| Layer | Responsibility | This Skill |
| --- | --- | --- |
| Sitecore-mapped component | Entry point for Sitecore rendering | Delegated to `sitecore-rendering-integration` |
| **Container** | API calls, session/persona, loading/error/empty state, orchestration | **CREATE** |
| View | Layout composition using prepared props | Wire only if needed |
| Feature display component | Business display block using prepared props | Already built — wire props only |
| Design-system component | Business-neutral reusable UI | **Do NOT modify** unless a prop addition is needed |

- Do not put business logic in design-system components
- Do not import feature components into other feature components unless explicitly approved

---

## 10. Scope Discipline

- ❌ **Never** invent API fields not present in the approved contract
- ❌ **Never** add unapproved API calls or endpoints
- ❌ **Never** implement backend business logic in the FE
- ❌ **Never** generate update/edit flows if they are out of story scope
- ❌ **Never** hardcode any labels, copy, CTA text, messages, routes, URLs, or icon names
- ❌ **Never** hardcode magic values — API paths, retry counts, timeouts belong in `Constants/`
- ❌ **Never** use fallback hardcoded content — only Storybook may use mock values

---

## Common Agent Mistakes to Avoid

| Mistake | Why it's wrong | Correct approach |
| --- | --- | --- |
| Generating a hook for a Presentational component | Presentational components only render Sitecore content | Check classification first; skip data fetching entirely |
| Putting `useQuery` directly in the component | Bypasses the hook layer; untestable, non-reusable | Always wrap `useQuery` in a feature hook |
| Hardcoding the BFF endpoint in the service | Hard to find, update, and test | Define in `Constants/`, pass to the service |
| Importing `headers()`/`cookies()` in the service | Breaks framework-agnostic guarantee | Keep Next.js APIs in the BFF route |
| Creating a separate QueryProvider per feature | Isolated caches; defeats app-wide caching | Always reuse the root provider |
| Skipping the query key factory | Hand-written keys cause cache collisions or drift | Always use the factory from `Constants/` |
| Generating update/edit flows when only read is in scope | Out-of-scope, untested code | Respect story scope |

---

### Delegation

- Forms and shared cross-component state → **`frontend-state-and-form-management`**
- Sitecore field wiring → **`sitecore-rendering-integration`**

### Learnings Namespace

Load only the `# LOGIC LEARNINGS` namespace. Do not read UI/TEST/STORYBOOK namespaces.

### Output Files (typical Transactional feature)

```text
Portals/Sme/Features/<Domain>/<FeatureName>/
├── Components/<Component>.tsx            # presentational (from earlier phase)
├── Components/<Component>Container.tsx
├── Hooks/use<Feature>.ts
├── Services/<Feature>Service.ts
├── Types/<Feature>Types.ts               # API + ViewModel types
├── Constants/<FEATURE>_CONSTANTS.ts
├── Mappers/<Feature>Mapper.ts
└── index.ts
```

---

### Gate: Complete When

```text
FILES ON DISK
- [ ] Every file in the manifest WRITTEN TO DISK at the exact path (not just described).
- [ ] Any unwritable file recorded as a gap; remaining files still written.

LAYERS
- [ ] Types (API + ViewModel), constants/query keys, mapper, service, hook, container generated.
- [ ] Generation followed the mandatory order (types → constants → mapper → service → hook → container).
- [ ] Raw API → ViewModel mapping in place; no DTO reaches a display component.
- [ ] Service is framework-agnostic — zero Next.js imports, zero React hooks.
- [ ] Service calls the BFF route, never the upstream service directly.

QUERY LAYER
- [ ] Query keys from the factory in Constants/ with `as const`; no inline keys.
- [ ] Endpoints from Constants/; no inline URLs.
- [ ] staleTime / gcTime / retry / refetchOnWindowFocus set per the plan.
- [ ] useInfiniteQuery used for all lists/tables; no numbered pagination.
- [ ] No new QueryClientProvider created.
- [ ] Hook returns a typed ViewModel result — raw query object not exposed.

CONTAINER
- [ ] All applicable states orchestrated (loading/error/empty/partial/success).
- [ ] Container owns navigation/toast; hook owns query + API success/error logic.
- [ ] No visual/layout markup in the container.

QUALITY
- [ ] No `any`; typed errors; interface suffix conventions applied.
- [ ] No hardcoded labels, copy, routes, URLs, or magic values.
- [ ] data-testid on interactive elements.
- [ ] Barrels updated with named re-exports.
- [ ] Forms/state and Sitecore delegated where relevant.
```

### Never Do

- Never run for a Presentational component.
- **Never produce only a summary, plan, or documentation — write the source files.**
- Never place API calls in design-system or feature display components.
- Never pass raw DTOs into presentational props.
- Never inline endpoint URLs or magic query keys.
- Never put React/hook code inside a service.
- Never import Next.js APIs in a service function.
- Never call the upstream service directly — always via the BFF.
- Never create a second QueryClientProvider.
- Never use numbered pagination for lists.
- Never invent API or Sitecore fields not in the approved contract.
- Never hardcode labels, copy, routes, URLs, or error messages.
- Never re-implement or modify presentational components (UI phase already built them).
- Never create Storybook `.stories` files or test files.
- Never run lint, type-check, or test commands.
- Never re-analyse the story or change approved architecture decisions.
