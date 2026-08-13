---
title: "Align Metadata With Dynamic Route Content"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: metadata, seo
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Align Metadata With Dynamic Route Content

Dynamic pages should generate metadata, canonical URLs, and sitemap behavior from validated route params.

**Incorrect:**

A product detail page has static metadata copied across all products.

**Correct:**

The route validates params and generates title, description, canonical, and not-found behavior.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding SEO-sensitive routes

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Metadata source is validated.
- Canonical/sitemap behavior is described.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
