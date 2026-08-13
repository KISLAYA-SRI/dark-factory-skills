---
title: "Enforce Module Boundaries With Imports And Ownership"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: module-boundary, ownership
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Enforce Module Boundaries With Imports And Ownership

Frontend modules should have clear allowed dependencies, public APIs, and ownership.

**Incorrect:**

A feature imports another feature internal file and creates circular dependencies.

**Correct:**

The feature consumes only public exports and CODEOWNERS/dependency rules define ownership.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding shared packages or reorganizing modules

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Public API boundary exists.
- No circular or internal imports introduced.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
