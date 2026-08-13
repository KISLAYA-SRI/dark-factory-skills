---
title: "Enforce Strict TypeScript Without Blocking Brownfield Incremental Work"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: typescript, strict
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "brownfield_change"]
doesNotApplyToModes: ["greenfield_build", "debug_fix", "review_judge"]
---

## Enforce Strict TypeScript Without Blocking Brownfield Incremental Work

Prefer strict TypeScript for new foundations while scoping brownfield strictness to impacted areas unless a full migration is requested.

**Incorrect:**

The agent flips strict mode across a large legacy app and leaves hundreds of unrelated errors.

**Correct:**

The agent enables strictness for new packages or proposes a staged migration with blockers and owner.

## Applies To Modes
- delta_change
- brownfield_change

## Does Not Apply To Modes
- greenfield_build
- debug_fix
- review_judge

## When To Apply
- Adding tsconfig or strict typing

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Strictness impact is assessed.
- Brownfield blast radius is controlled.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
