---
name: frontend-api-integration-skill
description: >
  Guides agents through frontend API integration including typed REST clients, GraphQL clients/codegen, OpenAPI type generation, BFF/API route layers, retries, pagination, error normalization, realtime WebSocket/SSE streams, and contract alignment.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend API Integration Skill

## When to Use This Skill
User asks to integrate REST/GraphQL APIs, generate frontend types from contracts, build API clients, add BFF/API routes, retries, pagination, realtime streams, or frontend API error handling.



## Prerequisites

- Locate API contract/schema or existing client.

- Identify auth/session and error model.

- Identify pagination/retry/idempotency requirements.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions

- Policy check: Maintain accessibility and security boundaries when applicable


## Workflow


### Step 1: Locate contract and client boundary
- Find OpenAPI/GraphQL schemas, generated clients, API wrappers, and MSW mocks.
- Identify whether the call belongs in browser, server component, server action, or BFF route.






### Step 2: Implement typed integration
- Use generated/shared types where possible.
- Normalize errors and preserve pagination, auth, idempotency, and retry semantics.






### Step 3: Verify API behavior
- Run typegen/typecheck/tests or report blockers.
- Update mocks and contract checks for changed calls.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-api-integration-skill`
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

  - `constraint:rest`

  - `constraint:graphql`

  - `constraint:openapi`

  - `constraint:typegen`

  - `constraint:typed client`

  - `constraint:api client`

  - `constraint:bff`

  - `constraint:websocket`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- API keys and privileged tokens must stay in server-only route handlers/server actions, not browser bundles.
- Frontend clients should map transport, validation, auth, conflict, and server errors into typed UI-safe errors.
- Retries must be limited to safe reads or writes with explicit idempotency semantics.
- MSW and test fixtures must follow current contract/generated types.


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
