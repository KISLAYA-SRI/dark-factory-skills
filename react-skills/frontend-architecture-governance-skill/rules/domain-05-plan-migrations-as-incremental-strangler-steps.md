---
title: "Plan Migrations As Incremental Strangler Steps"
impact: "HIGH"
impactDescription: "Prevents broad unvalidated rewrites, broken module ownership, and unnecessary micro-frontend complexity."
tags: migration, refactor
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "brownfield_change"]
doesNotApplyToModes: ["greenfield_build", "debug_fix", "review_judge"]
---

## Plan Migrations As Incremental Strangler Steps

Framework/library migrations should be sliced, reversible, and validated rather than completed as one risky rewrite.

**Incorrect:**

The agent migrates all Pages Router routes to App Router in one change with no test plan.

**Correct:**

The agent migrates one route group at a time, preserves compatibility, runs tests, and records rollback criteria.

## Applies To Modes
- delta_change
- brownfield_change

## Does Not Apply To Modes
- greenfield_build
- debug_fix
- review_judge

## When To Apply
- Planning or performing frontend migrations

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Migration slices and rollback criteria exist.
- Compatibility verified.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
