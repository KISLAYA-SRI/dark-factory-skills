# Frontend Accessibility I18n Skill

Guides agents through accessible and internationalized React/Next.js UI including WCAG semantics, ARIA, keyboard navigation, focus management, automated a11y audits, locale routing, translations, formatting, pluralization, and RTL support.

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
- `rules/domain-02-preserve-keyboard-and-focus-paths.md` - Preserve Keyboard And Focus Paths (HIGH)
- `rules/domain-03-do-not-invent-translations-or-locale-policy.md` - Do Not Invent Translations Or Locale Policy (HIGH)
- `rules/domain-04-use-locale-aware-formatting-instead-of-hard-code.md` - Use Locale Aware Formatting Instead Of Hard Coded Strings (HIGH)
- `rules/domain-05-verify-rtl-layout-and-directional-icons.md` - Verify RTL Layout And Directional Icons (HIGH)
- `rules/tool-call-discipline.md` - Prefer Semantic HTML Before ARIA (HIGH)

Install or reference this skill as `frontend-accessibility-i18n-skill`.
