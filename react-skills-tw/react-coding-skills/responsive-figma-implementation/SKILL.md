---
name: responsive-figma-implementation
description: Use to translate the reconciled responsive design intent and Figma context into token-based, responsive, RTL-ready React UI. Maps Figma values to existing project design tokens, applies mobile-first breakpoints, logical RTL spacing, and semantic structure. Triggers include responsive implementation, Figma to code, design tokens, RTL, breakpoints, or make this component responsive.
disable-model-invocation: true
---

## Responsive Figma Implementation

### Purpose

Turn the reconciled responsive design intent and raw Figma context into one responsive, token-based, RTL-ready implementation. This skill is invoked nested from `presentational-ui-generation` and is also reusable for review/remediation.

### Source Authority

Apply topic-based precedence for visual/responsive decisions:

```text
Visual disparity:
  Dev Notes (if implementation notes exist) → Figma Reconciliation → Analysis Plan

Responsive behaviour:
  Dev Notes → responsive_design_intent.json →  guidelines mentioned in skill
```

- Raw desktop/mobile `*-context.json` are used ONLY for implementation detail (exact spacing, radii, typography, colours) — never to override the reconciliation.
- If only one viewport context exists, use it directly.
- Never re-reconcile if `responsive_design_intent.json` already exists.

### One Responsive Implementation (Default)

Produce a **single** responsive component by default — not separate desktop/mobile components.

- **Mobile-first**: base styles target the smallest breakpoint; layer up with min-width breakpoints.
- Use the project's defined breakpoint tokens (do not invent pixel breakpoints).
- Only create breakpoint-specific content/markup when the reconciliation explicitly flags content that differs by viewport (e.g. desktop-only column, mobile-only stacked order).

### Token Mapping (No Hardcoded Values)

Map every Figma raw value to an existing project token:

<table>
<tr><th>Figma value</th><th>Map to</th></tr>
<tr><td>Colour hex</td><td>Design-system colour token (never raw hex in components)</td></tr>
<tr><td>Font size / weight / line-height</td><td>Typography token / text style (use directly; do not override weight ad-hoc)</td></tr>
<tr><td>Spacing / padding / gap</td><td>Spacing scale token</td></tr>
<tr><td>Corner radius</td><td>Radius token</td></tr>
<tr><td>Shadow</td><td>Elevation/shadow token</td></tr>
</table>

If a Figma value has no matching token, use the nearest token and **record the discrepancy** for the summary's Deviations section. Do not introduce a new hardcoded value.

### RTL Handling (Always)

- Use logical properties/directional utilities for spacing and alignment (start/end, not left/right).
- Mirror directional icons and horizontal interactions (e.g. carousel next/prev) under RTL.
- Derive direction from the app's `Directionality`/locale — never hardcode LTR.
- Keep numerals, currency, and date formatting locale-aware where the design shows them.

### Layout Rules

- Use the page grid only for page-level composition; use local flex/grid inside components.
- Preserve semantic heading hierarchy (`h1…h6`) from the design; do not choose heading levels for styling.
- Handle overflow/scroll per the design (truncation, wrap, scroll containers) — no clipped content.

### Effects & Motion

- Implement transitions/autoplay/parallax with standard React + CSS transitions.
- Always respect `prefers-reduced-motion` — disable non-essential motion when set.

### Gate: Complete When

```text
- [ ] Reconciliation used as authority; raw Figma used only for detail.
- [ ] Single responsive, mobile-first implementation produced (unless viewport content genuinely differs).
- [ ] Every Figma value mapped to a project token; discrepancies recorded.
- [ ] Logical RTL spacing/alignment applied; directional elements mirrored.
- [ ] Semantic headings preserved; overflow handled.
- [ ] Reduced-motion respected for effects.
```

### Never Do

- Never hardcode hex colours, pixel spacing, or font sizes in components when a token exists.
- Never override the responsive reconciliation with raw viewport JSON.
- Never re-reconcile when responsive_design_intent.json already exists.
- Never produce separate desktop/mobile components unless the plan requires viewport-specific content.
- Never use left/right physical properties where logical (start/end) properties are needed for RTL.
