---
title: "Avoid Micro Frontends Without Runtime Contract Justification"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: micro-frontend, module-federation
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Avoid Micro Frontends Without Runtime Contract Justification

Micro-frontends should require team/runtime isolation needs and explicit contracts, not just code organization.

**Incorrect:**

The agent splits a small dashboard into module federation remotes with no deployment or ownership need.

**Correct:**

The agent documents isolation driver, route ownership, shared dependency policy, fallback UI, and runtime contract.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Introducing micro-frontends or module federation

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Isolation reason exists.
- Runtime contract and fallback behavior defined.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
