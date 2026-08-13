---
title: "Separate Client State From Server State"
impact: "HIGH"
impactDescription: ""
tags: state, server-state
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Separate Client State From Server State

Server-derived data should live in query/cache tools; client stores should hold UI/application state only.

**Incorrect:**

The agent copies fetched orders into a global store and manually syncs stale data.

**Correct:**

The agent keeps orders in TanStack Query cache and stores only selected filters and modal state separately.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding state around async data

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Server cache ownership is clear.
- Client store has no duplicated server source of truth.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
