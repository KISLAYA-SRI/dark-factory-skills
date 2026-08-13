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
