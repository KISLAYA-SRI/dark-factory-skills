# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Designing or changing React state ownership, global UI state, server cache, URL/search-param state, optimistic updates, invalidation, or context providers.

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
- `frontend-api-integration-skill`: State depends on backend fetches, mutations, retries, pagination, generated clients, or realtime updates.
- `frontend-ui-component-system-skill`: State ownership affects reusable components or screen composition.

### Stop Conditions
- The source of truth for state, cache lifetime, persistence requirement, or URL shareability is unknown.
- The agent would need to invent server cache keys, invalidation rules, or persistence behavior without evidence.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Use local or lifted state unless multiple distant consumers require a shared store.
- Failure mode requires escalation: Server-state cache keys must include all meaningful parameters and mutations must invalidate or update affected queries.
- Failure mode requires escalation: URL/search params should store safe shareable filters and pagination, not secrets or volatile UI internals.
- Failure mode requires escalation: Optimistic UI must define rollback, conflict, and error behavior.

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
- `rules/domain-02-prefer-local-state-before-global-stores.md` - Prefer Local State Before Global Stores | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding UI state']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-use-stable-query-keys-and-explicit-invalidation.md` - Use Stable Query Keys And Explicit Invalidation | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Adding query/cache logic']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-treat-url-state-as-public-shareable-state.md` - Treat URL State As Public Shareable State | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Syncing state to URL']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-implement-optimistic-update-rollback.md` - Implement Optimistic Update Rollback | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Adding optimistic mutations']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Separate Client State From Server State | risk: medium | cost: load_only_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding state around async data']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-prefer-local-state-before-global-stores.md -->
---
title: "Prefer Local State Before Global Stores"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: local-state, global-store
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Prefer Local State Before Global Stores

Use local or lifted state unless multiple distant consumers require a shared store.

**Incorrect:**

The agent creates a Redux slice for a single dropdown.

**Correct:**

The component uses local state and lifts it only when sibling coordination is required.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding UI state

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- State consumer scope is identified.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-use-stable-query-keys-and-explicit-invalidation.md -->
---
title: "Use Stable Query Keys And Explicit Invalidation"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: query-key, invalidation
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Use Stable Query Keys And Explicit Invalidation

Server-state cache keys must include all meaningful parameters and mutations must invalidate or update affected queries.

**Incorrect:**

A customer query key omits tenant id and filters, causing cross-view stale data.

**Correct:**

The query key includes tenant/customer/filter params and mutation invalidates affected list/detail keys.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Adding query/cache logic

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Query keys include parameters.
- Invalidation/update behavior is explicit.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-treat-url-state-as-public-shareable-state.md -->
---
title: "Treat URL State As Public Shareable State"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: search-params
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Treat URL State As Public Shareable State

URL/search params should store safe shareable filters and pagination, not secrets or volatile UI internals.

**Incorrect:**

The agent puts access token and full customer name in search params.

**Correct:**

The agent stores page, sort, and status filter in the URL and keeps sensitive data server-side.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Syncing state to URL

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- URL state excludes secrets/PII.
- Back/forward behavior works.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-implement-optimistic-update-rollback.md -->
---
title: "Implement Optimistic Update Rollback"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: optimistic
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Implement Optimistic Update Rollback

Optimistic UI must define rollback, conflict, and error behavior.

**Incorrect:**

The agent removes an item optimistically but cannot restore it when the API fails.

**Correct:**

The mutation snapshots previous data, rolls back on error, and handles conflict responses.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Adding optimistic mutations

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Rollback path exists.
- Conflict/error states are handled.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Separate Client State From Server State"
impact: "HIGH"
impactDescription: ""
tags: state, server-state
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Separate Client State From Server State

Server-derived data should live in query/cache tools; client stores should hold UI/application state only.

**Incorrect:**

The agent copies fetched orders into a global store and manually syncs stale data.

**Correct:**

The agent keeps orders in TanStack Query cache and stores only selected filters and modal state separately.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding state around async data

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Server cache ownership is clear.
- Client store has no duplicated server source of truth.

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

User asks to add or refactor React state, Zustand/Redux/Jotai stores, TanStack Query/SWR cache, Context providers, optimistic updates, or URL state.

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
