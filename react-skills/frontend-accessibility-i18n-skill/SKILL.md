---
name: frontend-accessibility-i18n-skill
description: >
  Guides agents through accessible and internationalized React/Next.js UI including WCAG semantics, ARIA, keyboard navigation, focus management, automated a11y audits, locale routing, translations, formatting, pluralization, and RTL support.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend Accessibility I18n Skill

## When to Use This Skill
Agents working on Frontend Accessibility I18n Skill in React and Next.js frontends.



## Prerequisites

- Identify accessibility target and affected components/routes.

- Identify supported locales, translation source, and routing strategy.

- Inspect test/audit tooling and existing component primitives.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions


## Workflow


### Step 1: Map accessibility and locale scope
- Identify affected controls, forms, dialogs, routes, locales, formatting rules, and RTL requirements.
- Inspect existing primitives, translations, and a11y/i18n tests.






### Step 2: Implement accessible localized behavior
- Prefer semantic HTML and existing accessible primitives.
- Use locale-aware routing, translation keys, and formatters rather than hard-coded text/formatting.






### Step 3: Verify a11y and i18n evidence
- Run configured axe/keyboard/focus/unit/E2E/locale/RTL checks or report blockers.
- List remaining manual verification needs.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-accessibility-i18n-skill`
- Runtime role: `bounded_skill_step`
- Workflow steps: `3`
- Recipe supplies external context packs: `accepted_from_recipe`
- Recipe supplies external control packs: `accepted_from_recipe`
- Control tags:

  - `domain:general`

  - `type:technical`

  - `compliance:Use supplied controls only`

  - `compliance:Do not invent organization conventions`

  - `constraint:semantic HTML`

  - `constraint:keyboard focus`

  - `constraint:locale routing`

  - `constraint:translation keys`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Non-keyboard accessible control
- Invented translations
- Broken RTL layout
- Hard-coded date formatting


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
