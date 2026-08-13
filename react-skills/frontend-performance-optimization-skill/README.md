# Frontend Performance Optimization Skill

Guides agents through React/Next.js frontend performance optimization including Core Web Vitals, rendering strategy, bundle analysis, code splitting, image/font optimization, caching/revalidation, performance budgets, and virtualization for large data UIs.

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
- `rules/domain-02-do-not-publicly-cache-personalized-data.md` - Do Not Publicly Cache Personalized Data (HIGH)
- `rules/domain-03-optimize-lcp-assets-without-breaking-priority-co.md` - Optimize LCP Assets Without Breaking Priority Content (HIGH)
- `rules/domain-04-reduce-client-javascript-before-adding-more-memo.md` - Reduce Client JavaScript Before Adding More Memoization (HIGH)
- `rules/domain-05-virtualize-large-lists-without-breaking-accessib.md` - Virtualize Large Lists Without Breaking Accessibility (HIGH)
- `rules/tool-call-discipline.md` - Measure Before Claiming Performance Improvement (HIGH)

Install or reference this skill as `frontend-performance-optimization-skill`.
