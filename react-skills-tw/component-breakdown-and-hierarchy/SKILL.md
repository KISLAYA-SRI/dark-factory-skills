---
name: component-breakdown-and-hierarchy
description: Use this skill to produce the component hierarchy, responsibility matrix, ownership markers, and finalised prop model. Applies Presentational, Transactional, or Hybrid breakdown rules. Triggers include component breakdown, component hierarchy, folder structure, component responsibility matrix, atomic design breakdown, or file placement.
---

## Component Breakdown and Hierarchy

### Purpose

This skill produces the **component hierarchy, responsibility matrix, file placement decisions, and the finalised prop model**.

### Priority Order (Non-Negotiable at Every Decision Point)

```text
Dev Notes  →  Project Guidelines  →  Figma  →  React / Frontend Best Practices
```

⚠️ **Dev Notes are SACRED LAW.** Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").

---

### ⚠️ ANALYSIS DEPTH vs OUTPUT WIDTH — READ FIRST

**Perform every step in full.** Placement reasoning, naming conventions, folder boundaries and export patterns are all still applied — you need them to derive correct file names for the Code Generation Plan. What changed is that the **reference tables themselves are no longer emitted**, because they are embedded in the Coding Agent's `repository-structure-governance` skill.

| Work Performed (always, in full)                           | Emitted To                                 |
| ---------------------------------------------------------- | ------------------------------------------ |
| Apply breakdown rules (P1–P8 / T1–T8)                      | Internal                                   |
| Build component hierarchy tree                             | **§5**                                     |
| Determine container vs view vs display vs DS per component | **§6 — the `Type` column**                 |
| Define responsibility + must-not-own per component         | **§6**                                     |
| Run the placement decision tree                            | **§7 — ownership marker only**             |
| Apply naming conventions to derive concrete filenames      | **§8 — Files to Create / Files to Update** |
| Apply folder boundaries + export patterns                  | Internal — validates placement             |
| Finalise every prop's `Source` and `Source Detail`         | **§12**                                    |

⚠️ **Never emit:** a folder-structure tree diagram, a naming-conventions table, a folder-boundaries table, an export-patterns table, or a standalone Container/View Decision section. All four reference tables live in the Coding Agent's skill; the container/view decision lives in §6's `Type` column.

---

### Step 1 — Apply the Correct Breakdown Logic

Based on the classification from Phase 3, apply the matching rules.

**Presentational Scope Note** — additionally:

- Skip the responsibility row for any component that is a pure design-system passthrough with no logic or state.
- Only document components with meaningful rendering responsibility.
- Do NOT create a container — Presentational components have no API, state, or persona dependency.
- A Presentational component MAY own local visual state (carousel index, hover, expanded, paused). This does **not** justify a container.

#### Presentational Breakdown Rules

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

#### Transactional Breakdown Rules

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

#### Component Types and Their Responsibilities

| Component Type                 | Responsibility                                  | Presentational | Transactional                             |
| ------------------------------ | ----------------------------------------------- | -------------- | ----------------------------------------- |
| Sitecore-mapped component      | Entry point mapped from Sitecore rendering      | Yes            | Yes                                       |
| Feature controller / container | Data loading, mapping, persona, state decisions | **No**         | Yes, when data/logic exists               |
| View / layout component        | Arranges prepared child components              | Optional       | Recommended for complex data-driven areas |
| Feature display component      | Business/page-specific visible block            | Yes            | Yes                                       |
| Design-system component        | Reusable visual pattern                         | Yes            | Yes                                       |
| Atom / molecule                | Primitive UI building block                     | Yes            | Yes                                       |

---

### Step 2 — Build the Component Hierarchy → §5

#### Hierarchy Rules

- Use approved markers:
  - `[design-system]` — reusable design-system atom/molecule/organism
  - `[feature]` — feature display component
  - `[Sitecore-mapped]` — entry point mapped from Sitecore rendering
  - `[container]` — data-loading / state-managing controller
  - `[view]` — layout-only composition component
- Do **NOT** include file paths inside the hierarchy diagram.
- Separate containers from display components.
- Do not create a component for every icon, label, or text row — use design-system atoms.
- Do not create a container for a purely presentational section.

#### Hierarchy Output Format

```text
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

⚠️ Adapt the tree to the actual structure derived from the story and the Phase 5 design analysis. A Presentational story will typically have **no** `[container]` or `[view]` nodes.

---

### Step 3 — Component Responsibility Matrix → §6

For every component in the hierarchy, determine its type, what it owns, and what it must not own.

#### Output Columns (Exactly These Four)

| Component        | Type                                                                   | Owns                         | Must NOT Own                 |
| ---------------- | ---------------------------------------------------------------------- | ---------------------------- | ---------------------------- |
| [component name] | [Sitecore-mapped / Container / View / Feature Display / Design System] | [what it is responsible for] | [what it must never contain] |

⚠️ **The `Type` column carries the container/view decision.** The former standalone "Container / View Decision" section was eliminated — a component typed `Container` _is_ the container decision, and a Presentational story simply has no rows typed `Container` or `View`.

#### Logic-Allowed Reasoning (Internal — Determines `Type`)

Apply this internally to assign the correct `Type`; do not emit it as its own column.

| Value     | Meaning                                                               | Implies Type                                                  |
| --------- | --------------------------------------------------------------------- | ------------------------------------------------------------- |
| Rendering | Receives props and renders UI — no state, no API                      | Feature Display / Design System                               |
| State     | Manages local UI state (open/closed, selected tab, slide index)       | Feature Display (Presentational) or Container (Transactional) |
| API       | Triggers data fetching via hook/service — does NOT render detailed UI | Container                                                     |
| Layout    | Composes and arranges child components — no business logic, no API    | View                                                          |

#### Responsibility Matrix Rules

- Every component must have exactly one primary responsibility.
- Containers own: data loading, mapping, persona/session decisions, state.
- Views own: layout-only composition of prepared child components.
- Feature display components own: rendering a named business section from received props.
- Design-system components own: reusable visual pattern — no business/persona logic.
- No component may own both API calls AND detailed UI rendering — split into container + display.

#### Emission Discipline

Record only **story-specific** responsibilities. Do **not** write generic rows that restate rules the Coding Agent already enforces:

```text
❌ "Design-system components must not contain API calls"
❌ "Feature components must not contain business logic"
❌ "Containers must not render detailed UI"
```

Write instead what is specific to _this_ story — e.g. "Must NOT own slide autoplay timing (owned by parent carousel)".

---

### Step 4 — File Placement → §7 (Ownership Markers Only)

Run the full placement decision tree internally, then emit **only the ownership marker** for each component.

#### Placement Decision Tree (Internal)

```text
What kind of thing am I placing?
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

⚠️ **DON'T CREATE** a folder directly under `Features/` without a domain subfolder.
Example — DON'T: `Features/PolicyList` · DO: `Features/Motor/PolicyList`

#### Naming Conventions (Internal — Used to Derive §8 Filenames)

Apply these to produce the concrete file names that go into **§8 — Files to Create**. Do not emit this table.

| File Type              | Convention                                   | Example                |
| ---------------------- | -------------------------------------------- | ---------------------- |
| Component files (.tsx) | PascalCase                                   | `PolicyListClient.tsx` |
| Hook files (.ts)       | camelCase, starts with `use`                 | `usePolicyList.ts`     |
| Service files (.ts)    | PascalCase, ends with `Service`              | `PolicyListService.ts` |
| Type files (.ts)       | PascalCase, ends with `Types`                | `PolicyTypes.ts`       |
| Constants files (.ts)  | SCREAMING_SNAKE_CASE, ends with `_CONSTANTS` | `POLICY_CONSTANTS.ts`  |
| Test files             | Same as source + `.test.tsx` / `.test.ts`    | `Button.test.tsx`      |
| Barrel exports         | `index.ts` (lowercase)                       | `index.ts`             |

#### Folder Boundaries (Internal — Validates Placement)

| Folder                                    | Owns                                                                | Must NOT Contain                                        |
| ----------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| `Packages/DesignSystem/Foundation`        | Reusable, presentation-only atoms/molecules/organisms               | API calls, session/persona logic, business rules        |
| `Packages/Cms/CmsComponents`              | Sitecore-mapped presentational components                           | Feature-specific business logic, API/session-aware code |
| `Portals/Sme/Features/<Domain>/<Feature>` | One business feature: components, hooks, services, types, constants | Code belonging to another feature (use `Shared/`)       |
| `Portals/Sme/Features/Shared`             | Cross-feature components used by more than one feature              | Feature-specific business logic                         |

#### Export Patterns (Internal — Validates Placement)

| Path                               | Export Pattern                              |
| ---------------------------------- | ------------------------------------------- |
| `Packages/DesignSystem/Foundation` | **Named export** (`export function Button`) |
| `Packages/Cms/CmsComponents`       | **Default export** (required by registry)   |
| `Portals/Sme/Features`             | **Named export**                            |

- ❌ **Never** use `export *` in barrel files — always named re-exports.
- ✅ Every feature and design-system subfolder must have an `index.ts`.

#### Output → §7

| Component / File | Ownership Marker                                       |
| ---------------- | ------------------------------------------------------ |
| [ComponentName]  | `[design-system]` / `[cms]` / `[feature]` / `[shared]` |

⚠️ **Emit markers only.** The Coding Agent's `repository-structure-governance` skill resolves the full path, PascalCase folder casing, file naming, export style and barrel target from the marker alone.

#### Handoff to §8

The concrete file list — with paths and purposes — belongs in **§8 Files to Create / Files to Update**, produced using the naming conventions above. This is where the Coding Agent reads actual filenames.

---

### Step 5 — Finalise the Prop Model → §12

With Phase 5 and Phase 6 enrichment complete, §12 is now **final**.

For every prop in the model, confirm:

```text
✅ Source is one of: Sitecore | BFF API | FE Derived | Unknown
✅ Source Detail is resolved — the exact Sitecore field name, or endpoint + field path
✅ FE Derived props state their computation
✅ Any prop with no contract source reads:
     "Unknown — source contract not provided"
   AND has a matching gap recorded in DEV_REVIEW.md §5
```

⚠️ **No `To be resolved` placeholder may remain.** That marker was Phase 3's signal for later enrichment. If one survives to here, either resolve it from the Phase 5/6 outputs or convert it to `Unknown — source contract not provided` with a linked gap. The output contract's prohibition check will reject any that remain.

---

### Guardrails

#### Always Do

- Check the active Dev Notes list before every decision; label items with their DN ID.
- Apply the priority order at every decision point.
- **Apply every placement, naming, boundary and export rule in full** — they determine §7 and §8 correctness.
- Use the classification from Phase 3 and the design detail from Phase 5.
- Keep Sitecore-mapped components coarse-grained.
- Use containers only where there is API, state, persona, mapping, or business logic.
- Reuse design-system components wherever possible.
- Keep labels (Sitecore) and values (API/FE) separate.
- **Finalise §12 — every prop resolved or explicitly gapped.**
- Record every uncertain placement decision in DEV_REVIEW.md §1.

#### Never Do

- Never include file paths inside the component hierarchy diagram.
- Never create a component for every field, icon, or text row.
- Never create a container for a purely presentational component.
- Never put API calls inside feature display components.
- Never put business/persona logic inside design-system components.
- Never hardcode labels that should come from Sitecore/localisation.
- Never create a folder directly under `Features/` without a domain subfolder.
- Never use `export *` in barrel files.
- Never use kebab-case for a CMS component folder.
- **Never emit a folder-structure tree into ANALYSIS_PLAN.md.**
- **Never emit the naming-conventions, folder-boundaries, or export-patterns tables.**
- **Never emit a standalone Container / View Decision section** — it is the §6 `Type` column.
- **Never emit generic responsibility rows** that restate rules the coding skills enforce.
- **Never leave a `To be resolved` placeholder in §12.**
- Never override a Dev Note.
- Never generate implementation code.

---

### Gate: Phase 7 Complete When

**Analysis completeness:**

- [ ] Correct breakdown rules applied (P1–P8 / T1–T8 / both)
- [ ] Every component assigned a type via internal logic-allowed reasoning
- [ ] Placement decision tree run for every component
- [ ] Naming conventions applied to derive concrete filenames
- [ ] Folder boundaries validated — no cross-feature placement
- [ ] Export pattern validated per path (named vs default)
- [ ] No folder created directly under `Features/` without a domain subfolder

**Emission discipline:**

- [ ] §5 hierarchy tree produced with approved markers, no file paths
- [ ] Containers separated from display components (or absent for Presentational)
- [ ] §6 matrix uses exactly: Component │ Type │ Owns │ Must NOT Own
- [ ] §6 contains only story-specific responsibilities
- [ ] §7 emits ownership markers only — no folder tree
- [ ] Concrete filenames handed to §8
- [ ] No naming-convention, folder-boundary, or export-pattern table emitted
- [ ] No standalone Container/View section produced
- [ ] **§12 finalised — every prop has a resolved Source and Source Detail, or is explicitly `Unknown` with a linked gap**
- [ ] **No `To be resolved` placeholder remains**
- [ ] Every Dev Note applied and labelled with its DN ID
