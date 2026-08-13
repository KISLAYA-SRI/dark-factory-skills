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
