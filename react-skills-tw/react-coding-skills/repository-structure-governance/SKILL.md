---
name: repository-structure-governance
description: Use to determine and validate every target file path before writing code — file placement, PascalCase folders, naming conventions, export style, barrel updates, casing pre-checks, and package-boundary rules for the Sitecore-headless Next.js monorepo. Triggers include file placement, folder structure, naming conventions, barrel exports, where does this file go, or import path validation.
disable-model-invocation: true
---

## Repository Structure Governance

### Purpose

Decide **where** each generated file lives and validate it **before** any code is written. This skill embeds the project's file/folder structure and naming rules directly (no external guideline lookup required).

### Ownership Resolution (Do This First for Every File)

Assign each component/file one owner, then place it accordingly:

<table>
<tr><th>Owner Marker</th><th>What it is</th><th>Location</th></tr>
<tr><td>[design-system]</td><td>Reusable, business-neutral UI (atoms/molecules/organisms)</td><td>Packages/DesignSystem/Foundation/Src/{Atoms,Molecules,Organisms}/</td></tr>
<tr><td>[cms]</td><td>Sitecore-mapped rendering component</td><td>Packages/Cms/CmsComponents/&lt;ComponentName&gt;/</td></tr>
<tr><td>[feature]</td><td>Domain-specific feature component/logic</td><td>Portals/Sme/Features/&lt;DomainName&gt;/&lt;FeatureName&gt;/</td></tr>
<tr><td>[shared]</td><td>Cross-domain shared (used by 2+ features)</td><td>Portals/Sme/Features/Shared/&lt;ComponentName&gt;/</td></tr>
</table>

Feature/component sub-folders: `Components/`, `Hooks/`, `Services/`, `Types/`, `Constants/`, plus a barrel `index.ts`.

### Folder Casing (Resolved Conflict 1 — PascalCase)

**All feature and component directories are PascalCase.** This is the single authoritative rule; ignore any older kebab-case references.

```text
✅ Portals/Sme/Features/Motor/ProductOverview/
✅ Packages/Cms/CmsComponents/HeroBanner/
❌ portals/sme/features/motor/product-overview/
```

### Naming Conventions

<table>
<tr><th>File type</th><th>Convention</th><th>Example</th></tr>
<tr><td>Component (.tsx)</td><td>PascalCase</td><td>HeroCarousel.tsx</td></tr>
<tr><td>Hook (.ts)</td><td>camelCase, starts with use</td><td>useMotorQuote.ts</td></tr>
<tr><td>Service (.ts)</td><td>PascalCase, ends with Service</td><td>MotorQuoteService.ts</td></tr>
<tr><td>Type (.ts)</td><td>PascalCase, ends with Types</td><td>MotorQuoteTypes.ts</td></tr>
<tr><td>Mapper (.ts)</td><td>PascalCase, ends with Mapper</td><td>MotorQuoteMapper.ts</td></tr>
<tr><td>Constants (.ts)</td><td>SCREAMING_SNAKE_CASE, ends with _CONSTANTS</td><td>MOTOR_QUOTE_CONSTANTS.ts</td></tr>
<tr><td>Story (.tsx)</td><td>same as source + .stories</td><td>HeroCarousel.stories.tsx</td></tr>
<tr><td>Test</td><td>same as source + .test.tsx / .test.ts</td><td>HeroCarousel.test.tsx</td></tr>
</table>

Symbol naming: components PascalCase; props interfaces end with `Props`; view-model interfaces end with `ViewModel`; enums PascalCase; constants SCREAMING_SNAKE_CASE; boolean props read as predicates (`isLoading`, `hasError`).

### Export Style

- **Design System + shared reusable UI** → **named exports** re-exported from the nearest barrel.
- **CMS-mapped rendering components** → **default export** (required for the Sitecore component registry) plus a named export of props types.
- **Hooks / services / mappers / types** → named exports.

### Barrel Rules

- Update the **nearest** `index.ts` with an explicit named re-export for every new public symbol.
- Never use `export *` for CMS registry components — the registry needs explicit default bindings.
- Do not remove or reorder unrelated existing exports.

### Casing Pre-Check (Fail-Closed, Before Writing)

Case-insensitive filesystems silently collide (`HeroBanner.tsx` vs `herobanner.tsx`). Before creating any file:

1. Check whether a file with the same case-insensitive path already exists.
2. If it exists → **reuse the existing casing** and treat this as a file-update, not a new file.
3. If a semantically-equivalent component exists under a different name → route to reuse (do not duplicate).

Optional deterministic helper:

```bash
# validate-target-paths.sh — pass all planned paths as args
# fails if: duplicate casing, forbidden root, unknown owner folder, or missing barrel target
bash scripts/validate-target-paths.sh "Packages/DesignSystem/Foundation/Src/Organisms/HeroCarousel/HeroCarousel.tsx"
```

### Forbidden Roots (Block on Sight)

- ❌ Do not create a new `src` or `Src` root at repository level.
- ❌ Do not create a duplicate `.storybook` root.
- ❌ Do not create a new `.SS_WF` folder.
- ❌ Do not place `component-catalogue.json` anywhere other than the repository root (Resolved Conflict 2).

### Package Boundaries

- No direct feature-to-feature imports. Shared code goes to `Portals/Sme/Features/Shared/` or the Design System.
- CMS components may import Design System components, not the reverse.
- Design System components must not import feature, CMS, or API code.

### Gate: Complete When

```text
- [ ] Every planned file has a resolved owner marker and target path.
- [ ] PascalCase folder rule applied; no forbidden roots.
- [ ] Casing pre-check passed; existing casing reused where applicable.
- [ ] Naming conventions applied to all file types.
- [ ] Barrel update targets identified for every new public symbol.
- [ ] No cross-feature or reverse-dependency imports introduced.
```

### Never Do

- Never invent a new top-level folder outside the four owner locations.
- Never place a business/feature component in the Design System.
- Never give a CMS rendering component a named-only export (registry needs default).
- Never duplicate a component that already exists under different casing.
