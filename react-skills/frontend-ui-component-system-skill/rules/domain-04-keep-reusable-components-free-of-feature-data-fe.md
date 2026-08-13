---
title: "Keep Reusable Components Free Of Feature Data Fetching"
impact: "HIGH"
impactDescription: "Prevents fragile UI APIs and inaccessible reusable components."
tags: composition
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Keep Reusable Components Free Of Feature Data Fetching

Reusable components should receive data and callbacks through props rather than importing feature services.

**Incorrect:**

A reusable table component calls /api/accounts internally.

**Correct:**

The screen fetches data and passes rows/actions into a reusable table component.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Creating shared components

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- No feature API imports in shared UI.
- Data ownership remains at screen/feature boundary.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
