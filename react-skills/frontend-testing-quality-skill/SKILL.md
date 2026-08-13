---
name: frontend-testing-quality-skill
description: >
  Guides agents through React/Next.js testing and quality strategy including Vitest/Jest, React Testing Library, MSW integration tests, Playwright/Cypress E2E, Storybook interaction tests, visual regression, coverage, and quality gates.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend Testing Quality Skill

## When to Use This Skill
Agents working on Frontend Testing Quality Skill in React and Next.js frontends.



## Prerequisites

- Identify test runner and commands.

- Locate changed behavior and existing test style.

- Identify mocks/fixtures/providers and critical user journeys.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions


## Workflow


### Step 1: Select test level from changed behavior
- Map changed files and acceptance criteria to unit, component, integration, E2E, visual, accessibility, or contract tests.
- Reuse existing test utilities, providers, and MSW handlers.






### Step 2: Write targeted tests
- Prefer user-observable behavior and realistic async flows.
- Mock network with MSW or existing strategy and avoid over-mocking the component under test.






### Step 3: Run and report evidence
- Run targeted test command first, then broader quality gates if required.
- List command, result, skipped checks, and residual risk.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-testing-quality-skill`
- Runtime role: `bounded_skill_step`
- Workflow steps: `3`
- Recipe supplies external context packs: `accepted_from_recipe`
- Recipe supplies external control packs: `accepted_from_recipe`
- Control tags:

  - `domain:general`

  - `type:technical`

  - `compliance:Use supplied controls only`

  - `compliance:Do not invent organization conventions`

  - `constraint:component tests`

  - `constraint:frontend integration tests`

  - `constraint:E2E tests`

  - `constraint:visual regression`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Shallow snapshot-only tests
- Unstable async tests
- Missing API failure mocks
- Missing critical journey test


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
