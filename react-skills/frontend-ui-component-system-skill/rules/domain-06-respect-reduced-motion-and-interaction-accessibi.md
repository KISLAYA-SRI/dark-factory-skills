---
title: "Respect Reduced Motion And Interaction Accessibility"
impact: "HIGH"
impactDescription: "Prevents fragile UI APIs and inaccessible reusable components."
tags: motion, accessibility
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Respect Reduced Motion And Interaction Accessibility

Animations and interactions must preserve reduced-motion preferences and keyboard/focus behavior.

**Incorrect:**

A modal animates focus off-screen and ignores prefers-reduced-motion.

**Correct:**

The modal uses focus management, keyboard close behavior, and reduced-motion-safe transitions.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding motion or interactive components

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Reduced motion respected.
- Focus/keyboard behavior verified.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
