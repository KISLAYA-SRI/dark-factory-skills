# Frontend State Management Skill

Guides agents through React state architecture including local/client state, Zustand/Redux Toolkit/Jotai, React Context, server-state caching with TanStack Query/SWR, URL state, selectors, persistence, optimistic updates, and invalidation.

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
- `rules/domain-02-prefer-local-state-before-global-stores.md` - Prefer Local State Before Global Stores (HIGH)
- `rules/domain-03-use-stable-query-keys-and-explicit-invalidation.md` - Use Stable Query Keys And Explicit Invalidation (HIGH)
- `rules/domain-04-treat-url-state-as-public-shareable-state.md` - Treat URL State As Public Shareable State (HIGH)
- `rules/domain-05-implement-optimistic-update-rollback.md` - Implement Optimistic Update Rollback (HIGH)
- `rules/tool-call-discipline.md` - Separate Client State From Server State (HIGH)

Install or reference this skill as `frontend-state-management-skill`.
