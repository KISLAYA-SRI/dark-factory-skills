---
title: "Sanitize Or Avoid Untrusted HTML Rendering"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: xss, sanitization
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Sanitize Or Avoid Untrusted HTML Rendering

Untrusted HTML must be avoided or sanitized with an approved library and constrained rendering boundary.

**Incorrect:**

The app renders CMS HTML through dangerouslySetInnerHTML without sanitization.

**Correct:**

The app sanitizes CMS HTML with an approved policy or renders structured content instead.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Rendering user/CMS/third-party HTML

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Sanitization policy or structured rendering exists.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
