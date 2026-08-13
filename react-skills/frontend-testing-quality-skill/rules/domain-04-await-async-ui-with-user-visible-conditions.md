---
title: "Await Async UI With User Visible Conditions"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: async, testing-library
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Await Async UI With User Visible Conditions

Async tests should wait for visible UI outcomes instead of timers or implementation internals.

**Incorrect:**

The test clicks submit and immediately asserts that a mock function was called.

**Correct:**

The test awaits the success message or validation error that a user sees.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Testing async UI behavior

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Awaited condition is user-visible.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
