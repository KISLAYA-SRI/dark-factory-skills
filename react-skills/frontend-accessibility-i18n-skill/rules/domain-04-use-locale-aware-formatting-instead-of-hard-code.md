---
title: "Use Locale Aware Formatting Instead Of Hard Coded Strings"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: i18n, formatting
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Use Locale Aware Formatting Instead Of Hard Coded Strings

Dates, numbers, currencies, plurals, and relative times must use locale-aware formatters and translation keys.

**Incorrect:**

The component renders $1,000.00 and 1 items with hard-coded English strings.

**Correct:**

The component uses Intl formatters and pluralized translation messages for each locale.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding localized content or formatting

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Formatter/translation key used.
- Plural/locale behavior covered.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
