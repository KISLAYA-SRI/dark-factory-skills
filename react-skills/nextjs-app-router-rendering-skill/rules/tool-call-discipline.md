---
title: "Choose Rendering Strategy From Data Freshness And User Context"
impact: "HIGH"
impactDescription: ""
tags: nextjs, rendering
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Choose Rendering Strategy From Data Freshness And User Context

Rendering mode must follow data freshness, personalization, SEO, and cache requirements.

**Incorrect:**

The agent makes a personalized account route static because it improves speed.

**Correct:**

The agent uses dynamic/server rendering for personalized data and static/ISR for safe public content.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Choosing SSR, SSG, ISR, CSR, or streaming

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Freshness/user context is identified.
- Cache/revalidation setting matches route risk.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
