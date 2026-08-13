---
title: "Avoid Hydration Mismatches From Non Deterministic Rendering"
impact: "HIGH"
impactDescription: "Prevents stale personalized data, SEO regressions, and runtime hydration failures."
tags: hydration
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Avoid Hydration Mismatches From Non Deterministic Rendering

Do not render time, random ids, browser APIs, or user-only data differently on server and client.

**Incorrect:**

The server renders Date.now and the client re-renders a different value.

**Correct:**

The agent moves non-deterministic values to effects or stable server-provided props.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Changing mixed server/client UI

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- No non-deterministic SSR output without stabilization.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
