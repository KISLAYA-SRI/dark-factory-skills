---
name: sitecore-rendering-integration
description: Use to own the Sitecore-to-React boundary for CMS-mapped components — typed Sitecore field contracts, Layout Service field mapping, Sitecore helper utilities, rendering entry components, placeholder handling, page composition wiring, and component-registry integration. Keeps CMS labels separate from API values. Triggers include Sitecore, CMS component, Layout Service, rendering, placeholder, or page composition.
disable-model-invocation: true
---

## Sitecore Rendering Integration

### Purpose

Own the Sitecore-headless-to-React boundary independently of BFF business logic. Invoke only for Sitecore/CMS integration.

⚠️ **This skill embeds the project's page composition model and Sitecore helper contracts.** No external guideline lookup required.

---

## ⚠️ WRITE FILES, NOT DESCRIPTIONS

The PRIMARY deliverable is actual `.ts`/`.tsx` source files written to disk at the exact paths specified. Documenting code in the summary is **not** a substitute for writing it.

---

## 1. Page Composition Model

For Headless Sitecore XP + dynamic component composition, pages are dynamically composed and rendered using Sitecore-managed component trees.

### Three Logical Layers

| Layer | Owns | Responsibility |
| --- | --- | --- |
| **Frontend (Browser/Next.js)** | Request initiation & final render | Captures navigation, resolves routes, requests layout data, renders the page |
| **Sitecore Platform** | Page composition | Resolves content, placeholders, renderings, datasources, personalization, language → returns Layout JSON |
| **Frontend Server (Next.js)** | Component rendering | Maps Layout JSON to React components, injects props, builds the tree, renders SSR/CSR |

⚠️ **Layout JSON is the contract between Sitecore and Frontend.** It contains the complete component hierarchy, content references, and metadata required to build the page.

### The Flow

```text
1.  User opens page
2.  Next.js resolves via catch-all route pages/[[...path]].tsx
       _app.tsx runs server-side: parses lang (en/ar), sets dir, theme-mode,
       wraps with QueryProvider + ThemeProvider
3.  Layout Service request  → page path, language, context, preview flag
4.  Sitecore resolves page & composition
       page item · placeholders · renderings · variants · datasources
       rendering parameters · personalization · language/version
5.  Layout JSON response   → component hierarchy, placeholders, fields, metadata
6.  Component Resolution   → registry maps "HeroBanner" → HeroBanner.tsx
7.  Placeholder Resolution → builds the placeholder tree in correct order
8.  Inject Data & Props    → fields from datasource, rendering params, context
9.  React tree generated
10. Rendering Mode         → SSR (SEO/first paint) or CSR (in-app navigation)
11. Final page composed
```

### Key Architectural Principles

| Principle | Meaning |
| --- | --- |
| **Sitecore owns composition** | Authors build pages with placeholders/renderings/variants — no FE redeployment for content or structure changes |
| **Frontend owns rendering** | FE maps components and renders; Sitecore never dictates markup or styling |
| **Dynamic & reusable** | Components resolved dynamically from a registry |
| **Personalization-ready** | Sitecore applies rules and sends the resolved tree; FE simply renders it |
| **Multi-language** | Requested language flows through content resolution and the Layout Service response |

---

## 2. Routing — Catch-All Is the Default

**All Sitecore-driven pages go through `pages/[[...path]].tsx`.**

Any page whose content, layout, and rendering behaviour is driven by Sitecore should **not** have its own route. No code changes are needed to add a new page — content authors create it in Sitecore.

### Create a Dedicated Route ONLY When

| Condition | Allowed? |
| --- | --- |
| Different rendering strategy (static/ISR) needed | ✅ Yes |
| Custom metadata/SEO logic beyond Sitecore fields | ✅ Yes |
| Completely different layout or UI shell (checkout, dashboard, auth) | ✅ Yes |
| Page is Sitecore-authored content | ❌ No — use catch-all |

If creating a dedicated route: keep locale handling consistent with the catch-all, and confirm the route doesn't shadow a real Sitecore path.

⚠️ Language is derived from the **URL prefix** (`en`/`ar`) — never from query params.

⚠️ `Portals/` and `pages/` are **sibling directories** at the project root — never nest one inside the other.

---

## 3. Ordered Steps

```text
1. Field Contract  — typed interface for the rendering's Sitecore fields
2. Field Mapping   — Layout Service fields → component props (via Sitecore helpers)
3. Rendering Entry — CMS component (default export) reading fields, rendering presentational
4. Registry        — register the rendering entry in the component registry
5. Placeholders    — wire any child placeholders the rendering exposes
6. Separation      — keep CMS labels distinct from API/runtime values
```

---

## 4. Field Contract & Mapping

- Define a typed contract for every Sitecore field the rendering consumes (text, rich text, image, link, checkbox, droplink, multilist)
- Use the project's Sitecore field helpers to safely extract values (handle editing/preview vs normal render)
- Map fields to the presentational component's ViewModel/props — the presentational component stays **CMS-agnostic and reusable**
- ❌ Never invent Sitecore fields not present in the approved rendering contract

---

## 5. Sitecore Helper Utilities

**File:** `Packages/Common/Utils/SitecoreHelpers.ts`

Use these to extract and normalise Sitecore field data into typed frontend props.

| Helper | Purpose | Returns |
| --- | --- | --- |
| `extractFormField` | Extract form field config | `name`, `key`, `label`, `placeholder`, `informationMessage`, `validationMessages[]` |
| `extractCTA` | Extract CTA configuration | `text`, `type`, `link` (text/href/linktype/target), `additionalText` |
| `extractLink` | Extract link configuration | `text`, `href`, `linktype`, `target` |
| `findErrorMessage` | Find error message by API error code | Matched message + severity, or `null` |
| `transformSitecoreDynamicValue` | Replace placeholders in a message template | Message with `{key}` or `{0}`, `{1}` replaced |
| `extractApiResponseMessages` | Extract API response messages | `apiCode`, `message`, `severity` (name + value) |

⚠️ Always use these helpers rather than reaching into raw field objects.

---

## 6. Rendering Entry Component

- **Default export** (required by the Sitecore component registry) plus a named export of its field-contract type
- **Thin**: reads fields, maps to props, renders the presentational component
- No data fetching, no business logic here
- If the component also needs runtime BFF data (**Hybrid**), it receives that via the container from `frontend-logic-integration` — CMS fields and API data merge at the container/entry boundary, kept clearly separated in code

---

## 7. Placeholders

- Expose and render child placeholders **exactly as the layout defines them**
- ❌ Do not invent placeholder keys — use the keys from the Sitecore rendering definition
- Respect placeholder/rendering mapping as specified in the Analysis Plan

---

## 8. Component Registry

- CMS component folder name = Sitecore rendering name (**PascalCase, case-sensitive**)
- Must use `export default ComponentName`
- Register the rendering in the component registry if required by the Analysis Plan

After adding or renaming a CMS component:

```bash
pnpm run build:cms-component-registry   # Stage A — package-level
pnpm run build:component-registry       # Stage B — app-level aggregator
```

⚠️ A kebab-case folder produces a wrong registry key → silent runtime fallback to the missing-component placeholder.

---

## 9. Preview / Experience Editor

- Ensure fields render through the Sitecore field components so Experience Editor/preview remains editable
- Guard against null/unauthored fields with safe defaults — **never crash on missing optional fields**
- Preserve Experience Editor / preview compatibility where project convention requires it

---

## 10. CMS Labels vs API Values (Separation)

```text
CMS-authored → labels, copy, media, links, CTAs, variants, authored config,
               error message copy, localisation strings
API/runtime  → user-specific values, computed fields, policy/account/transaction data
```

- ❌ Never source a business value from a CMS field, or vice versa
- ❌ Never hardcode Sitecore-authored labels — they come from fields, never as fallback prop values either
- ❌ Never move FE-owned state into Sitecore
- ❌ Never make every inner card, tab, field, or block a Sitecore rendering unless specified
- ❌ Never place feature-specific Sitecore renderings into the generic CMS package unless approved

Keep the two clearly separated and document the split in the summary.

---

## 11. Page Composition Wiring

Wire the full page by connecting:

```text
Sitecore-mapped entry component → container → view → display components
```

Ensure all navigation, routing, and redirect logic is implemented as approved in the Analysis Plan.

---

### Output Files (per CMS component)

```text
Packages/Cms/CmsComponents/<ComponentName>/
├── <ComponentName>.tsx           # rendering entry (default export)
├── <ComponentName>Types.ts       # Sitecore field contract
├── <ComponentName>Mapper.ts      # fields → props (optional if trivial)
└── index.ts
```

### Learnings Namespace

Load only the `# LOGIC LEARNINGS` namespace (Sitecore wiring is part of logic).

---

### Gate: Complete When

```text
- [ ] All files WRITTEN TO DISK at exact paths (not just described).
- [ ] Typed Sitecore field contract defined for the rendering.
- [ ] Layout Service fields mapped to presentational props via Sitecore helpers.
- [ ] Rendering entry is default-exported and registered in the component registry.
- [ ] Folder name is PascalCase and matches the Sitecore rendering name exactly.
- [ ] Registry build commands noted for the summary.
- [ ] Child placeholders wired with correct keys from the rendering definition.
- [ ] CMS labels kept separate from API/runtime values.
- [ ] Preview/Experience Editor rendering safe for null/unauthored fields.
- [ ] Page composition wired: entry → container → view → display.
- [ ] Catch-all route used unless a dedicated route is genuinely justified.
- [ ] Barrel updated.
```

### Never Do

- **Never produce only a summary — write the source files.**
- Never hardcode CMS copy in the component — read it from Sitecore fields.
- Never use CMS copy as a fallback prop value.
- Never give the rendering entry a named-only export (registry needs default).
- Never place BFF data fetching inside the rendering entry.
- Never source a business value from a CMS field.
- Never invent placeholder keys or Sitecore fields not in the contract.
- Never use kebab-case for a CMS component folder.
- Never create a dedicated route just to add a Sitecore-authored page.
- Never place business logic, feature components, or design-system primitives inside `pages/`.
- Never shadow a real Sitecore path with a dedicated Next.js route.
- Never place an Error Boundary on `pages/[[...path]].tsx`.
- Never make inner data-driven blocks separate Sitecore renderings unless explicitly required.
- Never create Storybook `.stories` files or test files.
- Never run lint, type-check, or test commands.
