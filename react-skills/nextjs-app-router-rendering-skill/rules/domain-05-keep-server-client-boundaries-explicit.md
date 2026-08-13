---
title: "Keep Server Client Boundaries Explicit"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: server-component, client-component
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Keep Server Client Boundaries Explicit

Client components should be used only for interactivity; server data, secrets, and privileged calls stay server-side.

**Incorrect:**

A client component imports a server-only API client and reads process.env.SECRET.

**Correct:**

The server component fetches secure data and passes safe props to a small client component.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding interactivity or data fetching

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- No server-only imports in client components.
- Props are serializable and safe.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
