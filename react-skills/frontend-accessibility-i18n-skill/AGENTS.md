# Compiled Agent Rules

## Runtime Use Contract

Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.

### Use This Skill When
- Adding or reviewing frontend accessibility, WCAG behavior, ARIA, keyboard/focus support, screen-reader behavior, a11y tests, i18n locale routing, translations, formatting, or RTL layout.

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
- `frontend-ui-component-system-skill`: Accessibility/i18n changes affect components, design-system primitives, layout, motion, or Storybook examples.
- `nextjs-app-router-rendering-skill`: Locale routing, metadata, dynamic routes, server rendering, or App Router layouts are changed.
- `frontend-testing-quality-skill`: Accessibility audits, keyboard/focus tests, locale tests, or RTL visual tests are required.

### Stop Conditions
- Accessibility target, locale list, translation source, formatting rules, RTL requirement, or compliance standard is missing.
- The agent would need to invent translations, legal accessibility claims, locale routing policy, or unsupported WCAG conformance without evidence.
- A11y/i18n checks cannot be run or reported as blocked evidence.
- The request is outside activation_scope or matches non_activation_scope.
- Required context pack, control pack, API contract, repository files, or validation commands are missing.
- Business rules, auth policy, or regulated-data handling are unclear and cannot be verified from supplied sources.
- The agent would need to invent APIs, files, schemas, tools, or enterprise policy to proceed.
- Failure mode requires escalation: Non-keyboard accessible control
- Failure mode requires escalation: Invented translations
- Failure mode requires escalation: Broken RTL layout
- Failure mode requires escalation: Hard-coded date formatting

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
- `rules/domain-02-preserve-keyboard-and-focus-paths.md` - Preserve Keyboard And Focus Paths | risk: critical | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding dialogs, menus, tabs, popovers, modals, or custom controls']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-03-do-not-invent-translations-or-locale-policy.md` - Do Not Invent Translations Or Locale Policy | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding i18n support']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-04-use-locale-aware-formatting-instead-of-hard-code.md` - Use Locale Aware Formatting Instead Of Hard Coded Strings | risk: high | cost: load_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Adding localized content or formatting']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/domain-05-verify-rtl-layout-and-directional-icons.md` - Verify RTL Layout And Directional Icons | risk: high | cost: load_when_matched
  Applies to modes: review_judge
  Skip modes: greenfield_build, delta_change, brownfield_change, debug_fix
  Load when: ['Adding RTL locale support']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.
- `rules/tool-call-discipline.md` - Prefer Semantic HTML Before ARIA | risk: medium | cost: load_only_when_matched
  Applies to modes: delta_change, review_judge
  Skip modes: greenfield_build, brownfield_change, debug_fix
  Load when: ['Creating interactive UI']
  Do not load when: The task does not touch this rule's tags, trigger conditions, or affected implementation boundary.

<!-- domain-02-preserve-keyboard-and-focus-paths.md -->
---
title: "Preserve Keyboard And Focus Paths"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: keyboard, focus
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Preserve Keyboard And Focus Paths

Interactive flows must support keyboard operation, visible focus, focus restoration, and escape/close behavior where applicable.

**Incorrect:**

A dialog opens without moving focus and cannot be closed by keyboard.

**Correct:**

The dialog traps focus, restores focus to trigger, supports Escape, and exposes visible focus states.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding dialogs, menus, tabs, popovers, modals, or custom controls

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Keyboard path verified.
- Focus lifecycle documented.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-03-do-not-invent-translations-or-locale-policy.md -->
---
title: "Do Not Invent Translations Or Locale Policy"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: translation, locale
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Do Not Invent Translations Or Locale Policy

Translations, supported locales, fallback behavior, and legal copy must come from supplied source or be clearly marked as placeholders.

**Incorrect:**

The agent invents French legal consent copy and claims localization complete.

**Correct:**

The agent adds translation keys with placeholders and flags missing approved copy as a blocker.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding i18n support

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Translation source cited or placeholder marked.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-04-use-locale-aware-formatting-instead-of-hard-code.md -->
---
title: "Use Locale Aware Formatting Instead Of Hard Coded Strings"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: i18n, formatting
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Use Locale Aware Formatting Instead Of Hard Coded Strings

Dates, numbers, currencies, plurals, and relative times must use locale-aware formatters and translation keys.

**Incorrect:**

The component renders $1,000.00 and 1 items with hard-coded English strings.

**Correct:**

The component uses Intl formatters and pluralized translation messages for each locale.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding localized content or formatting

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Formatter/translation key used.
- Plural/locale behavior covered.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- domain-05-verify-rtl-layout-and-directional-icons.md -->
---
title: "Verify RTL Layout And Directional Icons"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: rtl, layout
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Verify RTL Layout And Directional Icons

RTL support requires layout mirroring, logical CSS, icon direction review, and bidirectional text handling.

**Incorrect:**

The app switches dir=rtl but left/right spacing and arrows remain wrong.

**Correct:**

The app uses logical properties, reviews directional icons, and tests key screens in RTL.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Adding RTL locale support

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- RTL layout checked.
- Directional assets reviewed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md


<!-- tool-call-discipline.md -->
---
title: "Prefer Semantic HTML Before ARIA"
impact: "HIGH"
impactDescription: ""
tags: accessibility, aria
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Prefer Semantic HTML Before ARIA

Use native semantic elements and labels before adding ARIA; ARIA should clarify, not replace, correct HTML.

**Incorrect:**

The agent builds a button from div role=button without keyboard handling.

**Correct:**

The agent uses a real button with accessible name and adds ARIA only for additional state where needed.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Creating interactive UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Native semantics used where possible.
- ARIA usage has a clear purpose.

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

User asks to improve accessibility, WCAG, ARIA, keyboard/focus behavior, screen-reader behavior, automated a11y audits, i18n, locale routing, translations, formatting, pluralization, or RTL.

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
