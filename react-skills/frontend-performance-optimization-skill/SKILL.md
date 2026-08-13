---
name: frontend-performance-optimization-skill
description: >
  Guides agents through React/Next.js frontend performance optimization including Core Web Vitals, rendering strategy, bundle analysis, code splitting, image/font optimization, caching/revalidation, performance budgets, and virtualization for large data UIs.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend Performance Optimization Skill

## When to Use This Skill
Agents working on Frontend Performance Optimization Skill in React and Next.js frontends.



## Prerequisites

- Identify target route/page/component and performance metric.

- Inspect current rendering/cache/bundle/asset patterns.

- Identify available measurement commands and baseline evidence.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions


## Workflow


### Step 1: Measure and scope performance issue
- Identify affected route/component, target metric, baseline, budget, and measurement method.
- Inspect rendering mode, server/client boundaries, cache behavior, bundle contributors, images/fonts, and large-data rendering.






### Step 2: Apply targeted optimization
- Remove avoidable request waterfalls, excessive client components, unnecessary bundles, unstable layout, and oversized assets.
- Preserve correctness, accessibility, SEO, security, and cache freshness boundaries.






### Step 3: Verify performance evidence
- Run available performance, build, typecheck, bundle, or route tests.
- Report measured before/after evidence or exact blocker and residual risk.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-performance-optimization-skill`
- Runtime role: `bounded_skill_step`
- Workflow steps: `3`
- Recipe supplies external context packs: `accepted_from_recipe`
- Recipe supplies external control packs: `accepted_from_recipe`
- Control tags:

  - `domain:general`

  - `type:technical`

  - `compliance:Use supplied controls only`

  - `compliance:Do not invent organization conventions`

  - `constraint:measured performance evidence`

  - `constraint:safe caching`

  - `constraint:Web Vitals budgets`

  - `constraint:bundle size control`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Unmeasured performance claim
- Public cache of personalized data
- Lazy-loaded LCP image
- Large list rendering jank


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
