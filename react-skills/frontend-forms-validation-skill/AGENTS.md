# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Building, reviewing, or refactoring React forms, field components, validation schemas, multi-step wizards, submit flows, or form/API error handling.

### Do Not Use This Skill When
- React Native or mobile-specific code; use the React Native mobile skill instead.
- Backend-only API implementation where no frontend code, contract consumption, or UI behavior is changed.
- Enterprise business rules not supplied by requirements, repository docs, context packs, control packs, design artifacts, or tests.

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
- `frontend-api-integration-skill`: Form submit calls APIs, maps backend validation errors, uses generated request types, or depends on idempotency.
- `frontend-ui-component-system-skill`: Form work changes shared field components, accessibility, design-system inputs, or visual states.
- `frontend-state-management-skill`: Form state is persisted, shared across steps, encoded in URL, or coordinated with server cache.

### Stop Conditions
- Field semantics, submit contract, validation source, accessibility requirements, or backend error shape is missing.
- The agent would need to invent request fields, validation constraints, or workflow steps without requirements or contract evidence.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Use register for native/uncontrolled inputs and Controller for controlled third-party components.
- Failure mode requires escalation: Backend validation and conflict errors should become clear field-level or form-level feedback.
- Failure mode requires escalation: Forms should prevent duplicate submits and expose pending, success, and retry states.
- Failure mode requires escalation: Multi-step wizard state persistence must be explicit, restorable, and safe for sensitive fields.

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
- `rules/domain-02-use-react-hook-form-register-or-controller-appro.md` - Use React Hook Form Register Or Controller Appropriately | risk: high | cost: load_when_matched
  Applies to modes: brownfield_change, debug_fix
  Skip modes: greenfield_build, delta_change, review_judge
  Load when: ['Building React Hook Form forms']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-map-backend-validation-errors-to-field-and-form-.md` - Map Backend Validation Errors To Field And Form Errors | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Submitting forms to APIs']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-persist-wizard-state-safely-and-intentionally.md` - Persist Wizard State Safely And Intentionally | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Building multi-step forms']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-handle-submit-pending-disabled-and-double-submit.md` - Handle Submit Pending Disabled And Double Submit | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding submit behavior']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Base Form Fields On Contract And User Editable Data Only | risk: medium | cost: load_only_when_matched
  Applies to modes: debug_fix, review_judge
  Skip modes: greenfield_build, delta_change, brownfield_change
  Load when: ['Creating request forms']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-use-react-hook-form-register-or-controller-appro.md -->
---
title: "Use React Hook Form Register Or Controller Appropriately"
impact: "HIGH"
impactDescription: "Prevents invalid requests, duplicate submissions, and unsafe user-editable server fields."
tags: react-hook-form
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Use React Hook Form Register Or Controller Appropriately

Use register for native/uncontrolled inputs and Controller for controlled third-party components. For complex forms, apply this rule through the approved form library pattern in `trigger-scope.md` rather than hand-writing raw `value`/`onChange` state for every field.

**Incorrect:**

The agent wraps every simple input in Controller and causes unnecessary rerenders.

**Correct:**

Native inputs use register; controlled date picker uses Controller with typed value mapping.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Building React Hook Form forms

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Field control pattern fits component type.
- If the form is complex, inputs are wired through the approved form library (`register`, `Controller`, or equivalent) and the library rule `trigger-scope.md` is satisfied.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
- rules/trigger-scope.md


<!-- domain-03-map-backend-validation-errors-to-field-and-form-.md -->
---
title: "Map Backend Validation Errors To Field And Form Errors"
impact: "HIGH"
impactDescription: "Prevents invalid requests, duplicate submissions, and unsafe user-editable server fields."
tags: backend-errors
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Map Backend Validation Errors To Field And Form Errors

Backend validation and conflict errors should become clear field-level or form-level feedback.

**Incorrect:**

The form shows a generic failed message for duplicate email and loses field context.

**Correct:**

The submit handler maps field violations to setError and conflicts to a form-level action message.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Submitting forms to APIs

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Error model mapped.
- User can correct failures.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-persist-wizard-state-safely-and-intentionally.md -->
---
title: "Persist Wizard State Safely And Intentionally"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: wizard, persistence
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Persist Wizard State Safely And Intentionally

Multi-step wizard state persistence must be explicit, restorable, and safe for sensitive fields.

**Incorrect:**

The wizard stores all PII in localStorage indefinitely.

**Correct:**

The wizard persists only approved draft data with expiry or server draft support.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Building multi-step forms

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Persistence scope and sensitivity assessed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-handle-submit-pending-disabled-and-double-submit.md -->
---
title: "Handle Submit Pending Disabled And Double Submit"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: submit, pending
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Handle Submit Pending Disabled And Double Submit

Forms should prevent duplicate submits and expose pending, success, and retry states.

**Incorrect:**

The submit button remains enabled and sends duplicate create requests.

**Correct:**

The form disables submit while pending and uses idempotency or retry-safe behavior where required.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding submit behavior

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Pending state present.
- Duplicate submit protected.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Base Form Fields On Contract And User Editable Data Only"
impact: "HIGH"
impactDescription: ""
tags: form, contract
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change"]
---

## Base Form Fields On Contract And User Editable Data Only

Forms must include only user-editable request fields from requirements/contracts and exclude caller identity, tenant, audit, state, or server-controlled fields.

**Incorrect:**

The agent adds tenantId, userId, createdBy, and status as editable form fields.

**Correct:**

The agent derives identity from auth context/server and includes only editable fields in the form schema.

## Applies To Modes
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change

## When To Apply
- Creating request forms

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Server-controlled fields excluded.
- Request schema matches contract.

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

User asks to build forms with React Hook Form, Zod/Yup validation, controlled/uncontrolled inputs, field arrays, multi-step wizards, submit behavior, or validation error handling.

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
