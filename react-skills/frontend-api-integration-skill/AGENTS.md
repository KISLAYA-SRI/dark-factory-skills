# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Connecting React/Next.js frontends to REST, GraphQL, BFF, realtime, or generated API contract clients.
- Reviewing frontend/backend contract alignment, retries, pagination, error mapping, and API failure handling.

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
- `frontend-state-management-skill`: API work affects cache keys, server state, invalidation, pagination, or optimistic updates.
- `nextjs-app-router-rendering-skill`: API calls run in server components, server actions, route handlers, or depend on Next.js caching/revalidation.
- `frontend-forms-validation-skill`: API requests are submitted from forms or share validation schemas.

### Stop Conditions
- API contract, auth mechanism, error model, pagination shape, retry/idempotency semantics, or generated schema source is missing.
- The agent would need to invent backend fields, endpoints, auth headers, or error codes without contract evidence.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: API keys and privileged tokens must stay in server-only route handlers/server actions, not browser bundles.
- Failure mode requires escalation: Frontend clients should map transport, validation, auth, conflict, and server errors into typed UI-safe errors.
- Failure mode requires escalation: Retries must be limited to safe reads or writes with explicit idempotency semantics.
- Failure mode requires escalation: MSW and test fixtures must follow current contract/generated types.

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
- `rules/domain-02-normalize-api-errors-to-ui-safe-error-models.md` - Normalize API Errors To UI Safe Error Models | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Handling API failures']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-keep-secrets-server-side-in-bff-and-server-actio.md` - Keep Secrets Server Side In BFF And Server Actions | risk: critical | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding BFF/API routes or secret-backed calls']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-keep-mocks-in-sync-with-contracts.md` - Keep Mocks In Sync With Contracts | risk: high | cost: load_when_matched
  Applies to modes: delta_change, debug_fix, review_judge
  Skip modes: greenfield_build, brownfield_change
  Load when: ['Adding API tests or mocks']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-retry-only-safe-or-explicitly-idempotent-request.md` - Retry Only Safe Or Explicitly Idempotent Requests | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding retry behavior']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Do Not Invent Frontend API Contracts | risk: medium | cost: load_only_when_matched
  Applies to modes: brownfield_change, review_judge
  Skip modes: greenfield_build, delta_change, debug_fix
  Load when: ['Adding frontend API calls']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-normalize-api-errors-to-ui-safe-error-models.md -->
---
title: "Normalize API Errors To UI Safe Error Models"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: error-handling
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Normalize API Errors To UI Safe Error Models

Frontend clients should map transport, validation, auth, conflict, and server errors into typed UI-safe errors.

**Incorrect:**

The component displays raw stack traces from a failed fetch.

**Correct:**

The API wrapper maps problem details/status codes into safe user and developer messages.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Handling API failures

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Status/error mapping exists.
- Sensitive details are not displayed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-keep-secrets-server-side-in-bff-and-server-actio.md -->
---
title: "Keep Secrets Server Side In BFF And Server Actions"
impact: "HIGH"
impactDescription: "Prevents frontend/backend drift and client-side leakage of privileged credentials."
tags: secrets, bff
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Keep Secrets Server Side In BFF And Server Actions

API keys and privileged tokens must stay in server-only route handlers/server actions, not browser bundles.

**Incorrect:**

The browser fetch client includes a private backend API key.

**Correct:**

A server route reads the secret and returns only safe data to the client.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding BFF/API routes or secret-backed calls

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Secret not exposed client-side.
- Server/client boundary explicit.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-keep-mocks-in-sync-with-contracts.md -->
---
title: "Keep Mocks In Sync With Contracts"
impact: "HIGH"
impactDescription: "Prevents frontend/backend drift and client-side leakage of privileged credentials."
tags: msw, mocks
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change"]
---

## Keep Mocks In Sync With Contracts

MSW and test fixtures must follow current contract/generated types.

**Incorrect:**

The test mock returns fields not in the schema and hides a runtime bug.

**Correct:**

The mock uses generated types and is updated with schema changes.

## Applies To Modes
- delta_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change

## When To Apply
- Adding API tests or mocks

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Mocks compile against types.
- Schema drift checked.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-retry-only-safe-or-explicitly-idempotent-request.md -->
---
title: "Retry Only Safe Or Explicitly Idempotent Requests"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: retry, idempotency
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Retry Only Safe Or Explicitly Idempotent Requests

Retries must be limited to safe reads or writes with explicit idempotency semantics.

**Incorrect:**

The client retries POST payment creation after timeout with no idempotency key.

**Correct:**

The client retries GETs and idempotent writes with idempotency key and bounded backoff.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding retry behavior

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Method/idempotency assessed.
- Backoff/limit configured.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Do Not Invent Frontend API Contracts"
impact: "HIGH"
impactDescription: ""
tags: contract, api
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "debug_fix"]
---

## Do Not Invent Frontend API Contracts

Frontend API code must be based on supplied schemas, generated clients, existing wrappers, or explicit user requirements.

**Incorrect:**

The agent guesses response fields and creates a client that does not match OpenAPI.

**Correct:**

The agent uses generated OpenAPI types or flags missing contract details before implementation.

## Applies To Modes
- brownfield_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- debug_fix

## When To Apply
- Adding frontend API calls

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Contract source is cited.
- Unknown fields are not invented.

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

User asks to integrate REST/GraphQL APIs, generate frontend types from contracts, build API clients, add BFF/API routes, retries, pagination, realtime streams, or frontend API error handling.

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
