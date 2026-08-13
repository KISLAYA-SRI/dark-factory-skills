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
