---
name: frontend-architecture-governance-skill
description: >
  Guides agents through large-scale React/Next.js frontend architecture and governance including feature-sliced/layered architecture, module boundaries, domain modeling, micro-frontends/module federation, scalability patterns, ADRs, CODEOWNERS, review standards, documentation, and migration/refactoring plans.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend Architecture Governance Skill

## When to Use This Skill
Agents working on frontend architecture governance in React codebases.



## Prerequisites

- Identify architecture/migration objective and affected modules.

- Inspect existing repository, ownership, docs, tests, and boundaries.

- Identify validation and rollout strategy before broad changes.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions


## Workflow


### Step 1: Map current architecture and target constraints
- Inspect modules, routes, shared packages, dependency graph, ownership, docs, tests, and CI.
- Identify explicit target architecture, migration drivers, and constraints.






### Step 2: Design incremental change path
- Prefer small safe slices with compatibility and rollback.
- Define boundaries, contracts, ownership, and tests before moving code.






### Step 3: Verify governance and migration evidence
- Run relevant tests/typecheck/lint and dependency boundary checks where configured.
- Document ADR/CODEOWNERS/migration notes if required and list residual risks.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-architecture-governance-skill`
- Runtime role: `bounded_skill_step`
- Workflow steps: `3`
- Recipe supplies external context packs: `accepted_from_recipe`
- Recipe supplies external control packs: `accepted_from_recipe`
- Control tags:

  - `domain:general`

  - `type:technical`

  - `compliance:Use supplied controls only`

  - `compliance:Do not invent organization conventions`

  - `constraint:explicit architecture scope`

  - `constraint:module boundaries`

  - `constraint:incremental migration`

  - `constraint:ownership evidence`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Unscoped architecture rewrite
- Unjustified micro-frontend split
- Circular feature imports
- Big-bang framework migration


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

- [Tool Contract](references/tools.md) — Read references/tools.md before changing performance tooling, deployment/observability tooling, architecture boundaries, CI commands, or governance files.

- [Compliance Requirements](references/compliance.md) — Read references/compliance.md before approving production readiness, performance budgets, observability data collection, release controls, architecture standards, ownership, or governance claims.

- [Edge Cases](references/edge-cases.md) — Read references/edge-cases.md when performance metrics, cache behavior, deployment target, feature-flag rollout, micro-frontend boundary, or migration risk is uncertain.

- [Compiled Agent Rules](AGENTS.md) — Read AGENTS.md when detailed rule guidance, examples, and validation expectations are needed.
