# Presentational UI Generation

Generates the prop-driven React presentation layer — design-system atoms/molecules/organisms, feature display components, and views — with typed props, typed callbacks, visual state shells, and accessibility contracts. Optimised so Presentational components stay lean.

## Use This For

- Generating stateless, prop-driven UI components (Phase 4).
- Building Presentational components (hero banner, hero carousel) without API, mappers, services, or stores.
- Producing the UI foundation that logic skills later wire in Transactional stories.
- Honouring reuse decisions before creating new components.

## Expected Flow

```text
For each component in the manifest hierarchy:
  → Apply reuse decision (reuse / enhance / create new / feature-specific)
  → Generate typed Props + typed callbacks
  → Render prop-driven visual states (loading/empty/error/disabled/default)
  → Apply accessibility contract
  → Delegate responsive/RTL and media to their skills
  → Update barrels
```

## Key Rules

- Never place API calls, data fetching, mappers, services, or stores in a presentational component.
- Everything is prop-driven — no hardcoded labels, values, or colours.
- Do NOT over-engineer Presentational components — no container/hook/service/store.
- Visual states are driven by props, not by data fetching.
- Load only the UI LEARNINGS namespace .

See [SKILL.md](./SKILL.md) for the full instructions.
