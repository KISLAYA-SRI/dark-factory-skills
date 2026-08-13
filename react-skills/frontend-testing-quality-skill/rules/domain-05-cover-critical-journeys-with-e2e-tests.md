---
title: "Cover Critical Journeys With E2E Tests"
impact: "HIGH"
impactDescription: "Prevents false confidence from shallow tests and missing frontend behavior evidence."
tags: playwright, cypress
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Cover Critical Journeys With E2E Tests

Critical flows need E2E coverage when route, auth, API, or cross-page behavior is changed.

**Incorrect:**

A login-protected checkout flow has only isolated button unit tests.

**Correct:**

A Playwright/Cypress test covers login/guard, form completion, API mock, confirmation, and failure path.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Changing critical multi-step flows

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- E2E path covers happy and key failure cases.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
