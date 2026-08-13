---
title: "Use MSW Or Existing Network Mock Strategy For API Flows"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: msw, api
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Use MSW Or Existing Network Mock Strategy For API Flows

API-backed UI tests should mock network at the boundary using MSW or the existing project strategy.

**Incorrect:**

The component test mocks internal fetch hooks and misses request/response behavior.

**Correct:**

The test uses MSW handlers matching the API contract and verifies loading, success, and error UI.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Testing API-backed UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Network boundary mocked consistently.
- Success and failure handlers exist.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
