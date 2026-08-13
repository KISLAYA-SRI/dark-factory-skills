---
title: "Tie Tests To Changed User Observable Behavior"
impact: "HIGH"
impactDescription: ""
tags: tests, evidence
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change"]
---

## Tie Tests To Changed User Observable Behavior

Frontend tests must validate changed user-visible behavior, not only implementation details or snapshots.

**Incorrect:**

The agent changes checkout validation and only updates a shallow snapshot.

**Correct:**

The agent tests the validation message, disabled submit state, API error handling, and successful submit outcome.

## Applies To Modes
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change

## When To Apply
- Adding or judging frontend tests

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Tests map to changed behavior.
- Assertions are user-observable.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
