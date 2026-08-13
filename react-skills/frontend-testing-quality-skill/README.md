# Frontend Testing Quality Skill

Guides agents through React/Next.js testing and quality strategy including Vitest/Jest, React Testing Library, MSW integration tests, Playwright/Cypress E2E, Storybook interaction tests, visual regression, coverage, and quality gates.

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
- `rules/domain-02-avoid-brittle-visual-and-snapshot-tests.md` - Avoid Brittle Visual And Snapshot Tests (HIGH)
- `rules/domain-03-use-msw-or-existing-network-mock-strategy-for-ap.md` - Use MSW Or Existing Network Mock Strategy For API Flows (HIGH)
- `rules/domain-04-await-async-ui-with-user-visible-conditions.md` - Await Async UI With User Visible Conditions (HIGH)
- `rules/domain-05-cover-critical-journeys-with-e2e-tests.md` - Cover Critical Journeys With E2E Tests (HIGH)
- `rules/tool-call-discipline.md` - Tie Tests To Changed User Observable Behavior (HIGH)

Install or reference this skill as `frontend-testing-quality-skill`.
