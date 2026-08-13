# Frontend API Integration Skill

Guides agents through frontend API integration including typed REST clients, GraphQL clients/codegen, OpenAPI type generation, BFF/API route layers, retries, pagination, error normalization, realtime WebSocket/SSE streams, and contract alignment.

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
- `rules/domain-02-normalize-api-errors-to-ui-safe-error-models.md` - Normalize API Errors To UI Safe Error Models (HIGH)
- `rules/domain-03-keep-secrets-server-side-in-bff-and-server-actio.md` - Keep Secrets Server Side In BFF And Server Actions (HIGH)
- `rules/domain-04-keep-mocks-in-sync-with-contracts.md` - Keep Mocks In Sync With Contracts (HIGH)
- `rules/domain-05-retry-only-safe-or-explicitly-idempotent-request.md` - Retry Only Safe Or Explicitly Idempotent Requests (HIGH)
- `rules/tool-call-discipline.md` - Do Not Invent Frontend API Contracts (HIGH)

Install or reference this skill as `frontend-api-integration-skill`.
