---
title: "Treat URL State As Public Shareable State"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: search-params
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Treat URL State As Public Shareable State

URL/search params should store safe shareable filters and pagination, not secrets or volatile UI internals.

**Incorrect:**

The agent puts access token and full customer name in search params.

**Correct:**

The agent stores page, sort, and status filter in the URL and keeps sensitive data server-side.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Syncing state to URL

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- URL state excludes secrets/PII.
- Back/forward behavior works.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
