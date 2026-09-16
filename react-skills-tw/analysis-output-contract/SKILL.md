---
name: analysis-output-contract
description: Use this skill to perform final self-validation and produce all three output documents (ANALYSIS_PLAN.md, DEV_REVIEW.md, CODING_AGENT_CHECKLIST.md). Runs the 13-section self-validation checklist, the content prohibition check, and the mandatory output templates including the API Contract Gaps section. Triggers include output contract, self-validation, analysis output, ANALYSIS_PLAN, DEV_REVIEW, CODING_AGENT_CHECKLIST, or Phase-9.
---

## Analysis Output Contract

### Purpose

This skill has two mandatory responsibilities:

- **Self-Validation** — Run the complete 13-section checklist to verify all analysis areas are complete and correct before any document is produced.
- **Output Production** — Generate all three output documents using the mandatory templates, fully populated from the analysis completed in all the Phases.

**CRITICAL**: No output document may be produced until ALL self-validation checks are completed. If any check fails, complete the missing analysis before proceeding.
---

### ⚠️ ANALYSIS_PLAN.md IS A HANDOFF CONTRACT — NOT AN ANALYSIS TRANSCRIPT

ANALYSIS_PLAN.md exists for **one consumer**: the Code Generation Agent.

> Every coding skill is self-contained — folder placement, naming, PascalCase, container/view rules, RTL, accessibility, prop-driven discipline and design-token usage are already embedded in the coding skills. Therefore any plan content that merely **restates a project rule is dead weight**. The plan carries only the **story-specific decision**.

**Provenance belongs in DEV_REVIEW.md, never in ANALYSIS_PLAN.md.** Columns such as `Basis`, `Confidence`, `Source`, `Confirmed In` and `Agent Decision` do not change what the Coding Agent builds.

**Analyse wide, hand off narrow.** Exhaustive extraction happens during analysis — that is how edge cases and contract gaps are discovered. Only the FE-relevant slice is serialised into the plan.

⚠️ **One exception: contract gaps are never compressed.** Every gap found during API analysis is reported in full in DEV_REVIEW.md §5.

---

### ⚠️ PHASE 9 CONTEXT RULE — READ FIRST

**All analysis is already complete.** The large raw artefacts — the full API spec files, the full component catalogue, and the raw Figma design trees — are **no longer needed** and must NOT be re-opened.

- Do **NOT** re-read the raw API spec files.
- Do **NOT** re-read the full component catalogue.
- Do **NOT** re-read the raw Figma JSON trees.
- If a detail seems missing, pull it from the **already-distilled Phase 1–8 outputs** in session context.

---

## PART A — Self-Validation Checklist

Before producing any document, validate that all required analysis areas are complete. This is a mandatory quality gate.

> **Note:** This checklist validates **analysis completeness**. It is different from the 13 sections of ANALYSIS_PLAN.md, which is the **handoff contract**. A check passing here does not mean its content is written into the plan — much of it goes to DEV_REVIEW.md instead.

### ⚡ PRESENTATIONAL COMPONENT FAST PATH — READ FIRST

If Phase 3 classified this story as **Presentational**:

| Checklist Section | Action for Presentational Component |
| --- | --- |
| Section 5: Backend / API Analysis | Mark ALL rows Not Applicable. Do not analyse. |
| Section 9: Loading / Error / Empty / Partial / Success / Unavailable rows | Mark Not Applicable. **UI interaction rows still apply — see below.** |
| Section 12: Data Fetching Pattern, Hook / Service / Query Key rows | Mark Not Applicable. Skip entirely. |
| Section 12: Container/mapper boundary rows | Mark Not Applicable. No container or mapper exists. |

All other sections (1–4, 6–8, 10–11, 13) MUST still be fully completed.

#### ⚠️ DEFENSIVE RULE — STATE ANALYSIS IS SCOPED, NEVER SKIPPED

**A Presentational component still has real states.** Skipping state analysis leaves §10 empty, deprives the Coding Agent of a state contract, and leaves Test Generation with no state cases.

For a Presentational story, §10 MUST contain:

```text
✅ Default / initial
✅ Active / selected (e.g. current carousel slide, selected tab)
✅ Hover / focus
✅ Transitioning / paused (autoplay, animation, carousel motion)
✅ Disabled
✅ Hidden (conditional render)
✅ Media edge cases (missing image / broken media URL)
✅ Overflow edge cases (long text, localisation growth, narrow viewport)

❌ Loading, Success, Empty, Partial data, Error, Unavailable  — API-driven, omit
❌ API failure, missing/partial/invalid data, unauthorised, empty list — API-driven, omit
```

If §10 is empty for a Presentational story, the analysis is **incomplete** — return to Phase 3 and scope it correctly.

**Corresponding output rules for Presentational:**
- §11 → `NOT REQUIRED — Presentational component. No API integration.`
- §6 → omit `Container` and `View` types.
- §10 → UI interaction states only.
- §8 → omit the State Handling Placement table.

**Rules:**
- Do not hide missing inputs. Mark unavailable information as Not Provided.
- Behaviour recommended from best practice → mark Derived **in DEV_REVIEW.md**, not the plan.
- Uncertain decisions → make the best decision, write it into the plan, record basis and confidence in DEV_REVIEW.md.
- If any task is incomplete, do not assume or fabricate. Complete the analysis first.

### 1. Story Understanding
- [ ] Story objective understood
- [ ] Story scope extracted
- [ ] Out-of-scope items identified *(→ §8, Things NOT to Implement)*
- [ ] Acceptance criteria mapped to FE implications
- [ ] Page/component name identified
- [ ] Journey context captured *(→ internal + DEV_REVIEW context)*
- [ ] Personas/roles captured
- [ ] All 11 story-understanding items extracted, including the 7 not emitted

### 2. Story Classification
- [ ] Classification completed — Presentational / Transactional / Hybrid
- [ ] Classification rationale documented
- [ ] **Classification derived from the story text alone, before Figma/API analysis**
- [ ] Data-fetching responsibility identified
- [ ] CMS-authored responsibility identified
- [ ] FE-only responsibility identified

### 3. Developer Notes Compliance
- [ ] Dev Notes extracted before any other analysis
- [ ] All Dev Notes numbered (DN-001, DN-002, …)
- [ ] Every analysis decision checked against the DN list
- [ ] Dev Notes Applied table completed as §1
- [ ] Every DN-xxx item appears in the table
- [ ] Every DN-influenced item labelled with its DN ID
- [ ] §1 table uses exactly the four required columns
- [ ] DN conflicts → DEV_REVIEW.md §3; DN ambiguity → DEV_REVIEW.md §4

### 4. Context Acquisition and Validation
- [ ] CONTEXT_MANIFEST produced by the context gathering phase
- [ ] Context Validation gate passed for this classification
- [ ] Sitecore artefact present and validated
- [ ] Figma artefacts present and validated for every declared URL
- [ ] BFF artefacts present and validated *(Transactional/Hybrid only)*
- [ ] BFF check correctly skipped for Pure Presentational

### 5. Backend / API Analysis
- [ ] Spec files read from disk — no fetching in the analysis phase
- [ ] Required endpoints identified from the CONTEXT_MANIFEST
- [ ] ALL request scenarios extracted *(analysis-wide)*
- [ ] ALL response scenarios extracted (2xx, 4xx, 5xx, empty, partial) *(analysis-wide)*
- [ ] ALL error codes and messages extracted *(analysis-wide)*
- [ ] ALL example payloads reviewed to validate contract understanding *(never emitted)*
- [ ] Response fields relevant to the FE story identified
- [ ] Conditional / nullable fields identified → mapper defaults
- [ ] Field-to-UI mapping drafted
- [ ] API-owned vs CMS-owned values separated
- [ ] Raw API response not passed to display components — mapper boundary defined
- [ ] Strict lookup rule followed — no folder browsing, no fallback files
- [ ] Data fetching pattern produced per endpoint
- [ ] **Distil step performed** — FE-relevant slice separated from full extraction

### 6. Contract Gap Analysis
- [ ] Gap sweep run against the prop model
- [ ] Gap sweep run against the acceptance criteria
- [ ] Gap sweep run against Figma-identified content
- [ ] Gap sweep run against states requiring data
- [ ] Every gap has a GAP-xxx ID and all eight columns populated
- [ ] Every gap cites contract evidence proving absence
- [ ] Every gap names a concrete consumer (AC / component / prop)
- [ ] Every prop marked `Unknown` has a corresponding GAP entry
- [ ] **DEV_REVIEW.md §5 populated — or explicitly states no gaps**
- [ ] §11.1 / §11.2 Gaps lines carry brief notes with GAP IDs

### 7. Figma / Design Context Analysis
- [ ] Figma context read from disk — no fetching in the analysis phase
- [ ] Viewport identified per file from `screenMetadata`, not filename
- [ ] Target frame/node identified
- [ ] Layer hierarchy reviewed
- [ ] Text/copy ownership inferred carefully — CMS vs API vs system
- [ ] Icon references noted (names only)
- [ ] Auto-layout/layout hints used as guidance, not hardcoded values
- [ ] Design ambiguity captured *(→ DEV_REVIEW.md §4)*
- [ ] Reconciliation performed only when both viewports present and no existing file
- [ ] Reconciliation JSON treated as authoritative once produced
- [ ] Design-only interactions added to §9 with continued INT-xxx numbering
- [ ] Design-required content captured in §12 for the gap sweep
- [ ] Classification left unchanged by design analysis

### 8. Component Breakdown Analysis
- [ ] Component hierarchy created without file paths
- [ ] Hierarchy uses approved markers
- [ ] Containers separated from display components *(Transactional/Hybrid only)*
- [ ] View component responsibility defined
- [ ] Feature display components identified
- [ ] Design-system candidates identified
- [ ] No unnecessary lowest-level atom detail
- [ ] Component responsibilities documented — owns / must-not-own
- [ ] `Type` assigned per component (carries the container/view decision)
- [ ] Placement decision tree run; ownership marker assigned per component
- [ ] Naming conventions applied internally to derive §8 filenames
- [ ] 4-Step Reuse Workflow completed for each applicable component
- [ ] `component-catalogue.json` consulted
- [ ] Containers excluded from reuse check

### 9. Props / View Model Analysis
- [ ] Prop-driven model defined — no hardcoded labels, values, messages, CTA text
- [ ] Prop shape produced per component with source, type, source detail
- [ ] Sitecore props identified; API props identified; derived props identified
- [ ] **Every provisional `Source Detail` resolved or gap-recorded**
- [ ] View model drafted for display components
- [ ] Mapper responsibility defined *(Transactional/Hybrid only)*
- [ ] Optional/missing data handling noted
- [ ] Sitecore helpers identified where relevant
- [ ] **Every ownership item from Phase 3 Step 7.1 appears as a prop row in §12**

### 10. State, Behaviour and Interaction Analysis
- [ ] Default / initial state analysed
- [ ] Active / selected state analysed *(applies to Presentational)*
- [ ] Hover / focus state analysed *(applies to Presentational)*
- [ ] Transitioning / paused state analysed *(applies to Presentational)*
- [ ] Disabled state analysed *(applies to Presentational)*
- [ ] Hidden / conditional-render state analysed *(applies to Presentational)*
- [ ] Media edge cases analysed *(applies to Presentational)*
- [ ] Overflow edge cases analysed *(applies to Presentational)*
- [ ] Loading / error / empty / partial / success / unavailable states analysed *(Transactional/Hybrid only)*
- [ ] API-driven edge cases analysed *(Transactional/Hybrid only)*
- [ ] Visibility rules analysed — persona/role/config-driven
- [ ] Interaction behaviour analysed
- [ ] State ownership assigned
- [ ] **§10 is non-empty** — including for Presentational stories

### 11. Accessibility, RTL and Responsive Analysis
- [ ] Semantic structure considered
- [ ] Keyboard interaction considered
- [ ] ARIA requirements noted
- [ ] RTL readiness considered — no left/right assumptions
- [ ] Localisation readiness considered — no hardcoded text
- [ ] Responsive behaviour considered
- [ ] Design tokens assumed over hardcoded colours/spacing
- [ ] Overflow & scroll handling considered

> All four categories analysed in full. Only **story-specific exceptions** written into §13.2.

### 12. ANALYSIS_PLAN.md Content Compliance
- [ ] No reference to DEV_REVIEW in ANALYSIS_PLAN.md
- [ ] No open questions or deferred decisions
- [ ] No `Needs clarification` reuse category and no `approval required` phrasing
- [ ] Every uncertain decision recorded in DEV_REVIEW.md §1
- [ ] 100% actionable without re-analysing the story
- [ ] **All 13 required sections present and populated**
- [ ] **No provenance columns** — no Basis, Confidence, Source, Confirmed In, Agent Decision
- [ ] **No project-rule restatement** — no folder trees, naming lists, generic NFR baselines
- [ ] **No eliminated sections** — no standalone Scope, Ownership, Container/View, Agent Decision Summary, or Assumptions section

### 13. Final Analysis Quality Gate
- [ ] No unsupported assumptions — no invented Sitecore/API fields
- [ ] No over-fragmentation
- [ ] No hardcoded implementation
- [ ] Ownership boundaries clear
- [ ] Component hierarchy readable
- [ ] Coding Agent can act without re-analysing the story
- [ ] Three output files created
- [ ] All files saved to `.SS_WF/Agent/Analysis/`

### Coverage Status Values

| Status | Meaning |
| --- | --- |
| Covered | Analysis completed with sufficient information |
| Partially Covered | Analysis done but some details missing or unclear |
| Not Provided | Required input not available |
| Derived | Recommendation based on project best practices |
| Not Applicable | Does not apply to this story/component type |
| Needs Developer Confirmation | Decision made but requires validation *(status only — never a phrase in the plan)* |

---

## PART B — ANALYSIS_PLAN.md Content Prohibition

**Apply this check to the content you are about to write, before writing it.**

### B.1 — Deferred-decision phrases
- "DEV REVIEW", "DEV_REVIEW", "dev review"
- "see DEV REVIEW", "confirm in DEV REVIEW"
- "needs developer approval", "to be confirmed", "pending review", "check with developer"
- "needs developer confirmation", "needs confirmation"
- "option A or B", any open question, any deferred decision
- **"Needs clarification"** · **"approval required"**, "requires approval", "awaiting approval"
- **"To be resolved in API analysis"** — provisional markers must be resolved or gap-recorded by Phase 6

### B.2 — Provenance columns
- `Basis`, `Confidence`, `Source`, `Confirmed In`, `Agent Decision`
- Any column explaining *why* a decision was reached rather than *what* to build

### B.3 — Rule-restatement content
- Folder-structure tree diagrams
- Naming-convention lists
- Folder-boundary or export-pattern tables
- Generic NFR baselines already embedded in the coding skills
- Generic responsibility rows such as "design-system components must not contain API calls"

### B.4 — Eliminated sections
- Standalone Derived Scope *(out-of-scope belongs to §8)*
- Standalone Sitecore/Backend/Frontend Ownership *(belongs per-prop to §12)*
- Standalone Container / View Decision *(belongs to §6's `Type` column)*
- Agent Decision Summary *(belongs to DEV_REVIEW.md §1)*
- Assumptions and Decisions Made *(belongs to DEV_REVIEW.md §2)*
- Full example payloads or unsurfaced response scenarios
- Standalone Sitecore-Authored Props table *(belongs to §12)*
- "How it will be used in development" narrative sections

**Every decision in ANALYSIS_PLAN.md must be final and definitive.** Uncertainty, basis, and confidence belong in DEV_REVIEW.md only.

⚠️ **Gaps are stated as fact, not as questions.** Write `policyEndDate not present in response (GAP-001)` — never `needs developer confirmation`.

---

## PART C — Output Document Production

After all 13 self-validation checks pass, produce all three documents. Every section must be fully populated.

### ⚠️ HOW TO WRITE THE DOCUMENTS

**This skill defines WHAT each document must contain. You decide HOW to write it using your available file-writing tool.**

Write each document **completely, in a single write operation**. Do not artificially split a document across multiple writes.

#### If a single write fails or is rejected for size

1. Write the document with the leading sections first, creating the file.
2. To add the remaining sections: **read the file's current content, concatenate the new sections onto it, and write the complete combined content back.** Repeat until all sections are present.
3. Choose your own split points. Keep sections whole — never split mid-section or mid-table.
4. Always write sections in ascending order.

⚠️ Do not assume an append mode exists. If your write tool only creates or overwrites files, read-concatenate-rewrite is the correct way to grow a document.

#### Non-negotiable outcomes

| Outcome | Requirement |
| --- | --- |
| **Completeness** | Every required section present and fully populated |
| **Order** | Sections in ascending numerical order |
| **Integrity** | No duplicated, truncated, or orphaned sections; no partial tables |
| **Content compliance** | Part B check applied before writing |
| **No loss** | Rewriting to add sections preserves all prior content verbatim |

#### Efficiency rules
- **Reuse computed content.** If a write fails, reuse what you already generated — never regenerate the analysis.
- **Do not re-read a file you just wrote** to confirm success — rely on the tool result.
- **Never restart the analysis** because of a write failure.
- **Do not use shell commands** to assemble, repair, or reorder documents.
- **If content must be reduced**, condense tables to essential rows; note as `[Condensed: Section X]`. **Never condense DEV_REVIEW.md §5 gaps.**

#### Final verification — one pass only
- All three files exist at the correct paths.
- ANALYSIS_PLAN.md contains all 13 section headers, in order, no duplicates.
- DEV_REVIEW.md contains all 5 sections.
- No prohibited phrases, provenance columns, or eliminated sections present.

---

### Document 1: ANALYSIS_PLAN.md

**Path:** `.SS_WF/Agent/Analysis/{{ticket_id}}_ANALYSIS_PLAN.md`

```markdown
# ANALYSIS PLAN {{ticket_id}}

---

## 1. Developer Notes Applied

| DN ID | Dev Note (verbatim) | Applied Where | Files / Components Affected |
| ----- | ------------------- | ------------- | --------------------------- |
| DN-001 |                    |               |                             |

> If none: "No Developer Notes / Dev Notes section found in the user story. Normal source priority order applied."

⚠️ Exactly these four columns. Do NOT add `Sections Affected`, `Basis`, `Confidence`, or `Impact if Wrong`.

---

## 2. Story Context

- **Story Title:** [exact JIRA title]
- **Page / Component:** [target page or component name]
- **Default View / State:** [what the user sees on first load]
- **Personas / Roles:** [personas driving visibility branching, or: None]

---

## 3. Classification

- **Classification:** Presentational / Transactional / Hybrid
- **Rationale:** [one clear sentence]
- **Data-Fetching Required:** Yes / No
- **CMS-Authored Required:** Yes / No
- **FE-Only Logic:** [local state, visibility, mapping, layout summary]

---

## 4. Acceptance Criteria

| AC ID | AC Statement | FE Implication | Owner Component | State / Interaction Impact |
| ----- | ------------ | -------------- | --------------- | -------------------------- |
| AC-001 |             |                |                 |                            |

---

## 5. Component Hierarchy

[ComponentName] [Sitecore-mapped]
  [ComponentName] [container]
    [ComponentName] [view]
      [ComponentName] [feature]
        [ComponentName] [design-system]

> Markers: `[design-system]` | `[feature]` | `[Sitecore-mapped]` | `[container]` | `[view]`
> No file paths. A Presentational story typically has no `[container]` or `[view]` nodes.

---

## 6. Component Responsibility Matrix

| Component | Type | Owns | Must NOT Own |
| --------- | ---- | ---- | ------------ |
|           |      |      |              |

> `Type` carries the container/view distinction. For Presentational, omit `Container`/`View`.
> Only story-specific responsibilities — no generic rule restatement.

---

## 7. Folder Placement

| Component / File | Ownership Marker |
| ---------------- | ---------------- |
| [ComponentName]  | [design-system] / [cms] / [feature] / [shared] |

> Ownership markers only. The Coding Agent resolves full path, casing, naming, export style and barrel target.

---

## 8. Code Generation Plan

### Files to Create

| # | File Name | Path | Purpose |
| - | --------- | ---- | ------- |
| 1 |           |      |         |

### Files to Update

| # | File Name | Path | Reason |
| - | --------- | ---- | ------ |
| 1 |           |      |        |

### Ordered Implementation Steps

1. [story-specific step]
...
N. Validate against CODING_AGENT_CHECKLIST.md

### State Handling Placement

> **Transactional / Hybrid only.** Omit for Presentational — local UI state described inline in the ordered steps.

| State | Owned By | Mechanism |
| ----- | -------- | --------- |
|       |          |           |

### Visibility Rule Placement

| Visibility Rule | Condition | Placed In | Passed As Prop? |
| --------------- | --------- | --------- | --------------- |
|                 |           |           |                 |

### Prop-Driven Wiring

| Prop Flow Step | From | To | Prop Name | Transformation |
| -------------- | ---- | -- | --------- | -------------- |
|                |      |    |           |                |

### Things NOT to Implement

> The single authoritative out-of-scope guardrail. Include features blocked by a contract gap, with the GAP ID.

- [item 1 — with reason]

---

## 9. Interaction Analysis

| Interaction ID | Description | Trigger | Owner Component | State Impact |
| -------------- | ----------- | ------- | --------------- | ------------ |
| INT-001        |             |         |                 |              |

---

## 10. State, Error and Edge Case Analysis

> **Presentational:** UI interaction states only. Omit API-driven rows.
> **This section must never be empty, including for Presentational stories.**

| State / Edge Case | Applicable Component | Trigger / Condition | Expected FE Behaviour |
| ----------------- | -------------------- | ------------------- | --------------------- |
|                   |                      |                     |                       |

---

## 11. API Contracts

> If not applicable: `NOT REQUIRED — Presentational component. No API integration.`

### 11.1 Sitecore Contract

| Rendering | FE Entry Component | Field Name | Field Type | Maps To Prop |
| --------- | ------------------ | ---------- | ---------- | ------------ |
|           |                    |            |            |              |

- **Placeholder:** [key, or: None]
- **Datasource / Template:** [name, or: Not Provided]
- **Gaps:** [brief note per gap with GAP ID, or: None]

### 11.2 BFF Contract

> FE-relevant slice only. No full example payloads, no unsurfaced response scenarios,
> no error codes without distinct UI treatment.

- **Endpoint:** [path]
- **Method:** [GET/POST/…]

**Request shape (fields actually sent):**

| Field | In | Type | Required? |
| ----- | -- | ---- | --------- |
|       |    |      |           |

**Response fields actually rendered:**

| Field | Type | Nullable / Conditional? | Mapper Default | Maps To Prop |
| ----- | ---- | ----------------------- | -------------- | ------------ |
|       |      |                         |                |              |

**Error → UI state mapping:**

| Error Code | UI State | Component |
| ---------- | -------- | --------- |
|            |          |           |

**Data Fetching Pattern:**

| Hook | Service | Query Key | Endpoint Constant |
| ---- | ------- | --------- | ----------------- |
|      |         |           |                   |

- **Gaps:** [brief note per gap with GAP ID, or: None]

---

## 12. Prop-Driven Component Model

**Component: [ComponentName]**
Type: [Sitecore-mapped / Container / View / Feature Display / Design System]

| Prop Name | Type | Source | Source Detail (field/endpoint) | Required? |
| --------- | ---- | ------ | ------------------------------ | --------- |
|           |      | Sitecore / BFF API / FE Derived / Unknown | | |

> `Source` + `Source Detail` are the authoritative per-prop ownership record.
> Every `Unknown` must have a corresponding GAP entry in DEV_REVIEW.md §5.
> No `To be resolved` markers may remain.

---

## 13. Reuse Validation & NFR Exceptions

### 13.1 Component Inventory & Reuse Validation

| Component | Atomic Level | Reuse Decision | Existing Component | Gap / Enhancement | New Component Name | Catalogue Update? |
| --------- | ------------ | -------------- | ------------------ | ----------------- | ------------------ | ----------------- |
|           |              |                |                    |                   |                    |                   |

> Definitive categories only. `Needs clarification` and `approval required` are prohibited.

### 13.2 NFR Exceptions

> **Story-specific exceptions ONLY.** Baseline RTL, a11y, responsive and overflow rules are
> already enforced by the coding skills.

| NFR Category | Story-Specific Exception / Requirement |
| ------------ | ------------------------------------- |
|              |                                       |

> If none: "No story-specific NFR exceptions. Standard project NFR rules apply."
```

---

### Document 2: DEV_REVIEW.md

**Path:** `.SS_WF/Agent/Analysis/{{ticket_id}}_DEV_REVIEW.md`

The **sole home for all provenance** and the **authoritative record of contract gaps**.

```markdown
# DEV REVIEW {{ticket_id}}

---

## 1. Decisions Made Under Uncertainty

| Decision ID | Area | Options Considered | Decision Made | Reason | Confidence Level |
| ----------- | ---- | ------------------ | ------------- | ------ | ---------------- |
| DEC-001     |      |                    |               |        | High / Medium / Low |

---

## 2. Assumptions Made (Missing Information)

| Assumption ID | Area | Assumption Made | Missing Input | Impact if Wrong | Action Required |
| ------------- | ---- | --------------- | ------------- | --------------- | --------------- |
| ASS-001       |      |                 |               |                 |                 |

---

## 3. Conflicts Resolved

| Conflict ID | Sources in Conflict | Resolution | Priority Rule Applied | Notes |
| ----------- | ------------------- | ---------- | --------------------- | ----- |
| CON-001     |                     |            |                       |       |

---

## 4. Derived Items and Provenance

| Plan Section | Item ID | Derived / Story-Confirmed / Figma | Basis |
| ------------ | ------- | --------------------------------- | ----- |
|              |         |                                   |       |

> Write "None" if every item was story-confirmed.

---

## 5. API Contract Gaps

> ⚠️ **MANDATORY SECTION.** Data the frontend requires that the API or CMS contract does not
> currently provide. Each gap blocks or degrades specific functionality and requires a
> backend/CMS decision before implementation can be completed.

| Gap ID | Category | What FE Needs | Needed For | Expected Source | Contract Evidence | Impact if Unresolved | Recommended Action |
| ------ | -------- | ------------- | ---------- | --------------- | ----------------- | -------------------- | ------------------ |
| GAP-001 | Missing field | [data item] | [AC-00x / component / prop] | [endpoint or Sitecore rendering] | [what the contract actually contains] | [what breaks or degrades] | [specific backend/CMS ask] |

**Categories:** Missing field · Missing endpoint · Insufficient detail · Missing error semantics ·
Missing pagination/metadata · Type/format mismatch · Missing CMS field

> If there are no gaps, write exactly:
> `No API contract gaps identified. All frontend data requirements are satisfied by the available contracts.`
>
> ⚠️ **Never leave this section blank** — blank is indistinguishable from "not checked".
> ⚠️ **Never condense or omit a gap**, even if the document must be reduced for size.
```

---

### Document 3: CODING_AGENT_CHECKLIST.md

**Path:** `.SS_WF/Agent/Analysis/{{ticket_id}}_CODING_AGENT_CHECKLIST.md`

**For Presentational components:** omit the API prefix category entirely.

```markdown
# CODING AGENT CHECKLIST {{ticket_id}}

> Complete before marking implementation done. Every item derived from ANALYSIS_PLAN.md.

---

## DN — Developer Notes Compliance (ALWAYS first)
- [ ] DN-001: [verbatim dev note — confirm implemented as specified]

## AC — Acceptance Criteria
- [ ] AC-001: [AC statement] — [what FE must do to satisfy it]

## INT — Interaction Behaviour
- [ ] INT-001: [interaction] — [expected FE behaviour]

## STATE — State / Error / Empty Behaviour
- [ ] STATE-001: [state] renders [UI] in [component]

## SCOPE — Out-of-Scope Protection
- [ ] SCOPE-001: [out-of-scope item] NOT implemented in this story

## PROP — Prop-Driven Implementation
- [ ] PROP-001: No hardcoded labels, values, copy, or colours in any feature component
- [ ] PROP-002: Props linked to a DEV_REVIEW §5 gap remain prop-driven — no hardcoded substitute

## CMS — Sitecore / Content Ownership
- [ ] CMS-001: [Sitecore field] mapped via [extractCTA/extractLink/extractFormField]

## API — Backend / API Ownership
> **SKIP for Presentational components** — omit this entire section.
- [ ] API-001: [endpoint] consumed via [HookName] + [ServiceName]
- [ ] API-002: Raw API response transformed by [MapperName] before reaching display components

## COMP — Component Responsibility
- [ ] COMP-001: [ComponentName] does NOT contain API calls
- [ ] COMP-002: [ComponentName] does NOT contain business logic
- [ ] COMP-003: Container/View separation maintained as specified

## DS — Design System Reuse
- [ ] DS-001: [ComponentName] reuses [DesignSystemComponent] with variant [variant]

## RESP — Responsive Behaviour
- [ ] RESP-001: Mobile-first implementation — base classes for mobile, `lg:` for desktop

## A11Y — Accessibility
- [ ] A11Y-001: [interactive element] has aria-label or visible label
- [ ] A11Y-002: All interactive elements are keyboard-navigable

## RTL — RTL / Localisation
- [ ] RTL-001: No `ml-`, `mr-`, `pl-`, `pr-` in layout-critical styles
- [ ] RTL-002: No `text-left` / `text-right` — `text-start` / `text-end` used

## NFR — Non-Functional Requirements
- [ ] NFR-001: [specific NFR requirement from analysis]

## FILE — Folder / File Structure
- [ ] FILE-001: All files created in correct folders per ownership markers
- [ ] FILE-002: Naming conventions followed
- [ ] FILE-003: index.ts barrel exports added

## TEST — Testability / Validation
- [ ] TEST-001: All props testable via prop injection — no hardcoded values
- [ ] TEST-002: All states testable via prop/mock
```

---

## Guardrails

### Always Do
- Complete ALL 13 self-validation checks before producing any document.
- **For Presentational**: skip API checks and API-driven state rows — but **scope UI-interaction rows, never skip them**.
- Verify §10 is non-empty for every classification.
- **Verify DEV_REVIEW.md §5 is populated or explicitly states no gaps.**
- Populate EVERY section of EVERY template.
- Produce documents in order: ANALYSIS_PLAN.md → DEV_REVIEW.md → CODING_AGENT_CHECKLIST.md.
- Save all three to `.SS_WF/Agent/Analysis/` with the ticket ID prefix.
- Route every `Basis`, `Confidence`, `Source`, `Confirmed In` into DEV_REVIEW.md.
- Use exactly four columns in the §1 table.
- **Apply the Part B prohibition check before writing.**
- **Write each document completely in a single write operation where possible.**
- **If a write fails, reuse already-generated content** — read, concatenate, rewrite whole.
- **Verify once** after all three documents are written.

### Never Do
- Never produce any document before completing all 13 checks.
- Never leave a template section empty or with placeholder text.
- **Never leave §10 empty for a Presentational story.**
- **Never leave DEV_REVIEW.md §5 blank.**
- **Never condense or omit a contract gap.**
- Never reference DEV_REVIEW.md inside ANALYSIS_PLAN.md.
- Never write deferred-decision phrases, `Needs clarification`, or `approval required` in the plan.
- **Never leave a `To be resolved in API analysis` marker in the final plan.**
- **Never write a provenance column into ANALYSIS_PLAN.md.**
- **Never restate a project rule in ANALYSIS_PLAN.md.**
- **Never write a separate scope, ownership, container/view, agent-decision or assumptions section.**
- **Never add a fifth column to the Developer Notes Applied table.**
- **Never dump full example payloads or unsurfaced response scenarios into §11.**
- Never produce a generic Code Generation Plan.
- Never omit "Things NOT to Implement", the Data Fetching Pattern, or the Prop-Driven Model.
- **Never assume an append mode exists.**
- **Never lose previously written content** when rewriting a file.
- **Never split a section or table across two writes.**
- **Never write sections out of ascending order.**
- **Never re-read a file you just wrote** merely to confirm success.
- **Never use shell commands to assemble or repair documents.**
- **Never regenerate the full analysis after a write failure.**
- **Never run more than one verification pass.**
- **Never re-open raw API specs, the full catalogue, or raw Figma trees in this phase.**
