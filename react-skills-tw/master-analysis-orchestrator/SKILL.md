---
name: master-analysis-orchestrator
description: Use when orchestrating the complete end-to-end FE Story Analysis workflow. Defines the mandatory nine-phase sequence, decision gates between phases, skill invocation map, the classification-aware context validation gate, and quality standards the final output must meet before being passed to the Coding Agent. Triggers include story analysis, analysis agent, FE analysis workflow, or analysis orchestration. Invoked when the user says something like "Implement JIRA <TICKET_ID>" or "Analyse JIRA <TICKET_ID>"
---

## Master Analysis Orchestrator

### Purpose

This is the **master orchestration skill** for the FE Story Analysis Agent. It defines:

- **What** the Analysis Agent must do — the complete analysis scope.
- **In what order** — the mandatory nine-phase sequence.
- **How** each skill's output feeds into the next skill.
- **What quality gates** must pass, including the hard Context Validation gate.
- **What three documents** must be generated at the end.

### Core Mandate

You are the **FE Story Analysis Agent**. Your job is to:

- Analyse a frontend user story end-to-end.
- Make every decision yourself — no open questions, no deferred approvals, no options.
- Produce three output documents that go **directly to the Code Generation Agent**.
- Apply the priority order at all times: **Dev Notes → Figma → React/Frontend Best Practices**.

⚠️ **CRITICAL**: The Coding Agent receives your output BEFORE any developer sees it. Every decision must be finalised. Zero ambiguity is permitted in ANALYSIS_PLAN.md.

---

### ⚠️ THE THREE ARCHITECTURAL PRINCIPLES

**1. Acquisition is separate from interpretation.**
All external context is fetched **once**, in Phase 2. Phases 5 and 6 read from disk. They never call Figma MCP, `curl`, the http tool, or the open-api-spec MCP tool, and never re-scan the story for URLs, endpoints, or operationIds.

**2. Classification precedes validation.**
Story Analysis (Phase 3) runs on the story text alone and produces the classification. Context Validation (Phase 4) then knows exactly which artefacts are mandatory — a Presentational component does not require a BFF spec, a Transactional one does.

**3. Analyse wide, hand off narrow.**
Every phase performs its full investigation. Only the FE-relevant slice reaches ANALYSIS_PLAN.md. Provenance goes to DEV_REVIEW.md. The coding skills are self-contained — the plan never restates project rules.

---

### Mandatory Execution Sequence

```text
PHASE 1  Dev Notes Extraction     [developer-notes-protocol]
PHASE 2  Context Gathering        [context-gathering]           ← ONLY phase that fetches
PHASE 3  Story Analysis           [story-analysis-end-to-end]   ← produces classification
PHASE 4  Context Validation       [context-validation]          ← HARD GATE, may halt
PHASE 5  Figma Analysis           [figma-design-analysis]
PHASE 6  API Analysis             [api-analysis-sitecore-and-bff]
PHASE 7  Component Breakdown      [component-breakdown-and-hierarchy]
PHASE 8  Component Reuse          [component-reuse-validation]
PHASE 9  Output Production        [analysis-output-contract]
```

Run phases strictly in order. Load ONE sub-skill's context per phase and discard it before the next.

Do not create analysis documents in individual phases. All three documents are created in Phase 9 only.

---

### ⚠️ TWO DIFFERENT FAILURE MODELS — DO NOT CONFUSE THEM

|            | Phase 2 — Context Gathering              | Phase 4 — Context Validation            |
| ---------- | ---------------------------------------- | --------------------------------------- |
| Level      | Per task (Sitecore / BFF / Figma)        | Whole agent                             |
| On failure | Stop **that task only**; others continue | **Halt everything**                     |
| Records    | Failure noted in CONTEXT_MANIFEST        | Error report; **no documents produced** |
| Downstream | Later phases still run                   | **No later phase runs**                 |

Phase 2 is permissive so one broken fetch does not block the others. Phase 4 is strict: once the classification is known, missing mandatory context makes the analysis unsound.

---

### Canonical Artefact Paths

| Artefact                  | Path                                                | Written By | Read By               |
| ------------------------- | --------------------------------------------------- | ---------- | --------------------- |
| Sitecore API JSON         | `./.SC_API_SPEC/sitecore-api.json`                  | Phase 2    | Phase 6               |
| BFF API spec              | `./.BFF_API_SPEC/{operationId}.json`                | Phase 2    | Phase 6               |
| Figma Design Intent       | `figma-output/figma_design_{Node_id}_-context.json` | Phase 2    | Phase 5               |
| Responsive Reconciliation | `figma-output/responsive_design_intent.json`        | Phase 5    | Phase 7, Coding Agent |

### Inputs Available to the Analysis Agent

| Input                       | Source                                          | Required?                         |
| --------------------------- | ----------------------------------------------- | --------------------------------- |
| JIRA User Story             | `.SS_WF/{{$var[ticket_id]s}}_JIRA_OUTPUT_.json` | **Mandatory**                     |
| Developer Notes / Dev Notes | Section inside the JIRA story                   | If present — SACRED LAW           |
| Component Catalogue         | `component-catalogue.json` at repo root         | **Mandatory** for reuse decisions |

All other context is **produced by Phase 2**, not supplied externally.

---

### PHASE 1 — Developer Notes Extraction

**Invoke: developer-notes-protocol** (extraction mode)

The **first and highest-priority phase**. It MUST complete before any other work — including context gathering.

#### What to Do

- Scan the JIRA user story for any Developer Notes / Dev Notes section.
- Extract every instruction verbatim and number them: DN-001, DN-002, DN-003 …
- Store them as an active working list live throughout ALL subsequent phases.
- For EVERY decision in Phases 2–8, check: "Does a Dev Note cover this topic?"
  - YES → The Dev Note IS the answer. Do not produce an alternative.
  - NO → Proceed with normal source priority order.

#### Output Contract

Section 1 of ANALYSIS_PLAN.md uses **exactly four columns**:

```text
| DN ID | Dev Note (verbatim) | Applied Where | Files / Components Affected |
```

DN conflicts → **DEV_REVIEW.md §3**. DN ambiguity and the interpretation chosen → **DEV_REVIEW.md §4**.

#### Gate: Phase 1 Complete When

- [ ] JIRA story scanned for Developer Notes.
- [ ] All Dev Notes extracted, numbered, stored in the working list.
- [ ] If none found — explicitly recorded: "No Developer Notes / Dev Notes section found in the user story. Normal source priority order applied."
- [ ] Section 1 table shape confirmed as the four required columns.

⚠️ **If this phase is skipped, the entire analysis is invalid.**

---

### PHASE 2 — Context Gathering (Acquisition Only)

**Invoke: context-gathering**

Acquires **all** external context in one pass and writes it to disk. **No reconciliation, no analysis.**

#### What to Do

- Read the JIRA story **once**; extract all Sitecore endpoints, BFF operationIds, and Figma URLs.
- Execute the Context Synthesisor prompt **verbatim** — it is validated in production.
- Fetch and write to the canonical paths above.
- Produce the **CONTEXT_MANIFEST** recording what was fetched, what was missing, and what failed — including a `VIEWPORT COVERAGE` block.

#### Scope Clarification

The embedded prompt says _"SKIP the whole task"_ when no Backend API details are provided. **"The whole task" means the BFF task only.** Sitecore and Figma extraction always proceed independently.

#### Fail-Stop (Per Task)

If any fetch fails, stop **that task only**, record it in the CONTEXT_MANIFEST, and continue with the other two. Never invent an endpoint, field, node, token, or component.

⚠️ Do **not** halt here for missing context. Phase 4 decides what is fatal, because only then is the classification known.

#### Gate: Phase 2 Complete When

- [ ] JIRA story read once; all endpoints, operationIds and Figma URLs extracted.
- [ ] Sitecore task completed — fetched, or recorded as Not Found / Fetch Failed.
- [ ] BFF task completed — each operationId written as `{operationId}.json`, or recorded.
- [ ] Figma task completed — each URL written, or recorded as Fetch Failed.
- [ ] Every Figma file has fully populated `screenMetadata` — the only viewport signal downstream.
- [ ] No invented endpoints, fields, nodes, or components.
- [ ] A failure in one task did not stop the other two.
- [ ] CONTEXT_MANIFEST produced, including VIEWPORT COVERAGE.

---

### PHASE 3 — Story Analysis End to End

**Invoke: story-analysis-end-to-end**

⚠️ **Runs on the STORY TEXT ALONE.** Figma and API artefacts exist on disk but are **not** read here — they are interpreted in Phases 5 and 6.

⚠️ **Its most important output is the CLASSIFICATION**, which drives the Phase 4 gate.

#### Provisional vs Final

| Output                                          | Status                                                | Enriched By                           |
| ----------------------------------------------- | ----------------------------------------------------- | ------------------------------------- |
| Story Understanding, Classification, Scope, ACs | **Final**                                             | —                                     |
| Interactions (§9)                               | Provisional — story-declared only                     | Phase 5 adds design-only interactions |
| States (§10)                                    | Provisional — story + UI states                       | Phase 6 adds API-driven states        |
| Prop model (§12)                                | Provisional — `Source` known, `Source Detail` pending | Phases 5–6 resolve field/endpoint     |
| NFR (§13.2)                                     | Provisional — story-derived                           | Phase 5 adds design-driven exceptions |

Unresolved detail is written as `To be resolved in Figma/API analysis` — **never invented**.

#### ⚠️ DEFENSIVE RULE — STATE ANALYSIS IS SCOPED, NEVER SKIPPED

For a Presentational story, Step 6 must be **scoped down, not skipped**:

```text
Presentational — KEEP:
  default / initial · active / selected · hover / focus ·
  transitioning / paused · disabled · hidden ·
  missing image / broken media · long text / overflow

Presentational — OMIT (API-driven, no trigger exists):
  loading · success · empty · partial data · error · unavailable ·
  API failure · missing/invalid data · unauthorised · empty list
```

⚠️ If §10 would be empty for a Presentational story, the analysis is **incomplete**. Return to Step 6 and scope it correctly.

#### Gate: Phase 3 Complete When

- [ ] All 11 story-understanding items extracted.
- [ ] **Component classified with rationale — definitive, no deferral.**
- [ ] In-scope and out-of-scope both derived (out-of-scope destined for §8).
- [ ] All ACs analysed with FE implications, owner components, state/interaction impact.
- [ ] All story-declared interactions identified.
- [ ] **All applicable states analysed — scoped, not skipped, for Presentational.**
- [ ] **§10 content is non-empty for every classification.**
- [ ] Ownership resolved per content/data item (Step 7.1, internal).
- [ ] Every Step 7.1 item appears as a Step 7.2 prop row.
- [ ] Provisional prop model produced; unresolved detail marked, never invented.
- [ ] NFR analysed in full; story-specific exceptions isolated.
- [ ] No Figma or API artefact was read in this phase.

---

### PHASE 4 — Context Validation (HARD GATE)

**Invoke: context-validation**

Verifies that every artefact **required by this classification** was both declared in the story and written to disk.

#### Validation Matrix

| Artefact     | Pure Presentational | Transactional | Hybrid      |
| ------------ | ------------------- | ------------- | ----------- |
| **Sitecore** | ✅ Required         | ✅ Required   | ✅ Required |
| **Figma**    | ✅ Required         | ✅ Required   | ✅ Required |
| **BFF**      | ⛔ **Not checked**  | ✅ Required   | ✅ Required |

⚠️ **Pure Presentational skips the BFF check entirely.** A presentational component has no API integration — an absent BFF spec is correct, not a failure.

⚠️ **Hybrid is validated as Transactional** — it contains transactional regions, so all three are mandatory.

#### The Two-Part Check

Every artefact must pass **both**:

```text
PART 1 — DECLARED?      Was the endpoint / URL found in the JIRA story?
PART 2 — MATERIALISED?  Was the artefact written to disk, non-empty and readable?
```

#### Outcomes

**SUCCESS** → emit the success report and continue to Phase 5.

**REQUIRED CONTEXT NOT FOUND** → emit the failure report and **HALT**:

- No further phase runs.
- **No ANALYSIS_PLAN.md, no DEV_REVIEW.md, no CODING_AGENT_CHECKLIST.md is produced.**
- The report lists every missing item and a specific required action for each.

⚠️ Check **all** applicable artefacts before reporting — one complete report is far more useful than halting on the first failure.

⚠️ A partial analysis built on missing context is worse than no analysis: the Coding Agent would treat it as complete.

#### Gate: Phase 4 Complete When

- [ ] Classification read; applicable rule set selected.
- [ ] Sitecore validated — declared AND artefact present.
- [ ] Figma validated — declared AND every declared URL has a context file.
- [ ] BFF validated (Transactional/Hybrid only) — every declared operationId has a spec.
- [ ] BFF check correctly skipped for Pure Presentational.
- [ ] All applicable artefacts checked before reporting.
- [ ] SUCCESS or REQUIRED CONTEXT NOT FOUND emitted.
- [ ] On failure: agent halted, zero documents produced, actionable remediation listed.

---

### PHASE 5 — Figma Design Analysis

**Invoke: figma-design-analysis**

Reconciles and analyses the Figma files from Phase 2. **Never fetches.**

#### What to Do

**Step 5.1 — Identify viewports from file content.** Filenames carry no viewport marker. Use `screenMetadata.deviceType`, else `frameDimensions` (≈390px → mobile, ≈1700px → desktop). If ambiguous → treat as single-viewport and record the risk.

**Step 5.2 — Reconcile (conditional).** Both viewports → produce `figma-output/responsive_design_intent.json`. One viewport → skip. Already exists → do NOT re-reconcile.

**Step 5.3 — Enrich the story analysis.** Add design-only interactions to §9, visual states to §10, confirmed label ownership to §12, design-driven RTL/responsive exceptions to §13.2, unsupported design elements to §8, reuse candidates to §13.1.

**Step 5.4 — Capture design-required content** in §12 so the Phase 6 gap sweep has something to check against.

⚠️ **Do not re-derive the classification.** If the design contradicts it, record an analysis risk in DEV_REVIEW.md §1 — never silently reclassify.

#### Gate: Phase 5 Complete When

- [ ] Viewport identified per file from `screenMetadata`, not filename.
- [ ] Reconciliation performed only when both viewports present and no existing file.
- [ ] Story-analysis structures enriched — §8, §9, §10, §12, §13 updated.
- [ ] Design-required content captured in §12 for the gap sweep.
- [ ] Classification left unchanged; any contradiction recorded as a risk.
- [ ] Design ambiguity and reconciliation conflicts recorded in DEV_REVIEW.md §4.
- [ ] No standalone Figma section prepared for the plan.

---

### PHASE 6 — API Analysis

**Invoke: api-analysis-sitecore-and-bff**

Analyses the Sitecore and BFF specs from Phase 2. **Never fetches.**

⚠️ **ANALYSE WIDE, HAND OFF NARROW.** Exhaustive extraction discovers edge cases and gaps. Only the FE-relevant slice reaches §11 — **but every gap is reported in full.**

#### What to Do

**Step 6.1 — Sitecore Analysis.** Read **only** `./.SC_API_SPEC/sitecore-api.json`. Analyse CMS rendering → FE component mapping, authored props, placeholder, datasource/template, and missing fields.

**Step 6.2 — BFF Analysis.** Read **only** the `{operationId}.json` files named in the CONTEXT_MANIFEST. Read each spec **completely**. Extract ALL request scenarios, ALL response scenarios (2xx/4xx/5xx/empty/partial), ALL error codes, ALL conditional/nullable fields, ALL example payloads.

> Pure Presentational → mark `BFF API NOT REQUIRED` and skip. This is correct, not a gap.

**Step 6.3 — ⚠️ CONTRACT GAP SWEEP (MANDATORY).**

Compare what the frontend needs against what the contracts deliver:

```text
FE REQUIREMENTS                          API CONTRACT
├── Provisional prop model (§12)   ──┐
├── Acceptance criteria (§4)       ──┼──►  Sitecore fields available
├── Figma-identified content       ──┤     BFF response fields available
└── States requiring data (§10)    ──┘
                                          ↓
                              Anything required but NOT available = GAP
```

For **every** §12 prop marked `Sitecore` or `BFF API`, locate its source field. If it cannot be located, **record a gap** — never silently leave the prop `Unknown`.

Gap categories: missing field · missing endpoint · insufficient detail · missing error semantics · missing pagination/metadata · type/format mismatch · missing CMS field.

**Every gap goes to DEV_REVIEW.md §5** with a `GAP-xxx` ID and all eight columns: Category, What FE Needs, Needed For, Expected Source, Contract Evidence, Impact if Unresolved, Recommended Action.

⚠️ **Gaps are never compressed, summarised, or omitted.** A gap found here but not reported becomes a runtime defect the Coding Agent cannot foresee.

⚠️ If there are no gaps, write `No API contract gaps identified.` **Never leave §5 blank** — blank is indistinguishable from "not checked".

**Step 6.4 — Resolve provisional prop sources.** Replace every `To be resolved in API analysis` with the actual field path. Unresolvable → GAP + `Unknown — source contract not provided`.

**Step 6.5 — Distil the FE-relevant slice** into §11. Retain endpoint + method, request shape, rendered response fields, nullable/conditional fields → mapper defaults, error codes with distinct UI treatment, Data Fetching Pattern, and gap notes. Drop full example payloads, unsurfaced response scenarios, and error codes with no distinct UI treatment.

State rendering rules feed **§10**, not §11.

#### Gate: Phase 6 Complete When

- [ ] Sitecore section completed (or marked NOT FOUND / NOT REQUIRED).
- [ ] BFF section completed (or marked NOT REQUIRED for Presentational).
- [ ] Complete spec read for every in-scope operation — not skimmed.
- [ ] All request/response scenarios, error codes and conditional fields analysed.
- [ ] Strict lookup rule followed — no folder browsing, no fallback files.
- [ ] **Gap sweep run against prop model, ACs, Figma content and states.**
- [ ] **Every gap recorded in DEV_REVIEW.md §5 with full evidence.**
- [ ] **§5 populated — or explicitly states no gaps.**
- [ ] Every provisional `Source Detail` resolved or gap-recorded.
- [ ] Distillation performed — FE-relevant slice separated from full extraction.
- [ ] No invented endpoints, fields, or properties.

---

### PHASE 7 — Component Breakdown and Hierarchy

**Invoke: component-breakdown-and-hierarchy**

#### What to Do

**Step 7.1 — Apply breakdown logic.** Presentational → P1–P8. Transactional → T1–T8. Hybrid → both, applied to the appropriate sections.

A Presentational component MAY own local visual state (carousel index, hover, expanded, paused). This does **not** justify a container.

**Step 7.2 — Build hierarchy.** Use markers `[design-system]`, `[feature]`, `[Sitecore-mapped]`, `[container]`, `[view]`. No file paths in the diagram. Do not create a component for every icon, label, or text row.

**Step 7.3 — Responsibility matrix.** **Component │ Type │ Owns │ Must NOT Own**. The `Type` column carries the container/view decision. For Presentational, omit `Container` and `View` types. Record only story-specific responsibilities.

**Step 7.4 — File placement.** Run the placement tree, naming conventions, folder boundaries and export patterns **internally**. Emit only ownership markers: `[design-system]`, `[cms]`, `[feature]`, `[shared]`.

**Step 7.5 — Finalise the prop model.** With Phase 5 and 6 enrichment complete, §12 is final: every prop has a resolved `Source` and `Source Detail`, or is explicitly `Unknown` with a linked gap. **No `To be resolved` placeholder may remain.**

⚠️ Do NOT produce a folder tree, naming-convention table, folder-boundary table, or export-pattern table. Naming conventions are applied internally — they produce the concrete filenames for **§8**.

#### Gate: Phase 7 Complete When

- [ ] Correct breakdown rules applied for the classification.
- [ ] Hierarchy tree produced with approved markers, no file paths.
- [ ] Matrix uses exactly: Component │ Type │ Owns │ Must NOT Own.
- [ ] Container/view expressed via `Type`; absent for Presentational.
- [ ] Only story-specific responsibilities recorded.
- [ ] Ownership marker assigned to every component/file.
- [ ] Concrete filenames derived for §8.
- [ ] **§12 finalised — no `To be resolved` placeholder remains.**
- [ ] No folder tree or convention table prepared for the plan.

---

### PHASE 8 — Component Reuse Validation

**Invoke: component-reuse-validation**

Execute the **4-Step Reuse Decision Workflow** for every applicable component:

**Step 8.1 — Classify Atomic Level** (Atom / Molecule / Organism, with justification).

**Step 8.2 — Exact Match Check** against `component-catalogue.json`. Found → `Reuse existing variant`. **STOP.**

**Step 8.3 — Partial Match Check.** If a partial match exists:

- ⚠️ **MANDATORY CODE CHECK** — inspect the actual source to verify the required variant/state does NOT already exist.
- Found in code → `Reuse existing variant`. **STOP.**
- Not in code → `Enhance existing component`. Record backward-compatibility impact in **DEV_REVIEW.md §1**. **STOP.**

**Step 8.4 — No Match.** Generic and business-neutral, or usable across features → `Create new reusable component`. Tightly coupled to a business domain or API shape → `Create feature-specific component`.

#### Definitive Decisions Only

⚠️ Every component receives a **definitive** category. `Needs clarification` and `approval required` are **prohibited**. When unclear: make the most defensible decision, emit it, record the uncertainty in **DEV_REVIEW.md §1**.

#### Exclusions

Containers / controllers, mappers, hooks, type files, visibility utilities, API service files.

#### Gate: Phase 8 Complete When

- [ ] Every applicable component went through all 4 steps.
- [ ] Every component has a **definitive** reuse category.
- [ ] Code check performed for every partial match.
- [ ] Containers/controllers excluded.
- [ ] `component-catalogue.json` used as the ONLY existence source.
- [ ] Uncertainty and backward-compatibility impact routed to DEV_REVIEW.md §1.
- [ ] `Catalogue Update?` flag set — it drives Storybook eligibility downstream.

---

### PHASE 9 — Self-Validation and Output Production

**Invoke: analysis-output-contract**

⚠️ **PRESENTATIONAL CONDENSED SELF-VALIDATION.** For a Presentational story, mark as Not Applicable without analysis:

- Backend / API Analysis checks
- API-driven state rows — loading, success, empty, partial, error, unavailable
- Data Fetching Pattern, hook/service/query key rows
- Container/mapper boundary rows

⚠️ **But UI-interaction state rows still apply.** §10 must be non-empty for a Presentational story.

For Presentational output:

- §11 → `NOT REQUIRED — Presentational component. No API integration.`
- §6 → omit `Container` and `View` types.
- §8 → omit the State Handling Placement table.
- §10 → UI interaction states only.

#### Three Responsibilities in Sequence

- **Part A: Self-Validation** — the complete 13-section checklist.
- **Part B: Content Prohibition Check** — verify content before writing it.
- **Part C: Output Production** — generate all three documents.

#### Step 9C — Output Production

- **ANALYSIS_PLAN.md** — all **13 sections**, fully populated.
- **DEV_REVIEW.md** — all **5 sections** (write "None" if no items; §5 must state gaps or "no gaps identified").
- **CODING_AGENT_CHECKLIST.md** — all prefix categories with story-specific items.

**How to write them:** Use your available file-writing tool and write each document completely in a single write operation. If a write fails or is rejected for size, read the file's current content, concatenate the remaining sections onto it, and write the complete combined content back — repeating until whole. Choose your own split points, keep every section and table intact, and write sections in ascending order.

⚠️ Do not assume an append mode exists. Do not regenerate the analysis after a write failure — reuse the content you already produced.

#### Gate: Phase 9 Complete When

- [ ] All 13 self-validation checklist sections completed.
- [ ] Content checked for prohibited phrases, provenance columns, rule-restatement, eliminated sections.
- [ ] Section 1 table uses exactly the four required columns.
- [ ] **§10 is non-empty, including for Presentational stories.**
- [ ] **DEV_REVIEW.md §5 (API Contract Gaps) populated or explicitly states no gaps.**
- [ ] Every uncertain decision and provenance value is in DEV_REVIEW.md.
- [ ] Every DN-xxx appears in the Developer Notes Applied table.
- [ ] **ANALYSIS_PLAN.md produced with all 13 sections, ascending order, no duplication or truncation.**
- [ ] DEV_REVIEW.md produced with all 5 sections.
- [ ] CODING_AGENT_CHECKLIST.md produced with story-specific items.
- [ ] All three files saved to `.SS_WF/Agent/Analysis/` with the ticket ID prefix.
- [ ] Single consolidated verification pass performed.

---

### OUTPUT PHASE — Three Documents

#### Document 1: ANALYSIS_PLAN.md

**Path:** `.SS_WF/Agent/Analysis/{{$var[ticket_id]s}}_ANALYSIS_PLAN.md`

```text
1.  Developer Notes Applied (4 columns exactly)
2.  Story Context
3.  Classification
4.  Acceptance Criteria
5.  Component Hierarchy
6.  Component Responsibility Matrix (Type carries container/view)
7.  Folder Placement (ownership markers only)
8.  Code Generation Plan (files, ordered steps, state handling, visibility,
    prop wiring, things NOT to implement)
9.  Interaction Analysis
10. State, Error and Edge Case Analysis (never empty)
11. API Contracts (11.1 Sitecore + 11.2 BFF — FE-relevant slice + gap notes)
12. Prop-Driven Component Model (per-prop Source + Source Detail)
13. Reuse Validation & NFR Exceptions
```

#### Document 2: DEV_REVIEW.md

**Path:** `.SS_WF/Agent/Analysis/{{$var[ticket_id]s}}_DEV_REVIEW.md`

```text
1. Decisions Made Under Uncertainty
2. Assumptions Made (incl. contract and artefact gaps)
3. Conflicts Resolved
4. Derived Items and Provenance
5. API Contract Gaps   ← data FE needs that the API does not provide
```

#### Document 3: CODING_AGENT_CHECKLIST.md

**Path:** `.SS_WF/Agent/Analysis/{{$var[ticket_id]s}}_CODING_AGENT_CHECKLIST.md`

Prefixes: DN · AC · INT · STATE · SCOPE · PROP · CMS · API _(omit for Presentational)_ · COMP · DS · RESP · A11Y · RTL · NFR · FILE · TEST

---

### Skill Invocation Map

| Phase | Skill                                   | Purpose                                                |
| ----- | --------------------------------------- | ------------------------------------------------------ |
| 1     | developer-notes-protocol _(extraction)_ | Extract Dev Notes as SACRED LAW                        |
| 2     | **context-gathering**                   | Fetch Sitecore, BFF, Figma; produce CONTEXT_MANIFEST   |
| 3     | story-analysis-end-to-end               | Story-only analysis; **produces classification**       |
| 4     | **context-validation**                  | **Classification-aware hard gate; may halt the agent** |
| 5     | figma-design-analysis                   | Reconcile viewports + enrich story analysis            |
| 6     | api-analysis-sitecore-and-bff           | Contract analysis + **gap detection** + distillation   |
| 7     | component-breakdown-and-hierarchy       | Hierarchy, responsibility matrix, ownership markers    |
| 8     | component-reuse-validation              | 4-step reuse workflow; definitive categories           |
| 9     | analysis-output-contract                | Self-validation, prohibition check, 3 documents        |

### Priority Order

```text
Dev Notes → Figma → React/Frontend Best Practices
```

Non-negotiable. Higher-priority source wins; conflict and resolution recorded in DEV_REVIEW.md §3.

⚠️ In Phase 3, Figma is not yet available — the order there is Dev Notes → Project Guidelines → Best Practices.

---

### Global Guardrails

#### Always Do

- Execute all nine phases in order. No skipping, no reordering.
- Extract Dev Notes FIRST — before context gathering.
- **Acquire all external context once, in Phase 2.**
- **Classify in Phase 3 from the story alone**, before validation.
- **Halt completely if Phase 4 fails** — produce no documents.
- **Run the gap sweep in Phase 6 and report every gap in DEV_REVIEW.md §5.**
- **Analyse wide, hand off narrow.**
- **Scope state analysis for Presentational — never skip it.** §10 must never be empty.
- Mark every missing input clearly: Not Provided.
- Record every uncertain decision and provenance value in DEV_REVIEW.md.
- Label every item influenced by a Dev Note with its DN ID.
- Keep all components prop-driven.
- Express ownership **per prop** in §12.
- Express out-of-scope **only** in §8's Things NOT to Implement.
- Express file placement as **ownership markers**.
- Assign a **definitive** reuse category to every component.
- **Write each output document completely, using your own file-writing tool.**

#### Never Do

- Never skip Phase 1 (Dev Notes extraction).
- **Never fetch in Phases 3–9** — acquisition belongs to Phase 2 only.
- **Never read Figma or API artefacts in Phase 3** — classification comes from the story.
- **Never continue past a failed Phase 4** — not even partially.
- **Never produce any document when Phase 4 fails.**
- **Never re-scan the JIRA story for URLs, endpoints, or operationIds after Phase 2.**
- **Never invent an endpoint, field, node, token, or component** to fill a gap — record the gap.
- **Never leave a prop `Unknown` without a corresponding GAP entry.**
- **Never leave DEV_REVIEW.md §5 blank.**
- **Never compress, summarise, or omit a gap.**
- **Never re-derive the classification in Phase 5 or 6** — record a risk instead.
- **Never skip Step 6 state analysis for a Presentational component — scope it.**
- Never reference DEV_REVIEW.md inside ANALYSIS_PLAN.md.
- Never write deferred-decision phrases, `Needs clarification`, or `approval required` into ANALYSIS_PLAN.md.
- **Never write a provenance column into ANALYSIS_PLAN.md.**
- **Never restate a project rule in ANALYSIS_PLAN.md.**
- **Never write a separate scope, ownership, container/view, assumptions or agent-decision section.**
- **Never dump full example payloads or unsurfaced response scenarios into the plan.**
- **Never assume an append mode exists** — to grow a file, read and rewrite it whole.
- **Never split a section or table across two writes.**
- Never override a Dev Note.
- Never browse spec folders or fall back to similarly-named files.
- Never skim a spec file — read it completely.
- Never create a new `src` folder — use the existing one.
- Never generate implementation code.

---

### Quick Reference: Phase Execution Summary

```text
PHASE 1  Dev Notes           [developer-notes-protocol]
         → DN-xxx list, 4-column contract, sacred law for all later phases

PHASE 2  Context Gathering   [context-gathering]  ← ONLY phase that fetches
         → Context Synthesisor prompt VERBATIM
         → .SC_API_SPEC/sitecore-api.json
         → .BFF_API_SPEC/{operationId}.json
         → figma-output/figma_design_{Node_id}_-context.json
         → CONTEXT_MANIFEST (incl. VIEWPORT COVERAGE)
         → Fail-stop PER TASK; never invent; never halt the agent here

PHASE 3  Story Analysis      [story-analysis-end-to-end]  ← STORY TEXT ONLY
         → Classification (drives Phase 4), ACs, scope, provisional §9/§10/§12/§13
         → ⚠ Presentational: SCOPE state analysis — §10 must not be empty
         → Unresolved detail marked "To be resolved" — never invented

PHASE 4  Context Validation  [context-validation]  ← HARD GATE
         → Presentational: Sitecore + Figma required, BFF NOT checked
         → Transactional/Hybrid: Sitecore + Figma + BFF ALL required
         → Two-part check: declared in story AND materialised on disk
         → SUCCESS → continue │ FAILURE → HALT, zero documents

PHASE 5  Figma Analysis      [figma-design-analysis] — reads from disk
         → viewport from screenMetadata (not filename)
         → reconcile if both viewports → responsive_design_intent.json
         → enriches §8, §9, §10, §12, §13; classification unchanged

PHASE 6  API Analysis        [api-analysis-sitecore-and-bff] — reads from disk
         → exhaustive contract analysis
         → ⚠ GAP SWEEP: FE needs vs contract reality → DEV_REVIEW §5 (GAP-xxx)
         → resolves provisional Source Detail in §12
         → distils FE-relevant slice → §11

PHASE 7  Component Breakdown [component-breakdown-and-hierarchy]
         → hierarchy, matrix (Type carries container/view), ownership markers
         → finalises §12

PHASE 8  Component Reuse     [component-reuse-validation]
         → 4-step workflow; definitive categories only

PHASE 9  Output Production   [analysis-output-contract]
         → Part A self-validation · Part B prohibition · Part C 3 documents
         → DEV_REVIEW.md has 5 sections (§5 = API Contract Gaps)
```
