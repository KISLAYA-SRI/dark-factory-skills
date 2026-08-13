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
