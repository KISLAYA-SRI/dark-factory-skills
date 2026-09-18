---
name: sitecore-rendering-integration
description: Use to own the Sitecore-to-React boundary for CMS-mapped components — typed Sitecore field contracts, Layout Service field mapping, rendering entry components, placeholder handling, and component-registry integration. Keeps CMS labels separate from API values.
disable-model-invocation: true
---

## Sitecore Rendering Integration

### Purpose

Own the Sitecore-headless-to-React boundary independently of BFF business logic. Invoke this skill only for the Sitecore Integration.

### Layout JSON is the Contract

The Sitecore Layout Service JSON is the Sitecore-to-frontend contract:
- Sitecore owns page composition and authored content.
- The frontend resolves and renders registered React components from the layout.
- Authored fields flow in as typed props; the frontend never hardcodes CMS copy.

### Ordered Steps

```text
1. Field Contract  — typed interface for the rendering's Sitecore fields
2. Field Mapping   — map Layout Service fields → component props (via Sitecore helpers)
3. Rendering Entry — CMS component (default export) that reads fields and renders the presentational component
4. Registry        — register the rendering entry in the component registry
5. Placeholders    — wire any child placeholders the rendering exposes
6. Separation      — keep CMS labels distinct from API/runtime values
```

### Field Contract & Mapping

- Define a typed contract for every Sitecore field the rendering consumes (text, rich text, image, link, checkbox, droplink, multilist).
- Use the project's Sitecore field helpers to safely extract values (handle editing/preview vs normal render).
- Map fields to the presentational component's ViewModel/props — the presentational component stays CMS-agnostic and reusable.

### Rendering Entry Component

- **Default export** (required by the Sitecore component registry) plus a named export of its field-contract type.
- Thin: reads fields, maps to props, renders the presentational component. No data fetching, no business logic here.
- If the component also needs runtime BFF data (Hybrid), it receives that via the container from `frontend-logic-integration` — CMS fields and API data are merged at the container/entry boundary, kept clearly separated in code.

### Placeholders

- Expose and render child placeholders exactly as the layout defines them.
- Do not invent placeholder keys; use the keys from the Sitecore rendering definition.

### Preview / Experience Editor

- Ensure fields render through the Sitecore field components so Experience Editor/preview remains editable.
- Guard against null/unauthored fields with safe defaults; never crash on missing optional fields.

### CMS Labels vs API Values (Separation)

- CMS-authored labels/copy come from Sitecore fields.
- Runtime/business values come from the BFF via the logic layer.
- Never source a business value from a CMS field or vice versa; keep the two clearly separated and documented in the summary.

### Output Files (per CMS component)

```text
Packages/Cms/CmsComponents/<ComponentName>/
├── <ComponentName>.tsx           # rendering entry (default export)
├── <ComponentName>Types.ts        # Sitecore field contract
├── <ComponentName>Mapper.ts       # fields → props (optional if trivial)
└── index.ts
```

### Learnings Namespace

Load only the `# LOGIC LEARNINGS` namespace (Sitecore wiring is part of logic).

### Gate: Complete When

```text
- [ ] Typed Sitecore field contract defined for the rendering.
- [ ] Layout Service fields mapped to presentational props via helpers.
- [ ] Rendering entry is default-exported and registered in the component registry.
- [ ] Child placeholders wired with correct keys.
- [ ] CMS labels kept separate from API/runtime values.
- [ ] Preview/Experience Editor rendering safe for null/unauthored fields.
```

### Never Do

- Never hardcode CMS copy in the component — read it from Sitecore fields.
- Never give the rendering entry a named-only export (registry needs default).
- Never place BFF data fetching inside the rendering entry — that belongs to the logic layer.
- Never source a business value from a CMS field.
- Never invent placeholder keys not defined in the rendering.
