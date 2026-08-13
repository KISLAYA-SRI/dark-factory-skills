---
title: "Keep Secrets Server Side In BFF And Server Actions"
impact: "HIGH"
impactDescription: "Prevents frontend/backend drift and client-side leakage of privileged credentials."
tags: secrets, bff
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Keep Secrets Server Side In BFF And Server Actions

API keys and privileged tokens must stay in server-only route handlers/server actions, not browser bundles.

**Incorrect:**

The browser fetch client includes a private backend API key.

**Correct:**

A server route reads the secret and returns only safe data to the client.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding BFF/API routes or secret-backed calls

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Secret not exposed client-side.
- Server/client boundary explicit.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
