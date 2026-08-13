---
title: "Avoid Brittle Visual And Snapshot Tests"
impact: "HIGH"
impactDescription: "Prevents false confidence from shallow tests and missing frontend behavior evidence."
tags: visual, snapshot
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "review_judge"]
---

## Avoid Brittle Visual And Snapshot Tests

Visual regression should focus stable states and meaningful diffs, not noisy full-page snapshots without controls.

**Incorrect:**

The agent snapshots an animated page with live timestamps and random data.

**Correct:**

The agent freezes data/time, captures stable component states, and documents acceptable diffs.

## Applies To Modes
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- review_judge

## When To Apply
- Adding visual/snapshot tests

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Dynamic data stabilized.
- Visual scope is meaningful.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
