# Frontend Delivery Observability Skill

Guides agents through React/Next.js frontend delivery and operations including CI/CD, preview deployments, Vercel/AWS/container deployments, Docker standalone output, feature flags, release/versioning, Sentry/Datadog, RUM, analytics, logging, tracing, and incident runbooks.

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
- `rules/domain-02-keep-deployment-secrets-environment-scoped.md` - Keep Deployment Secrets Environment Scoped (HIGH)
- `rules/domain-03-upload-source-maps-safely.md` - Upload Source Maps Safely (HIGH)
- `rules/domain-04-feature-flags-need-defaults-rollback-and-cleanup.md` - Feature Flags Need Defaults Rollback And Cleanup (HIGH)
- `rules/domain-05-instrument-analytics-with-consent-and-stable-eve.md` - Instrument Analytics With Consent And Stable Event Contracts (HIGH)
- `rules/tool-call-discipline.md` - Do Not Claim Production Readiness Without Delivery Evidence (HIGH)

Install or reference this skill as `frontend-delivery-observability-skill`.
