# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Adding, reviewing, or fixing frontend unit/component/integration/E2E/visual tests, MSW mocks, Storybook interaction tests, coverage strategy, or quality gates for React/Next.js apps.

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
- `frontend-ui-component-system-skill`: Tests cover reusable components, visual states, Storybook stories, or interactions.
- `frontend-api-integration-skill`: Tests use MSW, API mocks, generated clients, contract fixtures, pagination, or error responses.
- `frontend-auth-authorization-skill`: Tests cover login, route guards, roles/scopes, session expiry, or denied paths.
- `frontend-accessibility-i18n-skill`: Tests cover accessibility audits, keyboard/focus behavior, locale routing, formatting, or RTL.

### Stop Conditions
- Project test runner, app runtime command, mock strategy, critical journey, or expected behavior cannot be inspected or supplied.
- The agent would need to invent test IDs, API mocks, credentials, fixtures, or quality thresholds without evidence.
- Required tests cannot be generated/run and missing evidence is not reported as a blocker.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Shallow snapshot-only tests
- Failure mode requires escalation: Unstable async tests
- Failure mode requires escalation: Missing API failure mocks
- Failure mode requires escalation: Missing critical journey test

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
- `rules/domain-02-avoid-brittle-visual-and-snapshot-tests.md` - Avoid Brittle Visual And Snapshot Tests | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Adding visual/snapshot tests']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-use-msw-or-existing-network-mock-strategy-for-ap.md` - Use MSW Or Existing Network Mock Strategy For API Flows | risk: high | cost: load_when_matched
  Applies to modes: brownfield_change, debug_fix
  Skip modes: greenfield_build, delta_change, review_judge
  Load when: ['Testing API-backed UI']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-await-async-ui-with-user-visible-conditions.md` - Await Async UI With User Visible Conditions | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Testing async UI behavior']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-cover-critical-journeys-with-e2e-tests.md` - Cover Critical Journeys With E2E Tests | risk: high | cost: load_when_matched
  Applies to modes: brownfield_change, debug_fix
  Skip modes: greenfield_build, delta_change, review_judge
  Load when: ['Changing critical multi-step flows']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Tie Tests To Changed User Observable Behavior | risk: medium | cost: load_only_when_matched
  Applies to modes: brownfield_change, debug_fix, review_judge
  Skip modes: greenfield_build, delta_change
  Load when: ['Adding or judging frontend tests']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-avoid-brittle-visual-and-snapshot-tests.md -->
---
title: "Avoid Brittle Visual And Snapshot Tests"
impact: "HIGH"
impactDescription: "Prevents false confidence from shallow tests and missing frontend behavior evidence."
tags: visual, snapshot
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Avoid Brittle Visual And Snapshot Tests

Visual regression should focus stable states and meaningful diffs, not noisy full-page snapshots without controls.

**Incorrect:**

The agent snapshots an animated page with live timestamps and random data.

**Correct:**

The agent freezes data/time, captures stable component states, and documents acceptable diffs.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Adding visual/snapshot tests

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Dynamic data stabilized.
- Visual scope is meaningful.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-use-msw-or-existing-network-mock-strategy-for-ap.md -->
---
title: "Use MSW Or Existing Network Mock Strategy For API Flows"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: msw, api
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Use MSW Or Existing Network Mock Strategy For API Flows

API-backed UI tests should mock network at the boundary using MSW or the existing project strategy.

**Incorrect:**

The component test mocks internal fetch hooks and misses request/response behavior.

**Correct:**

The test uses MSW handlers matching the API contract and verifies loading, success, and error UI.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Testing API-backed UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Network boundary mocked consistently.
- Success and failure handlers exist.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-await-async-ui-with-user-visible-conditions.md -->
---
title: "Await Async UI With User Visible Conditions"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: async, testing-library
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Await Async UI With User Visible Conditions

Async tests should wait for visible UI outcomes instead of timers or implementation internals.

**Incorrect:**

The test clicks submit and immediately asserts that a mock function was called.

**Correct:**

The test awaits the success message or validation error that a user sees.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Testing async UI behavior

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Awaited condition is user-visible.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-cover-critical-journeys-with-e2e-tests.md -->
---
title: "Cover Critical Journeys With E2E Tests"
impact: "HIGH"
impactDescription: "Prevents false confidence from shallow tests and missing frontend behavior evidence."
tags: playwright, cypress
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Cover Critical Journeys With E2E Tests

Critical flows need E2E coverage when route, auth, API, or cross-page behavior is changed.

**Incorrect:**

A login-protected checkout flow has only isolated button unit tests.

**Correct:**

A Playwright/Cypress test covers login/guard, form completion, API mock, confirmation, and failure path.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Changing critical multi-step flows

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- E2E path covers happy and key failure cases.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Tie Tests To Changed User Observable Behavior"
impact: "HIGH"
impactDescription: ""
tags: tests, evidence
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change"]
---

## Tie Tests To Changed User Observable Behavior

Frontend tests must validate changed user-visible behavior, not only implementation details or snapshots.

**Incorrect:**

The agent changes checkout validation and only updates a shallow snapshot.

**Correct:**

The agent tests the validation message, disabled submit state, API error handling, and successful submit outcome.

## Applies To Modes
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change

## When To Apply
- Adding or judging frontend tests

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Tests map to changed behavior.
- Assertions are user-observable.

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

User asks to add or improve React/Next.js tests, Vitest/Jest, React Testing Library, MSW, Playwright/Cypress, visual regression, Storybook tests, coverage, or frontend quality gates.

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
