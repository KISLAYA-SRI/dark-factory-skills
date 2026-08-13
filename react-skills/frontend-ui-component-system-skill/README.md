# Frontend UI Component System Skill

Guides agents through React UI/component architecture including reusable component boundaries, design systems, tokens, styling strategy, headless accessible primitives, responsive layouts, Storybook documentation, and motion.

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
- `rules/domain-02-reuse-design-tokens-and-primitives-before-custom.md` - Reuse Design Tokens And Primitives Before Custom Styling (HIGH)
- `rules/domain-03-document-reusable-components-in-storybook.md` - Document Reusable Components In Storybook (HIGH)
- `rules/domain-04-keep-reusable-components-free-of-feature-data-fe.md` - Keep Reusable Components Free Of Feature Data Fetching (HIGH)
- `rules/domain-05-cover-loading-error-empty-and-disabled-states.md` - Cover Loading Error Empty And Disabled States (HIGH)
- `rules/domain-06-respect-reduced-motion-and-interaction-accessibi.md` - Respect Reduced Motion And Interaction Accessibility (HIGH)
- `rules/domain-07-compose-screens-as-thin-orchestration-layers.md` - Compose Screens As Thin Orchestration Layers (HIGH)
- `rules/domain-08-keep-custom-hooks-focused-and-testable.md` - Keep Custom Hooks Focused And Testable (HIGH)
- `rules/domain-09-make-interactive-components-accessible-by-defaul.md` - Make Interactive Components Accessible By Default (HIGH)
- `rules/tool-call-discipline.md` - Define Component Ownership And Prop Contracts Before Coding (HIGH)

Install or reference this skill as `frontend-ui-component-system-skill`.
