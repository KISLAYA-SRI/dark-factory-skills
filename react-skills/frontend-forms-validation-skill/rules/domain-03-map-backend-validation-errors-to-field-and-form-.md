---
title: "Map Backend Validation Errors To Field And Form Errors"
impact: "HIGH"
impactDescription: "Prevents invalid requests, duplicate submissions, and unsafe user-editable server fields."
tags: backend-errors
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Map Backend Validation Errors To Field And Form Errors

Backend validation and conflict errors should become clear field-level or form-level feedback.

**Incorrect:**

The form shows a generic failed message for duplicate email and loses field context.

**Correct:**

The submit handler maps field violations to setError and conflicts to a form-level action message.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Submitting forms to APIs

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Error model mapped.
- User can correct failures.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
