# Frontend Project Foundation Skill

Guides agents through enterprise React/Next.js project foundation work including Next.js scaffolding, monorepo setup, strict TypeScript, ESLint/Prettier conventions, path aliases, environment config, and baseline validation.

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
- `rules/domain-02-preserve-existing-package-manager-and-workspace-.md` - Preserve Existing Package Manager And Workspace Boundaries (HIGH)
- `rules/domain-03-validate-environment-variables-at-runtime-bounda.md` - Validate Environment Variables At Runtime Boundary (HIGH)
- `rules/domain-04-enforce-strict-typescript-without-blocking-brown.md` - Enforce Strict TypeScript Without Blocking Brownfield Incremental Work (HIGH)
- `rules/domain-05-do-not-invent-organization-foundation-templates.md` - Do Not Invent Organization Foundation Templates (HIGH)
- `rules/tool-call-discipline.md` - Validate Frontend Foundation With Project Native Commands (HIGH)

Install or reference this skill as `frontend-project-foundation-skill`.
