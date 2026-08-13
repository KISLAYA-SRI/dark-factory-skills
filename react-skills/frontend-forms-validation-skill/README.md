# Frontend Forms Validation Skill

Guides agents through React form engineering including React Hook Form, controlled/uncontrolled fields, schema validation with Zod/Yup, field arrays, multi-step wizards, persistence, submit states, accessibility, and API error mapping.

## Structure
- `SKILL.md` - Activation, workflow, references, and recipe contract.
- `AGENTS.md` - Compiled rule guide for agent execution.
- `rules/` - Atomic rules with impact, examples, and validation expectations.
- `references/` - Contracts, tools, systems, controls, and subskills.
- `scripts/` - Local validation and rule build helpers.
- `test-cases.json` - Evaluation prompts extracted from the rule corpus.
- `runtime-manifest.json` - Machine-readable activation, loading, companion-skill, and evidence contract.

## Commands
- `python scripts/validate_rules.py` - Validate rule frontmatter and examples.
- `python scripts/build_agents.py` - Rebuild `AGENTS.md` from `rules/`.
- `python scripts/extract_tests.py` - Rebuild `test-cases.json` from `rules/`.

## Rule Files
- `rules/trigger-scope.md` - Activate Only On The Declared Operational Trigger (CRITICAL)
- `rules/domain-02-use-react-hook-form-register-or-controller-appro.md` - Use React Hook Form Register Or Controller Appropriately (HIGH)
- `rules/domain-03-map-backend-validation-errors-to-field-and-form-.md` - Map Backend Validation Errors To Field And Form Errors (HIGH)
- `rules/domain-04-persist-wizard-state-safely-and-intentionally.md` - Persist Wizard State Safely And Intentionally (HIGH)
- `rules/domain-05-handle-submit-pending-disabled-and-double-submit.md` - Handle Submit Pending Disabled And Double Submit (HIGH)
- `rules/tool-call-discipline.md` - Base Form Fields On Contract And User Editable Data Only (HIGH)

Install or reference this skill as `frontend-forms-validation-skill`.
