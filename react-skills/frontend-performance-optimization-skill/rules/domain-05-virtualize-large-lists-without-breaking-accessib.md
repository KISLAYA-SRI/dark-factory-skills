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
