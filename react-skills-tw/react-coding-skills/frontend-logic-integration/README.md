# Frontend Logic Integration

Generates the transactional/integration layer over already-built presentational UI — API contract types, view models, mappers, constants/query keys, framework-agnostic services, TanStack Query hooks, containers, and state orchestration. For Transactional and Hybrid components only.

## Use This For

- Wiring data and business logic into Transactional components (Phase 6).
- Producing the Component → Hook → TanStack Query → Service → BFF flow.
- Transforming raw API responses into FE view models via mappers.
- Orchestrating loading/error/empty/partial states in containers.

## Expected Flow

```text
1. Types (API contract + FE ViewModel)
2. Constants + query keys
3. Mapper (raw response → ViewModel)
4. Service (framework-agnostic)
5. Hook (TanStack Query)
6. Container (consumes hook, orchestrates states)
7. Wire container to presentational component
8. Update barrels
```

## Key Rules

- Never runs for Presentational components.
- Raw API models must be mapped to ViewModels before reaching display components.
- No API calls in design-system or display components — only in services via hooks/containers.
- Services are framework-agnostic; endpoints/keys come from constants.
- Load only the LOGIC LEARNINGS namespace.

See [SKILL.md](./SKILL.md) for the full instructions.
