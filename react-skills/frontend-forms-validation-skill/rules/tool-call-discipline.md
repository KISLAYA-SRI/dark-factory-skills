---
title: "Base Form Fields On Contract And User Editable Data Only"
impact: "HIGH"
impactDescription: ""
tags: form, contract
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["debug_fix", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change"]
---

## Base Form Fields On Contract And User Editable Data Only

Forms must include only user-editable request fields from requirements/contracts and exclude caller identity, tenant, audit, state, or server-controlled fields.

**Incorrect:**

The agent adds tenantId, userId, createdBy, and status as editable form fields.

**Correct:**

The agent derives identity from auth context/server and includes only editable fields in the form schema.

## Applies To Modes
- debug_fix
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change

## When To Apply
- Creating request forms

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Server-controlled fields excluded.
- Request schema matches contract.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
