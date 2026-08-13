---
title: "Use React Hook Form Register Or Controller Appropriately"
impact: "HIGH"
impactDescription: "Prevents invalid requests, duplicate submissions, and unsafe user-editable server fields."
tags: react-hook-form
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Use React Hook Form Register Or Controller Appropriately

Use register for native/uncontrolled inputs and Controller for controlled third-party components. For complex forms, apply this rule through the approved form library pattern in `trigger-scope.md` rather than hand-writing raw `value`/`onChange` state for every field.

**Incorrect:**

The agent wraps every simple input in Controller and causes unnecessary rerenders.

**Correct:**

Native inputs use register; controlled date picker uses Controller with typed value mapping.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Building React Hook Form forms

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Field control pattern fits component type.
- If the form is complex, inputs are wired through the approved form library (`register`, `Controller`, or equivalent) and the library rule `trigger-scope.md` is satisfied.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
- rules/trigger-scope.md
