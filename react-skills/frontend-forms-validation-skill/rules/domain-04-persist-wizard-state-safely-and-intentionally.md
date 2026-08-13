---
title: "Persist Wizard State Safely And Intentionally"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: wizard, persistence
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Persist Wizard State Safely And Intentionally

Multi-step wizard state persistence must be explicit, restorable, and safe for sensitive fields.

**Incorrect:**

The wizard stores all PII in localStorage indefinitely.

**Correct:**

The wizard persists only approved draft data with expiry or server draft support.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Building multi-step forms

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Persistence scope and sensitivity assessed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
