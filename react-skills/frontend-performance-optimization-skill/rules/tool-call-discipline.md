---
title: "Measure Before Claiming Performance Improvement"
impact: "HIGH"
impactDescription: ""
tags: performance, evidence
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["brownfield_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "debug_fix"]
---

## Measure Before Claiming Performance Improvement

Performance work needs baseline and after-change evidence or a clear blocker; do not claim improvement from code appearance alone.

**Incorrect:**

The agent removes a dependency and says performance improved without measuring bundle size, Web Vitals, or route timing.

**Correct:**

The agent records baseline bundle/Lighthouse/Web Vitals evidence, applies a scoped change, and reports after-change evidence or a blocker.

## Applies To Modes
- brownfield_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- debug_fix

## When To Apply
- Optimizing or reviewing frontend performance

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Baseline or blocker exists.
- After-change evidence or residual risk is reported.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
