---
title: "Use Domain Modeling To Reduce Coupling Not Duplicate Backend Domains Blindly"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: domain-modeling, bounded-context
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Use Domain Modeling To Reduce Coupling Not Duplicate Backend Domains Blindly

Frontend domains should reflect user journeys and UI ownership while aligning with backend contracts where needed.

**Incorrect:**

The agent mirrors every backend table as a frontend domain and spreads API DTOs through UI components.

**Correct:**

The agent defines frontend domain models for UI behavior and maps API DTOs at boundaries.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Organizing frontend domains or bounded contexts

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Domain model purpose is UI-facing.
- API DTO mapping boundary exists.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
