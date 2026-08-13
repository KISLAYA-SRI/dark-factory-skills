---
title: "Do Not Rewrite Architecture Without Explicit Scope And Evidence"
impact: "HIGH"
impactDescription: ""
tags: architecture, scope
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change"]
---

## Do Not Rewrite Architecture Without Explicit Scope And Evidence

Large frontend architecture changes require explicit scope, target boundaries, validation plan, and migration evidence; do not broad-rewrite by preference.

**Incorrect:**

The agent reorganizes the entire app into a new architecture because it prefers feature-sliced design.

**Correct:**

The agent maps current boundaries, proposes an incremental target slice, updates only impacted modules, and verifies with tests/typecheck.

## Applies To Modes
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change

## When To Apply
- Changing architecture, folders, module boundaries, or migration strategy

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Scope and target architecture are explicit.
- Incremental validation path exists.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
