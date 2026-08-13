# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Optimizing React/Next.js pages, routes, components, assets, bundles, cache behavior, large lists/tables, or Core Web Vitals.
- Reviewing frontend performance regressions, performance budgets, route rendering choices, or production performance evidence.

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
- `nextjs-app-router-rendering-skill`: Performance work changes App Router rendering mode, server/client boundaries, streaming, fetch cache, or revalidation.
- `frontend-api-integration-skill`: Performance work changes API pagination, caching, request waterfalls, prefetching, or realtime data flow.
- `frontend-ui-component-system-skill`: Performance work changes component rendering, responsive layout, images, motion, or design-system primitives.
- `frontend-testing-quality-skill`: Performance budgets, regression tests, Lighthouse/Playwright checks, bundle analysis, or visual stability checks are required.

### Stop Conditions
- Target performance metric, route/page scope, measurement method, baseline, budget, or production-like environment is missing.
- The agent would need to invent Core Web Vitals targets, CDN/cache policy, traffic assumptions, or acceptable quality tradeoffs without evidence.
- Performance improvement cannot be measured or reported with explicit blocker and residual risk.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Unmeasured performance claim
- Failure mode requires escalation: Public cache of personalized data
- Failure mode requires escalation: Lazy-loaded LCP image
- Failure mode requires escalation: Large list rendering jank

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
- `rules/domain-02-do-not-publicly-cache-personalized-data.md` - Do Not Publicly Cache Personalized Data | risk: critical | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Changing rendering or cache policy']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-optimize-lcp-assets-without-breaking-priority-co.md` - Optimize LCP Assets Without Breaking Priority Content | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Optimizing LCP or asset-heavy pages']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-reduce-client-javascript-before-adding-more-memo.md` - Reduce Client JavaScript Before Adding More Memoization | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Improving bundle or hydration cost']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-virtualize-large-lists-without-breaking-accessib.md` - Virtualize Large Lists Without Breaking Accessibility | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Rendering large lists, tables, or grids']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Measure Before Claiming Performance Improvement | risk: medium | cost: load_only_when_matched
  Applies to modes: brownfield_change, review_judge
  Skip modes: greenfield_build, delta_change, debug_fix
  Load when: ['Optimizing or reviewing frontend performance']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-do-not-publicly-cache-personalized-data.md -->
---
title: "Do Not Publicly Cache Personalized Data"
impact: "HIGH"
impactDescription: "Prevents false performance claims, cache leaks, and regressions to Web Vitals or accessibility."
tags: cache, privacy
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Do Not Publicly Cache Personalized Data

Caching strategy must respect personalization, auth, tenant, and data sensitivity boundaries.

**Incorrect:**

The agent marks an account dashboard as force-static and caches user balances publicly.

**Correct:**

The route uses dynamic/server rendering or private cache controls for personalized data and static/ISR only for safe public content.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Changing rendering or cache policy

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Personalization/data sensitivity assessed.
- Cache scope is safe.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-optimize-lcp-assets-without-breaking-priority-co.md -->
---
title: "Optimize LCP Assets Without Breaking Priority Content"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: lcp, image, font
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Optimize LCP Assets Without Breaking Priority Content

Hero images, critical fonts, and above-the-fold content should be optimized for LCP without lazy-loading critical content.

**Incorrect:**

The agent lazy-loads the hero image and adds multiple blocking web fonts.

**Correct:**

The hero image uses proper sizing/priority and fonts are subset/preloaded or swapped according to project policy.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Optimizing LCP or asset-heavy pages

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Critical asset treatment is explicit.
- Layout dimensions prevent shifts.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-reduce-client-javascript-before-adding-more-memo.md -->
---
title: "Reduce Client JavaScript Before Adding More Memoization"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: bundle, client-components
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Reduce Client JavaScript Before Adding More Memoization

Prefer removing unnecessary client boundaries, heavy libraries, and duplicated code before broad memoization.

**Incorrect:**

The agent wraps everything in memo/useMemo but leaves a heavy chart library in the initial route bundle.

**Correct:**

The agent moves static work server-side, dynamically imports the chart, and keeps memoization targeted.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Improving bundle or hydration cost

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Bundle contributors inspected.
- Client JS reduction considered.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-virtualize-large-lists-without-breaking-accessib.md -->
---
title: "Virtualize Large Lists Without Breaking Accessibility"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: virtualization, accessibility
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Virtualize Large Lists Without Breaking Accessibility

Large lists/tables can use virtualization, but keyboard navigation, row semantics, focus, and screen reader behavior must be preserved.

**Incorrect:**

The agent virtualizes a table but removes table semantics and keyboard access.

**Correct:**

The virtualized grid preserves roles/labels/focus and documents accessibility tradeoffs.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Rendering large lists, tables, or grids

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Large-data threshold is justified.
- A11y behavior is verified or risk-owned.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Measure Before Claiming Performance Improvement"
impact: "HIGH"
impactDescription: ""
tags: performance, evidence
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "debug_fix"]
---

## Measure Before Claiming Performance Improvement

Performance work needs baseline and after-change evidence or a clear blocker; do not claim improvement from code appearance alone.

**Incorrect:**

The agent removes a dependency and says performance improved without measuring bundle size, Web Vitals, or route timing.

**Correct:**

The agent records baseline bundle/Lighthouse/Web Vitals evidence, applies a scoped change, and reports after-change evidence or a blocker.

## Applies To Modes
- brownfield_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- debug_fix

## When To Apply
- Optimizing or reviewing frontend performance

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Baseline or blocker exists.
- After-change evidence or residual risk is reported.

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

User asks to improve Core Web Vitals, LCP/CLS/INP, route speed, bundle size, rendering strategy, caching, image/font assets, virtualization, or frontend performance budgets.

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
