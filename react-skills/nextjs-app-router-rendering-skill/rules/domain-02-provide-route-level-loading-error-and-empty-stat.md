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
