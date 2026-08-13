---
title: "Do Not Invent Frontend API Contracts"
impact: "HIGH"
impactDescription: ""
tags: contract, api
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "debug_fix"]
---

## Do Not Invent Frontend API Contracts

Frontend API code must be based on supplied schemas, generated clients, existing wrappers, or explicit user requirements.

**Incorrect:**

The agent guesses response fields and creates a client that does not match OpenAPI.

**Correct:**

The agent uses generated OpenAPI types or flags missing contract details before implementation.

## Applies To Modes
- brownfield_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- debug_fix

## When To Apply
- Adding frontend API calls

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Contract source is cited.
- Unknown fields are not invented.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
