---
name: frontend-project-foundation-skill
description: >
  Guides agents through enterprise React/Next.js project foundation work including Next.js scaffolding, monorepo setup, strict TypeScript, ESLint/Prettier conventions, path aliases, environment config, and baseline validation.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend Project Foundation Skill

## When to Use This Skill
Scaffold or standardize a frontend React Next.js project foundation.



## Prerequisites

- Identify greenfield versus brownfield mode.

- Inspect package manager and existing scripts before adding commands.

- Identify TypeScript, lint, formatting, env, and workspace conventions before editing.

- Policy check: Do not expose secrets to browser bundles

- Policy check: Do not invent organization conventions


## Workflow


### Step 1: Classify project mode and conventions
- Determine greenfield scaffold, monorepo setup, or brownfield foundation update.
- Inspect package.json, lockfiles, tsconfig, lint/format configs, env files, workspace config, and CI.
- Preserve existing toolchain unless the request explicitly changes it.






### Step 2: Apply foundation changes
- Add only necessary scaffold/config/workspace/env changes.
- Keep server-only secrets out of client-exposed env variables.
- Prefer explicit scripts for lint, typecheck, test, build, and validate-env.






### Step 3: Verify foundation
- Run or report lint, typecheck, build, and env validation commands.
- List blocked commands with exact reason.
- Summarize changed files and remaining setup risks.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-project-foundation-skill`
- Runtime role: `bounded_skill_step`
- Workflow steps: `3`
- Recipe supplies external context packs: `accepted_from_recipe`
- Recipe supplies external control packs: `accepted_from_recipe`
- Control tags:

  - `domain:general`

  - `type:technical`

  - `compliance:Do not expose secrets to browser bundles`

  - `compliance:Do not invent organization conventions`

  - `constraint:Next.js`

  - `constraint:React`

  - `constraint:TypeScript`

  - `constraint:ESLint`

  - `constraint:Prettier`

  - `constraint:environment schema`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Wrong package manager
- Client-side secret exposure
- Inconsistent folder conventions


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
