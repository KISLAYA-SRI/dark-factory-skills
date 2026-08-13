---
name: frontend-state-management-skill
description: >
  Guides agents through React state architecture including local/client state, Zustand/Redux Toolkit/Jotai, React Context, server-state caching with TanStack Query/SWR, URL state, selectors, persistence, optimistic updates, and invalidation.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend State Management Skill

## When to Use This Skill
User asks to add or refactor React state, Zustand/Redux/Jotai stores, TanStack Query/SWR cache, Context providers, optimistic updates, or URL state.



## Prerequisites

- Identify source of truth.

- Identify persistence and shareability requirements.

- Inspect existing state/cache/provider conventions.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions

- Policy check: Maintain accessibility and security boundaries when applicable


## Workflow


### Step 1: Classify state source of truth
- Separate local UI state, global client state, server-derived state, and URL state.
- Identify cache lifetime, invalidation, persistence, and optimistic behavior.






### Step 2: Implement state change
- Use the smallest viable state mechanism.
- Keep server data in query/cache layers instead of duplicating stores.






### Step 3: Verify state behavior
- Test reload, navigation, invalidation, optimistic rollback, and URL shareability where applicable.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-state-management-skill`
- Runtime role: `bounded_skill_step`
- Workflow steps: `3`
- Recipe supplies external context packs: `accepted_from_recipe`
- Recipe supplies external control packs: `accepted_from_recipe`
- Control tags:

  - `domain:general`

  - `type:technical`

  - `compliance:Use supplied controls only`

  - `compliance:Do not invent organization conventions`

  - `compliance:Maintain accessibility and security boundaries when applicable`

  - `constraint:react`

  - `constraint:state`

  - `constraint:zustand`

  - `constraint:redux toolkit`

  - `constraint:jotai`

  - `constraint:context`

  - `constraint:tanstack query`

  - `constraint:swr`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Use local or lifted state unless multiple distant consumers require a shared store.
- Server-state cache keys must include all meaningful parameters and mutations must invalidate or update affected queries.
- URL/search params should store safe shareable filters and pagination, not secrets or volatile UI internals.
- Optimistic UI must define rollback, conflict, and error behavior.


## Deep Rule Pack
This package includes a maintainable rule corpus for high-fidelity agent behavior.

- Read `AGENTS.md` when detailed rule guidance, incorrect/correct examples, and evidence expectations are needed.
- Read `rules/` when a specific atomic rule applies to the current task.
- Run `python scripts/validate_rules.py` after editing rules.
- Run `python scripts/build_agents.py` after changing `rules/` to refresh the compiled guide.
- Use `test-cases.json` as evaluation scenarios for the generated skill.



## Reference Files

- [Recipe Interface Contract](references/recipe-interface.json) — Read references/recipe-interface.json if an orchestrator needs machine-readable skill contract fields.

- [Recipe Usage Boundary](references/recipe-usage.md) — Read references/recipe-usage.md if this skill is invoked as a recipe step with external context or control packs.

- [Tool Contract](references/tools.md) — Read references/tools.md before changing commands, dependencies, config, routing, generated clients, form libraries, or build setup.

- [Compliance Requirements](references/compliance.md) — Read references/compliance.md before approving accessibility, privacy, security, environment, API-contract, or enterprise conventions.

- [Edge Cases](references/edge-cases.md) — Read references/edge-cases.md when repo conventions, runtime boundaries, hydration behavior, cache behavior, or validation semantics are uncertain.

- [Compiled Agent Rules](AGENTS.md) — Read AGENTS.md when detailed rule guidance, examples, and validation expectations are needed.
