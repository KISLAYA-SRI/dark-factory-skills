---
name: frontend-state-and-form-management
description: Use to implement state ownership and form behaviour — server-first state strategy, local transient state with React state, shared cross-component state with focused Zustand stores, controlled form fields, validation utilities, touched/submitted behaviour, and submit guarding. Embeds the project state management guideline in full. Only for Transactional components that need forms or genuinely shared state. Triggers include state management, Zustand store, form handling, validation, controlled inputs, or manage shared state.
disable-model-invocation: true
---

## Frontend State and Form Management

### Purpose

Implement the approved state ownership model and form behaviour. Runs ONLY when a Transactional/Hybrid component genuinely needs forms or shared cross-component state. **A read-only transactional card does not need this skill.**

⚠️ **This skill embeds the project's complete state management guideline.** No external lookup required.

---

## ⚠️ WRITE FILES, NOT DESCRIPTIONS

The PRIMARY deliverable is actual `.ts`/`.tsx` source files written to disk at the exact paths specified.

---

## 1. Server-First Philosophy

The frontend follows a **server-first, distributed state management approach** aligned with Next.js and Sitecore's server-driven rendering model. The objective is to **minimise client-side state**, keep components self-contained, and maintain clear separation between server-rendered content, local UI state, and shared application state.

### Design Principles

| Principle | Meaning |
| --- | --- |
| **Server-First Strategy** | Prioritise server-rendered content over client state. The FE renders content rather than owning or duplicating it. |
| **Component-Level Isolation** | Keep state as close as possible to the component that owns it. |
| **Stateless Page Composition** | Each page render is an independent composition driven by Layout Service data, not persisted FE state. |
| **Minimal Global State** | Use global state only when information must be shared across components or pages. |
| **Predictable Data Flow** | `Sitecore Layout Service → Component → UI`. Avoid multiple writable sources for the same data. |

---

## 2. State Ownership Model — Three Layers

```text
Server state   → TanStack Query (owned by frontend-logic-integration)
                 Never duplicate into a store.
Local state    → React useState/useReducer for transient, component-scoped interaction.
Shared state   → focused Zustand store ONLY when 2+ distant components must share writable state.
CMS state      → Sitecore fields (read-only). Never a store.
```

⚠️ **Rule: one writable source of truth per piece of state.** Never mirror server data into Zustand.

### Layer 1 — Server State (Primary Source of Truth)

Server-rendered content is the primary source of truth. The application retrieves page layouts and component content from the Sitecore Layout Service during page rendering.

**Benefits:** consistent rendering across requests · improved SEO · reduced client state · no duplicated content state · better performance.

**Rules:**
- ✅ Prefer server-side rendering for CMS-driven content
- ✅ Fetch content as close as possible to the component that consumes it
- ✅ Treat server-rendered content as **read-only** within the UI
- ✅ Revalidate or refetch content instead of maintaining client-side copies
- ❌ **Never** use global state to cache CMS-rendered content
- ❌ **Never** mix server-rendered content with client interaction state

### Layer 2 — Client-Side State (UI & Interaction)

Limited to transient UI behaviour and interactions existing only during the current session.

**Typical examples:** form inputs and validation · modal visibility · tabs and accordions · dropdown selections · loading indicators · temporary interaction state · component-level client-fetched data where SSR isn't applicable.

**Managed with:** React `useState`, component-level state isolation.

**Rules:**
- ✅ Keep UI state local to the component whenever possible
- ✅ Lift state only when multiple related components need to share it
- ✅ Store only the minimum state required; derive values where possible
- ✅ Remove temporary state when no longer required
- ❌ **Never** place local UI state into global stores

### Layer 3 — Shared / Cross-Component State (Zustand)

For state that must be shared across multiple components or pages. Zustand stores are used **only** for state genuinely read or written from more than one component — not a replacement for `useState` or server-rendered content.

**Typical shared state:** user session context · global UI state · feature flags · cross-component workflow state.

---

## 3. When to Create a Zustand Store

Create a store only if **ALL** are true:

```text
✅ The state is written by one component and read/written by another that is NOT a direct child
✅ Prop-drilling would cross more than ~2 levels or unrelated subtrees
✅ The state is client-owned (not server data)
```

Otherwise use local state or lift to the nearest common parent.

### Defining a Store

- **One store per concern**, colocated under `Store/` (e.g. `useUserStore`)
- Keep state and its actions together in the same store
- Keep the state shape **flat and typed**
- Give fields sensible defaults instead of `undefined`
- Expose typed state + typed actions; no `any`

### Reading State in a Component

- **Select only the field you need**, not the whole store
- Write the selector where it's used, not in a shared file
- Use `getState()` only outside React (e.g. event handlers); use the hook inside components

### Selecting Multiple Fields

Select a single field wherever possible. When a component needs more than one at once, use `useShallow` so it only re-renders when a selected field actually changes:

```ts
import { useShallow } from "zustand/react/shallow";
import { useUserStore } from "@/store/useUserStore";

const { user, isAuthenticated } = useUserStore(
  useShallow((state) => ({
    user: state.user,
    isAuthenticated: state.isAuthenticated,
  })),
);
```

### Communication Between Components

- Components talk **through the store**, not through each other
- Don't pass store values as props just to relay them — read the store directly
- Change state only via **store actions**, never with a local copy that can drift out of sync

### Store Usage Guidelines

- ❌ Zustand stores are **not** used to hold data owned by the Sitecore Layout Service
- ❌ A store must not grow to hold unrelated concerns — split into a new store rather than expanding scope
- ✅ Keep stores small and focused on a single responsibility
- ✅ Organise stores by feature or domain
- ✅ Expose state through reusable custom hooks
- ✅ Update only the required slices to minimise re-renders
- ✅ Clear temporary shared state when no longer needed

---

## 4. Controlled Forms

- ✅ **All inputs are controlled** (`value` + `onChange`) bound to local or store state
- ✅ Field-level validation via **pure validation utilities**; typed error messages
- ✅ Track `touched` and `submitted`; show errors **only after** user interaction or submission
- ✅ **Disable the form during submission** to prevent duplicate requests
- ✅ Provide visual feedback for loading/submitting states
- ✅ On submit: run full validation → call the mutation (from the logic layer) → handle success/error via UI state
- ❌ **Never** show validation errors on initial render before user interaction

### Reference Pattern

```ts
const [formData, setFormData] = useState<FormData>(initialState);
const [validationErrors, setValidationErrors] = useState<ValidationErrors>({});
const [showValidation, setShowValidation] = useState(false);

const handleFieldChange = (field: keyof FormData, value: string) => {
  setFormData((prev) => ({ ...prev, [field]: value }));
  if (showValidation && validationErrors[field]) {
    setValidationErrors((prev) => {
      const newErrors = { ...prev };
      delete newErrors[field];
      return newErrors;
    });
  }
};

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setShowValidation(true);
  const errors = validateForm(formData);
  if (hasValidationErrors(errors)) return;
  // Submit form
};
```

---

## 5. Validation Utilities

```text
Utils/<Feature>Validation.ts
  validateField(name, value): string | undefined
  validateForm(values): Record<field, string>   // empty = valid
```

- Validation logic lives in the container or a dedicated validation utility — **NOT** in presentational components
- Pass validation state (error messages, field states) as **props** to presentational components
- Business validation rules come from the Analysis Plan / API contract — **not invented here**
- ❌ **Never** hardcode validation error messages — they come from Sitecore props or localisation
- ❌ **Never** put API calls or side effects inside validators
- Validation utilities are pure and reusable; RTL-safe messages

---

## 6. Persona / Session State

- Consume persona/session state from the **existing app-level source**
- ❌ Do not create a parallel store or new providers unless explicitly approved in the Analysis Plan
- Branch UI/behaviour per persona **only** as the plan specifies

---

### Output Files (typical)

```text
Portals/Sme/Features/<Domain>/<FeatureName>/
├── Store/use<Feature>Store.ts        # only if shared state is justified
├── Utils/<Feature>Validation.ts
└── (form components live in Components/, wired via container)
```

### Learnings Namespace

Load only the `# LOGIC LEARNINGS` namespace.

---

### Gate: Complete When

```text
- [ ] All files WRITTEN TO DISK at exact paths (not just described).
- [ ] State placed in the correct home (server / local / shared / CMS).
- [ ] Server-first strategy honoured — SSR content not duplicated client-side.
- [ ] Zustand store created ONLY when all three sharing conditions are met.
- [ ] Stores are focused per concern, flat, typed, with sensible defaults.
- [ ] Selectors narrow; useShallow used for multi-field selection.
- [ ] No server data duplicated into a store.
- [ ] No CMS/Layout Service data held in a store.
- [ ] Forms fully controlled; validation utilities pure and typed.
- [ ] touched/submitted handled; errors shown only after interaction or submit.
- [ ] Submit guarded during invalid/in-flight state.
- [ ] Validation messages sourced from Sitecore/localisation, never hardcoded.
- [ ] Persona/session consumed from the existing source, not re-created.
```

### Never Do

- **Never produce only a summary — write the source files.**
- Never mirror TanStack Query server data into Zustand.
- Never use global state to cache CMS-rendered content.
- Never create a global mega-store; keep stores focused per concern.
- Never let a store grow to hold unrelated concerns — split it instead.
- Never place local UI state into a global store.
- Never create a store for state that can live locally or lift one level.
- Never put API calls or side effects inside validators.
- Never show validation errors before touch/submit.
- Never hardcode validation error messages.
- Never put validation logic inside presentational components.
- Never invent new state management patterns not approved in the Analysis Plan.
- Never create new context providers unless approved.
- Never create Storybook `.stories` files or test files.
- Never run lint, type-check, or test commands.
