# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Hardening React/Next.js frontend security, CSP, XSS/CSRF protections, secure headers, dependency supply chain, secrets boundaries, cookie/privacy consent, or frontend compliance behavior.

### Do Not Use This Skill When
- React Native or mobile-specific code; use the React Native mobile skill instead.
- Backend-only authentication, authorization, security, testing, or compliance implementation where no frontend code or browser behavior is changed.
- Enterprise business rules not supplied by requirements, repository docs, context packs, control packs, design artifacts, identity docs, or tests.

### Operating Mode Selection
- Default mode: `delta_change`.
- Prefer lowest-cost valid mode: True.
- Do not use `greenfield_build` when repository files, failing tests, logs, diffs, or a narrow change request already exist.
- Select the mode before loading rules, then apply that mode max_rules_initial and workflow.
- Use `delta_change` for incremental changes and `debug_fix` for symptom-driven investigation before considering broader modes.
- `greenfield_build`: Creating a new service, new API journey, major feature, eventing/messaging capability, or full implementation from a requirement, template, or reference implementation.
  Max initial rules: 8; strategy: full_design_then_targeted_implementation.
  Required inputs:
  - business requirement
  - target stack
  - service or feature boundary
  Workflow:
  - Confirm the service or feature boundary, target stack, template/reference source, and acceptance criteria before implementation.
  - Load architecture, contract, model, persistence, security, testing, and readiness rules only when those boundaries are in scope.
  - Use broader validation only after the first implementation pass is complete.
  Escalate when:
  - A narrow change reveals missing architecture, contract, security, or persistence decisions.
  Output:
  - Implementation summary by layer
  - Files created or changed
  - Verification performed
  - Residual risks and follow-up work
  Full mode triggers:
  - New service creation
  - New API journey or major feature
  - Database schema or migration change
  - Authentication or authorization change
  - Cross-cutting error-handling change
  - Large refactor across multiple packages
  - New eventing or messaging capability
  - Build failures caused by deeper architectural issues
  - User explicitly requests full generation or full review
- `delta_change`: Existing codebase incremental changes: small refactors, bug fixes, DTO changes, controller signature changes, validation tweaks, test fixes, or single-endpoint updates.
  Max initial rules: 2; strategy: exact_change_impacted_artifacts_only.
  Required inputs:
  - exact change requested
  - target file, endpoint, test, DTO, controller, or suspected component when available
  Workflow:
  - Identify the exact change requested and classify whether it is incremental or full mode.
  - Identify only impacted files, packages, APIs, tests, and configuration.
  - Inspect the minimum files required to implement or validate the change.
  - Reuse existing project patterns instead of regenerating broad structures.
  - Preserve the existing API wire contract unless the request explicitly requires a contract change.
  - Avoid reprocessing unrelated persistence, security, OpenAPI, tests, or build configuration unless directly impacted.
  - Avoid invoking unrelated skills and avoid rewriting code not required for the change.
  Escalate when:
  - The change affects multiple layers.
  - The change introduces new APIs.
  - The change modifies persistence, migrations, authentication, authorization, cross-cutting errors, eventing, or messaging.
  - Targeted build/test failures cannot be resolved locally.
  - The user explicitly requests full generation or full review.
  Output:
  - Change type
  - Impacted files
  - Actions performed
  - Skipped areas with reason
  - Verification performed
  - Residual risks, if any
- `brownfield_change`: Existing codebase changes that are broader than delta mode, such as multi-layer feature changes, major enhancements, or coordinated refactors.
  Max initial rules: 3; strategy: impacted_layers_then_targeted_rules.
  Required inputs:
  - target files or feature area
  - expected behavior
  - existing behavior
  Workflow:
  - First determine whether the request can remain in delta mode; do not use this mode for small local changes.
  - Inspect existing files, tests, contracts, and project conventions for only the impacted layers.
  - Load only rules matching touched files, changed API boundaries, changed data models, or changed controls.
  - Do not redesign unrelated endpoints, persistence, security, deployment, or package structure without evidence of impact.
  Escalate when:
  - The change crosses API, auth, persistence, operational, or compatibility boundaries.
  Output:
  - Change type
  - Impacted layers and files
  - Actions performed
  - Verification performed
  - Skipped areas with reason
  - Residual risks
- `debug_fix`: Defect, incident, production issue, startup failure, runtime exception, incorrect business behavior, integration failure, build failure, or test failure.
  Max initial rules: 2; strategy: symptom_logs_tests_first_then_targeted_rules.
  Required inputs:
  - error, failing test, logs, or observed defect
  - suspected area or command
  Issue classifications:
  - Startup Failure
  - Runtime Exception
  - Functional Defect
  - Integration Failure
  - Persistence Failure
  - Security Failure
  - Build Failure
  - Test Failure
  Workflow:
  - Start from the symptom, not the architecture.
  - Classify the issue type.
  - Identify the smallest set of files, components, services, configurations, or tests related to the symptom.
  - Collect evidence from stack traces, logs, failing tests, impacted API, and impacted service.
  - Inspect only impacted artifacts; do not review unrelated controllers, services, entities, repositories, APIs, security rules, migrations, or configuration.
  - Propose likely root causes, implement the minimal fix only if required, and run targeted verification.
  - Run broader verification only if targeted verification fails.
  Escalate when:
  - Evidence proves the failure crosses components or cannot be fixed locally.
  Output:
  - Issue classification
  - Suspected root cause
  - Files inspected
  - Fix applied
  - Verification performed
  - Residual risk
- `review_judge`: Reviewing generated or modified code against acceptance criteria, tests, controls, and readiness evidence.
  Max initial rules: 4; strategy: acceptance_criteria_and_diff_first.
  Required inputs:
  - acceptance criteria
  - diff or generated code
  - available validation evidence
  Workflow:
  - Review acceptance criteria, changed files, and validation evidence before loading implementation-only rules.
  - Load judge, build, security, contract, persistence, and observability rules only for changed or claimed boundaries.
  - Return findings with evidence, missing checks, unsupported assumptions, hallucinated artifacts, and residual risks.
  Escalate when:
  - A ready/production claim lacks build, test, security, contract, persistence, or operational evidence.

### Context Budget
- Initial rule load limit: 4 rule files.
- Load references conditionally: True.
- Full pack review only on explicit request: True.
- Prefer `runtime-manifest.json` `rule_index` before bulk-loading `AGENTS.md`: True.
- Do not bulk-load every rule by default. Start with `rule_index` entries whose `load_when`, `tags`, and risk match the task.
- Skip rules whose `does_not_apply_to` matches the task; state skipped high-risk rules in the final evidence summary when relevant.

### Rule Loading Order
1. Check `activation_scope` and `non_activation_scope`.
2. Select the smallest relevant set from `rule_index` using `load_when`, `tags`, `risk`, and `cost_hint`.
3. Load referenced files only when their `load_when` condition is met.
4. Load companion skills when the task crosses their stated boundary.
5. Stop and ask for missing contract, context, policy, repository, or command evidence when a stop condition applies.

### Companion Skill Triggers
- `frontend-auth-authorization-skill`: Security changes touch sessions, cookies, CSRF, login, protected routes, tokens, or identity provider configuration.
- `frontend-api-integration-skill`: Security changes affect BFF/API routes, secret-backed calls, API keys, headers, or request signing.
- `frontend-testing-quality-skill`: Security controls need automated tests, dependency scans, secrets scans, or CI quality gates.

### Stop Conditions
- Required security policy, CSP sources, cookie consent requirements, data classification, or privacy/legal basis is missing.
- The agent would need to invent allowed script/style/connect/image domains, secrets policy, retention policy, or compliance obligations without evidence.
- Security/privacy checks cannot be run or reported as blocked evidence.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Client-side secret exposure
- Failure mode requires escalation: Overbroad CSP
- Failure mode requires escalation: Unsanitized HTML
- Failure mode requires escalation: Tracker before consent

### Evidence Summary Required
- `assumptions`
- `files_inspected`
- `rules_loaded`
- `references_loaded`
- `commands_run`
- `checks_skipped`
- `residual_risks`

**Claim Policy:** Do not claim implementation, validation, API behavior, control compliance, or test success without file, diff, tool, test, or explicit human-approved assumption evidence.

### Runtime Rule Index
- `rules/trigger-scope.md` - Activate Only On The Declared Operational Trigger | risk: medium | cost: load_only_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['The user intent matches the generated skill description.', 'At least one declared system, role, process stage, or domain keyword is present.']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-02-use-least-privilege-csp-sources.md` - Use Least Privilege CSP Sources | risk: high | cost: load_when_matched
  Applies to modes: review_judge
  Skip modes: greenfield_build, delta_change, brownfield_change, debug_fix
  Load when: ['Changing CSP or security headers']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-sanitize-or-avoid-untrusted-html-rendering.md` - Sanitize Or Avoid Untrusted HTML Rendering | risk: critical | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Rendering user/CMS/third-party HTML']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-gate-analytics-and-cookies-by-consent-requiremen.md` - Gate Analytics And Cookies By Consent Requirements | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding analytics, cookies, tracking, or consent UI']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-treat-dependency-and-secret-scan-findings-as-rel.md` - Treat Dependency And Secret Scan Findings As Release Evidence | risk: high | cost: load_when_matched
  Applies to modes: review_judge
  Skip modes: greenfield_build, delta_change, brownfield_change, debug_fix
  Load when: ['Changing dependencies or claiming secure/release readiness']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Do Not Expose Secrets To Client Bundles | risk: medium | cost: load_only_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding env vars, API clients, analytics, or BFF routes']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-use-least-privilege-csp-sources.md -->
---
title: "Use Least Privilege CSP Sources"
impact: "HIGH"
impactDescription: "Prevents browser-side credential leakage, XSS exposure, and unsupported compliance claims."
tags: csp, headers
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Use Least Privilege CSP Sources

CSP should allow only required sources and avoid unsafe-inline/wildcards unless justified by source evidence.

**Incorrect:**

The agent sets script-src * unsafe-inline to make a widget work.

**Correct:**

The agent identifies required widget domains, uses nonces/hashes where available, and documents any unavoidable exception.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Changing CSP or security headers

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Allowed domains are justified.
- Unsafe directives are avoided or explicitly risk-owned.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-sanitize-or-avoid-untrusted-html-rendering.md -->
---
title: "Sanitize Or Avoid Untrusted HTML Rendering"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: xss, sanitization
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Sanitize Or Avoid Untrusted HTML Rendering

Untrusted HTML must be avoided or sanitized with an approved library and constrained rendering boundary.

**Incorrect:**

The app renders CMS HTML through dangerouslySetInnerHTML without sanitization.

**Correct:**

The app sanitizes CMS HTML with an approved policy or renders structured content instead.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Rendering user/CMS/third-party HTML

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Sanitization policy or structured rendering exists.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-gate-analytics-and-cookies-by-consent-requiremen.md -->
---
title: "Gate Analytics And Cookies By Consent Requirements"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: privacy, consent
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Gate Analytics And Cookies By Consent Requirements

Analytics, tracking cookies, and session replay should follow supplied consent and privacy requirements.

**Incorrect:**

The app loads analytics and session replay before cookie consent is captured.

**Correct:**

The app delays optional trackers until consent and records consent state according to policy.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding analytics, cookies, tracking, or consent UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Consent category and load timing are explicit.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-treat-dependency-and-secret-scan-findings-as-rel.md -->
---
title: "Treat Dependency And Secret Scan Findings As Release Evidence"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: sca, secrets, dependency
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Treat Dependency And Secret Scan Findings As Release Evidence

Frontend supply-chain checks and secret scans should be run or listed as pending before release/security claims.

**Incorrect:**

The agent upgrades dependencies and claims secure without checking audit/SCA or secrets scan.

**Correct:**

The agent runs configured audit/SCA/secrets checks or reports unavailable CI gates as pending.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Changing dependencies or claiming secure/release readiness

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Configured scans run or blockers listed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Do Not Expose Secrets To Client Bundles"
impact: "HIGH"
impactDescription: ""
tags: secrets, next-public
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Do Not Expose Secrets To Client Bundles

Frontend code must keep API keys, tokens, signing secrets, and privileged config out of NEXT_PUBLIC variables and browser bundles.

**Incorrect:**

The agent adds NEXT_PUBLIC_BACKEND_ADMIN_TOKEN so the browser can call an admin API directly.

**Correct:**

The server route reads the admin token server-side and the browser receives only safe response data.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding env vars, API clients, analytics, or BFF routes

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Client-visible env vars contain no secrets.
- Secret-backed calls run server-side.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- trigger-scope.md -->
---
title: "Activate Only On The Declared Operational Trigger"
impact: "CRITICAL"
impactDescription: "Prevents broad or unsafe skill activation outside the intended operation or coding domain."
tags: activation, scope, general
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Activate Only On The Declared Operational Trigger

Use the skill only when the user request matches the generated skill description, systems, or domain-specific trigger terms. Do not activate for generic writing, planning, or unrelated tasks.

**Incorrect:**

User asks for an unrelated backend deployment review. The agent applies this skill because it sees a generic word like validation.

**Correct:**

User asks to harden frontend security, add CSP/XSS/CSRF controls, secure headers, sanitize HTML, protect secrets, audit dependencies, add cookie consent, or implement frontend privacy/GDPR behavior.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- The user intent matches the generated skill description.
- At least one declared system, role, process stage, or domain keyword is present.

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Record the matched trigger phrase or recipe step id.
- If the match is weak, return an elicitation question instead of executing.

## References
- SKILL.md
- references/recipe-interface.json
