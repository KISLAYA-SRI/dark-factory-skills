---
title: "Do Not Expose Secrets To Client Bundles"
impact: "HIGH"
impactDescription: ""
tags: secrets, next-public
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Do Not Expose Secrets To Client Bundles

Frontend code must keep API keys, tokens, signing secrets, and privileged config out of NEXT_PUBLIC variables and browser bundles.

**Incorrect:**

The agent adds NEXT_PUBLIC_BACKEND_ADMIN_TOKEN so the browser can call an admin API directly.

**Correct:**

The server route reads the admin token server-side and the browser receives only safe response data.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding env vars, API clients, analytics, or BFF routes

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Client-visible env vars contain no secrets.
- Secret-backed calls run server-side.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
