---
name: frontend-auth-authorization-skill
description: >
  Guides agents through React/Next.js frontend authentication and authorization including Auth.js/NextAuth, Clerk, Auth0, enterprise SSO, secure sessions, JWT/cookie handling, protected routes, RBAC/ABAC UI gating, and denied-path tests.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend Auth Authorization Skill

## When to Use This Skill
Agents working on Frontend Auth Authorization Skill in React and Next.js frontends.



## Prerequisites

- Identify auth provider and session model.

- Locate route protection matrix and role/scope requirements.

- Inspect existing auth helpers, middleware, API clients, and tests.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions


## Workflow


### Step 1: Map identity and route access model
- Identify provider, session source, required claims/scopes/roles, protected routes, and public routes.
- Determine which checks must run in middleware, server components/actions, API route handlers, and client UI.






### Step 2: Implement auth boundary
- Keep protected data access server-side.
- Use secure cookie/session patterns and avoid client-side token storage unless approved.
- Apply UI gating only as UX, not as the only authorization control.






### Step 3: Verify auth behavior
- Add or update login, logout, redirect, denied path, role/scope, and API auth tests.
- Report blocked provider or SSO checks with exact missing evidence.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-auth-authorization-skill`
- Runtime role: `bounded_skill_step`
- Workflow steps: `3`
- Recipe supplies external context packs: `accepted_from_recipe`
- Recipe supplies external control packs: `accepted_from_recipe`
- Control tags:

  - `domain:general`

  - `type:technical`

  - `compliance:Use supplied controls only`

  - `compliance:Do not invent organization conventions`

  - `constraint:React frontend auth`

  - `constraint:Next.js protected routes`

  - `constraint:session cookies`

  - `constraint:RBAC UI`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Client-only route protection
- Unsafe browser token storage
- Redirect loop
- Missing denied-path tests


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

- [Tool Contract](references/tools.md) — Read references/tools.md before changing auth providers, security headers, test tooling, accessibility tooling, i18n routing, or project commands.

- [Compliance Requirements](references/compliance.md) — Read references/compliance.md before approving security, privacy, WCAG, authorization, test coverage, cookie consent, locale, or regulatory behavior.

- [Edge Cases](references/edge-cases.md) — Read references/edge-cases.md when identity boundaries, browser security behavior, async tests, keyboard/focus behavior, locale routing, or RTL behavior are uncertain.

- [Compiled Agent Rules](AGENTS.md) — Read AGENTS.md when detailed rule guidance, examples, and validation expectations are needed.
