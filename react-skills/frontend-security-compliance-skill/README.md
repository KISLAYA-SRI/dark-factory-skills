# Frontend Security Compliance Skill

Guides agents through browser/frontend security and compliance including CSP, XSS/CSRF controls, secure headers, sanitization, secrets boundaries, dependency/SCA/SBOM checks, cookie consent, privacy/GDPR controls, and safe audit logging.

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
- `rules/domain-02-use-least-privilege-csp-sources.md` - Use Least Privilege CSP Sources (HIGH)
- `rules/domain-03-sanitize-or-avoid-untrusted-html-rendering.md` - Sanitize Or Avoid Untrusted HTML Rendering (HIGH)
- `rules/domain-04-gate-analytics-and-cookies-by-consent-requiremen.md` - Gate Analytics And Cookies By Consent Requirements (HIGH)
- `rules/domain-05-treat-dependency-and-secret-scan-findings-as-rel.md` - Treat Dependency And Secret Scan Findings As Release Evidence (HIGH)
- `rules/tool-call-discipline.md` - Do Not Expose Secrets To Client Bundles (HIGH)

Install or reference this skill as `frontend-security-compliance-skill`.
