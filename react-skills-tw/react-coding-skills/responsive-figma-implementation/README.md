# Responsive Figma Implementation

Translates the reconciled responsive design intent and Figma context into token-based, responsive, RTL-ready React UI — mapping Figma values to existing project tokens, applying mobile-first breakpoints, logical RTL spacing, and semantic structure.

## Use This For

- Implementing responsive layout and breakpoints from the design (nested in Phase 4).
- Mapping Figma raw values to existing design tokens.
- Applying RTL-safe spacing, alignment, and mirrored directional elements.
- Preserving semantic heading hierarchy and handling overflow.

## Expected Flow

```text
Read responsive_design_intent.json (authority) + raw Figma context (detail)
  → Produce one mobile-first responsive implementation
  → Map every Figma value to a project token (record discrepancies)
  → Apply logical RTL spacing + mirror directional elements
  → Preserve semantic headings; respect prefers-reduced-motion
```

## Key Rules

- Reconciliation JSON is authoritative for responsive strategy; raw Figma is detail-only (Resolved Conflict 3).
- Never hardcode colours, spacing, or font sizes when a token exists.
- Never re-reconcile if responsive_design_intent.json already exists.
- One responsive component by default — split only when viewport content genuinely differs.
- Use logical start/end properties for RTL, never physical left/right.

See [SKILL.md](./SKILL.md) for the full instructions.
