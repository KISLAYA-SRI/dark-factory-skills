# Frontend Auth Authorization Skill

Guides agents through React/Next.js frontend authentication and authorization including Auth.js/NextAuth, Clerk, Auth0, enterprise SSO, secure sessions, JWT/cookie handling, protected routes, RBAC/ABAC UI gating, and denied-path tests.

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
- `rules/domain-02-prevent-auth-redirect-loops.md` - Prevent Auth Redirect Loops (HIGH)
- `rules/domain-03-test-denied-paths-and-session-expiry.md` - Test Denied Paths And Session Expiry (HIGH)
- `rules/domain-04-keep-tokens-out-of-browser-storage-unless-explic.md` - Keep Tokens Out Of Browser Storage Unless Explicitly Approved (HIGH)
- `rules/domain-05-derive-permissions-from-trusted-session-claims.md` - Derive Permissions From Trusted Session Claims (HIGH)
- `rules/tool-call-discipline.md` - Do Not Treat Client UI Gating As Authorization (HIGH)

Install or reference this skill as `frontend-auth-authorization-skill`.
