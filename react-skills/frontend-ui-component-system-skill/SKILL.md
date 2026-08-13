---
name: frontend-ui-component-system-skill
description: >
  Guides agents through React UI/component architecture including reusable component boundaries, design systems, tokens, styling strategy, headless accessible primitives, responsive layouts, Storybook documentation, and motion.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend UI Component System Skill

## When to Use This Skill
User asks to build React screens, reusable components, design-system primitives, styling strategy, responsive layouts, Storybook stories, or motion interactions.



## Prerequisites

- Inspect existing design system and component patterns.

- Identify whether this is screen-level composition or reusable primitive work.

- Identify accessibility and responsive requirements.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions

- Policy check: Maintain accessibility and security boundaries when applicable


## Workflow


### Step 1: Scope the requested code change or review
- Identify the screen, component, hook, form, state path, or Storybook story affected by the request.
- Classify the work as screen composition, reusable component, design-system primitive, styling/layout, motion, or review-only.
- Inspect existing component, token, Storybook, test, accessibility, and styling conventions before editing.


Read references/tools.md to identify project-native typecheck, lint, test, Storybook, and accessibility commands before editing.





### Step 2: Implement with existing UI boundaries
- Use existing tokens/primitives where available.
- Keep data fetching and business orchestration out of reusable UI components.
- Preserve loading, error, empty, disabled, pending, responsive, and reduced-motion behavior where relevant.






### Step 3: Verify component behavior
- Add/update Storybook stories or examples where relevant.
- Run typecheck, lint, component tests, Storybook, or accessibility checks when configured.
- Report skipped checks with command, blocker, and residual risk.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-ui-component-system-skill`
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

  - `constraint:component`

  - `constraint:screen`

  - `constraint:props`

  - `constraint:design system`

  - `constraint:tokens`

  - `constraint:storybook`

  - `constraint:tailwind`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Use existing tokens, primitives, and theme APIs instead of hard-coded colors, spacing, or controls.
- Reusable components should receive data and callbacks through props rather than importing feature services.
- Components and screens should implement realistic loading, error, empty, disabled, and pending states.
- Animations and interactions must preserve reduced-motion preferences and keyboard/focus behavior.


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
