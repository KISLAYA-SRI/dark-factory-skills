---
title: "Compose Screens As Thin Orchestration Layers"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: react, screens, composition
costHint: "load_for_screen_composition_changes"
risk: "high"
appliesToModes: ["brownfield_change"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "debug_fix", "review_judge"]
---

## Compose Screens As Thin Orchestration Layers

Compose screens from data/loading boundaries and child components without burying reusable logic in route files.

**Incorrect:**

The screen file owns fetching, form state, formatting, modal state, and table rendering in one large component.

**Correct:**

The screen coordinates data and layout, then delegates reusable behavior to typed hooks and components.

## Applies To Modes
- brownfield_change

## Does Not Apply To Modes
- greenfield_build
- delta_change
- debug_fix
- review_judge

## When To Apply
- Creating or refactoring a React screen or route

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Screen orchestration is separated from reusable hooks/components.
- Route-level ownership remains clear.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
