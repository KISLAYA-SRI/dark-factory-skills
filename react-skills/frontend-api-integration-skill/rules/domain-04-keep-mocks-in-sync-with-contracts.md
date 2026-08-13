---
title: "Keep Mocks In Sync With Contracts"
impact: "HIGH"
impactDescription: "Prevents frontend/backend drift and client-side leakage of privileged credentials."
tags: msw, mocks
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change"]
---

## Keep Mocks In Sync With Contracts

MSW and test fixtures must follow current contract/generated types.

**Incorrect:**

The test mock returns fields not in the schema and hides a runtime bug.

**Correct:**

The mock uses generated types and is updated with schema changes.

## Applies To Modes
- delta_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change

## When To Apply
- Adding API tests or mocks

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Mocks compile against types.
- Schema drift checked.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
