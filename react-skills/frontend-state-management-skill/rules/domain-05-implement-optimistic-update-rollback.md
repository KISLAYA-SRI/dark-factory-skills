---
title: "Implement Optimistic Update Rollback"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: optimistic
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Implement Optimistic Update Rollback

Optimistic UI must define rollback, conflict, and error behavior.

**Incorrect:**

The agent removes an item optimistically but cannot restore it when the API fails.

**Correct:**

The mutation snapshots previous data, rolls back on error, and handles conflict responses.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Adding optimistic mutations

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Rollback path exists.
- Conflict/error states are handled.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
