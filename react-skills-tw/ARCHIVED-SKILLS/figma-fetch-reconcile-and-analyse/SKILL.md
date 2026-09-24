---
name: figma-fetch-reconcile-and-analyse
description: Use when fetching Figma design intent from all Figma URLs in a Jira story, reconciling mobile and desktop viewports when both are provided, and producing the responsive design intent JSON for the Analysis Agent. Triggers include Figma fetch, Figma design intent, Figma reconciliation, responsive design intent, mobile desktop reconciliation, or Figma MCP.
---

# Figma Fetch, Reconcile, and Analyse

## Overview

This skill combines three phases into one:

1. **PHASE 1 — Fetch:** Extract all Figma URLs from the Jira story, connect to Figma MCP, and generate Design Intent JSON files for each viewport.
2. **PHASE 2 — Reconcile (conditional):** If BOTH mobile and desktop Figma files are provided, produce a lean Responsive Design Intent JSON. If only one viewport is provided, skip reconciliation.
3. **PHASE 3 — Analyse:** Use the Figma outputs as inputs for the Analysis Agent to inform component planning, responsive behaviour, and design-system reuse.

---

## Inputs Available to the Agent

Before starting, confirm what inputs are available:

| Input           | Source                                         | Required?     |
| --------------- | ---------------------------------------------- | ------------- |
| JIRA User Story | `.SS_WF/{{$var[ticket_id]s}}_jira_output.json` | **Mandatory** |

## PHASE 1 — Figma Design Intent Extraction

### Role

You are a Figma Design Intent Extraction Agent. From the JIRA Story data, find all Figma URL endpoints and extract design intent for each.

### Hard Rules

- The output MUST focus on design intent and implementation guidance.
- DO NOT return raw Figma node data.
- DO NOT return unnecessary MCP payloads.
- DO NOT return variable definitions, design token definitions, full vector data, or verbose style definitions.
- Minimise tokens while maximising implementation accuracy.

### Step 1 — Connect to Figma

Use the Figma MCP server to:

- Open the supplied node.
- Traverse all nested children.
- Identify screen hierarchy.
- Identify reusable components.
- Extract only implementation-relevant metadata.

### Step 2 — Analyse Screen Structure

Identify:

- Page Name, Screen Name, Node ID, Frame Dimensions, Device Type, Primary Layout Pattern
- Classify screen as: Page, Modal, Drawer, Bottom Sheet, Tab View, Wizard, Dashboard, List View, Form, Detail View, or Other

### Step 3 — Extract Layout Grid Information

Capture: Grid Type, Column Count, Row Count, Gutter Width, Margins, Grid Alignment, Grid Width Behaviour, Stretch Behaviour.

Extract how all components are structured and fit on the Desktop and Mobile grid in terms of columns.

### Step 4 — Extract Responsive Behaviour

**Constraints:** Horizontal Constraint, Vertical Constraint (Left, Right, LeftRight, TopBottom, Centre, Scale)

**Resizing Behaviour:** Fixed Width, Fixed Height, Hug Content, Fill Container

**Size Limits (when defined):** Min Width, Max Width, Min Height, Max Height

### Step 5 — Extract Auto Layout Information

For every auto-layout container capture:

- Direction, Padding, Gap, Cross-Axis Alignment, Main-Axis Alignment, Wrap Setting, Fill/Hug Settings
- Represent using implementation-friendly values (directly mappable to Flexbox or CSS Grid)

### Step 6 — Build Component Hierarchy

Generate complete parent-child hierarchy:

- Component Name, Component Type, Parent Component, Child Components, Text/Name if present
- Preserve nesting. Never flatten the structure.
- Add nested component with details as per hierarchy inside `childComponents` array (do not just mention IDs)

### Step 7 — Extract Component Instance Information

Capture only:

- Referenced Component Name, Variant Selection, Component State (Default, Hover, Focus, Active, Disabled, Error, Loading)
- DO NOT return the full component instance payload.

### Step 8 — Extract Design Token Usage

> IMPORTANT: DO NOT extract Variable Definitions, Token Definitions, or Token Values.

Extract only **token references** used by components:

- Colours, Typography, Spacing, Border Radius, Shadows, Elevation, Borders
- Examples: `colour-primary-500`, `spacing-4`, `font-body-md`, `radius-md`
- NEVER hardcode any value — use only token names.
- Values without a token name go into `missing_tokens`.

### Step 9 — Identify Semantic Component Types

For every component, infer the most likely semantic type based on component instance information, name, and type.

- Example: An element visually a link but built using Button Component → should be a "Button" with design tokens and variants of that element.
- Classifications: Button, Link, Input, Text Area, Select, Radio, Checkbox, Switch, Card, Table, Tabs, Badge, Chip, Banner, Alert, Header, Footer, Navigation, Breadcrumb, Pagination, Modal, Drawer, Accordion, Carousel, Skeleton, Progress Indicator

### Step 10 — Typography Intent

Capture: Semantic Role, Token Name, Text Style Usage (e.g., Heading XL, Heading LG, Body MD, Caption SM)

- DO NOT capture verbose text style metadata.

### Step 11 — Icon Inventory

Capture: Icon Name, Semantic Meaning

- DO NOT export binary image content or SVG path data.

### Output Format (Per Figma URL)

```json
{
  "screenMetadata": {},
  "layoutGrid": {},
  "responsiveRules": {},
  "componentHierarchy": [],
  "missing_tokens": []
}
```

Save each output to `.src/figma-output/` folder with name: `figma_design_{Node_id}_{viewport}-context.json`

---

## PHASE 2 — Figma Reconciliation (Conditional)

> ⚠️ **CONDITIONAL:** Only perform reconciliation if BOTH a mobile Figma file AND a desktop Figma file are provided for the same logical component or screen. If only one viewport is provided, skip this phase entirely and proceed directly to Phase 3.

### Role

You are a Figma Reconciliation Agent. Compare the mobile and desktop Design Intent JSON files and produce a lean responsive context JSON for the Analysis Agent.

### Design Reference Viewports

- Mobile: `390px`
- Desktop: `1700px`

### What NOT to Output

- Full mobile JSON or full desktop JSON
- Raw Figma node tree or raw component hierarchy dump
- Token definitions, variable definitions, full style objects
- Raw colour definitions unless no token or semantic reference exists
- SVG paths, image binaries, repeated low-value metadata
- Every single child node if it does not affect implementation

### Reconciliation Rules

**Rule 1 — Reconcile by semantic intent, not node names.**

- `Forgot Username Button` and `Forgot username?` may both represent the same action.
- `Mobile/Top Navigation` and `Desktop Header` may both represent header areas but with breakpoint-specific structures.

**Rule 2 — Keep shared components lean.**
For each shared component include only: Name, What it contains, Mobile behaviour, Desktop behaviour, Key responsive differences, Design-system reuse guidance.

**Rule 3 — Identify breakpoint-specific components.**
Classify as:

- `mobile-only`
- `desktop-only`
- `shared-responsive`
- `same-purpose-different-structure`
- `same-component-different-variant`

If a component exists in desktop only, do not invent mobile behaviour. If mobile only, do not invent desktop behaviour.

**Rule 4 — Convert Figma dimensions into implementation intent.**

- Mobile `fill container` → fluid width
- Desktop fixed form width → `max-width`, not hard fixed width
- Mobile column layout + desktop row layout → responsive direction switching

**Rule 5 — Always include RTL expectations.**

- Use `start` and `end`, not hardcoded `left` and `right`
- Use logical spacing and alignment
- Do not mirror brand logos
- Mirror only directional icons when needed
- Ensure Arabic text can expand without clipping
- Prefer `text-start` and `text-end`
- Ensure button icon placement works in RTL

### Reconciliation Output Format

Save as `figma-output/responsive_design_intent.json`.

```json
{
  "componentName": "",
  "componentType": "page | component | pattern",
  "sourceViewports": {
    "mobile": "390px",
    "desktop": "1700px"
  },
  "responsiveStrategy": "",
  "implementationModel": "single-responsive-component | single-responsive-page | responsive-composition-with-breakpoint-specific-subcomponents",
  "sharedComponents": [
    {
      "name": "",
      "responsibility": "",
      "contains": [],
      "mobile": {
        "layout": "",
        "width": "",
        "spacing": "",
        "typography": {},
        "visibility": "visible"
      },
      "desktop": {
        "layout": "",
        "width": "",
        "spacing": "",
        "typography": {},
        "visibility": "visible"
      },
      "responsiveHandling": []
    }
  ],
  "breakpointSpecificComponents": [
    {
      "name": "",
      "visibility": "mobile-only | desktop-only",
      "reason": "",
      "implementationHandling": ""
    }
  ],
  "layoutRules": {
    "mobile": {
      "rootDirection": "",
      "grid": "",
      "horizontalMargin": "",
      "contentPriority": [],
      "containerBehaviour": ""
    },
    "desktop": {
      "rootDirection": "",
      "grid": "",
      "horizontalMargin": "",
      "contentPriority": [],
      "containerBehaviour": ""
    },
    "transformation": []
  },
  "keyResponsiveDifferences": [{ "area": "", "mobile": "", "desktop": "" }],
  "stateAndInteractionGuidance": [
    { "element": "", "stateOrInteraction": "", "codingGuidance": "" }
  ],
  "rtlGuidance": [""]
}
```

---

## PHASE 3 — Using Figma Outputs in Analysis

### Inputs Available to Analysis Agent

After Phase 1 and Phase 2 (if applicable), the Analysis Agent has access to:

1. **Mobile Design Context JSON** — `figma-output/*_mobile-context.json`
2. **Desktop Design Context JSON** — `figma-output/*_desktop-context.json`
3. **Responsive Reconciliation JSON** — `figma-output/responsive_design_intent.json` (only if both viewports were provided)

### How to Use These Inputs

**If Responsive Reconciliation JSON exists (both viewports provided):**

The Responsive Reconciliation JSON is the **authoritative source** for responsive interpretation.

- Do NOT perform mobile vs desktop responsive reconciliation again.
- Do NOT reclassify shared, mobile-only or desktop-only components.
- Do NOT derive new responsive rules from the raw mobile or desktop context JSONs.

Use the Responsive Reconciliation JSON as the source of truth for:

- `responsiveStrategy`, `implementationModel`, `sharedComponents`, `breakpointSpecificComponents`
- `layoutRules`, `keyResponsiveDifferences`, `rtlGuidance`, `doNotCreateComponents`
- `codingAgentInstructions`, `bestPracticeLearnings`

Use the Mobile and Desktop Design Intent Context JSONs **only as supporting references** for:

- Confirming exact design-system component references
- Checking component variant names, state names, text labels, token names
- Checking source node names or hierarchy when relevant
- Validating whether a required element exists in the source design

If the context JSONs conflict with the Responsive Reconciliation JSON, preserve the reconciliation JSON as the source of truth and report the conflict as an analysis risk.

**If only one viewport is provided (no reconciliation):**

Use the single Design Context JSON directly for:

- Story analysis, component planning, design-system reuse planning
- Identifying missing requirements and implementation risks
- Passing clear guidance to the Coding Agent

### Design Reference Widths for Analysis

- Mobile: `390px`
- Desktop: `1700px`

### Figma Analysis Checklist

| Check                                  | What to Validate                                                     |
| -------------------------------------- | -------------------------------------------------------------------- |
| Figma context read                     | Confirm figma data was available                                     |
| Target frame/node identified           | Node name and type captured                                          |
| Layer hierarchy reviewed               | Understand visible UI structure                                      |
| Text/copy ownership inferred carefully | Determine whether labels come from CMS or API/system                 |
| Icon references noted                  | Capture icon names only, not actual assets                           |
| Auto-layout/layout hints considered    | Use dimensions/layout only as guidance, not hardcoded implementation |
| Design ambiguity captured              | Missing/unclear component intent documented                          |

### Guardrails for Analysis Phase

- ✅ Use the Responsive Reconciliation JSON as the authoritative responsive contract
- ✅ Use Mobile/Desktop context JSONs only as detail references
- ✅ Identify shared components vs breakpoint-specific components
- ✅ Identify responsive layout transformations
- ✅ Identify RTL requirements
- ✅ Identify design-system primitives and semantic components to reuse
- ✅ Identify what must not be created as a new component
- ❌ Do not treat desktop as the default source of truth
- ❌ Do not treat mobile as a scaled-down version of desktop
- ❌ Do not perform reconciliation again if Responsive Reconciliation JSON already exists
- ❌ Do not use context JSONs to override the Responsive Reconciliation JSON
- ❌ Do not hardcode Figma dimensions — convert to implementation intent
- ❌ Do not recreate design-system components from Figma visuals
