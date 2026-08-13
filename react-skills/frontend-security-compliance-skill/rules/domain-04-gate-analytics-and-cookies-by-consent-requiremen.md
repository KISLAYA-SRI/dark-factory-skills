---
title: "Gate Analytics And Cookies By Consent Requirements"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: privacy, consent
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Gate Analytics And Cookies By Consent Requirements

Analytics, tracking cookies, and session replay should follow supplied consent and privacy requirements.

**Incorrect:**

The app loads analytics and session replay before cookie consent is captured.

**Correct:**

The app delays optional trackers until consent and records consent state according to policy.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding analytics, cookies, tracking, or consent UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Consent category and load timing are explicit.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
