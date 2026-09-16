---
name: figma-design-analysis
description: Use this skill to reconcile mobile and desktop Figma Design Intent JSONs into a responsive design intent contract, and analyse Figma outputs to enrich component planning, responsive behaviour, RTL, and design-system reuse. Reads already-fetched Figma context files; performs no fetching. Triggers include Figma analysis, Figma reconciliation, responsive design intent, mobile desktop reconciliation, or responsive strategy.
---

## Figma Design Analysis

### Purpose

This skill **reconciles and analyses** Figma Design Intent JSONs already fetched.

- ✅ **Reconcile** mobile and desktop Design Intent JSONs into `responsive_design_intent.json` (conditional)
- ✅ **Analyse** the Figma outputs to enrich component planning, responsive behaviour, RTL, and design-system reuse
- ❌ **No fetching.** Never connect to Figma MCP, never open a Figma node, never re-scan the JIRA story for URLs.

---

### Inputs

| Input                     | Source                                                | Required?                    |
| ------------------------- | ----------------------------------------------------- | ---------------------------- |
| Figma Design Intent JSONs | `./figma-output/figma_design_{Node_id}_-context.json` | Validated present in Phase 4 |
| Existing reconciliation   | `./figma-output/responsive_design_intent.json`        | If already present           |

---

### ⚠️ VIEWPORT IDENTIFICATION — READ FIRST

Figma filenames follow `./figma_design_{Node_id}_-context.json` and **carry no viewport marker**. Identify viewport from file **content**, not filename:

```text
1. Read screenMetadata.deviceType   → "mobile" | "desktop" | similar
2. If absent or ambiguous, read screenMetadata.frameDimensions:
     width ≈ 390px   → mobile
     width ≈ 1700px  → desktop
3. If still ambiguous → treat as a single-viewport story.
   Record the ambiguity as an analysis risk in DEV_REVIEW.md §4. Do NOT guess.
```

Design reference viewports: **Mobile 390px · Desktop 1700px**

The CONTEXT_MANIFEST's `VIEWPORT COVERAGE` block already states whether both viewports are present — use it to decide whether reconciliation is required before opening the files.

---

## PART 1 — Reconciliation (Conditional)

⚠️ **Run only if BOTH a mobile and a desktop Design Intent JSON exist for the same logical component or screen.**

- Only one viewport present → **skip reconciliation entirely**, go to Part 2.
- `responsive_design_intent.json` already exists → **do NOT re-reconcile**. Use the existing file.

### Role

You are a Figma Reconciliation Agent. Compare the mobile and desktop Design Intent JSONs and produce a lean responsive context JSON.

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
- `Mobile/Top Navigation` and `Desktop Header` may both represent header areas with breakpoint-specific structures.

**Rule 2 — Keep shared components lean.** For each shared component include only: Name, What it contains, Mobile behaviour, Desktop behaviour, Key responsive differences, Design-system reuse guidance.

**Rule 3 — Identify breakpoint-specific components.** Classify as:

- `mobile-only`
- `desktop-only`
- `shared-responsive`
- `same-purpose-different-structure`
- `same-component-different-variant`

If a component exists in desktop only, **do not invent mobile behaviour**. If mobile only, **do not invent desktop behaviour**.

**Rule 4 — Convert Figma dimensions into implementation intent.**

- Mobile fill container → fluid width
- Desktop fixed form width → max-width, not hard fixed width
- Mobile column layout + desktop row layout → responsive direction switching

**Rule 5 — Always include RTL expectations.**

- Use start and end, not hardcoded left and right
- Use logical spacing and alignment
- Do not mirror brand logos
- Mirror only directional icons when needed
- Ensure Arabic text can expand without clipping
- Prefer `text-start` and `text-end`
- Ensure button icon placement works in RTL

### Reconciliation Output

Save as `./figma-output/responsive_design_intent.json`.

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

## PART 2 — Analysis and Enrichment

### Source Authority

**If `responsive_design_intent.json` exists (both viewports were provided):**

It is the **authoritative source** for responsive interpretation.

- Do NOT perform mobile vs desktop reconciliation again.
- Do NOT reclassify shared, mobile-only or desktop-only components.
- Do NOT derive new responsive rules from the raw context JSONs.

Use it as the source of truth for: `responsiveStrategy`, `implementationModel`, `sharedComponents`, `breakpointSpecificComponents`, `layoutRules`, `keyResponsiveDifferences`, `rtlGuidance`.

Use the Mobile and Desktop Design Intent JSONs **only as supporting references** for:

- Confirming exact design-system component references
- Checking component variant names, state names, text labels, token names
- Checking source node names or hierarchy when relevant
- Validating whether a required element exists in the source design

If a context JSON conflicts with the reconciliation JSON, **preserve the reconciliation JSON as the source of truth** and report the conflict in DEV_REVIEW.md §3.

**If only one viewport is provided (no reconciliation):**

Use the single Design Context JSON directly for component planning, design-system reuse planning, and identifying implementation risks.

### ⚠️ ANALYSIS DEPTH vs OUTPUT WIDTH

Perform every analysis check below in full. What is emitted into ANALYSIS_PLAN.md is narrower.

| Work Performed (always, in full)                     | Emitted To                                 |
| ---------------------------------------------------- | ------------------------------------------ |
| Target frame/node identification                     | Internal                                   |
| Layer hierarchy review                               | Internal → enriches **§5** hierarchy       |
| Semantic component identification                    | Internal → enriches **§5**, **§13.1**      |
| Text/copy ownership inference (CMS vs API vs system) | **§12** per-prop `Source`                  |
| Icon reference capture                               | Internal → enriches **§12** props          |
| Auto-layout / responsive interpretation              | **§13.2** exceptions                       |
| Design-system primitive identification               | **§13.1** reuse decisions                  |
| "Do not create" component identification             | **§8** Things NOT to Implement             |
| Figma-only interactions                              | **§9** — continue INT-xxx numbering        |
| Design-driven states (hover, focus, transitioning)   | **§10** — continue STATE-xxx numbering     |
| RTL requirements                                     | **§13.2** — story-specific exceptions only |
| Design ambiguity                                     | **DEV_REVIEW.md §4**                       |
| Content the design requires but no source provides   | Flag for the Next Phase gap sweep          |

⚠️ Do **not** emit a standalone Figma analysis section into ANALYSIS_PLAN.md. Figma findings feed the existing sections above. Baseline RTL/responsive/a11y rules are already embedded in the Coding Agent's skills — emit only story-specific exceptions.

### Enrichment Duties (From Phase 3 Drafts)

Phase 3 ran on story text alone. Complete what it could not know:

| Draft from Phase 3                                           | Enrichment here                                                                                                                     |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| **§9 interactions** — story-stated only                      | Add Figma-only interactions. **Continue INT-xxx numbering; never renumber.** Record `Figma-derived` provenance in DEV_REVIEW.md §4. |
| **§10 states** — story-stated only                           | Add design-driven visual states (hover, focus, transitioning, paused). **Continue STATE-xxx numbering.**                            |
| **§12 prop model** — `Source Detail` marked `To be resolved` | Resolve Sitecore-sourced props where the design confirms the field. API-sourced props are resolved in API Phase 6.                  |
| **§13.2 NFR exceptions**                                     | Add design-driven exceptions — e.g. a carousel needing `rtl:rotate-180` on pager arrows, or a fixed-height scroll region.           |
| **§8 Things NOT to Implement**                               | Add design elements deliberately not built in this story.                                                                           |

### Feeding the API Gap Sweep

While analysing the design, note every piece of **content the design displays** — labels, values, media, counts, status text. Phase 6 runs next and compares these against the actual contracts. Anything the design requires but no contract provides becomes a recorded gap.

⚠️ Do not attempt the gap analysis here — the API contracts have not been read yet. Simply ensure design-required content is captured in the §12 prop model so the gap sweep has something to check against.

### Figma Analysis Checklist

| Check                                  | What to Validate                                                     |
| -------------------------------------- | -------------------------------------------------------------------- |
| Figma context read                     | Confirm Figma data was available                                     |
| Viewport identified per file           | Derived from `screenMetadata`, not filename                          |
| Target frame/node identified           | Node name and type captured                                          |
| Layer hierarchy reviewed               | Understand visible UI structure                                      |
| Text/copy ownership inferred carefully | Determine whether labels come from CMS or API/system                 |
| Icon references noted                  | Capture icon names only, not actual assets                           |
| Auto-layout/layout hints considered    | Use dimensions/layout only as guidance, not hardcoded implementation |
| Design ambiguity captured              | Missing/unclear component intent → DEV_REVIEW.md §4                  |
| Design-required content captured       | Present in §12 for the Phase 6 gap sweep                             |

### Guardrails for Analysis

- ✅ Use the Responsive Reconciliation JSON as the authoritative responsive contract
- ✅ Use Mobile/Desktop context JSONs only as detail references
- ✅ Identify shared components vs breakpoint-specific components
- ✅ Identify responsive layout transformations
- ✅ Identify RTL requirements
- ✅ Identify design-system primitives and semantic components to reuse
- ✅ Identify what must not be created as a new component → feeds §8
- ❌ Do not treat desktop as the default source of truth
- ❌ Do not treat mobile as a scaled-down version of desktop
- ❌ Do not perform reconciliation again if `responsive_design_intent.json` already exists
- ❌ Do not use context JSONs to override the Responsive Reconciliation JSON
- ❌ Do not hardcode Figma dimensions — convert to implementation intent
- ❌ Do not recreate design-system components from Figma visuals

---

### Guardrails

#### Always Do

- Read only the Figma files already written in Phase 2.
- Identify viewport from `screenMetadata`, never from the filename.
- Reconcile only when both viewports are present and no reconciliation file exists.
- Treat the reconciliation JSON as authoritative once produced.
- Enrich Phase 3's drafts — §5, §8, §9, §10, §12, §13.
- **Continue existing INT-xxx and STATE-xxx numbering; never renumber.**
- Capture design-required content in §12 so the Phase 6 gap sweep can check it.
- Record design ambiguity in DEV_REVIEW.md §4 and conflicts in §3.

#### Never Do

- **Never fetch from Figma MCP** — acquisition was Phase 2.
- **Never re-scan the JIRA story for Figma URLs** — use the CONTEXT_MANIFEST.
- **Never re-derive or silently change the component classification.** If the design contradicts it, record an analysis risk in DEV_REVIEW.md §1.
- **Never invent design intent, node names, tokens, or component structure.**
- Never invent mobile behaviour for a desktop-only component, or vice versa.
- Never re-reconcile when `responsive_design_intent.json` already exists.
- Never emit a standalone Figma section into ANALYSIS_PLAN.md.
- Never emit baseline RTL/responsive rules — only story-specific exceptions.
- **Never renumber IDs assigned in Phase 3.**
- Never perform API gap analysis here — the contracts have not been read yet.

---

### Gate: This Skill Completes When

- [ ] CONTEXT_MANIFEST consulted for viewport coverage.
- [ ] Viewport identified per file from `screenMetadata`.
- [ ] Reconciliation performed **only** when both viewports present and no existing reconciliation file.
- [ ] `responsive_design_intent.json` written (or correctly skipped).
- [ ] All analysis checklist rows completed.
- [ ] Phase 3 drafts enriched: §5, §8, §9, §10, §12, §13.
- [ ] Figma-only interactions added with continued INT-xxx numbering.
- [ ] Design-driven states added with continued STATE-xxx numbering.
- [ ] Design-required content captured in §12 for the gap sweep.
- [ ] Classification left unchanged; any contradiction recorded as a risk.
- [ ] No standalone Figma section produced.
- [ ] Design ambiguity → DEV_REVIEW.md §4; conflicts → DEV_REVIEW.md §3.
