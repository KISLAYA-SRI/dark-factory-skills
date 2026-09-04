---
name: component-breakdown-and-hierarchy
description: Use when producing the complete component hierarchy, responsibility matrix, and folder/file structure for a frontend user story. Applies Presentational, Transactional, or Hybrid breakdown rules, builds the hierarchy tree, defines component responsibilities, and proposes folder/file structure with naming conventions. Triggers include component breakdown, component hierarchy, folder structure, component responsibility matrix, atomic design breakdown, or Presentational Transactional Hybrid classification.
---

# Component Breakdown and Hierarchy

## Purpose

This skill produces the **complete component hierarchy and folder structure** for a frontend user story. It is invoked as Phase 5 of the master analysis orchestrator and must complete before Phase 6 (Component Reuse Validation) begins.

This skill covers:

1. Applying the correct breakdown logic based on the classification from Phase 3.
2. Building the component hierarchy tree.
3. Defining the component responsibility matrix.
4. Proposing the folder/file structure with correct naming conventions.

> ⚠️ **Prerequisite**: Phase 3 (Story Analysis End to End) MUST be complete. The component classification (Presentational / Transactional / Hybrid) produced in Phase 3 is the mandatory input to this skill.

---

## Priority Order (Non-Negotiable at Every Decision Point)

```
Dev Notes  →  Project Guidelines  →  Figma  →  React / Frontend Best Practices
```

When two sources conflict, the higher-priority source wins. The conflict and resolution MUST be recorded in DEV_REVIEW.md.

> ⚠️ **Dev Notes are SACRED LAW.** If a Dev Note covers a topic, it IS the answer. Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").

---

## Step 1 — Apply the Correct Breakdown Logic

Based on the classification from Phase 3, apply the matching breakdown rules below.

- If **Presentational** → apply Presentational Breakdown Rules (P1–P8).
- If **Transactional** → apply Transactional Breakdown Rules (T1–T8).
- If **Hybrid** → apply both sets of rules to the appropriate sections.

### Presentational Breakdown Rules

| Rule | Question                                                       | Decision                                                      |
| ---- | -------------------------------------------------------------- | ------------------------------------------------------------- |
| P1   | Is this component placed by Sitecore as a rendering?           | Create one Sitecore-mapped component                          |
| P2   | What fields are authored in Sitecore?                          | Define props/content model around authored fields             |
| P3   | Does the component have visual variants?                       | Use variant-driven rendering inside the same component        |
| P4   | Does it contain repeatable authored content?                   | Create list/item subcomponents where useful                   |
| P5   | Is a child block reusable outside this component?              | Use/create a design-system or shared presentational component |
| P6   | Is the child block only for readability within this component? | Keep as internal subcomponent                                 |
| P7   | Is it only text, icon, image, link, button or spacing?         | Use design-system atom/molecule                               |
| P8   | Is there no API, state, persona or session dependency?         | Do not create a container                                     |

### Transactional Breakdown Rules

| Rule | Question                                                               | Decision                                                              |
| ---- | ---------------------------------------------------------------------- | --------------------------------------------------------------------- |
| T1   | Is this the main rendering received from Sitecore Layout API?          | Create one Sitecore-mapped feature component                          |
| T2   | Which regions are visible business sections?                           | Create feature display components                                     |
| T3   | Which region loads API data or reads session/persona?                  | Create a container/controller                                         |
| T4   | Which region only arranges prepared child components?                  | Create a view/layout component                                        |
| T5   | Does a block represent a named business concept?                       | Create a feature display component                                    |
| T6   | Is the UI structure generic and reusable?                              | Use/create a design-system component                                  |
| T7   | Is it only a field, icon, label, text, button, row or spacing wrapper? | Do not create a feature component; use design-system atoms/molecules  |
| T8   | Is a child block independently authorable in Sitecore?                 | Consider separate Sitecore rendering only if genuinely CMS-composable |

### Component Types and Their Responsibilities

| Component Type                 | Responsibility                                  | Presentational Usage | Transactional Usage                       |
| ------------------------------ | ----------------------------------------------- | -------------------- | ----------------------------------------- |
| Sitecore-mapped component      | Entry point mapped from Sitecore rendering      | Yes                  | Yes                                       |
| Feature controller / container | Data loading, mapping, persona, state decisions | Usually no           | Yes, when data/logic exists               |
| View / layout component        | Arranges prepared child components              | Optional             | Recommended for complex data-driven areas |
| Feature display component      | Business/page-specific visible block            | Yes                  | Yes                                       |
| Design-system component        | Reusable visual pattern                         | Yes                  | Yes                                       |
| Atom / molecule                | Primitive UI building block                     | Yes                  | Yes                                       |

---

## Step 2 — Build the Component Hierarchy

Produce a clean tree diagram of the component hierarchy.

### Hierarchy Rules

- Use approved markers to label each component:
  - `[design-system]` — reusable design-system atom/molecule/organism
  - `[feature]` — feature display component
  - `[Sitecore-mapped]` — entry point mapped from Sitecore rendering
  - `[container]` — data-loading / state-managing controller
  - `[view]` — layout-only composition component
- Do **NOT** include file paths inside the hierarchy diagram.
- Separate containers from display components.
- Do not create a component for every icon, label, or text row — use design-system atoms.
- Do not create a container for a purely presentational section.

### Hierarchy Output Format

```
<RootComponentName> [Sitecore-mapped]
├── <ContainerName> [container]                  ← data loading, state, persona
│   └── <ViewName> [view]                        ← layout-only composition
│       ├── <SectionAName> [feature]             ← named business section
│       │   ├── <AtomName> [design-system]       ← reused atom
│       │   └── <MoleculeOrOrganismName> [design-system]
│       └── <SectionBName> [feature]
│           └── <AtomName> [design-system]
└── <PresentationalSectionName> [feature]        ← no API, no state
    └── <AtomName> [design-system]
```

> ⚠️ Adapt the tree to the actual component structure derived from the story and Figma. The format above is illustrative.

---

## Step 3 — Component Responsibility Matrix

For every component in the hierarchy, define:

| Component        | Responsibility (What It Owns)            | Logic Allowed                    | Must NOT Own                             |
| ---------------- | ---------------------------------------- | -------------------------------- | ---------------------------------------- |
| [component name] | [what this component is responsible for] | Rendering / State / API / Layout | [what this component must never contain] |

### Logic Allowed Values

| Value     | Meaning                                                               |
| --------- | --------------------------------------------------------------------- |
| Rendering | Receives props and renders UI — no state, no API                      |
| State     | Manages local UI state (open/closed, selected tab, etc.)              |
| API       | Triggers data fetching via hook/service — does NOT render detailed UI |
| Layout    | Composes and arranges child components — no business logic, no API    |

### Responsibility Matrix Rules

- Every component must have exactly one primary responsibility.
- Containers own: data loading, mapping, persona/session decisions, state.
- Views own: layout-only composition of prepared child components.
- Feature display components own: rendering a named business section from received props.
- Design-system components own: reusable visual pattern — no business/persona logic.
- No component may own both API calls AND detailed UI rendering — split into container + display.

---

## Step 4 — Folder Structure Proposal

Propose the folder/file structure for every component in the hierarchy.

### Placement Decision Tree

```text
What kind of thing am I placing?
│
├── Reusable UI element — no API calls, no session/persona logic, no domain rules?
│   └── → Packages/DesignSystem/Foundation/Src/{Atoms,Molecules,Organisms}/
│         └── <ComponentName>.tsx   (PascalCase, no subfolder)
│         ⚠ Always check here FIRST. If a suitable element already exists, import it.
│           Never recreate a DesignSystem element inside a feature or CMS folder.
│
├── Sitecore-authored presentational component (CMS-mapped)?
│   └── → Packages/Cms/CmsComponents/<ComponentName>/
│         └── <ComponentName>.tsx   (PascalCase — folder name = Sitecore rendering name)
│         ⚠ Folder name becomes the registry key — must be PascalCase, case-sensitive.
│
└── Domain-specific business feature (may call APIs, hold state, contain domain rules)?
    └── → Portals/Sme/Features/
        │
        ├── Specific to ONE domain (Motor, Health)?
        │   └── Features/<DomainName>/<FeatureName>/
        │       ├── Components/<ComponentName>.tsx
        │       ├── Hooks/use<Name>.ts
        │       ├── Services/<Name>Service.ts
        │       ├── Types/<Name>Types.ts
        │       ├── Constants/<NAME>_CONSTANTS.ts
        │       └── index.ts
        │
        └── Used across 2+ domains?
            └── Features/Shared/<ComponentName>/
                ├── Components/<ComponentName>.tsx
                └── index.ts
```

> ⚠️ **DON'T CREATE** a folder directly under `SME/FEATURES` without a domain subfolder.
> Example — DON'T: `SME/FEATURES/PolicyList` | DO: `SME/FEATURES/Motor/PolicyList`

### Naming Conventions

| File Type                | Convention                                   | Example                |
| ------------------------ | -------------------------------------------- | ---------------------- |
| Component files (`.tsx`) | PascalCase                                   | `PolicyListClient.tsx` |
| Hook files (`.ts`)       | camelCase, starts with `use`                 | `usePolicyList.ts`     |
| Service files (`.ts`)    | PascalCase, ends with `Service`              | `PolicyListService.ts` |
| Type files (`.ts`)       | PascalCase, ends with `Types`                | `PolicyTypes.ts`       |
| Constants files (`.ts`)  | SCREAMING_SNAKE_CASE, ends with `_CONSTANTS` | `POLICY_CONSTANTS.ts`  |
| Test files               | Same as source + `.test.tsx` / `.test.ts`    | `Button.test.tsx`      |
| Barrel exports           | `index.ts` (lowercase)                       | `index.ts`             |

### Folder Boundaries

| Folder                                | Owns                                                                | Must NOT Contain                                          |
| ------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------- |
| `Packages/DesignSystem/Foundation`    | Reusable, presentation-only atoms/molecules/organisms               | API calls, session/persona logic, business rules          |
| `Packages/Cms/CmsComponents`          | Sitecore-mapped presentational components                           | Feature-specific business logic, API/session-aware code   |
| `Portals/Sme/Features/<feature-name>` | One business feature: components, hooks, services, types, constants | Code belonging to another feature (use `Shared/` instead) |
| `Portals/Sme/Features/Shared`         | Cross-feature components used by more than one feature              | Feature-specific business logic                           |

### Export Patterns

| Path                               | Export Pattern                                                            |
| ---------------------------------- | ------------------------------------------------------------------------- |
| `Packages/DesignSystem/Foundation` | **Named export** (`export function Button`)                               |
| `Packages/Cms/CmsComponents`       | **Default export** (required by registry: `export default ComponentName`) |
| `Portals/Sme/Features`             | **Named export** (`export function PolicyListClient`)                     |

- ❌ **Never** use `export *` in barrel files — always use named re-exports.
- ✅ Every feature and design-system subfolder must have an `index.ts`.

### Folder Structure Output Format

```
Packages/
  DesignSystem/
    Foundation/
      Src/
        Atoms/
          <AtomName>.tsx
        Molecules/
          <MoleculeName>.tsx
        Organisms/
          <OrganismName>.tsx
  Cms/
    CmsComponents/
      <CmsComponentName>/
        <CmsComponentName>.tsx

Portals/
  Sme/
    Features/
      <DomainName>/
        <FeatureName>/
          Components/
            <ComponentName>.tsx
          Hooks/
            use<Name>.ts
          Services/
            <Name>Service.ts
          Types/
            <Name>Types.ts
          Constants/
            <NAME>_CONSTANTS.ts
          index.ts
```

> ⚠️ Adapt the structure to the actual components identified. Only include sub-folders that are needed for this story.

---

## Guardrails

### Always Do

- Check active Dev Notes list before every decision. If a Dev Note covers the topic, it IS the answer.
- Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").
- Apply the priority order at every decision point: Dev Notes → Guidelines → Figma → Best Practices.
- Classify the component before proposing hierarchy — use the classification from Phase 3.
- Keep Sitecore-mapped components coarse-grained.
- Use containers only where there is API, state, persona, mapping, or business logic.
- Use views for layout-only composition when useful.
- Use feature display components for meaningful visible business blocks.
- Reuse design-system components wherever possible — check before creating new ones.
- Keep labels (Sitecore) and values (API/FE) separate.
- Keep persona/business rules out of design-system components.
- Separate containers from display components in the hierarchy diagram.
- Propose folder structure with correct naming conventions for every component.
- Mark every derived recommendation clearly: `Derived from project frontend best practices.`
- Record every uncertain decision in DEV_REVIEW.md — never in ANALYSIS_PLAN.md.

### Never Do

- Never include file paths inside the component hierarchy diagram.
- Never create a component for every field, icon, or text row — use design-system atoms.
- Never create a container for a purely presentational component.
- Never put API calls inside feature display components.
- Never put business/persona logic inside design-system components.
- Never create separate Sitecore renderings for internal data-driven blocks unless explicitly required.
- Never hardcode labels that should come from Sitecore/localisation.
- Never generate update/edit flows if they are out of story scope.
- Never create a folder directly under `SME/FEATURES` without a domain subfolder.
- Never use `export *` in barrel files.
- Never use kebab-case for a CMS component folder — it produces a wrong registry key.
- Never override a Dev Note — not even as a "suggestion" or "recommendation".
- Never generate implementation code — that is the Coding Agent's job.

---

## Output Checklist (Self-Verify Before Proceeding to Phase 6)

Before passing output to Phase 6 (Component Reuse Validation), verify:

- [ ] Correct breakdown rules applied based on classification (Presentational / Transactional / Hybrid)
- [ ] Component hierarchy tree produced — uses approved markers only
- [ ] No file paths inside the hierarchy diagram
- [ ] Containers separated from display components in the hierarchy
- [ ] No container created for a purely presentational section
- [ ] Component responsibility matrix completed for every component in the hierarchy
- [ ] Every component has a defined responsibility, allowed logic, and what it must NOT own
- [ ] Folder/file structure proposed for every component
- [ ] Naming conventions applied correctly for all file types
- [ ] No folder created directly under `SME/FEATURES` without a domain subfolder
- [ ] Export patterns applied correctly (named for DS/features, default for CMS)
- [ ] Every Dev Note applied and labelled with DN ID
- [ ] Every uncertain decision recorded in DEV_REVIEW.md, not in ANALYSIS_PLAN.md
