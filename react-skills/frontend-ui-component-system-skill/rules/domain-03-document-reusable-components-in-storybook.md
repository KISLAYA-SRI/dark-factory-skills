---
title: "Document Reusable Components In Storybook"
impact: "HIGH"
impactDescription: "Prevents fragile UI APIs and inaccessible reusable components."
tags: storybook, documentation, components
costHint: "load_for_reusable_component_storybook_changes"
risk: "high"
appliesToModes: ["brownfield_change"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "debug_fix", "review_judge"]
---

## Document Reusable Components In Storybook

Reusable or design-system components should include Storybook stories for variants, states, and interactions.

**Incorrect:**

The agent adds a reusable Button variant but no story for disabled, loading, icon, or error-adjacent states.

**Correct:**

The agent adds stories for default, disabled, loading, destructive, responsive, and interaction states using project conventions.

## Applies To Modes
- brownfield_change

## Does Not Apply To Modes
- greenfield_build
- delta_change
- debug_fix
- review_judge

## When To Apply
- Adding or changing reusable components

## Does Not Apply To
- Private one-off screen fragments with no reuse contract

## Evidence And Validation
- Stories cover variants and key states.
- Storybook command is run or blocker reported.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
