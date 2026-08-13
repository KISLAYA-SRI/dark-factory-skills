# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Designing, reviewing, or refactoring large React/Next.js architecture, module boundaries, domain/bounded-context structure, micro-frontends, scalability patterns, ownership, documentation, CODEOWNERS, ADRs, or framework/library migrations.

### Do Not Use This Skill When
- React Native or mobile-specific code; use the React Native mobile skill instead.
- Backend-only performance, deployment, observability, architecture, or governance implementation where no frontend code, browser behavior, or frontend delivery pipeline is changed.
- Enterprise business rules not supplied by requirements, repository docs, context packs, control packs, design artifacts, architecture docs, or tests.

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
- `frontend-project-foundation-skill`: Architecture work changes monorepo/workspace structure, package scripts, TypeScript paths, lint boundaries, or shared packages.
- `nextjs-app-router-rendering-skill`: Architecture work changes App Router structure, route groups, layouts, or Pages-to-App Router migration.
- `frontend-ui-component-system-skill`: Architecture work changes design-system/component-library boundaries, Storybook docs, or shared primitives.
- `frontend-testing-quality-skill`: Architecture/migration work needs regression tests, coverage, CI gates, or migration validation.

### Stop Conditions
- Architecture goal, ownership model, affected modules, dependency boundaries, migration target, or acceptance criteria are missing.
- The agent would need to invent team ownership, micro-frontend boundaries, domain model, ADR decisions, or migration strategy without evidence.
- Large refactor cannot be scoped into safe increments or validated with tests/checks.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Unscoped architecture rewrite
- Failure mode requires escalation: Unjustified micro-frontend split
- Failure mode requires escalation: Circular feature imports
- Failure mode requires escalation: Big-bang framework migration

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
- `rules/domain-02-avoid-micro-frontends-without-runtime-contract-j.md` - Avoid Micro Frontends Without Runtime Contract Justification | risk: high | cost: load_when_matched
  Applies to modes: review_judge
  Skip modes: greenfield_build, delta_change, brownfield_change, debug_fix
  Load when: ['Introducing micro-frontends or module federation']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-enforce-module-boundaries-with-imports-and-owner.md` - Enforce Module Boundaries With Imports And Ownership | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding shared packages or reorganizing modules']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-use-domain-modeling-to-reduce-coupling-not-dupli.md` - Use Domain Modeling To Reduce Coupling Not Duplicate Backend Domains Blindly | risk: high | cost: load_when_matched
  Applies to modes: review_judge
  Skip modes: greenfield_build, delta_change, brownfield_change, debug_fix
  Load when: ['Organizing frontend domains or bounded contexts']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-plan-migrations-as-incremental-strangler-steps.md` - Plan Migrations As Incremental Strangler Steps | risk: high | cost: load_when_matched
  Applies to modes: delta_change, brownfield_change
  Skip modes: greenfield_build, debug_fix, review_judge
  Load when: ['Planning or performing frontend migrations']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Do Not Rewrite Architecture Without Explicit Scope And Evidence | risk: medium | cost: load_only_when_matched
  Applies to modes: brownfield_change, debug_fix, review_judge
  Skip modes: greenfield_build, delta_change
  Load when: ['Changing architecture, folders, module boundaries, or migration strategy']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-avoid-micro-frontends-without-runtime-contract-j.md -->
---
title: "Avoid Micro Frontends Without Runtime Contract Justification"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: micro-frontend, module-federation
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Avoid Micro Frontends Without Runtime Contract Justification

Micro-frontends should require team/runtime isolation needs and explicit contracts, not just code organization.

**Incorrect:**

The agent splits a small dashboard into module federation remotes with no deployment or ownership need.

**Correct:**

The agent documents isolation driver, route ownership, shared dependency policy, fallback UI, and runtime contract.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Introducing micro-frontends or module federation

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Isolation reason exists.
- Runtime contract and fallback behavior defined.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-enforce-module-boundaries-with-imports-and-owner.md -->
---
title: "Enforce Module Boundaries With Imports And Ownership"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: module-boundary, ownership
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Enforce Module Boundaries With Imports And Ownership

Frontend modules should have clear allowed dependencies, public APIs, and ownership.

**Incorrect:**

A feature imports another feature internal file and creates circular dependencies.

**Correct:**

The feature consumes only public exports and CODEOWNERS/dependency rules define ownership.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding shared packages or reorganizing modules

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Public API boundary exists.
- No circular or internal imports introduced.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-use-domain-modeling-to-reduce-coupling-not-dupli.md -->
---
title: "Use Domain Modeling To Reduce Coupling Not Duplicate Backend Domains Blindly"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: domain-modeling, bounded-context
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Use Domain Modeling To Reduce Coupling Not Duplicate Backend Domains Blindly

Frontend domains should reflect user journeys and UI ownership while aligning with backend contracts where needed.

**Incorrect:**

The agent mirrors every backend table as a frontend domain and spreads API DTOs through UI components.

**Correct:**

The agent defines frontend domain models for UI behavior and maps API DTOs at boundaries.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Organizing frontend domains or bounded contexts

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Domain model purpose is UI-facing.
- API DTO mapping boundary exists.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-plan-migrations-as-incremental-strangler-steps.md -->
---
title: "Plan Migrations As Incremental Strangler Steps"
impact: "HIGH"
impactDescription: "Prevents broad unvalidated rewrites, broken module ownership, and unnecessary micro-frontend complexity."
tags: migration, refactor
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "brownfield_change"]
doesNotApplyToModes: ["greenfield_build", "debug_fix", "review_judge"]
---

## Plan Migrations As Incremental Strangler Steps

Framework/library migrations should be sliced, reversible, and validated rather than completed as one risky rewrite.

**Incorrect:**

The agent migrates all Pages Router routes to App Router in one change with no test plan.

**Correct:**

The agent migrates one route group at a time, preserves compatibility, runs tests, and records rollback criteria.

## Applies To Modes
- delta_change
- brownfield_change

## Does Not Apply To Modes
- greenfield_build
- debug_fix
- review_judge

## When To Apply
- Planning or performing frontend migrations

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Migration slices and rollback criteria exist.
- Compatibility verified.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Do Not Rewrite Architecture Without Explicit Scope And Evidence"
impact: "HIGH"
impactDescription: ""
tags: architecture, scope
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change"]
---

## Do Not Rewrite Architecture Without Explicit Scope And Evidence

Large frontend architecture changes require explicit scope, target boundaries, validation plan, and migration evidence; do not broad-rewrite by preference.

**Incorrect:**

The agent reorganizes the entire app into a new architecture because it prefers feature-sliced design.

**Correct:**

The agent maps current boundaries, proposes an incremental target slice, updates only impacted modules, and verifies with tests/typecheck.

## Applies To Modes
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change

## When To Apply
- Changing architecture, folders, module boundaries, or migration strategy

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Scope and target architecture are explicit.
- Incremental validation path exists.

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

User asks to design frontend architecture, define module boundaries, add micro-frontends/module federation, improve scalability, organize frontend domains, add governance docs/CODEOWNERS/ADRs, or plan migrations/refactors such as Pages to App Router.

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
