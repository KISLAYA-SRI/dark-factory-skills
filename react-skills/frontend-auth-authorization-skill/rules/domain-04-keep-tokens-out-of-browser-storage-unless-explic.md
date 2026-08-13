---
title: "Keep Tokens Out Of Browser Storage Unless Explicitly Approved"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: tokens, storage
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Keep Tokens Out Of Browser Storage Unless Explicitly Approved

Avoid localStorage/sessionStorage token persistence for sensitive sessions; prefer secure HttpOnly cookies or provider-managed session boundaries.

**Incorrect:**

The agent stores an access token and refresh token in localStorage for convenience.

**Correct:**

The app uses secure HttpOnly same-site cookies or provider-managed sessions and keeps tokens out of script-readable storage.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Implementing sessions or token handling

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Storage mechanism is identified.
- Script-readable sensitive tokens are absent or explicitly justified.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
