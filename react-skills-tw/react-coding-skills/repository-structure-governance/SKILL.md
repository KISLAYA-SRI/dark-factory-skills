---
name: repository-structure-governance
description: Use to determine and validate every target file path before writing code — file placement, PascalCase folders, naming conventions, export style, barrel updates, casing pre-checks, registry rules, and package-boundary rules for the Sitecore-headless Next.js monorepo. Embeds the project file and folder structure guideline in full. Triggers include file placement, folder structure, naming conventions, barrel exports, where does this file go, or import path validation.
disable-model-invocation: true
---

## Repository Structure Governance

### Purpose

Decide **where** each generated file lives and validate it **before** any code is written. This skill embeds the project's complete file/folder structure and naming rules — no external guideline lookup required.

### Core Principles

- **Naming signals intent.** Casing tells you what a thing is before you open it — PascalCase = component/type/service, camelCase = hook, SCREAMING_SNAKE_CASE = constants.
- **Location signals ownership.** Every file lives in exactly one place reflecting who owns it and why.
- **Structure is enforced, not optional.** Naming and placement are backed by ESLint and CI. Violations fail linting, not just review.
- **When in doubt, match the nearest existing example.**

---

## 1. Ownership Resolution (Do This First for Every File)

```text
What kind of thing am I creating?
│
├── Reusable UI element — no API calls, no session/persona logic, no domain rules?
│   └── → [design-system]
│         Packages/DesignSystem/Foundation/Src/{Atoms,Molecules,Organisms}/
│         ⚠ Always check here FIRST. If a suitable element exists, import it.
│           Never recreate a DesignSystem element inside a feature or CMS folder.
│
├── Sitecore-authored presentational component (CMS-mapped)?
│   └── → [cms]
│         Packages/Cms/CmsComponents/<ComponentName>/
│         ⚠ Folder name becomes the registry key — PascalCase, case-sensitive.
│
└── Domain-specific business feature (may call APIs, hold state, contain domain rules)?
    │
    ├── Specific to ONE domain (Motor, Health)?
    │   └── → [feature]
    │         Portals/Sme/Features/<DomainName>/<FeatureName>/
    │
    └── Used across 2+ domains?
        └── → [shared]
              Portals/Sme/Features/Shared/<ComponentName>/
```

| Owner Marker | What it is | Location |
| --- | --- | --- |
| `[design-system]` | Reusable, business-neutral UI | `Packages/DesignSystem/Foundation/Src/{Atoms,Molecules,Organisms}/` |
| `[cms]` | Sitecore-mapped rendering component | `Packages/Cms/CmsComponents/<ComponentName>/` |
| `[feature]` | Domain-specific feature component/logic | `Portals/Sme/Features/<DomainName>/<FeatureName>/` |
| `[shared]` | Cross-domain shared (2+ features) | `Portals/Sme/Features/Shared/<ComponentName>/` |

**Domains allowed for SME:** `Health`, `Motor`, `Shared`

⚠️ **DON'T CREATE** a folder for a feature directly under `Features/`.

```text
❌ Portals/Sme/Features/PolicyList/
✅ Portals/Sme/Features/Motor/PolicyList/
```

**Ownership rule of thumb:** reusable with zero API/session/persona logic → design-system. Sitecore-authored and presentational → cms-components. Business/portal-specific, may fetch data or hold state → portal features.

---

## 2. Folder Casing — PascalCase Everywhere

**All feature and component directories are PascalCase.** This is the single authoritative rule.

```text
✅ Portals/Sme/Features/Motor/ProductOverview/
✅ Packages/Cms/CmsComponents/HeroBanner/
✅ Packages/DesignSystem/Foundation/Src/Atoms/
❌ portals/sme/features/motor/product-overview/
❌ Packages/Cms/CmsComponents/hero-banner/
```

⚠️ A kebab-case CMS folder produces a **wrong registry key** and causes "Component not found" errors at runtime.

### Standard Feature Sub-Folders

```text
Portals/Sme/Features/<Domain>/<FeatureName>/
├── Components/     → PascalCase subfolder
├── Hooks/          → PascalCase subfolder
├── Services/       → PascalCase subfolder
├── Types/          → PascalCase subfolder
├── Constants/      → PascalCase subfolder
└── index.ts        → barrel export
```

⚠️ **Do not invent new subfolder names** (`helpers/`, `utils/`) — use the standard set.

---

## 3. File Naming Conventions

| File Type | Convention | Example |
| --- | --- | --- |
| Component (.tsx) | **PascalCase** | `PolicyListClient.tsx` |
| Hook (.ts) | **camelCase**, starts with `use` | `usePolicyList.ts` |
| Service (.ts) | **PascalCase**, ends with `Service` | `PolicyListService.ts` |
| Type (.ts) | **PascalCase**, ends with `Types` | `PolicyTypes.ts` |
| Mapper (.ts) | **PascalCase**, ends with `Mapper` | `PolicyMapper.ts` |
| Constants (.ts) | **SCREAMING_SNAKE_CASE**, ends with `_CONSTANTS` | `POLICY_CONSTANTS.ts` |
| Test | same as source + `.test.tsx` / `.test.ts` | `Button.test.tsx` |
| Story | same as source + `.stories.tsx` | `Button.stories.tsx` |
| Barrel | `index.ts` (lowercase) | `index.ts` |
| Config | lowercase-with-dots | `vitest.config.ts` |

⚠️ **Never** use `.spec.tsx` / `.spec.ts` — only `.test.*` is recognised by the test runner.

### Symbol Naming

| Symbol | Convention | Example |
| --- | --- | --- |
| Components | PascalCase | `Button` |
| Props interfaces | End with `Props` | `ButtonProps` |
| View-model interfaces | End with `ViewModel` | `PolicyViewModel` |
| Domain models | PascalCase, **no suffix** | `Policy` |
| Enums | PascalCase | `ThemeMode` |
| Enum members | UPPER_CASE | `LIGHT`, `DARK` |
| Local variables | camelCase | `userProfile` |
| Boolean variables | `is`/`has`/`can`/`should` prefix | `isLoading`, `hasError` |
| Exported constants (primitives) | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Local const bindings | camelCase | `fetchedData` |
| React component refs via const | PascalCase | `const Button = ...` |

⚠️ **Never prefix interfaces with `I`** — `ButtonProps`, not `IButtonProps`. Never create empty interfaces. Never use single-letter names except loop counters. Never use abbreviations unless universally understood (`url`, `id`, `api` are fine; `usrPrf` is not). Never export anonymous constants.

---

## 4. Export Style

| Path | Export Pattern |
| --- | --- |
| `Packages/DesignSystem/Foundation` | **Named export** (`export const Button = ...`) |
| `Packages/Cms/CmsComponents` | **Default export** (required by the registry) |
| `Portals/Sme/Features` | **Named export** |
| Hooks / services / mappers / types | **Named export** |

Design-system components must also set `Button.displayName = 'Button'`.

---

## 5. Barrel Rules

- Every feature and design-system subfolder must have an `index.ts` re-exporting its public API
- Update the **nearest** `index.ts` with an explicit named re-export for every new public symbol
- ❌ **Never use `export *`** — always named re-exports (breaks tree-shaking and hides the public API surface)
- Do not remove or reorder unrelated existing exports

```ts
// Portals/Sme/Features/Motor/PolicyList/index.ts
export { PolicyListClient } from "./Components/PolicyListClient";
export type { PolicyListClientProps } from "./Components/PolicyListClient";
export type { Policy, PolicyListParams, PolicyListResponse } from "./Types/PolicyTypes";
```

For presentational components with no API/backend dependency, add the main component to `Packages/Cms/CmsComponents/index.ts`.

---

## 6. Import / Export Path Rules

- Use **relative imports** when the path is only one level deep (`./`)
- For deeper relative paths (`../../`, `../../../`), **always use the `@` package name**
- Omit extensions for `.ts`/`.tsx`; always include for `.css`, `.json`, `.svg`
- Import order: built-ins → externals → `@dxp/*` → relatives (alphabetical within groups)

```ts
import path from "node:path";                          // built-in
import { useQuery } from "@tanstack/react-query";      // external
import { Button } from "@dxp/foundation";              // @dxp/*
import { usePolicyList } from "./Hooks/usePolicyList"; // relative
```

---

## 7. Casing Pre-Check (Fail-Closed, Before Writing)

Case-insensitive filesystems silently collide. Linux/CI filesystems are case-sensitive — creating `Components/` when `components/` exists produces two separate folders on CI, causing broken imports and build failures invisible on macOS.

**Before creating ANY file or folder:**

1. Perform a **case-insensitive existence check** at the target parent path
2. If a file/folder with the same name exists (any casing) → **use the existing name exactly**
3. Never create a parallel folder with different casing
4. **The existing filesystem casing wins** over the Analysis Plan casing
5. If a semantically-equivalent component exists under a different name → route to reuse, do not duplicate

---

## 8. Reference Implementation

`Portals/Sme/Features/.example/PolicyList/` is the **reference** for domain feature structure, including the full API interaction pattern.

```text
Portals/Sme/Features/.example/PolicyList/
├── Components/
│   └── PolicyListClient.tsx        ← PascalCase subfolder + PascalCase file
├── Hooks/
│   └── usePolicyList.ts            ← PascalCase subfolder + camelCase hook
├── Services/
│   └── PolicyListService.ts        ← PascalCase subfolder + PascalCase service
├── Types/
│   └── PolicyTypes.ts              ← PascalCase subfolder + PascalCase types
├── Constants/
│   └── POLICY_CONSTANTS.ts         ← PascalCase subfolder + SCREAMING_SNAKE_CASE
└── index.ts                        ← barrel export at feature root
```

**Copy this layering for any new data-fetching feature.** It is a pattern to copy, not production code to import from.

---

## 9. Folder Boundaries and Ownership

| Folder | Owns | Must NOT contain |
| --- | --- | --- |
| `pages/**` | Routing, API routes, `_app.tsx`, `_error.tsx` | Business logic, design-system primitives, feature components |
| `Packages/DesignSystem/Foundation` | Reusable presentation-only atoms/molecules/organisms | API calls, session/persona logic, business rules |
| `Packages/DesignSystem/Tokens` | Raw primitive + semantic design tokens | Components, logic |
| `Packages/DesignSystem/Themes` | Theme provider, mode switching, generated CSS | Business/feature logic |
| `Packages/Cms/CmsComponents` | Sitecore-mapped presentational components | Feature-specific business logic, API/session-aware code |
| `Packages/Cms/CmsUtils` | Layout orchestration, registry generation | UI components |
| `Packages/PlatformConfig` | Environment config, aggregated registry | Component source code |
| `Packages/Common` | Cross-portal shared utilities/providers | Portal-specific or CMS-specific logic |
| `Portals/Sme/Features/<Domain>/<Feature>` | One business feature: components, hooks, services, types, constants | Code belonging to another feature (use `Shared/`) |
| `Portals/Sme/Features/Shared` | Cross-feature components used by 2+ features | Feature-specific business logic |
| `Portals/Sme/Features/.example` | Reference/pattern implementations only | Production feature code |

### Package Boundaries

- ❌ No direct feature-to-feature imports — shared code goes to `Features/Shared/` or the Design System
- ✅ CMS components may import Design System components — **not the reverse**
- ❌ Design System components must not import feature, CMS, or API code

---

## 10. Forbidden Roots (Block on Sight)

```text
❌ Do NOT create a new `src` or `Src` root at repository level
     The existing Src folder is the code base — place all files inside it

❌ Do NOT create a duplicate `.storybook` root
     Storybook config folders already exist at:
       /.storybook/
       /Packages/DesignSystem/Foundation/.storybook/
       /Portals/Sme/.storybook/
       /Packages/Cms/CmsComponents/.storybook/

❌ Do NOT create a new `.SS_WF` folder
     It already exists at repository root — use the existing one

❌ Do NOT move, recreate, or duplicate `component-catalogue.json`
     It lives at ./src/component-catalogue.json ONLY
     Never at repository root, never inside .SS_WF/, never anywhere else
     To update it, edit the file in place
```

---

## 11. Component Registry Rules

### CMS Components

- Folder name = component name (**PascalCase**) = Sitecore rendering name (case-sensitive)
- File path: `<ComponentName>/<ComponentName>.tsx`
- Must use `export default ComponentName`
- After adding/renaming, run:
  ```bash
  pnpm run build:cms-component-registry   # Stage A — package-level
  pnpm run build:component-registry       # Stage B — app-level aggregator
  ```

### Portal Feature Components

- Feature folder: **PascalCase**
- Component files: **PascalCase**
- Must use named export: `export const ComponentName = ...`
- After adding/renaming, run `pnpm run build:component-registry`

### Design-System Components

- File name must match the component display name exactly (case-sensitive)
- Must use named export and set `displayName`
- Must be re-exported from the atomic barrel (`Atoms/index.ts`, etc.)

⚠️ **Never rename a CMS component folder without updating the Sitecore rendering name to match.** A mismatch causes a silent runtime fallback to the missing-component placeholder.

---

### Optional Deterministic Helper

```bash
# validate-target-paths.sh — pass all planned paths as args
# fails if: duplicate casing, forbidden root, unknown owner folder, or missing barrel target
bash scripts/validate-target-paths.sh "Packages/DesignSystem/Foundation/Src/Organisms/HeroCarousel/HeroCarousel.tsx"
```

---

### Gate: Complete When

```text
- [ ] Every planned file has a resolved owner marker and target path.
- [ ] PascalCase folder rule applied at every level; no kebab-case anywhere.
- [ ] No folder created directly under Features/ without a domain subfolder.
- [ ] Standard feature subfolders used (Components/Hooks/Services/Types/Constants).
- [ ] Casing pre-check passed; existing filesystem casing reused where applicable.
- [ ] Naming conventions applied to all file types and symbols.
- [ ] Export pattern correct per path (named vs default for CMS).
- [ ] Barrel update targets identified; named re-exports only, no export *.
- [ ] No forbidden roots created.
- [ ] component-catalogue.json path confirmed as ./src/component-catalogue.json.
- [ ] No cross-feature or reverse-dependency imports introduced.
- [ ] Registry build commands noted if a CMS or portal feature component was added/renamed.
```

### Never Do

- Never invent a new top-level folder outside the four owner locations.
- Never place a business/feature component in the Design System.
- Never place API calls or business logic inside `Packages/DesignSystem`.
- Never place feature-specific code inside `Features/Shared/`.
- Never give a CMS rendering component a named-only export.
- Never use kebab-case for any folder.
- Never use `export *` in barrel files.
- Never prefix interfaces with `I`.
- Never use `.spec.*` for test files.
- Never duplicate a component that already exists under different casing.
- Never move `component-catalogue.json` from `./src/`.
- Never skip barrel exports for new public symbols.
