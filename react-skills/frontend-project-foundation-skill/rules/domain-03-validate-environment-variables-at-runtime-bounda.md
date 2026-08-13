---
title: "Validate Environment Variables At Runtime Boundary"
impact: "HIGH"
impactDescription: "Prevents client-side secret leakage and runtime configuration drift."
tags: env, secrets, zod
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Validate Environment Variables At Runtime Boundary

Environment variables should be schema-validated and separated between server-only and client-visible values.

**Incorrect:**

The agent reads SECRET_KEY through NEXT_PUBLIC_SECRET_KEY in client code.

**Correct:**

The agent validates server secrets server-side and exposes only safe NEXT_PUBLIC values.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding env config or accessing environment variables

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Server/client env boundary is explicit.
- Missing env values fail clearly.
- Secrets are not bundled client-side.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
