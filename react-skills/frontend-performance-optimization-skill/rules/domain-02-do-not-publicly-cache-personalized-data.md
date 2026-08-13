---
title: "Do Not Publicly Cache Personalized Data"
impact: "HIGH"
impactDescription: "Prevents false performance claims, cache leaks, and regressions to Web Vitals or accessibility."
tags: cache, privacy
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Do Not Publicly Cache Personalized Data

Caching strategy must respect personalization, auth, tenant, and data sensitivity boundaries.

**Incorrect:**

The agent marks an account dashboard as force-static and caches user balances publicly.

**Correct:**

The route uses dynamic/server rendering or private cache controls for personalized data and static/ISR only for safe public content.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Changing rendering or cache policy

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Personalization/data sensitivity assessed.
- Cache scope is safe.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
