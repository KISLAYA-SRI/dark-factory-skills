# Frontend State and Form Management

Implements state ownership and form behaviour — local transient state with React state, shared cross-component state with focused Zustand stores, server state kept in TanStack Query, controlled fields, validation utilities, and submit guarding. Only for Transactional components that need forms or shared state.

## Use This For

- Choosing the correct home for each piece of state (Phase 7).
- Creating focused Zustand stores only when sharing is genuinely justified.
- Building controlled forms with pure validation utilities.
- Handling touched/submitted behaviour and submit guarding.

## Expected Flow

```text
Classify state → server (TanStack Query) | local (React) | shared (Zustand) | CMS (Sitecore)
  → Create focused store only if sharing justified
  → Build controlled inputs + pure validators
  → Track touched/submitted, guard submit
  → Consume persona/session from existing source
```

## Key Rules

- One writable source of truth per piece of state.
- Never mirror server data into Zustand.
- Create a store only when sharing crosses distant components; otherwise use local/lifted state.
- Validators are pure — no API calls inside them.
- Load only the LOGIC LEARNINGS namespace.

See [SKILL.md](./SKILL.md) for the full instructions.
