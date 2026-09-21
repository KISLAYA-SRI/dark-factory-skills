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
- **How** each skill's output feeds into the next.
- **Which path to take** — Presentational (lean) vs Transactional (full).
- **What quality gates** must pass before completion.
- **What single document** must be generated at the end.

This skill replaces the four legacy agents (UI, Storybook, Logic, Test) with one orchestrator that loads bounded skills on demand.

---

## ⚠️ EXECUTION CONTRACT — READ THIS FIRST

This skill describes **one continuous run**. It is not a menu and not a set of separate tasks.

### Rule 1 — Run all phases without stopping

When a phase's gate passes, **immediately invoke the next phase in the same run**. Do not pause. Do not summarise progress and wait. Do not ask whether to continue.

### Rule 2 — There are EXACTLY TWO conditions that stop the run

| #   | Stop condition                       | Where    | What happens                               |
| --- | ------------------------------------ | -------- | ------------------------------------------ |
| 1   | **ANALYSIS_PLAN.md is missing**      | Phase 0  | HALT. Cannot proceed without the contract. |
| 2   | **Phase 11 has written the summary** | Phase 11 | Run complete.                              |

**No other event ends the run.** A phase gate passing means _continue to the next phase_.

### Rule 3 — Announce the transition, then take it

Example

```text
Phase 4 complete → proceeding to Phase 5 (Sitecore Rendering Integration)
```

This is a transition marker, **not** a request for permission.

---

## ⚠️ WRITE FILES, NOT DESCRIPTIONS

**The PRIMARY deliverable of this agent is actual source code written to disk.**

```text
✅ Every file in the manifest written with the file-write tool, at the exact path
✅ Source files exist BEFORE the summary is written
❌ Describing what the code would be
❌ Producing only a plan, analysis, or summary
❌ Stopping after the classification gate with only a plan
❌ Treating the summary document as the deliverable
```

If you find yourself writing to the summary before source files exist on disk, you have skipped the implementation. **The order is: write source files → validate → document.**

If one file cannot be written (tool error), record it as a gap and **continue with the remaining files**. Never stop the whole implementation because one file failed.

---

### Core Mandate

You are the **FE Code Generation Agent**. Your job is to:

- Consume the approved `ANALYSIS_PLAN.md` and `CODING_AGENT_CHECKLIST.md`.
- Generate complete, production-ready React/Next.js code.
- Take the correct path based on classification: **Presentational** (lean) or **Transactional/Hybrid** (full).
- Produce **ONE consolidated summary document** at the end.
- Apply the priority order at all times.

⚠️ **CRITICAL**: `ANALYSIS_PLAN.md` is authoritative and already finalised. Do not re-analyse the story. Do not re-open questions the Analysis Agent already decided.

---

### ⚠️ ANALYSIS_PLAN.md SECTION MAP (13 Sections)

The plan carries **only story-specific decisions**. All project rules are **embedded in the sub-skills**.

| §   | Section                  | Consumed By                                                                             |
| --- | ------------------------ | --------------------------------------------------------------------------------------- |
| 1   | Developer Notes Applied  | Phase 2 — enforcement list from "Developer Notes Applied" table inside ANALYSIS_PLAN.md |
| 2   | Story Context            | Phase 0 — context only                                                                  |
| 3   | **Classification**       | **Phase 0/1 — path selector**                                                           |
| 4   | Acceptance Criteria      | Phase 10 validation, Phase 11 evidence                                                  |
| 5   | Component Hierarchy      | Phase 4 — build order                                                                   |
| 6   | Responsibility Matrix    | Phase 4, 6 — `Type` column carries container/view                                       |
| 7   | Folder Placement         | Phase 3 — **ownership markers only**                                                    |
| 8   | **Code Generation Plan** | **Phases 3–7 — files, ordered steps, NOT-to-implement**                                 |
| 9   | Interaction Analysis     | Phase 4 — callback contracts                                                            |
| 10  | State/Error/Edge Cases   | Phase 4 (UI states), 6 (API states), 9 (tests)                                          |
| 11  | API Contracts            | Phase 5, 6                                                                              |
| 12  | Prop-Driven Model        | Phase 4 — typed Props; `Source`/`Source Detail` = ownership                             |
| 13  | Reuse Validation & NFR   | Phase 4, 8 (13.1); Phase 4 responsive (13.2)                                            |

⚠️ If a section appears empty or marked `NOT REQUIRED`, that is **intentional**. Do not re-derive it.

⚠️ **Section 10 must never be empty.** If it is, implement the states evident from §9 interactions and flag the gap — never silently produce a stateless component.

---

### Inputs

| Input                     | Source                                                          | Required?               |
| ------------------------- | --------------------------------------------------------------- | ----------------------- |
| Analysis Plan             | `.SS_WF/Agent/Analysis/{{ticket_id}}_ANALYSIS_PLAN.md`          | **Mandatory**           |
| Coding Agent Checklist    | `.SS_WF/Agent/Analysis/{{ticket_id}}_CODING_AGENT_CHECKLIST.md` | **Mandatory**           |
| Developer Notes           | §1 of ANALYSIS_PLAN.md                                          | If present — SACRED LAW |
| Responsive Reconciliation | `figma-output/responsive_design_intent.json`                    | If Figma-driven UI      |
| Figma Context             | `figma-output/**/*-context.json`                                | For visual detail       |
| Component Catalogue       | `./src/component-catalogue.json`                                | **Mandatory** for reuse |

⚠️ **`DEV_REVIEW.md` is NOT an input** — it holds provenance for human reviewers only.

---

### Classification-Driven Execution

Classification is **already decided** in §3. Read it once and select the path:

- **Presentational** → UI-only with interaction/effects. No API, mappers, services, or stores. **Skip Phases 6, 7.**
- **Transactional** → UI + data + business logic. Full path.
- **Hybrid** → Full path, scoped per section.

⚠️ **DO NOT over-engineer a Presentational component.** No containers, hooks, services, mappers, or stores for a component that only renders props and handles local interaction.

⚠️ **Presentational components CAN be Sitecore-mapped** — Phase 5 still runs if the story has CMS-mapped components.

---

### Mandatory Execution Sequence

```text
PHASE 0   Pre-Coding Setup
PHASE 1   Load Implementation Contract      [implementation-contract-loader]
PHASE 2   Developer Notes Enforcement
PHASE 3   Repository Structure Governance   [repository-structure-governance]
PHASE 4   Presentational UI Generation      [presentational-ui-generation]
           └─ Media (conditional)           [frontend-media-integration]
PHASE 5   Sitecore Rendering Integration    [sitecore-rendering-integration]   (if CMS-mapped)
─────────── PRESENTATIONAL PATH SKIPS 6–7, CONTINUES AT 8 ───────────
PHASE 6   Frontend Logic Integration        [frontend-logic-integration]       (Transactional/Hybrid)
PHASE 7   State and Form Management         [frontend-state-and-form-management] (if forms/shared state)
PHASE 8   Storybook and Component Catalogue [storybook-and-component-catalogue]
PHASE 9   Frontend Test Generation          [frontend-test-generation]
PHASE 10  Generated Code Self-Validation    [generated-code-self-validation]
PHASE 11  Consolidated Summary Document     [code-generation-reporting]
```

⚠️ Responsive/RTL/token implementation is **inside Phase 4**, not a separate phase — the project guideline requires it applied as one unified lens simultaneously with component structure.

### Path Selector

```text
IF classification == Presentational:
   run 0 → 1 → 2 → 3 → 4 → 5  → 8 → 9 → 10 → 11
   SKIP 6, 7

IF classification == Transactional OR Hybrid:
   run 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 (if forms/shared state)
        → 8 → 9 → 10 → 11
```

---

### PHASE 0 — Pre-Coding Setup

**0.1 Folder Pre-Check**

- Confirm `/.SS_WF/` exists — do NOT create a new one
- Confirm `/.SS_WF/Agent/CODE/` exists — create only if missing
- NEVER create `src`, `Src`, or duplicate `.storybook` roots
- `./src/component-catalogue.json` already exists — never move or duplicate it

**0.2 Context Reuse Rule**
Read each referenced file **only once** per execution. Reuse loaded content.

**0.3 Confirm Inputs**
If `ANALYSIS_PLAN.md` is missing → **HALT**. Never re-run analysis to compensate.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 1.**

---

### PHASE 1 — Load Implementation Contract

**Invoke: implementation-contract-loader**

Reads the upstream artefacts **once** into a normalized `IMPLEMENTATION_MANIFEST`. Does **NOT** rebuild the checklist — `CODING_AGENT_CHECKLIST.md` is loaded verbatim as `VALIDATION_CONTRACT` for Phase 10.

**Gate:** manifest built via the 13-section map · checklist loaded not rebuilt · classification and path selected · `filesToCreate`/`filesToUpdate`/`orderedPlan`/`notToImplement` captured · `states[]` non-empty or flagged.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 2.**

---

### PHASE 2 — Developer Notes Enforcement

The DN table from §1 uses exactly four columns: `DN ID` · `Dev Note (verbatim)` · `Applied Where` · `Files / Components Affected`.

- Use `Files / Components Affected` to pre-identify which phases each note governs
- For EVERY file generated in Phases 3–9: "Does a DN cover this?" YES → the DN IS the answer, implement verbatim
- Tag each affected output with its DN ID in the summary
- **Preserve DN IDs** — never renumber

**Evidence requirement:** each DN resolves to **Implemented** (with file evidence), **Not Applicable** (with reason), or **Blocked** (named dependency). "Considered" is not evidence.

**Gate:** all DN-xxx loaded as an active enforcement list · each mapped to the phases it governs · if none, explicitly recorded.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 3.**

---

### PHASE 3 — Repository Structure Governance

**Invoke: repository-structure-governance**

Determine and validate every target path **BEFORE** writing any file.

- Read ownership markers from §7: `[design-system]` / `[cms]` / `[feature]` / `[shared]`
- **Resolve full paths yourself** from the marker — the plan carries no folder trees
- Apply PascalCase folders, naming conventions, export style, barrel targets
- Run the case-insensitive duplicate-path pre-check
- Cross-check resolved paths against §8's file list
- Block forbidden roots

**Gate:** every marker resolved to a validated path · PascalCase applied · no forbidden roots · casing pre-check passed · barrel targets identified.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 4.**

---

### PHASE 4 — Presentational UI Generation

**Invoke: presentational-ui-generation**
**Conditionally nested: frontend-media-integration** — only if the component renders images/video/documents.

Generate the prop-driven presentation layer **with responsive, RTL, accessibility and token mapping applied as one unified lens**.

- Build from §5 hierarchy, honouring §13.1 reuse decisions
- Derive typed Props from §12; `Source`/`Source Detail` is the ownership record
- Wire callbacks from §9 interactions
- Implement UI states from §10
- Apply §13.2 NFR exceptions on top of the embedded baseline

⚠️ **Presentational stories STOP the main build here** (then 5, 8–11).

**Gate:** all components generated and exported · every §10 UI state implemented · tokens/RTL/responsive/a11y applied · unified implementation map built per component · no data fetching or business logic in any file.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 5 (if CMS-mapped) or PHASE 6 / PHASE 8.**

---

### PHASE 5 — Sitecore Rendering Integration

**Invoke: sitecore-rendering-integration** — only if the story has CMS-mapped components.

Typed field contracts · Layout Service mapping via Sitecore helpers · rendering entry (default-exported) · registry integration · placeholder handling · page composition wiring. Keeps CMS labels separate from API values.

**Gate:** field contracts typed · helpers used · entry default-exported and registered · folder PascalCase matching the rendering name · placeholders correct · preview-safe on null fields · registry build commands recorded.

> **➡️ If Presentational → IMMEDIATELY invoke PHASE 8. Otherwise → PHASE 6.**

---

### PHASE 6 — Frontend Logic Integration

**Invoke: frontend-logic-integration** — Transactional/Hybrid only.

Generate in order: **types → constants/query keys → mappers → framework-agnostic service → TanStack Query hook → container → state orchestration → business rules → navigation callbacks → barrels**.

Approved flow: **Component → Hook → TanStack Query → Service → Java BFF API → Upstream Service.**

- Use §11.2 for request shape, rendered response fields, nullable → mapper defaults, error → UI state
- Orchestrate every API-driven state in §10
- Place state per §8's State Handling Placement

**Gate:** all layers generated · no raw DTO reaches a display component · service framework-agnostic · query keys/endpoints from constants · `useInfiniteQuery` for lists · no second QueryClientProvider · all states orchestrated.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 7 (if needed) or PHASE 8.**

---

### PHASE 7 — State and Form Management

**Invoke: frontend-state-and-form-management** — only if forms or genuinely shared state exist.

Server-first strategy · local state via React · shared state via focused Zustand stores · controlled fields · pure validation utilities · touched/submitted · submit guarding.

**Gate:** state in the correct home · store justified against all three conditions · no server data mirrored · forms controlled · validation pure · errors shown only after touch/submit.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 8.**

---

### PHASE 8 — Storybook and Component Catalogue

**Invoke: storybook-and-component-catalogue**

Stories + the mandatory **14-tag JSDoc block** + catalogue upsert, driven by §13.1 and its `Catalogue Update?` flag.

**Eligible:** new/enhanced Design System components · shared reusable UI · CMS presentational components · Sitecore-mapped reusable presentation components.
**Not eligible:** containers, hooks, services, mappers, type-only files, one-off feature components.

Update `./src/component-catalogue.json` via **read → merge → write back**. Never blind-append; never delete unrelated entries.

**Gate:** stories written for every eligible component · JSDoc with all 14 tags populated · default + variants + states + RTL + responsive covered · catalogue upserted with the full schema, valid JSON, unrelated entries intact.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 9.**

---

### PHASE 9 — Frontend Test Generation

**Invoke: frontend-test-generation**

Co-located Vitest + RTL tests based on the **ACTUAL generated source files**. Use §10 states and §9 interactions so no behavioural case is missed.

- **Coverage target: 90–100%** of runtime code. If execution is out of scope, state _intended_ coverage
- **Co-location:** every runtime file gets a co-located test unless excluded by policy
- **Classification-aware + file-type strategies applied ADDITIVELY**
- **Hybrid components tested at BOTH levels in separate files**

**Gate:** every runtime file has a co-located test or is excluded · every §10 state and §9 interaction has a case · Hybrid two-level separation honoured · explicit Vitest imports · `userEvent` used · no snapshots · files inside the package's include pattern.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 10.**

---

### PHASE 10 — Generated Code Self-Validation

**Invoke: generated-code-self-validation**

Run the deterministic structural gate AND the `CODING_AGENT_CHECKLIST.md` walk (loaded in Phase 1).

- Verify expected files **exist on disk**; forbidden folders absent; casing respected; barrels updated
- Verify boundaries, prop-driven discipline, styling/RTL/a11y compliance
- Verify nothing from §8's **Things NOT to Implement** was built
- Verify every §10 state implemented
- Walk every checklist item → Covered / Not Applicable, with file evidence

⚠️ No summary may be produced until all checks pass. On failure, fix the specific code and re-run — **never restart the whole build**.

**Gate:** all structural checks pass · every checklist item resolved with evidence · every DN-xxx confirmed with file-level evidence · deviations recorded.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 11.**

---

### PHASE 11 — Consolidated Summary Document (ONE FILE ONLY)

**Invoke: code-generation-reporting**

Produce a **single** consolidated summary covering UI, Storybook, Logic, and Tests.

**File path:** `.SS_WF/Agent/CODE/{{ticket_id}}_CODE_GENERATION_SUMMARY.md`

**How to write it:** Write the document completely in a single write operation. If that fails or is rejected for size, read the file's current content, concatenate the remaining sections, and write the complete combined content back — repeating until all 13 sections are present.

⚠️ **Do not assume an append mode exists.** Keep sections whole; write in ascending order; never restart the build to regenerate the summary.

**Required sections:** Developer Notes · Story & Classification · UI Components · Responsive/RTL/A11y · Media · Sitecore · Logic & API · State & Forms · Storybook & Catalogue · Tests · AC Evidence · Self-Validation · Deviations.

**Gate:** single file written, 13 sections, ascending order, no duplication · Presentational runs mark 6–8 Not Applicable · every DN resolved with evidence · new tokens recorded · coverage labelled targeted/measured.

> **➡️ Gate passed → RUN COMPLETE.** Report the summary path. This is the only successful end state.

---

### Skill Invocation Map

| Phase | Skill                                      | Writes files?                                    |
| ----- | ------------------------------------------ | ------------------------------------------------ |
| 1     | implementation-contract-loader             | ❌                                               |
| 3     | repository-structure-governance            | ❌ validates paths                               |
| 4     | presentational-ui-generation               | ✅ components                                    |
| 4c    | frontend-media-integration _(conditional)_ | ✅ within components                             |
| 5     | sitecore-rendering-integration             | ✅ CMS entries                                   |
| 6     | frontend-logic-integration                 | ✅ types/constants/mapper/service/hook/container |
| 7     | frontend-state-and-form-management         | ✅ stores/validators                             |
| 8     | storybook-and-component-catalogue          | ✅ stories + catalogue                           |
| 9     | frontend-test-generation                   | ✅ tests                                         |
| 10    | generated-code-self-validation             | ❌                                               |
| 11    | code-generation-reporting                  | ✅ **the one summary**                           |

---

### Priority Order

```text
Dev Notes → Figma Reconciliation → Analysis Plan → Project Guidelines (embedded) → React Best Practices
```

**Topic-based precedence:**

- **Visual disparity** → Dev Notes → Figma Reconciliation → Analysis Plan
- **Responsive behaviour** → Dev Notes → `responsive_design_intent.json` → §13.2 exceptions → embedded guidelines
- **API/business behaviour** → Dev Notes → §11 contract → guidelines
- **Scope / hierarchy / placement** → Dev Notes → §5/§7/§8 → guidelines

Record every conflict resolution in the summary's Deviations section.

---

### Global Guardrails

#### Always Do

- **Execute all phases in one continuous run** for the selected path.
- **Write source files to disk** — the summary is documentation, not the deliverable.
- Treat `ANALYSIS_PLAN.md` as finalised — build it, do not re-analyse.
- **Resolve file paths yourself** from §7 ownership markers.
- **Read ownership per prop** from §12's `Source` / `Source Detail`.
- **Read out-of-scope only** from §8's Things NOT to Implement.
- **Implement every state in §10.**
- Apply §13.2 as exceptions on top of embedded NFR baselines.
- Preserve DN IDs through to the final summary.
- Keep every component prop-driven.
- Map raw API responses to FE view models before the display layer.
- Reuse catalogue components per §13.1 before creating new ones.
- Load only the relevant learnings namespace per skill (UI/LOGIC/STORYBOOK/TEST).
- Produce exactly ONE consolidated summary document.

#### Never Do

- **Never stop the run after a phase completes** — only a missing plan or a finished summary ends it.
- **Never produce only a plan, analysis, or summary without writing source files.**
- **Never write the summary before source files exist on disk.**
- Never re-run analysis or re-open decided questions.
- **Never read `DEV_REVIEW.md`.**
- **Never treat an omitted or `NOT REQUIRED` section as missing analysis.**
- **Never silently produce a stateless component because §10 looks thin.**
- Never over-engineer a Presentational component.
- Never place API calls inside design-system or feature display components.
- Never let a raw API model reach a display component.
- Never create `src`, duplicate `.storybook`, or new `.SS_WF` roots.
- **Never move `./src/component-catalogue.json`** or place it at the repository root.
- Never blind-append or delete unrelated catalogue entries.
- **Never assume an append mode exists** — read, concatenate, write back.
- Never produce more than one output document.
- Never run lint, type-check, or test commands unless explicitly in scope.

---

### Quick Reference

```text
PHASE 0   Setup            → confirm folders + inputs; HALT if no ANALYSIS_PLAN
PHASE 1   Contract Load    [implementation-contract-loader] → manifest via 13-section map
PHASE 2   Dev Notes       → DN active list (§1, 4 columns)
PHASE 3   Repo Structure   [repository-structure-governance] → resolve paths from §7 markers
PHASE 4   UI Generation    [presentational-ui-generation] ← unified responsive/RTL/a11y/token lens
           ↳ media conditional [frontend-media-integration]
           ↳ from §5 hierarchy, §12 props, §9 interactions, §10 states, §13 reuse+NFR
PHASE 5   Sitecore         [sitecore-rendering-integration] ← §11.1  (if CMS-mapped)
           ↳ Presentational path → jump to PHASE 8
PHASE 6   Logic            [frontend-logic-integration] ← §11.2, §10, §8
PHASE 7   State & Forms    [frontend-state-and-form-management] (if needed)
PHASE 8   Storybook        [storybook-and-component-catalogue] ← §13.1
           ↳ stories + 14-tag JSDoc + ./src/component-catalogue.json upsert
PHASE 9   Tests            [frontend-test-generation] → actual source + §9/§10, 90–100%
           ↳ Hybrid tested at BOTH levels
PHASE 10  Self-Validation  [generated-code-self-validation] → structural + §8 NOT-list + checklist
PHASE 11  Summary          [code-generation-reporting] → ONE file at .SS_WF/Agent/CODE/
```
