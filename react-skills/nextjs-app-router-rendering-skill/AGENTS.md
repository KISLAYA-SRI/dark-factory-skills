# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Designing or modifying Next.js App Router route trees, layouts, route groups, metadata, loading/error states, server actions, or rendering mode decisions.

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
- `frontend-api-integration-skill`: Routes fetch backend data, use server actions, rely on API clients, or need cache/revalidation behavior.
- `frontend-ui-component-system-skill`: Route work creates shared layouts, visual states, or reusable components.

### Stop Conditions
- Route ownership, rendering requirements, cache freshness, SEO metadata, or auth gating requirements are unknown.
- The agent would need to invent route structure or rendering strategy without repo/design evidence.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Client components should be used only for interactivity; server data, secrets, and privileged calls stay server-side.
- Failure mode requires escalation: App routes need explicit loading, error, not-found, and empty states for realistic user flows.
- Failure mode requires escalation: Dynamic pages should generate metadata, canonical URLs, and sitemap behavior from validated route params.
- Failure mode requires escalation: Do not render time, random ids, browser APIs, or user-only data differently on server and client.

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
- `rules/domain-02-provide-route-level-loading-error-and-empty-stat.md` - Provide Route Level Loading Error And Empty States | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Adding data-backed routes']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-avoid-hydration-mismatches-from-non-deterministi.md` - Avoid Hydration Mismatches From Non Deterministic Rendering | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Changing mixed server/client UI']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-align-metadata-with-dynamic-route-content.md` - Align Metadata With Dynamic Route Content | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding SEO-sensitive routes']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-keep-server-client-boundaries-explicit.md` - Keep Server Client Boundaries Explicit | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding interactivity or data fetching']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Choose Rendering Strategy From Data Freshness And User Context | risk: medium | cost: load_only_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Choosing SSR, SSG, ISR, CSR, or streaming']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-provide-route-level-loading-error-and-empty-stat.md -->
---
title: "Provide Route Level Loading Error And Empty States"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: loading, error, empty
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Provide Route Level Loading Error And Empty States

App routes need explicit loading, error, not-found, and empty states for realistic user flows.

**Incorrect:**

The page awaits data and crashes to a generic runtime error on failure.

**Correct:**

The route has loading.tsx, error boundary, not-found handling, and empty state copy.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Adding data-backed routes

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- States exist or are explicitly not applicable.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-avoid-hydration-mismatches-from-non-deterministi.md -->
---
title: "Avoid Hydration Mismatches From Non Deterministic Rendering"
impact: "HIGH"
impactDescription: "Prevents stale personalized data, SEO regressions, and runtime hydration failures."
tags: hydration
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Avoid Hydration Mismatches From Non Deterministic Rendering

Do not render time, random ids, browser APIs, or user-only data differently on server and client.

**Incorrect:**

The server renders Date.now and the client re-renders a different value.

**Correct:**

The agent moves non-deterministic values to effects or stable server-provided props.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Changing mixed server/client UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- No non-deterministic SSR output without stabilization.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-align-metadata-with-dynamic-route-content.md -->
---
title: "Align Metadata With Dynamic Route Content"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: metadata, seo
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Align Metadata With Dynamic Route Content

Dynamic pages should generate metadata, canonical URLs, and sitemap behavior from validated route params.

**Incorrect:**

A product detail page has static metadata copied across all products.

**Correct:**

The route validates params and generates title, description, canonical, and not-found behavior.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding SEO-sensitive routes

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Metadata source is validated.
- Canonical/sitemap behavior is described.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-keep-server-client-boundaries-explicit.md -->
---
title: "Keep Server Client Boundaries Explicit"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: server-component, client-component
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Keep Server Client Boundaries Explicit

Client components should be used only for interactivity; server data, secrets, and privileged calls stay server-side.

**Incorrect:**

A client component imports a server-only API client and reads process.env.SECRET.

**Correct:**

The server component fetches secure data and passes safe props to a small client component.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding interactivity or data fetching

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- No server-only imports in client components.
- Props are serializable and safe.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Choose Rendering Strategy From Data Freshness And User Context"
impact: "HIGH"
impactDescription: ""
tags: nextjs, rendering
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Choose Rendering Strategy From Data Freshness And User Context

Rendering mode must follow data freshness, personalization, SEO, and cache requirements.

**Incorrect:**

The agent makes a personalized account route static because it improves speed.

**Correct:**

The agent uses dynamic/server rendering for personalized data and static/ISR for safe public content.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Choosing SSR, SSG, ISR, CSR, or streaming

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Freshness/user context is identified.
- Cache/revalidation setting matches route risk.

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

User asks to create or refactor Next.js App Router routes, layouts, loading/error UI, dynamic routes, metadata, SEO, server actions, or rendering strategy.

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
