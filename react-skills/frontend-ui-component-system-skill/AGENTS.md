# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Building, reviewing, or refactoring React components, screens, design-system primitives, styling strategy, responsive layouts, Storybook stories, or motion.

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
- Initial rule load limit: 5 rule files.
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
- `frontend-forms-validation-skill`: Components include forms, fields, validation states, or multi-step input flows.
- `frontend-state-management-skill`: Component work introduces shared state, URL state, server cache, or cross-component data flow.

### Stop Conditions
- Design-system source, component ownership, accessibility expectations, or styling convention cannot be inspected or supplied.
- The agent would need to invent visual design language or tokens without a design artifact, existing system, or user instruction.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Use existing tokens, primitives, and theme APIs instead of hard-coded colors, spacing, or controls.
- Failure mode requires escalation: Reusable components should receive data and callbacks through props rather than importing feature services.
- Failure mode requires escalation: Components and screens should implement realistic loading, error, empty, disabled, and pending states.
- Failure mode requires escalation: Animations and interactions must preserve reduced-motion preferences and keyboard/focus behavior.

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
- `rules/domain-02-reuse-design-tokens-and-primitives-before-custom.md` - Reuse Design Tokens And Primitives Before Custom Styling | risk: high | cost: load_when_matched
  Applies to modes: brownfield_change, debug_fix
  Skip modes: greenfield_build, delta_change, review_judge
  Load when: ['Building shared UI']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-document-reusable-components-in-storybook.md` - Document Reusable Components In Storybook | risk: high | cost: load_for_reusable_component_storybook_changes
  Applies to modes: brownfield_change
  Skip modes: greenfield_build, delta_change, debug_fix, review_judge
  Load when: ['Adding or changing reusable components']
  Do not load when: Private one-off screen fragments with no reuse contract
- `rules/domain-04-keep-reusable-components-free-of-feature-data-fe.md` - Keep Reusable Components Free Of Feature Data Fetching | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Creating shared components']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-cover-loading-error-empty-and-disabled-states.md` - Cover Loading Error Empty And Disabled States | risk: high | cost: load_when_matched
  Applies to modes: debug_fix
  Skip modes: greenfield_build, delta_change, brownfield_change, review_judge
  Load when: ['Adding data-backed UI']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-06-respect-reduced-motion-and-interaction-accessibi.md` - Respect Reduced Motion And Interaction Accessibility | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding motion or interactive components']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-07-compose-screens-as-thin-orchestration-layers.md` - Compose Screens As Thin Orchestration Layers | risk: high | cost: load_for_screen_composition_changes
  Applies to modes: brownfield_change
  Skip modes: greenfield_build, delta_change, debug_fix, review_judge
  Load when: ['Creating or refactoring a React screen or route']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-08-keep-custom-hooks-focused-and-testable.md` - Keep Custom Hooks Focused And Testable | risk: medium | cost: load_for_custom_hook_changes
  Applies to modes: brownfield_change, debug_fix, review_judge
  Skip modes: greenfield_build, delta_change
  Load when: ['Extracting or reviewing reusable React hooks']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-09-make-interactive-components-accessible-by-defaul.md` - Make Interactive Components Accessible By Default | risk: critical | cost: load_for_interactive_accessibility
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding buttons, menus, dialogs, tabs, popovers, accordions, or custom interactive controls']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Define Component Ownership And Prop Contracts Before Coding | risk: medium | cost: load_only_when_matched
  Applies to modes: brownfield_change, debug_fix, review_judge
  Skip modes: greenfield_build, delta_change
  Load when: ['Creating or refactoring React components']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-reuse-design-tokens-and-primitives-before-custom.md -->
---
title: "Reuse Design Tokens And Primitives Before Custom Styling"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: tokens, design-system
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Reuse Design Tokens And Primitives Before Custom Styling

Use existing tokens, primitives, and theme APIs instead of hard-coded colors, spacing, or controls.

**Incorrect:**

The agent hard-codes hex colors and creates a custom modal despite an existing Dialog primitive.

**Correct:**

The agent uses theme tokens and the existing Dialog primitive with required variants.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Building shared UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Tokens/primitives inspected.
- Hard-coded visual values justified or avoided.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-document-reusable-components-in-storybook.md -->
---
title: "Document Reusable Components In Storybook"
impact: "HIGH"
impactDescription: "Prevents fragile UI APIs and inaccessible reusable components."
tags: storybook, documentation, components
costHint: "load_for_reusable_component_storybook_changes"
risk: "high"
appliesToModes: ["brownfield_change"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "debug_fix", "review_judge"]
---

## Document Reusable Components In Storybook

Reusable or design-system components should include Storybook stories for variants, states, and interactions.

**Incorrect:**

The agent adds a reusable Button variant but no story for disabled, loading, icon, or error-adjacent states.

**Correct:**

The agent adds stories for default, disabled, loading, destructive, responsive, and interaction states using project conventions.

## Applies To Modes
- brownfield_change

## Does Not Apply To Modes
- greenfield_build
- delta_change
- debug_fix
- review_judge

## When To Apply
- Adding or changing reusable components

## Does Not Apply To
- Private one-off screen fragments with no reuse contract

## Evidence And Validation
- Stories cover variants and key states.
- Storybook command is run or blocker reported.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-keep-reusable-components-free-of-feature-data-fe.md -->
---
title: "Keep Reusable Components Free Of Feature Data Fetching"
impact: "HIGH"
impactDescription: "Prevents fragile UI APIs and inaccessible reusable components."
tags: composition
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Keep Reusable Components Free Of Feature Data Fetching

Reusable components should receive data and callbacks through props rather than importing feature services.

**Incorrect:**

A reusable table component calls /api/accounts internally.

**Correct:**

The screen fetches data and passes rows/actions into a reusable table component.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Creating shared components

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- No feature API imports in shared UI.
- Data ownership remains at screen/feature boundary.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-cover-loading-error-empty-and-disabled-states.md -->
---
title: "Cover Loading Error Empty And Disabled States"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: states
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Cover Loading Error Empty And Disabled States

Components and screens should implement realistic loading, error, empty, disabled, and pending states.

**Incorrect:**

A list renders nothing while loading and crashes on failed fetch.

**Correct:**

The screen shows skeleton/loading, empty copy, retryable error, and disabled pending action.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Adding data-backed UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Required states are present or skipped with reason.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-06-respect-reduced-motion-and-interaction-accessibi.md -->
---
title: "Respect Reduced Motion And Interaction Accessibility"
impact: "HIGH"
impactDescription: "Prevents fragile UI APIs and inaccessible reusable components."
tags: motion, accessibility
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Respect Reduced Motion And Interaction Accessibility

Animations and interactions must preserve reduced-motion preferences and keyboard/focus behavior.

**Incorrect:**

A modal animates focus off-screen and ignores prefers-reduced-motion.

**Correct:**

The modal uses focus management, keyboard close behavior, and reduced-motion-safe transitions.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding motion or interactive components

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Reduced motion respected.
- Focus/keyboard behavior verified.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-07-compose-screens-as-thin-orchestration-layers.md -->
---
title: "Compose Screens As Thin Orchestration Layers"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: react, screens, composition
costHint: "load_for_screen_composition_changes"
risk: "high"
appliesToModes: ["brownfield_change"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "debug_fix", "review_judge"]
---

## Compose Screens As Thin Orchestration Layers

Compose screens from data/loading boundaries and child components without burying reusable logic in route files.

**Incorrect:**

The screen file owns fetching, form state, formatting, modal state, and table rendering in one large component.

**Correct:**

The screen coordinates data and layout, then delegates reusable behavior to typed hooks and components.

## Applies To Modes
- brownfield_change

## Does Not Apply To Modes
- greenfield_build
- delta_change
- debug_fix
- review_judge

## When To Apply
- Creating or refactoring a React screen or route

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Screen orchestration is separated from reusable hooks/components.
- Route-level ownership remains clear.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-08-keep-custom-hooks-focused-and-testable.md -->
---
title: "Keep Custom Hooks Focused And Testable"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: react, hooks
costHint: "load_for_custom_hook_changes"
risk: "medium"
appliesToModes: ["brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change"]
---

## Keep Custom Hooks Focused And Testable

Custom hooks should encapsulate reusable behavior without hiding rendering, global side effects, or unrelated business workflows.

**Incorrect:**

A useDashboard hook fetches unrelated data, mutates global state, opens modals, and returns rendered JSX.

**Correct:**

Focused hooks return typed state/actions for one behavior and are tested separately from presentation.

## Applies To Modes
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change

## When To Apply
- Extracting or reviewing reusable React hooks

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Hook has a single responsibility.
- No JSX returned from behavior-only hooks.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-09-make-interactive-components-accessible-by-defaul.md -->
---
title: "Make Interactive Components Accessible By Default"
impact: "HIGH"
impactDescription: "Prevents fragile UI APIs and inaccessible reusable components."
tags: accessibility, aria, keyboard
costHint: "load_for_interactive_accessibility"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Make Interactive Components Accessible By Default

Interactive components need semantic elements, accessible names, keyboard behavior, visible focus, and ARIA only where needed.

**Incorrect:**

A clickable div opens a menu, has no role, no keyboard support, and loses focus after selection.

**Correct:**

The component uses a button/menu primitive with accessible name, keyboard navigation, visible focus, and tested open/close states.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding buttons, menus, dialogs, tabs, popovers, accordions, or custom interactive controls

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Keyboard path works.
- Accessible names and focus management are present.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Define Component Ownership And Prop Contracts Before Coding"
impact: "HIGH"
impactDescription: ""
tags: react, props
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change"]
---

## Define Component Ownership And Prop Contracts Before Coding

Components need clear ownership, prop contracts, state boundaries, and failure states before implementation.

**Incorrect:**

The agent creates a reusable Card component that fetches account data and hides internal loading errors.

**Correct:**

The agent separates screen data loading from a typed presentational Card component with documented props and states.

## Applies To Modes
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change

## When To Apply
- Creating or refactoring React components

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Component level is identified.
- Props and states are typed.
- Data ownership is explicit.

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

User asks to build React screens, reusable components, design-system primitives, styling strategy, responsive layouts, Storybook stories, or motion interactions.

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
