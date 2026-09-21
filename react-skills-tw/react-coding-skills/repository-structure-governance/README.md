# Repository Structure Governance

Determines and validates every target file path before code is written — ownership resolution, PascalCase folders, naming conventions, export style, barrel updates, casing pre-checks, and package-boundary rules for the Sitecore-headless Next.js monorepo.

## Use This For

- Resolving where each generated file belongs (design-system, CMS, feature, shared).
- Enforcing PascalCase directories and project naming conventions.
- Preventing case-insensitive filesystem collisions before writing.
- Applying correct export style and barrel updates.
- Blocking forbidden roots and cross-feature imports.

## Expected Flow

```text
For each planned file:
  → Resolve owner marker ([design-system] | [cms] | [feature] | [shared])
  → Map to target location + PascalCase folder
  → Apply naming convention for the file type
  → Run case-insensitive duplicate pre-check (reuse existing casing)
  → Identify nearest barrel + export style
  → Validate package boundaries
```

## Key Rules

- All feature/component directories are PascalCase .
- component-catalogue.json lives only at the repository root .
- CMS rendering components use default exports (registry requirement); DS/shared UI uses named exports.
- Never create src, duplicate .storybook, or new .SS_WF roots.
- No feature-to-feature imports; Design System never imports feature/CMS/API code.

See [SKILL.md](./SKILL.md) for the full instructions.
