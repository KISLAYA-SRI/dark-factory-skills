---
name: master-react-coding-orchestrator
description: Use when orchestrating the complete end-to-end FE Code Generation workflow that turns an approved ANALYSIS_PLAN.md into production React/Next.js code. Defines the mandatory phase sequence, decision gates, skill invocation map, Presentational vs Transactional execution paths, and the single consolidated summary document produced at the end. Triggers include code generation, coding agent, UI generation, logic generation, storybook generation, test generation, or FE coding orchestration. Invoked when the user says something like "Generate code for JIRA <TICKET_ID>" or "Implement the analysis plan for <TICKET_ID>".
disable-model-invocation: true
---

## Master React Coding Orchestrator

### Purpose

This is the **master orchestration skill** for the FE Code Generation Agent. It defines:
- **What** the Coding Agent must build — UI, logic, Sitecore wiring, state, media, Storybook, and tests.
- **In what order** — the mandatory execution sequence of all sub-skills.
- **How** each skill's output feeds into the next skill.
- **Which path to take** — Presentational (lean) vs Transactional (full) execution.
- **What quality gates** must pass before completion.
- **What single document** must be generated at the end.

The Coding Agent MUST follow this master skill as its primary execution blueprint. All other skills are invoked from within this master skill at the correct phase. This skill replaces the four legacy agents (UI, Storybook, Logic, Test) with one orchestrator that loads bounded skills on demand.

### Core Mandate

You are the **FE Code Generation Agent**. Your job is to:
- Consume the approved `ANALYSIS_PLAN.md` and `CODING_AGENT_CHECKLIST.md` produced by the Analysis Agent.
- Generate complete, production-ready React/Next.js code for the story.
- Take the correct path based on component classification: **Presentational** (no API/business logic) or **Transactional** (full integration).
- Produce **ONE consolidated summary document** at the end — not four separate documents.
- Apply the priority order at all times: **Dev Notes → Figma Reconciliation → Analysis Plan → Project Guidelines (embedded in each skill) → React/Frontend Best Practices**.

⚠️ **CRITICAL**: The `ANALYSIS_PLAN.md` is authoritative and already finalised. Do not re-analyse the story. Do not re-open questions the Analysis Agent already decided. Build exactly what the plan specifies.

### Inputs Available to the Coding Agent

Before starting, confirm what inputs are available:

<table>
<tr><th>Input</th><th>Source</th><th>Required?</th></tr>
<tr><td>Analysis Plan</td><td>.SS_WF/Agent/Analysis/{{ticket_id}}_ANALYSIS_PLAN.md</td><td>**Mandatory**</td></tr>
<tr><td>Coding Agent Checklist</td><td>.SS_WF/Agent/Analysis/{{ticket_id}}_CODING_AGENT_CHECKLIST.md</td><td>**Mandatory**</td></tr>
<tr><td>Developer Notes (DN-xxx)</td><td>"Developer Notes Applied" table inside ANALYSIS_PLAN.md</td><td>If present — SACRED LAW</td></tr>
<tr><td>Responsive Reconciliation</td><td>.SS_WF/figma-output/responsive_design_intent.json</td><td>If Figma-driven UI</td></tr>
<tr><td>Figma Context (Desktop/Mobile)</td><td>.SS_WF/figma-output/**/**-context.json</td><td>For visual detail</td></tr>
<tr><td>Sitecore / BFF API Contracts</td><td>As referenced in ANALYSIS_PLAN.md Sections 16–17</td><td>If Transactional</td></tr>
<tr><td>Component Catalogue</td><td>component-catalogue.json at repository root</td><td>**Mandatory** for reuse + catalogue update</td></tr>
</table>

### Classification-Driven Execution

Component classification is **already decided** in `ANALYSIS_PLAN.md` (Section 3). Read it once and select the path:

- **Presentational** → UI-only component with interaction/effects (e.g. hero banner, hero carousel). No API, no mappers, no services, no state stores. Skip Phases 6, 7, 8. Run the **lean path**.
- **Transactional** → UI + data + business logic. Run the **full path** (all phases).
- **Hybrid** → Run the full path but scope each skill to the relevant sections.

⚠️ **DO NOT over-engineer a Presentational component.** No containers, hooks, services, mappers, Zustand stores, or API state for a component that only renders props and handles local interaction.

### Mandatory Execution Sequence

Run phases strictly in order. Load ONE sub-skill's context per phase and discard it before the next phase to conserve tokens.

```text
PHASE 0  Pre-Coding Setup
PHASE 1  Load Implementation Contract        [implementation-contract-loader]
PHASE 2  Developer Notes Enforcement                
PHASE 3  Repository Structure Governance      [repository-structure-governance]
PHASE 4  Presentational UI Generation         [presentational-ui-generation]
          ├─ Responsive/Figma implementation  [responsive-figma-implementation]
          └─ Media integration (if assets)    [frontend-media-integration]
──────────── PRESENTATIONAL PATH STOPS AFTER PHASE 5 & Skips 6-8 and then executes 9–12 ────────────
PHASE 5  Sitecore Rendering Integration       [sitecore-rendering-integration]  (if CMS-mapped)
PHASE 6  Frontend Logic Integration           [frontend-logic-integration]      (Transactional)
PHASE 7  State and Form Management             [frontend-state-and-form-management] (if forms/shared state)
PHASE 8  (Logic wiring completed in 5–7)
PHASE 9  Storybook and Component Catalogue     [storybook-and-component-catalogue]
PHASE 10 Frontend Test Generation              [frontend-test-generation]
PHASE 11 Generated Code Self-Validation        [generated-code-self-validation]
PHASE 12 Consolidated Summary Document          [code-generation-reporting]
```

### Path Selector (Read This First)

```text
IF classification == Presentational:
   run PHASE 0 → 1 → 2 → 3 → 4  -> 5 
                → 9 (Storybook, if reusable/DS/CMS-mapped) → 10 → 11 → 12
   SKIP PHASE  6, 7

IF classification == Transactional OR Hybrid:
   run PHASE 0 → 1 → 2 → 3 → 4 → 5  → 6 → 7 
                → 9 → 10 → 11 → 12
```

---

### PHASE 0 — Pre-Coding Setup (Mandatory Before Everything Else)

#### 0.1 — Folder Pre-Check
- Confirm `/.SS_WF/` already exists — do NOT create a new `.SS_WF` folder.
- Confirm `/.SS_WF/Agent/Coding/` exists — create only if missing.
- The single consolidated summary will be saved to `.SS_WF/Agent/Coding/`.
- NEVER create `src`, `Src`, or duplicate `.storybook` roots. Respect the existing repository layout.

#### 0.2 — Context Reuse Rule
Read and process each referenced file, plan, or spec **only once** per execution. Once loaded into working context, reuse the already-available content. Do not re-fetch, re-read, or re-process the same source again.

#### 0.3 — Confirm Inputs Available
Scan and record which inputs are available. If `ANALYSIS_PLAN.md` is missing, HALT — the Coding Agent cannot proceed without the analysis contract. Never re-run analysis to compensate.

---

### PHASE 1 — Load Implementation Contract

**Invoke: implementation-contract-loader**

This phase reads the upstream artefacts **once** and converts them into a single normalized working manifest for the whole run. It does **NOT** rebuild a checklist — `CODING_AGENT_CHECKLIST.md` already exists and is reused as-is for validation in Phase 11.

#### What to Do
- Load `ANALYSIS_PLAN.md` and extract: classification, DN table, files-to-create, files-to-update, component hierarchy, reuse decisions, Sitecore/BFF contracts, states, interactions, ACs, prop models, and the ordered Code Generation Plan (Section 11).
- Load `CODING_AGENT_CHECKLIST.md` and hold it as the validation contract (do not regenerate it).
- Load `responsive_design_intent.json` and Figma context if UI is Figma-driven.
- Build the in-memory `IMPLEMENTATION_MANIFEST` used by every later phase.

#### Gate: Phase 1 Complete When
- [ ] ANALYSIS_PLAN.md fully parsed into the manifest.
- [ ] CODING_AGENT_CHECKLIST.md loaded as the validation contract (not rebuilt).
- [ ] Classification and execution path selected.
- [ ] File create/update list, reuse decisions, and ordered plan captured.

---

### PHASE 2 — Developer Notes Enforcement

#### What to Do
- READ the "Developer Notes" table from the ANALYSIS_PLAN.md file
- For EVERY file generated in Phases 3–10, check: "Does a DN cover this?" If YES → the DN IS the answer; implement it verbatim. If NO → follow normal priority order.
- Tag each affected output with its DN ID in the summary (e.g. "Per DN-002").

#### Gate: Phase 2 Complete When
- [ ] All DN-xxx items loaded as an active enforcement list.
- [ ] If no Dev Notes exist, explicitly recorded: "No Developer Notes. Normal priority order applies."

---

### PHASE 3 — Repository Structure Governance

**Invoke: repository-structure-governance**

Determine and validate every target path BEFORE writing any file.

#### What to Do
- Resolve ownership for each file: `[design-system]`, `[cms]`, `[feature]`, or `[shared]`.
- Apply folder placement, PascalCase directories, naming conventions, export style, and barrel updates.
- Run the case-insensitive duplicate-path pre-check; reuse existing filesystem casing.
- Block forbidden roots (`src`, duplicate `.storybook`, new `.SS_WF`).

#### Gate: Phase 3 Complete When
- [ ] Every target path validated and approved.
- [ ] No forbidden folders. No casing collisions. Barrel targets identified.

---

### PHASE 4 — Presentational UI Generation

**Invoke: presentational-ui-generation**
**Also invoke (nested): responsive-figma-implementation**, and **frontend-media-integration** if assets are present.

Generate ONLY the prop-driven presentation layer: design-system atoms/molecules/organisms, feature display components, views, typed props, typed callbacks, accessibility contracts, and visual state shells.

#### What to Do
- Build each component from the manifest hierarchy, reusing catalogue components per the reuse decisions.
- Apply `responsive-figma-implementation` for token mapping, responsive layout, RTL, and breakpoint behaviour.
- Apply `frontend-media-integration` only if the component renders images/video/documents.
- **Presentational stories STOP the main build here** — no API, no mappers, no services, no state stores.

#### Gate: Phase 4 Complete When
- [ ] All presentational components generated and exported via barrels.
- [ ] Tokens, RTL, responsive behaviour, and a11y applied.
- [ ] No data-fetching or business logic present in any presentational file.


---

### PHASE 5 — Sitecore Rendering Integration

**Invoke: sitecore-rendering-integration** (only if the story has CMS-mapped components)

Own the Sitecore-to-React boundary: typed field contracts, Layout Service mapping, rendering entry components (default-exported CMS components), placeholder handling, and registry integration. Keep CMS labels separate from API values.

#### Gate: Phase 5 Complete When
- [ ] CMS field contracts typed and mapped.
- [ ] Rendering entry component registered and default-exported.
- [ ] CMS-authored content wired via props (no hardcoded labels).

⚠️ **If classification == Presentational → skip Phases  6, 7 and go to Phase 9.**

---

### PHASE 6 — Frontend Logic Integration

**Invoke: frontend-logic-integration** (Transactional / Hybrid only)

Generate the transactional layer over the existing UI in order: API contract types → constants/query keys → mappers (raw response → FE view model) → framework-agnostic service → TanStack Query hook → container → loading/error/empty/partial orchestration → business rules → navigation callbacks → barrel + prop wiring.

Approved flow: **Component → Hook → TanStack Query → Service → Java BFF API → Upstream Service.** Raw API models MUST be mapped to FE view models before reaching display components.

#### Gate: Phase 6 Complete When
- [ ] Types, constants, mapper, service, hook, and container generated.
- [ ] All loading/error/empty/partial states handled.
- [ ] No raw API model reaches a display component. No API call inside design-system components.

---

### PHASE 7 — State and Form Management

**Invoke: frontend-state-and-form-management** (only if forms or genuinely shared state exist)

Local transient state via React state; shared cross-component state via focused Zustand stores; server state stays in TanStack Query. Controlled fields, validation utilities, touched/submitted behaviour, submit-disabling, and success/error handling.

#### Gate: Phase 7 Complete When
- [ ] State ownership correct (server vs local vs shared).
- [ ] Forms controlled, validated, and submission-guarded.
- [ ] No duplicate writable source of truth.

---

### PHASE 9 — Storybook and Component Catalogue

**Invoke: storybook-and-component-catalogue**

Generate/update stories and catalogue metadata for eligible components only.

**Story eligibility (per resolved Conflict 7):**
- ✅ New/enhanced Design System components (Foundation atoms/molecules/organisms).
- ✅ Sitecore-mapped reusable presentation components.
- ✅ Any reusable UI component/file created in the Design System.
- ❌ Containers, hooks, services, mappers, type-only files, one-off feature-orchestration components.

Update the root `component-catalogue.json` via upsert (never blind append; never delete unrelated entries).

#### Gate: Phase 9 Complete When
- [ ] Co-located `*.stories.tsx` created for every eligible component.
- [ ] Required/optional props, variants, visual states, RTL and responsive contexts covered.
- [ ] `component-catalogue.json` upserted at repository root.

---

### PHASE 10 — Frontend Test Generation

**Invoke: frontend-test-generation**

Generate co-located Vitest + React Testing Library tests based on the ACTUAL generated source files.

- **Coverage target: 90%–100%** of generated runtime code (per resolved Conflict 4). Design branch-mapped tests to reach this; if execution is out of scope, state intended coverage and do not claim measured coverage without a run.
- **Co-location rule (Conflict 5):** every new or modified file containing runtime behaviour gets a co-located test, unless excluded by the runtime-file classification policy (barrels, type-only files, stories, configs, primitive constants).

#### Gate: Phase 10 Complete When
- [ ] Every runtime source file has a co-located test (or is explicitly excluded).
- [ ] Branches, callbacks, states, and exports covered toward 90–100%.
- [ ] Explicit Vitest imports and `userEvent` used; no snapshots.

---

### PHASE 11 — Generated Code Self-Validation

**Invoke: generated-code-self-validation**

Run the deterministic structural gate AND the `CODING_AGENT_CHECKLIST.md` (loaded in Phase 1) before producing the summary.

#### What to Do
- Verify expected files exist; forbidden folders absent; existing casing respected; barrels updated.
- Verify no cross-feature imports; no hardcoded labels/URLs where prohibited; no raw API model in display components; no API calls in design-system components.
- Walk every `CODING_AGENT_CHECKLIST.md` item and mark Covered / Not Applicable, with evidence (file path).

#### Gate: Phase 11 Complete When
- [ ] All structural checks pass.
- [ ] Every checklist item resolved with evidence.
- [ ] Any deviation recorded for the summary's "Deviations & Assumptions" section.

⚠️ No summary may be produced until all validation checks pass. If a check fails, fix the code and re-run — never restart the whole build.

---

### PHASE 12 — Consolidated Summary Document (ONE FILE ONLY)

**Invoke: code-generation-reporting**

Produce a **single** consolidated summary — NOT four documents. It covers UI, Storybook, Logic, and Tests in one file, written with the **Chunked Write Protocol** (write first chunk in `write` mode, all following chunks in `append` mode) to conserve tokens.

**File path:** `.SS_WF/Agent/Coding/{{ticket_id}}_CODE_GENERATION_SUMMARY.md`

⚠️ **MANDATORY**: Do NOT write the summary in a single `write_file` call. Write 2–3 sections per call, switch to append mode after the first chunk, and apply a maximum 2-retry guard per chunk. If a chunk fails twice, write a condensed version and continue. Never restart the build to regenerate the summary.

#### Consolidated Summary — Required Sections (in order)
1. Developer Notes Applied (DN-xxx → files affected)
2. Story & Classification Summary (Presentational / Transactional / Hybrid)
3. UI Components Generated (files, reuse vs new, DS/CMS/feature)
4. Responsive / RTL / Accessibility Implementation
5. Media Integration (or: Not Applicable)
6. Sitecore Rendering Integration (or: Not Applicable)
7. Logic & API Integration — types, mapper, service, hooks, container, states (or: Not Applicable — Presentational)
8. State & Form Management (or: Not Applicable)
9. Storybook & Catalogue Updates (eligible components + catalogue entries)
10. Test Generation Summary (files, coverage map, intended coverage %)
11. Acceptance Criteria Evidence (AC → files/tests)
12. Self-Validation Result (checklist pass/deviation table)
13. Deviations & Assumptions Made

#### Gate: Phase 12 Complete When
- [ ] Single summary file written via chunked write/append.
- [ ] All 13 sections populated with story-specific detail.
- [ ] Presentational runs mark Sections 6–8 as Not Applicable.
- [ ] File saved to `.SS_WF/Agent/Coding/` with the ticket-ID prefix.

---

### Skill Invocation Map

<table>
<tr><th>Phase</th><th>Skill Invoked</th><th>Purpose</th></tr>
<tr><td>Phase 1</td><td>implementation-contract-loader</td><td>Load ANALYSIS_PLAN + CODING_AGENT_CHECKLIST into one manifest (no checklist rebuild)</td></tr>
<tr><td>Phase 3</td><td>repository-structure-governance</td><td>Path ownership, PascalCase folders, naming, barrels, casing pre-check</td></tr>
<tr><td>Phase 4</td><td>presentational-ui-generation</td><td>Prop-driven UI, states, a11y (+ responsive-figma, + media)</td></tr>
<tr><td>Phase 5</td><td>sitecore-rendering-integration</td><td>CMS field contracts, rendering entry, registry (Transactional/CMS)</td></tr>
<tr><td>Phase 6</td><td>frontend-logic-integration</td><td>Types, mappers, services, TanStack hooks, containers, states</td></tr>
<tr><td>Phase 7</td><td>frontend-state-and-form-management</td><td>Zustand/local state, controlled forms, validation</td></tr>
<tr><td>Phase 9</td><td>storybook-and-component-catalogue</td><td>Stories + catalogue upsert for eligible components</td></tr>
<tr><td>Phase 10</td><td>frontend-test-generation</td><td>Co-located Vitest/RTL tests, 90–100% target</td></tr>
<tr><td>Phase 11</td><td>generated-code-self-validation</td><td>Structural gate + CODING_AGENT_CHECKLIST walk</td></tr>
<tr><td>Phase 12</td><td>code-generation-reporting</td><td>ONE consolidated summary, chunked write/append</td></tr>
</table>

### Priority Order (Applied at Every Decision Point)

```text
Dev Notes → Figma Reconciliation → Analysis Plan → Project Guidelines → React/Frontend Best Practices
```

**Topic-based precedence (per resolved Conflict 3):**
- **Visual disparity** → Dev Notes (if implementation notes exist) → Figma Reconciliation → Analysis Plan.
- **Responsive behaviour** → Dev Notes → responsive_design_intent.json → guidelines.
- **API/business behaviour** → Dev Notes → Analysis Plan / API contract → guidelines.
- **Scope / hierarchy / file placement** → Dev Notes → Analysis Plan → guidelines.

Record every conflict resolution in the summary's "Deviations & Assumptions" section.

### Global Guardrails

#### Always Do
- Execute phases in order for the selected path. Load one sub-skill per phase; discard before the next.
- Treat `ANALYSIS_PLAN.md` as finalised — build it, do not re-analyse.
- Keep every component prop-driven — no hardcoded labels, values, or copy.
- Map raw API responses to FE view models before the display layer.
- Reuse catalogue components per the reuse decisions before creating new ones.
- Load only the relevant learnings namespace per skill (UI/LOGIC/STORYBOOK/TEST) — per resolved Conflict 6.
- Produce exactly ONE consolidated summary document.

#### Never Do
- Never re-run analysis or re-open decided questions.
- Never over-engineer a Presentational component (no containers/hooks/services/mappers/stores).
- Never place API calls inside design-system components or feature display components.
- Never let a raw API model reach a display component.
- Never create `src`, duplicate `.storybook`, or new `.SS_WF` roots.
- Never blind-append or delete unrelated entries in `component-catalogue.json`.
- Never write the summary in a single call — always chunked write/append.
- Never produce more than one output document.

### Quick Reference: Phase Execution Summary

```text
PHASE 0  Pre-Coding Setup            → confirm folders + inputs; HALT if no ANALYSIS_PLAN
PHASE 1  Contract Load               [implementation-contract-loader] → manifest (reuse checklist)
PHASE 3  Repo Structure              [repository-structure-governance] → validated paths
PHASE 4  Presentational UI           [presentational-ui-generation] (+responsive, +media)
          ↳ Presentational path → jump to PHASE 9
PHASE 5  Sitecore Rendering          [sitecore-rendering-integration] (if CMS)
PHASE 6  Logic Integration           [frontend-logic-integration] (Transactional)
PHASE 7  State & Forms               [frontend-state-and-form-management] (if needed)
PHASE 9  Storybook + Catalogue       [storybook-and-component-catalogue] (eligible only)
PHASE 10 Tests                       [frontend-test-generation] → 90–100% target, co-located
PHASE 11 Self-Validation             [generated-code-self-validation] → structural + checklist
PHASE 12 Consolidated Summary        [code-generation-reporting] → ONE file, chunked write/append
```
