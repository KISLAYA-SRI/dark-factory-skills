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
