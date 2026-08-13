# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Adding or reviewing frontend login/signup/session flows, Auth.js/NextAuth/Clerk/Auth0 integration, protected routes, middleware redirects, RBAC/ABAC UI gating, or enterprise SSO behavior.
- Changing frontend session/token handling, client/server auth boundaries, or authorization-based rendering.

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
- `nextjs-app-router-rendering-skill`: Auth behavior affects Next.js middleware, App Router layouts, server components, route groups, redirects, or metadata.
- `frontend-api-integration-skill`: Auth behavior affects API clients, bearer tokens, cookies, refresh flows, BFF routes, or server actions.
- `frontend-security-compliance-skill`: Session cookies, CSRF, token storage, CSP, PII, or privacy behavior is changed.
- `frontend-testing-quality-skill`: Auth flows, route guards, denied paths, role-based UI, or SSO flows need tests.

### Stop Conditions
- Identity provider, session model, auth callback URLs, required scopes/roles/claims, protected route matrix, or tenant/organization model is missing.
- The agent would need to invent authorization policy, enterprise identity provider settings, token claims, cookie settings, or SSO metadata without source evidence.
- Security-sensitive auth behavior cannot be tested or reported as blocked evidence.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Client-only route protection
- Failure mode requires escalation: Unsafe browser token storage
- Failure mode requires escalation: Redirect loop
- Failure mode requires escalation: Missing denied-path tests

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
- `rules/domain-02-prevent-auth-redirect-loops.md` - Prevent Auth Redirect Loops | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding route guards or middleware redirects']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-test-denied-paths-and-session-expiry.md` - Test Denied Paths And Session Expiry | risk: high | cost: load_when_matched
  Applies to modes: brownfield_change, debug_fix
  Skip modes: greenfield_build, delta_change, review_judge
  Load when: ['Changing auth flows or route guards']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-keep-tokens-out-of-browser-storage-unless-explic.md` - Keep Tokens Out Of Browser Storage Unless Explicitly Approved | risk: critical | cost: load_when_matched
  Applies to modes: review_judge
  Skip modes: greenfield_build, delta_change, brownfield_change, debug_fix
  Load when: ['Implementing sessions or token handling']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-derive-permissions-from-trusted-session-claims.md` - Derive Permissions From Trusted Session Claims | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding RBAC/ABAC rendering']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Do Not Treat Client UI Gating As Authorization | risk: medium | cost: load_only_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding protected routes or role-based UI']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-prevent-auth-redirect-loops.md -->
---
title: "Prevent Auth Redirect Loops"
impact: "HIGH"
impactDescription: "Prevents protected data leaks from client-only auth checks and unsafe token storage."
tags: middleware, redirect
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Prevent Auth Redirect Loops

Auth middleware and route groups must clearly separate public, auth, and protected routes.

**Incorrect:**

Middleware redirects /login to /dashboard, then /dashboard back to /login when the session is loading.

**Correct:**

Middleware handles public/auth/protected route groups with deterministic redirects and loading states.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding route guards or middleware redirects

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Route groups are listed.
- Redirect cycle risk is checked.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-test-denied-paths-and-session-expiry.md -->
---
title: "Test Denied Paths And Session Expiry"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: tests, denied-paths
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Test Denied Paths And Session Expiry

Auth changes require tests for unauthenticated, unauthorized, expired session, and allowed paths where tooling exists.

**Incorrect:**

Only the happy-path login is tested.

**Correct:**

Tests cover redirect to login, 403/denied UI, expired session handling, and allowed role access.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Changing auth flows or route guards

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Denied-path tests exist or blocker reported.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-keep-tokens-out-of-browser-storage-unless-explic.md -->
---
title: "Keep Tokens Out Of Browser Storage Unless Explicitly Approved"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: tokens, storage
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Keep Tokens Out Of Browser Storage Unless Explicitly Approved

Avoid localStorage/sessionStorage token persistence for sensitive sessions; prefer secure HttpOnly cookies or provider-managed session boundaries.

**Incorrect:**

The agent stores an access token and refresh token in localStorage for convenience.

**Correct:**

The app uses secure HttpOnly same-site cookies or provider-managed sessions and keeps tokens out of script-readable storage.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Implementing sessions or token handling

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Storage mechanism is identified.
- Script-readable sensitive tokens are absent or explicitly justified.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-derive-permissions-from-trusted-session-claims.md -->
---
title: "Derive Permissions From Trusted Session Claims"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: roles, claims
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Derive Permissions From Trusted Session Claims

Frontend permission decisions must use trusted session claims or server-provided permissions, not user-editable request data.

**Incorrect:**

A user can pass role=admin in query params to reveal privileged UI.

**Correct:**

The app derives permissions from validated session claims or a server authorization response.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding RBAC/ABAC rendering

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Permission source is trusted.
- User-editable inputs are ignored for auth.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Do Not Treat Client UI Gating As Authorization"
impact: "HIGH"
impactDescription: ""
tags: auth, authorization, client-ui
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Do Not Treat Client UI Gating As Authorization

Client-side hiding of links or buttons is only UX; protected data and privileged actions require server-side route/action/API checks.

**Incorrect:**

The agent hides the Admin link but still renders admin data in the page payload for non-admin users.

**Correct:**

The server component/middleware/server action checks session permissions before fetching or mutating admin data, while the client also hides the link for UX.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding protected routes or role-based UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Server-side authorization check exists for protected data/actions.
- Client gating is documented as UX only.

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

User asks to add frontend authentication, NextAuth/Auth.js, Clerk, Auth0, route guards, RBAC/ABAC rendering, JWT/session handling, refresh flow, protected routes, or enterprise SSO.

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
