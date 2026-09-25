---
name: storybook-and-component-catalogue
description: Use to generate or update Storybook stories, the mandatory JSDoc documentation block, and ./src/component-catalogue.json for eligible reusable components — Design System components, Sitecore-mapped reusable presentation components, and any reusable file created in the Design System. Covers props, variants, visual states, RTL and responsive contexts, and catalogue upsert. Triggers include Storybook, stories, component catalogue, JSDoc, or document this component.
disable-model-invocation: true
---

## Storybook and Component Catalogue

### Purpose

Generate co-located `*.stories.tsx`, the mandatory JSDoc documentation block, and upsert `./src/component-catalogue.json` for reusable components created/enhanced in this run. Consumes the **actual generated source** (props, variants, states) — not the plan alone.

⚠️ Write Storybook with the project's quality and standards, but **do NOT run lint, type-check, or test commands** — a separate quality gate handles that.

---

## ⚠️ WRITE FILES, NOT DESCRIPTIONS

Every `.stories.tsx` file and the catalogue update must be **written to disk**. Files described in the summary but not written do not count.

---

## 1. Eligibility

Write stories ONLY for:

```text
✅ New or enhanced Design System components (Foundation atoms/molecules/organisms)
✅ Shared reusable UI components
✅ CMS presentational components
✅ Sitecore-mapped reusable presentational components
✅ Any reusable component/file created in the Design System
```

Do NOT write stories for:

```text
❌ Containers, hooks, services, mappers, type-only files
❌ One-off feature-orchestration components (not reusable)
❌ Configuration or constants files
```

If none of the generated components are eligible, record *"No Storybook-eligible components"* and skip to the catalogue check.

---

## 2. ⚠️ MANDATORY JSDoc DOCUMENTATION BLOCK

When creating or enhancing a reusable component, generate or update a **JSDoc block comment at the top of the file, before imports**, documenting the component for human readers.

**All 14 tags are required:**

```ts
/**
 * @component {ComponentName}
 * @category {atom | molecule | organism | cms-component}
 * @library {design-system | cms}
 *
 * @description
 * {One or two sentence human-readable description of what this component does,
 *  what problem it solves, and when to use it.}
 *
 * @usage
 * - Use this component when: {list primary use cases}
 * - Do NOT use this component when: {list anti-patterns or alternatives}
 *
 * @props
 * | Prop Name     | Type                        | Required | Default   | Description                          |
 * |---------------|-----------------------------|----------|-----------|--------------------------------------|
 * | {propName}    | {TypeScript type}           | {Yes/No} | {default} | {what this prop controls}            |
 *
 * @variants
 * {List all visual/behavioural variants if applicable, e.g., primary, secondary, ghost}
 *
 * @designTokens
 * {List all CSS custom properties / design tokens consumed by this component}
 *
 * @accessibility
 * - ARIA Role: {role}
 * - Keyboard Support: {Yes/No — describe keyboard interactions}
 * - Semantic Element: {HTML element rendered}
 * - Focus Management: {describe focus behaviour}
 *
 * @dependencies
 * - External: {npm packages used}
 * - Internal: {other design system atoms/molecules used}
 *
 * @importStatement
 * import { {ComponentName} } from '{package-import-path}';
 *
 * @storybook
 * Title: {Library}/{ComponentName}
 * Stories: {list story names}
 *
 * @createdAt {YYYY-MM-DD}
 * @version 1.0.0
 */
```

⚠️ Populate every tag with **real, component-specific** content — never leave placeholder braces in the output.

---

## 3. Story Generation (From Actual Source)

Read the generated component's exported Props and build stories covering:

```text
- Default (all required props)
- Each variant (from discriminated union / variant prop)
- Optional-prop permutations that change appearance
- Visual states where applicable: loading, error, empty, disabled
- Interaction callbacks wired to Storybook actions (args: onSelect, onSlideChange, …)
- RTL context (dir="rtl") story
- Responsive/viewport contexts (mobile 390px + desktop 1700px)
```

### Story Rules

- Co-locate: `<ComponentName>.stories.tsx` beside the component
- Story title follows the atomic hierarchy: `Atoms/ComponentName`, `Molecules/ComponentName`, `Organisms/ComponentName`
- Use accessible, human-readable story names
- Provide `argTypes` for controls; use `args` for default prop values
- Stories are prop-driven — no hardcoded data the component should receive via props
- ❌ Do not fetch data or import services in a story; pass **mock props only**

⚠️ **Storybook is the ONLY place mock/hardcoded values are permitted.** Components themselves must never carry hardcoded content.

### Storybook Environment

- Storybook dev environment in `@dxp/foundation` runs on **port 6006**
- Storybook config folders already exist — **never create a new `.storybook/` folder**

---

## 4. Component Catalogue Upsert

**Path:** `./src/component-catalogue.json`

⚠️ This is the **master inventory file** for all components and the **primary source read by the Component Inventory & Reuse Agent**. It lives at `./src/component-catalogue.json` — **never** at the repository root, never inside `.SS_WF/`, never duplicated elsewhere. To update it, edit the file in place.

The catalogue must include **every** reusable design-system and CMS/presentational component. Whenever a reusable component is created or enhanced, update this global file.

### Full Schema

```json
{
  "_meta": {
    "description": "Primary source read by the Component Inventory and Reuse Agent. Contains all reusable design-system and CMS/presentational components.",
    "lastUpdated": "dd-mm-yyyy hh:mm:ss",
    "version": "1.0.0"
  },
  "components": [
    {
      "name": "",
      "displayName": "",
      "componentType": "design-system | cms-component | feature-component",
      "category": "atom | molecule | organism | template | rendering",
      "classification": "presentational | transactional | hybrid",
      "description": "",
      "supportedPatterns": [],
      "imports": [],
      "props": [
        {
          "name": "",
          "type": "",
          "required": true,
          "description": "",
          "default": null
        }
      ],
      "variants": [
        {
          "name": "",
          "description": "",
          "propsRequired": []
        }
      ],
      "states": [],
      "composition": [],
      "usageGuidance": {
        "useWhen": [],
        "doNotUseWhen": []
      },
      "accessibility": {
        "semanticSupport": true,
        "ariaNotes": "",
        "ariaRoles": [""],
        "keyboardSupport": true,
        "semanticElement": "",
        "focusManagement": "",
        "notes": ""
      },
      "responsiveBehaviour": [],
      "figma": {
        "componentKeys": [],
        "knownLayerNames": []
      },
      "createdAt": "",
      "lastUpdated": ""
    }
  ]
}
```

### Field Guidance

| Field | Content |
| --- | --- |
| `supportedPatterns` | Design patterns the component supports (e.g. "card list", "form field") |
| `imports` | Internal design-system components consumed |
| `composition` | Sub-components composed within |
| `usageGuidance.useWhen` / `doNotUseWhen` | Mirrors the JSDoc `@usage` tag |
| `responsiveBehaviour` | How the component adapts mobile → desktop |
| `figma.componentKeys` | Figma component keys from the design context |
| `figma.knownLayerNames` | Layer names seen in Figma, for future matching |

### Upsert Rules

```text
- Match by component NAME: update in place if it exists, insert if new
- NEVER blind-append duplicates
- NEVER delete or reorder unrelated entries
- Keep the file valid JSON; preserve formatting/ordering of untouched entries
- Update _meta.lastUpdated on every write
- Set component-level createdAt on insert; lastUpdated on every change
```

⚠️ **Read the current file, merge your entries, write the complete updated content back.** Do not assume an append mode exists.

---

### Learnings Namespace

Load only the `# STORYBOOK LEARNINGS` namespace.

---

### Gate: Complete When

```text
- [ ] Story files WRITTEN TO DISK for every eligible component (and only those)
- [ ] Non-eligible artefacts (containers/hooks/services/mappers/types) excluded
- [ ] JSDoc block with ALL 14 tags added at the top of every reusable component file
- [ ] Every JSDoc tag populated with real content — no placeholder braces
- [ ] Default + variants + applicable states + RTL + responsive contexts covered
- [ ] Story titles follow the atomic hierarchy (Atoms/ Molecules/ Organisms/)
- [ ] Callbacks wired to actions; props mocked (no data fetching in stories)
- [ ] ./src/component-catalogue.json upserted with the FULL schema
- [ ] JSON valid; unrelated entries intact; _meta.lastUpdated refreshed
- [ ] No new .storybook/ folder created
```

### Never Do

- **Never describe a story without writing the file to disk.**
- Never write stories for containers, hooks, services, mappers, or one-off feature components.
- Never omit the JSDoc block or leave placeholder braces in it.
- Never blind-append or delete unrelated entries in the catalogue.
- Never move or duplicate `component-catalogue.json` from `./src/`.
- Never place the catalogue at the repository root.
- Never fetch data or import services inside a story.
- Never hardcode data a component should receive as props.
- Never create a new `.storybook/` configuration folder.
- Never run lint, type-check, or test commands.
- Never modify the component source beyond adding its JSDoc block.
