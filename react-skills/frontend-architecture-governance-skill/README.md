# Frontend Architecture Governance Skill

Guides agents through large-scale React/Next.js frontend architecture and governance including feature-sliced/layered architecture, module boundaries, domain modeling, micro-frontends/module federation, scalability patterns, ADRs, CODEOWNERS, review standards, documentation, and migration/refactoring plans.

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
- `rules/domain-02-avoid-micro-frontends-without-runtime-contract-j.md` - Avoid Micro Frontends Without Runtime Contract Justification (HIGH)
- `rules/domain-03-enforce-module-boundaries-with-imports-and-owner.md` - Enforce Module Boundaries With Imports And Ownership (HIGH)
- `rules/domain-04-use-domain-modeling-to-reduce-coupling-not-dupli.md` - Use Domain Modeling To Reduce Coupling Not Duplicate Backend Domains Blindly (HIGH)
- `rules/domain-05-plan-migrations-as-incremental-strangler-steps.md` - Plan Migrations As Incremental Strangler Steps (HIGH)
- `rules/tool-call-discipline.md` - Do Not Rewrite Architecture Without Explicit Scope And Evidence (HIGH)

Install or reference this skill as `frontend-architecture-governance-skill`.
