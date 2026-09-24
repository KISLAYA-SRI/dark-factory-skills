# Figma Fetch, Reconcile, and Analyse

Skill for fetching Figma design intent from all Figma URLs in a Jira story, reconciling mobile and desktop viewports when both are provided, and producing the responsive design intent JSON for the Analysis Agent.

## Use This For

- Extracting all Figma URLs from a Jira story and fetching design intent via Figma MCP.
- Generating Design Intent JSON files for each viewport (mobile and/or desktop).
- Reconciling mobile and desktop Figma designs into a single Responsive Design Intent JSON.
- Identifying component structure, spacing, typography, and responsive behaviour from Figma.
- Providing Figma-derived design inputs to the Story Analysis phase.

## Expected Flow

```text
Jira Story
  → PHASE 1 — Fetch:
    Extract all Figma URLs
    → Connect to Figma MCP
    → Generate Design Intent JSON per viewport
  → PHASE 2 — Reconcile (conditional):
    Both mobile + desktop provided? → Produce Responsive Design Intent JSON
    Only one viewport? → Skip reconciliation
  → PHASE 3 — Analyse:
    Use Figma outputs to inform component planning, responsive behaviour, and design-system reuse
```

All three phases run in sequence within this single skill invocation.

## Key Rules

- Output must focus on design intent and implementation guidance — not raw Figma node data.
- Do not return variable definitions, design token definitions, full vector data, or verbose style definitions.
- Minimise tokens while maximising implementation accuracy.
- If both mobile and desktop Figma files are provided, reconciliation is mandatory.
- If only one viewport is provided, skip reconciliation and proceed directly to analysis.
- Figma is the third-priority source — Dev Notes and Project Guidelines override Figma.

See [SKILL.md](./SKILL.md) for the full instructions.
