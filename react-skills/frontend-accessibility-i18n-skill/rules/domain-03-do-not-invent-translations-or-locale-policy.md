---
title: "Do Not Invent Translations Or Locale Policy"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: translation, locale
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Do Not Invent Translations Or Locale Policy

Translations, supported locales, fallback behavior, and legal copy must come from supplied source or be clearly marked as placeholders.

**Incorrect:**

The agent invents French legal consent copy and claims localization complete.

**Correct:**

The agent adds translation keys with placeholders and flags missing approved copy as a blocker.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding i18n support

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Translation source cited or placeholder marked.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
