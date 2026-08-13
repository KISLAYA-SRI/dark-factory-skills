---
title: "Do Not Invent Organization Foundation Templates"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: template, organization
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["greenfield_build", "brownfield_change", "review_judge"]
doesNotApplyToModes: ["delta_change", "debug_fix"]
---

## Do Not Invent Organization Foundation Templates

Organization-specific scaffolds, folder names, CI conventions, and env names require repository or user evidence.

**Incorrect:**

The agent invents an enterprise app shell, package scope, and deployment target with no source.

**Correct:**

The agent uses supplied template evidence or asks for the missing convention.

## Applies To Modes
- greenfield_build
- brownfield_change
- review_judge

## Does Not Apply To Modes
- delta_change
- debug_fix

## When To Apply
- Enterprise project setup is requested

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Template/convention evidence is cited or blocker listed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
