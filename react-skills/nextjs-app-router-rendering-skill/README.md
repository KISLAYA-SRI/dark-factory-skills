# Next.js App Router Rendering Skill

Guides agents through Next.js App Router architecture including layouts, route groups, loading/error boundaries, server/client component boundaries, metadata, dynamic routes, SEO, caching, streaming, and rendering mode choices.

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
- `rules/domain-02-provide-route-level-loading-error-and-empty-stat.md` - Provide Route Level Loading Error And Empty States (HIGH)
- `rules/domain-03-avoid-hydration-mismatches-from-non-deterministi.md` - Avoid Hydration Mismatches From Non Deterministic Rendering (HIGH)
- `rules/domain-04-align-metadata-with-dynamic-route-content.md` - Align Metadata With Dynamic Route Content (HIGH)
- `rules/domain-05-keep-server-client-boundaries-explicit.md` - Keep Server Client Boundaries Explicit (HIGH)
- `rules/tool-call-discipline.md` - Choose Rendering Strategy From Data Freshness And User Context (HIGH)

Install or reference this skill as `nextjs-app-router-rendering-skill`.
