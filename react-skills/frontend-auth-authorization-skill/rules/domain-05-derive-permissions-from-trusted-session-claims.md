---
title: "Derive Permissions From Trusted Session Claims"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: roles, claims
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Derive Permissions From Trusted Session Claims

Frontend permission decisions must use trusted session claims or server-provided permissions, not user-editable request data.

**Incorrect:**

A user can pass role=admin in query params to reveal privileged UI.

**Correct:**

The app derives permissions from validated session claims or a server authorization response.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding RBAC/ABAC rendering

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Permission source is trusted.
- User-editable inputs are ignored for auth.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
