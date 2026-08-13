---
title: "Retry Only Safe Or Explicitly Idempotent Requests"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: retry, idempotency
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Retry Only Safe Or Explicitly Idempotent Requests

Retries must be limited to safe reads or writes with explicit idempotency semantics.

**Incorrect:**

The client retries POST payment creation after timeout with no idempotency key.

**Correct:**

The client retries GETs and idempotent writes with idempotency key and bounded backoff.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding retry behavior

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Method/idempotency assessed.
- Backoff/limit configured.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
