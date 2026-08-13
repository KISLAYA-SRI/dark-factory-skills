---
title: "Prefer Local State Before Global Stores"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: local-state, global-store
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Prefer Local State Before Global Stores

Use local or lifted state unless multiple distant consumers require a shared store.

**Incorrect:**

The agent creates a Redux slice for a single dropdown.

**Correct:**

The component uses local state and lifts it only when sibling coordination is required.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding UI state

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- State consumer scope is identified.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
