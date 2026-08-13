---
title: "Prefer Semantic HTML Before ARIA"
impact: "HIGH"
impactDescription: ""
tags: accessibility, aria
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Prefer Semantic HTML Before ARIA

Use native semantic elements and labels before adding ARIA; ARIA should clarify, not replace, correct HTML.

**Incorrect:**

The agent builds a button from div role=button without keyboard handling.

**Correct:**

The agent uses a real button with accessible name and adds ARIA only for additional state where needed.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Creating interactive UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Native semantics used where possible.
- ARIA usage has a clear purpose.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
