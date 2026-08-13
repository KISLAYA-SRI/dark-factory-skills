---
title: "Do Not Treat Client UI Gating As Authorization"
impact: "HIGH"
impactDescription: ""
tags: auth, authorization, client-ui
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Do Not Treat Client UI Gating As Authorization

Client-side hiding of links or buttons is only UX; protected data and privileged actions require server-side route/action/API checks.

**Incorrect:**

The agent hides the Admin link but still renders admin data in the page payload for non-admin users.

**Correct:**

The server component/middleware/server action checks session permissions before fetching or mutating admin data, while the client also hides the link for UX.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding protected routes or role-based UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Server-side authorization check exists for protected data/actions.
- Client gating is documented as UX only.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
