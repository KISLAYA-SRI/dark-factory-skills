---
name: nextjs-app-router-rendering-skill
description: >
  Guides agents through Next.js App Router architecture including layouts, route groups, loading/error boundaries, server/client component boundaries, metadata, dynamic routes, SEO, caching, streaming, and rendering mode choices.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Next.js App Router Rendering Skill

## When to Use This Skill
User asks to create or refactor Next.js App Router routes, layouts, loading/error UI, dynamic routes, metadata, SEO, server actions, or rendering strategy.



## Prerequisites

- Inspect existing app router structure.

- Identify route data freshness and SEO needs.

- Identify server/client component boundary before coding.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions

- Policy check: Maintain accessibility and security boundaries when applicable


## Workflow


### Step 1: Inspect route tree and rendering needs
- Map affected routes, layouts, loading/error boundaries, metadata, and data dependencies.
- Classify rendering mode and cache/revalidation requirements.






### Step 2: Implement route changes
- Keep server-only logic in server components/actions.
- Add loading, error, empty, and not-found states where route behavior requires them.






### Step 3: Verify route behavior
- Run build/typecheck or targeted Next.js checks.
- Report cache, SEO, and hydration risks.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `nextjs-app-router-rendering-skill`
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

  - `constraint:nextjs`

  - `constraint:app router`

  - `constraint:layout`

  - `constraint:route group`

  - `constraint:server component`

  - `constraint:client component`

  - `constraint:server action`

  - `constraint:ssr`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Client components should be used only for interactivity; server data, secrets, and privileged calls stay server-side.
- App routes need explicit loading, error, not-found, and empty states for realistic user flows.
- Dynamic pages should generate metadata, canonical URLs, and sitemap behavior from validated route params.
- Do not render time, random ids, browser APIs, or user-only data differently on server and client.


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
