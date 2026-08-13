# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Creating or modernizing React/Next.js application foundations.
- Configuring monorepos, linting, formatting, strict TypeScript, path aliases, workspace scripts, or environment validation.
- Reviewing project foundation readiness before feature development.

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
- `nextjs-app-router-rendering-skill`: The foundation work creates or changes App Router structure, layouts, route groups, metadata, or rendering mode decisions.
- `frontend-ui-component-system-skill`: The foundation work creates shared UI folders, styling strategy, design tokens, or Storybook/component library structure.

### Stop Conditions
- No target framework, package manager, or repository convention can be inspected or supplied.
- The agent would need to invent organization templates, package names, lint rules, env names, deployment targets, or workspace boundaries.
- Required install/build/lint/typecheck commands cannot be identified or reported as blocked evidence.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Wrong package manager
- Failure mode requires escalation: Client-side secret exposure
- Failure mode requires escalation: Inconsistent folder conventions

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
- `rules/domain-02-preserve-existing-package-manager-and-workspace-.md` - Preserve Existing Package Manager And Workspace Boundaries | risk: high | cost: load_when_matched
  Applies to modes: brownfield_change, debug_fix
  Skip modes: greenfield_build, delta_change, review_judge
  Load when: ['Changing dependencies, scripts, or monorepo setup']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-validate-environment-variables-at-runtime-bounda.md` - Validate Environment Variables At Runtime Boundary | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding env config or accessing environment variables']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-enforce-strict-typescript-without-blocking-brown.md` - Enforce Strict TypeScript Without Blocking Brownfield Incremental Work | risk: high | cost: load_when_matched
  Applies to modes: delta_change, brownfield_change
  Skip modes: greenfield_build, debug_fix, review_judge
  Load when: ['Adding tsconfig or strict typing']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-do-not-invent-organization-foundation-templates.md` - Do Not Invent Organization Foundation Templates | risk: high | cost: load_when_matched
  Applies to modes: greenfield_build, brownfield_change, review_judge
  Skip modes: delta_change, debug_fix
  Load when: ['Enterprise project setup is requested']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Validate Frontend Foundation With Project Native Commands | risk: medium | cost: load_only_when_matched
  Applies to modes: greenfield_build, brownfield_change, debug_fix, review_judge
  Skip modes: delta_change
  Load when: ['Scaffolding or modifying frontend project foundation']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-preserve-existing-package-manager-and-workspace-.md -->
---
title: "Preserve Existing Package Manager And Workspace Boundaries"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: package-manager, workspace
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Preserve Existing Package Manager And Workspace Boundaries

Do not introduce npm/yarn/pnpm/Turborepo/Nx changes that conflict with existing repo conventions.

**Incorrect:**

The repo uses pnpm workspaces but the agent adds npm scripts and package-lock.json.

**Correct:**

The agent uses pnpm, updates workspace files consistently, and avoids unrelated package churn.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Changing dependencies, scripts, or monorepo setup

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Lockfile/package manager is identified.
- Workspace packages remain valid.
- No unrelated package config is rewritten.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-validate-environment-variables-at-runtime-bounda.md -->
---
title: "Validate Environment Variables At Runtime Boundary"
impact: "HIGH"
impactDescription: "Prevents client-side secret leakage and runtime configuration drift."
tags: env, secrets, zod
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Validate Environment Variables At Runtime Boundary

Environment variables should be schema-validated and separated between server-only and client-visible values.

**Incorrect:**

The agent reads SECRET_KEY through NEXT_PUBLIC_SECRET_KEY in client code.

**Correct:**

The agent validates server secrets server-side and exposes only safe NEXT_PUBLIC values.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding env config or accessing environment variables

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Server/client env boundary is explicit.
- Missing env values fail clearly.
- Secrets are not bundled client-side.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-enforce-strict-typescript-without-blocking-brown.md -->
---
title: "Enforce Strict TypeScript Without Blocking Brownfield Incremental Work"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: typescript, strict
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "brownfield_change"]
doesNotApplyToModes: ["greenfield_build", "debug_fix", "review_judge"]
---

## Enforce Strict TypeScript Without Blocking Brownfield Incremental Work

Prefer strict TypeScript for new foundations while scoping brownfield strictness to impacted areas unless a full migration is requested.

**Incorrect:**

The agent flips strict mode across a large legacy app and leaves hundreds of unrelated errors.

**Correct:**

The agent enables strictness for new packages or proposes a staged migration with blockers and owner.

## Applies To Modes
- delta_change
- brownfield_change

## Does Not Apply To Modes
- greenfield_build
- debug_fix
- review_judge

## When To Apply
- Adding tsconfig or strict typing

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Strictness impact is assessed.
- Brownfield blast radius is controlled.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-do-not-invent-organization-foundation-templates.md -->
---
title: "Do Not Invent Organization Foundation Templates"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: template, organization
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["greenfield_build", "brownfield_change", "review_judge"]
doesNotApplyToModes: ["delta_change", "debug_fix"]
---

## Do Not Invent Organization Foundation Templates

Organization-specific scaffolds, folder names, CI conventions, and env names require repository or user evidence.

**Incorrect:**

The agent invents an enterprise app shell, package scope, and deployment target with no source.

**Correct:**

The agent uses supplied template evidence or asks for the missing convention.

## Applies To Modes
- greenfield_build
- brownfield_change
- review_judge

## Does Not Apply To Modes
- delta_change
- debug_fix

## When To Apply
- Enterprise project setup is requested

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Template/convention evidence is cited or blocker listed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Validate Frontend Foundation With Project Native Commands"
impact: "HIGH"
impactDescription: ""
tags: frontend, foundation, tooling
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["greenfield_build", "brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["delta_change"]
---

## Validate Frontend Foundation With Project Native Commands

Project foundation changes must be verified with repo-native lint, typecheck, build, and env validation evidence.

**Incorrect:**

The agent adds tsconfig and env files but does not inspect package scripts or run validation.

**Correct:**

The agent preserves package manager conventions, updates scripts, runs lint/typecheck/build or reports blockers, and lists foundation evidence.

## Applies To Modes
- greenfield_build
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- delta_change

## When To Apply
- Scaffolding or modifying frontend project foundation

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Relevant config files are inspected.
- Commands run or blockers reported.
- Secrets boundaries are preserved.

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

User asks to scaffold a Next.js app, set up frontend project foundation, configure a monorepo, enforce TypeScript/linting conventions, or add environment config validation.

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
