---
name: frontend-state-and-form-management
description: Use to implement state ownership and form behaviour — local transient state with React state, shared cross-component state with focused Zustand stores, server state kept in TanStack Query, controlled form fields, validation utilities, touched/submitted behaviour, and submit guarding. Only for Transactional components that need forms or genuinely shared state. Triggers include state management, Zustand store, form handling, validation, controlled inputs, or manage shared state.
disable-model-invocation: true
---

## Frontend State and Form Management

### Purpose

Implement the approved state ownership model and form behaviour. Runs ONLY when a Transactional/Hybrid component genuinely needs forms or shared cross-component state. A read-only transactional card does not need this skill.

### State Ownership Model (Choose the Right Home)

```text
Server state   → TanStack Query (owned by frontend-logic-integration). Never duplicate into a store.
Local state    → React useState/useReducer for transient, component-scoped interaction.
Shared state   → focused Zustand store ONLY when 2+ distant components must share writable state.
CMS state      → Sitecore fields (read-only), never a store.
```

Rule: **one writable source of truth per piece of state.** Never mirror server data into Zustand.

### When to Create a Zustand Store

Create a store only if ALL are true:
- The state is written by one component and read/written by another that is not a direct child.
- Prop-drilling would cross more than ~2 levels or unrelated subtrees.
- The state is client-owned (not server data).

Otherwise use local state or lift state to the nearest common parent.

Store rules:
- One focused store per concern (e.g. `useMotorQuoteFormStore`), not a global mega-store.
- Expose typed state + typed actions; no `any`.
- Keep selectors narrow so components re-render only on relevant changes.

### Controlled Forms

- All inputs are controlled (value + onChange) bound to local or store state.
- Field-level validation via pure validation utilities; typed error messages.
- Track `touched` and `submitted`; show errors only after touch/submit (avoid premature errors).
- Disable submit while invalid or while a mutation is in flight (`isSubmitting`).
- On submit: run full validation → call the mutation (from the logic layer) → handle success/error via UI state.
- Validation utilities are pure and reusable; no side effects or API calls inside validators.

### Validation Utilities

```text
Utils/<Feature>Validation.ts
  validateField(name, value): string | undefined
  validateForm(values): Record<field, string>   // empty = valid
```

- Business validation rules come from the Analysis Plan / API contract, not invented here.
- Localise error messages (RTL-safe); never hardcode raw copy where the plan expects tokens/labels.

### Persona / Session State

- Consume persona/session state from the existing app-level source; do not create a parallel store.
- Branch UI/behaviour per persona only as the plan specifies.

### Learnings Namespace

Load only the `# LOGIC LEARNINGS` namespace.

### Output Files (typical)

```text
<FeatureName>/
├── Store/use<Feature>Store.ts        # only if shared state is justified
├── Utils/<Feature>Validation.ts
└── (form components live in Components/, wired via container)
```

### Gate: Complete When

```text
- [ ] State placed in the correct home (server/local/shared/CMS).
- [ ] Zustand store created only when sharing is genuinely justified; focused + typed.
- [ ] No server data duplicated into a store.
- [ ] Forms fully controlled; validation utilities pure and typed.
- [ ] touched/submitted handled; submit guarded during invalid/in-flight.
- [ ] Persona/session consumed from existing source, not re-created.
```

### Never Do

- Never mirror TanStack Query server data into Zustand.
- Never create a global mega-store; keep stores focused per concern.
- Never put API calls inside validators.
- Never show validation errors before touch/submit.
- Never create a store for state that can live locally or lift one level.
