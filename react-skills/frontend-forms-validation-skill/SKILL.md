---
name: frontend-forms-validation-skill
description: >
  Guides agents through React form engineering including React Hook Form, controlled/uncontrolled fields, schema validation with Zod/Yup, field arrays, multi-step wizards, persistence, submit states, accessibility, and API error mapping.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend Forms Validation Skill

## When to Use This Skill
User asks to build forms with React Hook Form, Zod/Yup validation, controlled/uncontrolled inputs, field arrays, multi-step wizards, submit behavior, or validation error handling.



## Prerequisites

- Identify form library and field patterns.

- Locate validation schema or API contract.

- Identify submit, persistence, accessibility, and backend error behavior.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions

- Policy check: Maintain accessibility and security boundaries when applicable


## Workflow


### Step 1: Map form contract and field ownership
- Identify request/response types, validation source, field components, and backend error shape.
- Classify simple form, complex form, or wizard.






### Step 2: Implement form and validation
- Use React Hook Form patterns that match existing code.
- Use schema validation and cross-field/async validation where required.






### Step 3: Verify form behavior
- Test valid submit, invalid fields, backend validation errors, pending/disabled state, focus, and wizard persistence where applicable.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-forms-validation-skill`
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

  - `constraint:react hook form`

  - `constraint:form`

  - `constraint:validation`

  - `constraint:zod`

  - `constraint:yup`

  - `constraint:field array`

  - `constraint:wizard`

  - `constraint:controlled`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Use register for native/uncontrolled inputs and Controller for controlled third-party components.
- Backend validation and conflict errors should become clear field-level or form-level feedback.
- Forms should prevent duplicate submits and expose pending, success, and retry states.
- Multi-step wizard state persistence must be explicit, restorable, and safe for sensitive fields.


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
