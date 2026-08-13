---
title: "Use Stable Query Keys And Explicit Invalidation"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: query-key, invalidation
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Use Stable Query Keys And Explicit Invalidation

Server-state cache keys must include all meaningful parameters and mutations must invalidate or update affected queries.

**Incorrect:**

A customer query key omits tenant id and filters, causing cross-view stale data.

**Correct:**

The query key includes tenant/customer/filter params and mutation invalidates affected list/detail keys.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Adding query/cache logic

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Query keys include parameters.
- Invalidation/update behavior is explicit.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
