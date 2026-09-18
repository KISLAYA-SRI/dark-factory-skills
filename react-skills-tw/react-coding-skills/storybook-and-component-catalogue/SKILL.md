---
name: storybook-and-component-catalogue
description: Use to generate or update Storybook stories and the root component-catalogue.json for eligible reusable components — Design System components, Sitecore-mapped reusable presentation components, and any reusable file created in the Design System. Covers props, variants, visual states, RTL and responsive contexts, and catalogue upsert. Triggers include Storybook, stories, component catalogue, or document this component.
disable-model-invocation: true
---

## Storybook and Component Catalogue

### Purpose

Generate co-located `*.stories.tsx` and upsert the root `component-catalogue.json` for reusable components created/enhanced in this run. Consumes the actual generated source (props, variants, states) — not the plan alone.

### Eligibility (Resolved Conflict 7)

Write stories ONLY for:

- ✅ New or enhanced **Design System** components (Foundation atoms/molecules/organisms).
- ✅ **Sitecore-mapped reusable presentation** components.
- ✅ Any reusable component/file created in the **Design System**.

Do NOT write stories for:

- ❌ Containers, hooks, services, mappers, type-only files.
- ❌ One-off feature-orchestration components (not reusable).
- ❌ Configuration or constants files.

If none of the generated components are eligible, record "No Storybook-eligible components" and skip to catalogue check.

### Story Generation (from Actual Source)

Read the generated component's exported `Props` and build stories covering:

```text
- Default (all required props)
- Each variant (from discriminated union / variant prop)
- Optional-prop permutations that change appearance
- Visual states where applicable: loading, error, empty, disabled
- Interaction callbacks wired to Storybook actions (args: onSelect, onSlideChange, …)
- RTL context (dir="rtl") story
- Responsive/viewport contexts (mobile + desktop)
```

Rules:

- Co-locate: `<ComponentName>.stories.tsx` beside the component.
- Use accessible, human-readable story names.
- Provide `argTypes` for controls; use `args` for default prop values.
- Stories are prop-driven — no hardcoded data that the component should receive via props.
- Do not fetch data or import services in a story; pass mock props only.

### Component Catalogue Upsert (Root)

`./src/component-catalogue.json` lives at the **repository root** (Resolved Conflict 2). For each eligible reusable component:

```text
Upsert an entry:
  {
    "name": "HeroCarousel",
    "atomicLevel": "organism",
    "location": "Packages/DesignSystem/Foundation/Src/Organisms/HeroCarousel",
    "props": [ … prop name/type/required … ],
    "variants": [ … ],
    "states": [ … ],
    "reuse": "new" | "enhanced",
    "storybook": "HeroCarousel.stories.tsx"
  }
```

Upsert rules:

- **Match by component name**: update in place if it exists, insert if new.
- **Never blind-append** duplicates; **never delete or reorder** unrelated entries.
- Keep the file valid JSON; preserve existing formatting/ordering of untouched entries.

### Learnings Namespace (Resolved Conflict 6)

Load only the `# STORYBOOK LEARNINGS` namespace.

### Gate: Complete When

```text
- [ ] Stories created for every eligible component (DS / Sitecore-mapped reusable / DS file).
- [ ] Non-eligible artefacts (containers/hooks/services/mappers/types) excluded.
- [ ] Default + variants + applicable states + RTL + responsive contexts covered.
- [ ] Callbacks wired to actions; props mocked (no data fetching in stories).
- [ ] component-catalogue.json upserted at repo root; JSON valid; unrelated entries intact.
```

### Never Do

- Never write stories for containers, hooks, services, mappers, or one-off feature components.
- Never blind-append or delete unrelated entries in component-catalogue.json.
- Never move or duplicate component-catalogue.json from the repository root.
- Never fetch data or import services inside a story.
- Never hardcode data a component should receive as props.
