---
name: frontend-security-compliance-skill
description: >
  Guides agents through browser/frontend security and compliance including CSP, XSS/CSRF controls, secure headers, sanitization, secrets boundaries, dependency/SCA/SBOM checks, cookie consent, privacy/GDPR controls, and safe audit logging.
license: MIT
compatibility: codex, claude-code, cursor, copilot
metadata:
  orchestrator_contract_ref: references/recipe-interface.json
  orchestrator_contract_version: "1.0.0"
  orchestrator_domain: "general"
  orchestrator_domain_type: "technical"
---

# Frontend Security Compliance Skill

## When to Use This Skill
Agents working on Frontend Security Compliance Skill in React and Next.js frontends.



## Prerequisites

- Identify security/privacy requirement source.

- Inspect headers/CSP/env/dependency/analytics configuration.

- Identify checks available locally or in CI.

- Policy check: Use supplied controls only

- Policy check: Do not invent organization conventions


## Workflow


### Step 1: Map frontend attack surface
- Identify scripts, styles, API/connect domains, cookies, forms, HTML rendering, analytics, and env variables.
- Classify data sensitivity and consent requirements from supplied controls.






### Step 2: Implement security controls
- Apply least-privilege headers/CSP and safe sanitization.
- Keep secrets server-only and reduce client-visible data.
- Update dependency/security config without broad unrelated churn.






### Step 3: Verify security evidence
- Run configured tests, audit/SCA, secrets, lint, and header checks or report blockers.
- List CI-only security gates separately from local evidence.










## Recipe Orchestrator Contract
- Contract version: `1.0.0`
- Skill ID: `frontend-security-compliance-skill`
- Runtime role: `bounded_skill_step`
- Workflow steps: `3`
- Recipe supplies external context packs: `accepted_from_recipe`
- Recipe supplies external control packs: `accepted_from_recipe`
- Control tags:

  - `domain:general`

  - `type:technical`

  - `compliance:Use supplied controls only`

  - `compliance:Do not invent organization conventions`

  - `constraint:browser security`

  - `constraint:client secrets boundary`

  - `constraint:privacy consent`

- Contract artifact: `references/recipe-interface.json`
- Usage boundary: `references/recipe-usage.md`


## On Failure
If any mandatory gate fails, stop execution and escalate with evidence.
- Client-side secret exposure
- Overbroad CSP
- Unsanitized HTML
- Tracker before consent


## Deep Rule Pack
This package includes a maintainable rule corpus for high-fidelity agent behavior.

- Read `AGENTS.md` when detailed rule guidance, incorrect/correct examples, and evidence expectations are needed.
- Read `rules/` when a specific atomic rule applies to the current task.
- Run `python scripts/validate_rules.py` after editing rules.
- Run `python scripts/build_agents.py` after changing `rules/` to refresh the compiled guide.
- Use `test-cases.json` as evaluation scenarios for the generated skill.



## Reference Files

- [Recipe Interface Contract](references/recipe-interface.json) — Read references/recipe-interface.json if an orchestrator needs machine-readable skill contract fields.

- [Recipe Usage Boundary](references/recipe-usage.md) — Read references/recipe-usage.md if this skill is invoked as a recipe step with external context or control packs.

- [Tool Contract](references/tools.md) — Read references/tools.md before changing auth providers, security headers, test tooling, accessibility tooling, i18n routing, or project commands.

- [Compliance Requirements](references/compliance.md) — Read references/compliance.md before approving security, privacy, WCAG, authorization, test coverage, cookie consent, locale, or regulatory behavior.

- [Edge Cases](references/edge-cases.md) — Read references/edge-cases.md when identity boundaries, browser security behavior, async tests, keyboard/focus behavior, locale routing, or RTL behavior are uncertain.

- [Compiled Agent Rules](AGENTS.md) — Read AGENTS.md when detailed rule guidance, examples, and validation expectations are needed.
