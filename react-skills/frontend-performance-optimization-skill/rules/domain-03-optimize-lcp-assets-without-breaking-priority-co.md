---
title: "Optimize LCP Assets Without Breaking Priority Content"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: lcp, image, font
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Optimize LCP Assets Without Breaking Priority Content

Hero images, critical fonts, and above-the-fold content should be optimized for LCP without lazy-loading critical content.

**Incorrect:**

The agent lazy-loads the hero image and adds multiple blocking web fonts.

**Correct:**

The hero image uses proper sizing/priority and fonts are subset/preloaded or swapped according to project policy.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Optimizing LCP or asset-heavy pages

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Critical asset treatment is explicit.
- Layout dimensions prevent shifts.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
