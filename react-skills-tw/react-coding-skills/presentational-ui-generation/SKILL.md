---
name: presentational-ui-generation
description: Use to generate the prop-driven React presentation layer — design-system atoms/molecules/organisms, feature display components, and views — with typed props, typed callbacks, visual state shells, and accessibility contracts. Optimised for Presentational components (hero banner, hero carousel) that need NO API, mappers, services, or state stores. Triggers include UI generation, presentational component, display component, prop-driven UI, or generate the UI for a component.
disable-model-invocation: true
---

## Presentational UI Generation

### Purpose

Generate ONLY the presentation layer: stateless, prop-driven React components that render data passed in and raise typed callbacks. This is the primary build step for **Presentational** stories and the UI foundation for **Transactional** stories (logic is layered on later by other skills).

### Scope Boundary (Critical)

**Generate:**
- Design-system atoms, molecules, organisms.
- Feature display components and view/layout components.
- Typed `Props` interfaces and typed callback signatures.
- Visual state shells (loading skeleton, empty, error display) driven by props — NOT by data fetching.
- Accessibility contract (roles, labels, keyboard handlers, focus order).
- Barrel exports.

**Never generate here:**
- API calls, `fetch`, TanStack Query, hooks that fetch.
- Mappers, services, view-model transforms.
- Sitecore field extraction.
- Zustand stores / shared state.
- Business validation or persona/session logic.

> The moment a component needs data or business logic, it stops being this skill's job — the container/logic skills wire that in and pass results down as props.

### Presentational Path — Keep It Lean (Do Not Over-Engineer)

A Presentational component (e.g. hero banner, hero carousel) is plainly a UI component with interaction/effects only. For these:

- Build a **single component file** (plus sub-parts only if the hierarchy in the plan requires them).
- Local interaction state via `useState` / `useRef` is fine (carousel index, hover, expanded).
- **Do NOT** create a container, hook file, service, mapper, or store.
- **Do NOT** invoke `frontend-logic-integration`, `frontend-state-and-form-management`, or `sitecore-rendering-integration` unless the plan explicitly marks the component Transactional/Hybrid or CMS-mapped. These are part of next phases in development workflow.
- Effects (autoplay, transitions, parallax) live inside the component using standard React + CSS/transition utilities.

```text
Hero carousel (Presentational) → ONE organism component:
  props: slides[], activeIndex?, autoPlayMs?, onSlideChange?
  local state: current index, paused-on-hover
  no API, no store, no mapper — done.
```

### Reuse-First

Before creating any component, honour the `reuseDecisions[]` from the manifest:
- **Reuse existing variant** → import from the catalogue location; pass props. Do not recreate.
- **Enhance existing** → extend the existing component with the approved new prop/variant/slot (backward compatible).
- **Create new reusable** → build in the Design System; mark it as a Storybook + catalogue target.
- **Create feature-specific** → build under the feature folder; reuse DS components internally.

### Prop-Driven Rules

- Every label, value, image src, and copy comes from props — **no hardcoded strings/values/colours**.
- Props interface is explicit and typed; optional props have sensible defaults.
- Callbacks are typed (`onSelect: (id: string) => void`) — components never own navigation or side effects, they raise events.
- Booleans are predicates (`isDisabled`, `hasError`, `isLoading`).
- No `any`. Prefer discriminated unions for variant/state props.

### Visual States (Prop-Driven, Not Data-Driven)

Render states based on incoming props so the same component works in both Presentational and Transactional contexts:

```text
isLoading  → skeleton/placeholder shell
error      → error display slot (message from props)
empty      → empty state slot
disabled   → disabled styling + aria-disabled
default    → normal render
```

The component does not decide *when* it is loading — the parent passes that in.

### Accessibility Contract (Always)

- Correct semantic elements and ARIA roles; preserve heading hierarchy from the design.
- Keyboard operability for all interactive elements (Enter/Space/Arrow where relevant, e.g. carousel arrows and pager).
- Visible focus states; logical focus order; `aria-label`/`aria-labelledby` for icon-only controls.
- Respect `prefers-reduced-motion` for autoplay/transition effects.

### Responsive + RTL

Delegate responsive layout, breakpoint behaviour, token mapping, and RTL handling to **responsive-figma-implementation** (invoked nested from the orchestrator). This skill consumes the tokens/utilities that skill defines; it does not hardcode pixel values or LTR-only spacing.

### Media

If the component renders images/video/documents, delegate asset handling to **frontend-media-integration** (optimised `src`, `alt`, dimensions, lazy-loading). Never hardcode asset URLs.

### Output Files (per component)

```text
<ComponentName>/
├── <ComponentName>.tsx          # the presentational component
├── <ComponentName>Types.ts      # Props + any local view types (if non-trivial)
└── index.ts                     # barrel (named export; default export only for CMS-mapped)
```

Stories and tests are produced by their own skills (Phases 9–10), not here.

### Learnings Namespace (Resolved Conflict 6)

Load only the `# UI LEARNINGS` namespace from the learnings document. Do not read LOGIC/TEST/STORYBOOK namespaces.

### Gate: Complete When

```text
- [ ] All presentational components in the manifest generated (or reused per decisions).
- [ ] Every component is fully prop-driven — no hardcoded labels/values/colours.
- [ ] Typed Props + typed callbacks defined; no `any`.
- [ ] Visual states rendered from props; a11y contract applied.
- [ ] Responsive/RTL delegated; media delegated; barrels updated.
- [ ] NO data fetching, mappers, services, or stores in any file.
- [ ] Presentational path: no container/hook/service/store created.
```

### Never Do

- Never place API calls, TanStack Query, or data fetching in a presentational component.
- Never hardcode copy, values, or colours.
- Never create a container/hook/service/store for a plain Presentational component.
- Never introduce a raw API/Sitecore type into props — props use FE view models only.
