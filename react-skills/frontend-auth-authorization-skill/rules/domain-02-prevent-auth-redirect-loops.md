---
title: "Prevent Auth Redirect Loops"
impact: "HIGH"
impactDescription: "Prevents protected data leaks from client-only auth checks and unsafe token storage."
tags: middleware, redirect
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Prevent Auth Redirect Loops

Auth middleware and route groups must clearly separate public, auth, and protected routes.

**Incorrect:**

Middleware redirects /login to /dashboard, then /dashboard back to /login when the session is loading.

**Correct:**

Middleware handles public/auth/protected route groups with deterministic redirects and loading states.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding route guards or middleware redirects

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Route groups are listed.
- Redirect cycle risk is checked.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
