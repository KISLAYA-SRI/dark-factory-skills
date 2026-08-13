---
title: "Test Denied Paths And Session Expiry"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: tests, denied-paths
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Test Denied Paths And Session Expiry

Auth changes require tests for unauthenticated, unauthorized, expired session, and allowed paths where tooling exists.

**Incorrect:**

Only the happy-path login is tested.

**Correct:**

Tests cover redirect to login, 403/denied UI, expired session handling, and allowed role access.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Changing auth flows or route guards

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Denied-path tests exist or blocker reported.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
