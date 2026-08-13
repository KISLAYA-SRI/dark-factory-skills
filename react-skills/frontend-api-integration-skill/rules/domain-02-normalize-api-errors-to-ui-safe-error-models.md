---
title: "Normalize API Errors To UI Safe Error Models"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: error-handling
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Normalize API Errors To UI Safe Error Models

Frontend clients should map transport, validation, auth, conflict, and server errors into typed UI-safe errors.

**Incorrect:**

The component displays raw stack traces from a failed fetch.

**Correct:**

The API wrapper maps problem details/status codes into safe user and developer messages.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Handling API failures

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Status/error mapping exists.
- Sensitive details are not displayed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
