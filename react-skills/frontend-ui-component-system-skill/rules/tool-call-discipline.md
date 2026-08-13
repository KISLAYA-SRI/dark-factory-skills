---
title: "Define Component Ownership And Prop Contracts Before Coding"
impact: "HIGH"
impactDescription: ""
tags: react, props
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change"]
---

## Define Component Ownership And Prop Contracts Before Coding

Components need clear ownership, prop contracts, state boundaries, and failure states before implementation.

**Incorrect:**

The agent creates a reusable Card component that fetches account data and hides internal loading errors.

**Correct:**

The agent separates screen data loading from a typed presentational Card component with documented props and states.

## Applies To Modes
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change

## When To Apply
- Creating or refactoring React components

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Component level is identified.
- Props and states are typed.
- Data ownership is explicit.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
