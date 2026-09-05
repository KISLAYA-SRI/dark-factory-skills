---
name: analysis-output-contract
description: Use when performing final self-validation and producing all three output documents (ANALYSIS_PLAN.md, DEV_REVIEW.md, CODING_AGENT_CHECKLIST.md) for the FE Story Analysis Agent. Runs 13-section self-validation checklist, prohibition check, and mandatory output templates. Triggers include output contract, self-validation, analysis output, ANALYSIS_PLAN, DEV_REVIEW, CODING_AGENT_CHECKLIST, or Phase-8.
---

# Analysis Output Contract

## Purpose

This skill is the **final phase** of the FE Story Analysis Agent workflow. It has two mandatory responsibilities:

1. **Self-Validation** — Run the complete 13-section checklist to verify all analysis areas are complete and correct before any document is produced.
2. **Output Production** — Generate all three output documents using the mandatory templates defined in this skill, with full detail populated from the analysis completed in Phases 1–7.

> **CRITICAL**: No output document may be produced until ALL self-validation checks are completed. If any check fails, the agent must complete the missing analysis before proceeding to output production.

---

## ⚠️ PHASE 8 CONTEXT RULE — READ FIRST

**All analysis is already complete before Phase 8 begins.** The large raw source artifacts loaded in earlier phases — the full API spec file, the full component catalogue JSON, and the raw Figma design trees — are **no longer needed** and must NOT be re-opened or re-read during Phase 8.

- Do **NOT** re-read the raw API spec file.
- Do **NOT** re-read the full component catalogue.
- Do **NOT** re-read the raw Figma JSON trees.
- If any detail appears to be missing, pull it from the **already-distilled Phase 1–7 outputs** in the current session context — never from re-reading original large files.

Re-reading these large artifacts during Phase 8 multiplies cost on every tool call. Everything needed to write the three documents is already in the analysis results.

---

## PART A — Self-Validation Checklist

Before producing any output document, the Analysis Agent MUST validate whether all required analysis areas have been completed. This checklist is a mandatory quality gate — not optional.

**Rules:**

- You must not hide missing inputs.
- If information is not available in the user story, Figma, Sitecore details or backend API spec, clearly mark it as `Not Provided`.
- If behaviour is recommended using project/frontend best practices, clearly mark it as `Derived`.
- If the analysis depends on developer judgement or had uncertainty, make the best decision, mark the basis clearly, and record it in DEV_REVIEW.md.
- If any task is not completed, do not assume any information and do not provide incorrect information. Complete that analysis before generating the analysis document.

---

### 1. Story Understanding

| Check                          | What to Validate                                      | Status | Notes |
| ------------------------------ | ----------------------------------------------------- | ------ | ----- |
| Story objective understood     | Identify what user/business outcome the story enables |        |       |
| Story scope extracted          | Capture what is in scope for this story               |        |       |
| Out-of-scope items identified  | Capture items explicitly excluded or deferred         |        |       |
| Acceptance criteria mapped     | Each AC is translated into FE implications            |        |       |
| Page/component name identified | Identify target page, section, or component           |        |       |
| Journey context captured       | Identify where user enters this experience from       |        |       |
| Personas/roles captured        | Identify relevant personas if story mentions them     |        |       |

---

### 2. Story Classification

| Check                                   | What to Validate                                           | Status | Notes |
| --------------------------------------- | ---------------------------------------------------------- | ------ | ----- |
| Component classification completed      | Presentational / Transactional / Hybrid                    |        |       |
| Classification rationale documented     | Explain why the classification was chosen                  |        |       |
| Data-fetching responsibility identified | Confirm whether API/BFF data is required                   |        |       |
| CMS-authored responsibility identified  | Confirm whether Sitecore fields/config are required        |        |       |
| FE-only responsibility identified       | Confirm local state, visibility, mapping, and layout logic |        |       |

---

### 3. Developer Notes Compliance

| Check                                           | What to Validate                                                | Status | Notes |
| ----------------------------------------------- | --------------------------------------------------------------- | ------ | ----- |
| Dev Notes extracted before any other analysis   | Scanned Jira story for Developer Notes / Dev Notes section      |        |       |
| All Dev Notes numbered (DN-001, DN-002, ...)    | Every note is numbered and recorded in working list             |        |       |
| Every analysis decision checked against DN list | No topic covered by a Dev Note has a conflicting recommendation |        |       |
| Dev Notes Applied table completed in Section 1  | Table appears as Section 1 of ANALYSIS_PLAN.md                  |        |       |
| Every DN-xxx item appears in the table          | No Dev Note is missing from the Applied table                   |        |       |
| Every DN-influenced item labelled with DN ID    | All analysis items reference their source Dev Note ID           |        |       |

---

### 4. Sitecore / CMS Analysis

| Check                                 | What to Validate                                                                | Status | Notes |
| ------------------------------------- | ------------------------------------------------------------------------------- | ------ | ----- |
| Sitecore input read                   | Confirm Sitecore rendering/layout contract was available                        |        |       |
| Page route captured                   | Route name/path/language/site documented if available                           |        |       |
| Renderings identified                 | List all Sitecore renderings relevant to the story                              |        |       |
| FE mapping identified                 | Map each rendering to FE entry component                                        |        |       |
| Placeholder usage captured            | Identify placeholder where component is placed                                  |        |       |
| Datasource/template noted             | Capture datasource/template name if provided                                    |        |       |
| Authored fields listed                | Identify all CMS-authored labels/copy/config                                    |        |       |
| Rendering parameters listed           | Capture variant/config/default state fields                                     |        |       |
| Authoring boundary defined            | Confirm which components are CMS-authored vs FE-composed                        |        |       |
| Inner FE components not over-authored | Ensure agent does not make every card/tab a Sitecore rendering unless specified |        |       |
| CMS vs FE ownership table created     | Separate Sitecore-authored, FE-controlled, and API-controlled values            |        |       |
| Sitecore gaps captured                | Missing field/template/rendering details documented                             |        |       |

---

### 5. Backend / API Analysis

| Check                                             | What to Validate                                             | Status | Notes |
| ------------------------------------------------- | ------------------------------------------------------------ | ------ | ----- |
| API spec input read                               | Confirm API/OpenAPI details were available, if provided      |        |       |
| Required endpoints identified                     | List endpoint(s) needed for the story                        |        |       |
| HTTP method captured                              | GET/POST/PUT/etc.                                            |        |       |
| Request inputs identified                         | Path/query/body/header requirements                          |        |       |
| ALL request scenarios from YAML extracted         | Every distinct request variant individually listed           |        |       |
| Response fields identified                        | Only fields relevant to FE story extracted                   |        |       |
| ALL response scenarios from YAML extracted        | Every response case (2xx, 4xx, 5xx, empty, partial) listed   |        |       |
| ALL error codes and messages extracted            | Every error code and message from spec listed                |        |       |
| Conditional / nullable fields identified          | Fields that appear only in certain scenarios captured        |        |       |
| Field-to-UI mapping drafted                       | Map API fields to display/view model fields                  |        |       |
| API-owned vs CMS-owned values separated           | Values from API not confused with labels from CMS            |        |       |
| Missing API data captured                         | Any UI field not supported by API response flagged           |        |       |
| Error/loading/empty requirements identified       | UI states needed from API behaviour derived                  |        |       |
| Raw API response not passed to display components | Mapper/view model boundary defined                           |        |       |
| Strict endpoint lookup rule followed              | Only exact endpoint looked up — no folder browsing           |        |       |
| Data fetching pattern produced per endpoint       | Hook / Service / Query Key / Endpoint Constant / State rules |        |       |

---

### 6. Figma / Design Context Analysis

| Check                                  | What to Validate                                                        | Status | Notes |
| -------------------------------------- | ----------------------------------------------------------------------- | ------ | ----- |
| Figma context read                     | Confirm figma data was available                                        |        |       |
| Target frame/node identified           | Node name and type captured                                             |        |       |
| Layer hierarchy reviewed               | Understand visible UI structure                                         |        |       |
| Text/copy ownership inferred carefully | Determine whether labels come from CMS or API/system                    |        |       |
| Icon references noted                  | Capture icon names only, not actual assets                              |        |       |
| Auto-layout/layout hints considered    | Use dimensions/layout only as guidance, not hardcoded implementation    |        |       |
| Design ambiguity captured              | Missing/unclear component intent documented                             |        |       |
| Responsive Reconciliation JSON used    | If both viewports provided, reconciliation JSON used as source of truth |        |       |
| Reconciliation not repeated            | Did not re-reconcile if responsive_design_intent.json already exists    |        |       |

---

### 7. Component Breakdown Analysis

| Check                                        | What to Validate                                                     | Status | Notes |
| -------------------------------------------- | -------------------------------------------------------------------- | ------ | ----- |
| Component hierarchy created                  | Show logical FE hierarchy without file paths                         |        |       |
| Hierarchy uses approved markers              | Use markers like `[design-system]`, `[feature]`, `[Sitecore-mapped]` |        |       |
| Containers separated from display components | Data/state components separated from presentational components       |        |       |
| View component responsibility defined        | Layout composition only                                              |        |       |
| Feature display components identified        | Business-meaningful UI blocks listed                                 |        |       |
| Design-system candidates identified          | Generic reusable UI patterns identified                              |        |       |
| No unnecessary lowest-level atom detail      | Avoid over-documenting atoms/molecules if not needed                 |        |       |
| Component responsibilities documented        | Each component has clear owns/does-not-own definition                |        |       |
| 4-Step Reuse Workflow completed for each     | Every component went through all applicable steps                    |        |       |
| component-catalogue.json consulted           | Reuse decisions based on catalogue, not assumptions                  |        |       |
| Containers excluded from reuse check         | Containers/controllers not validated against catalogue               |        |       |

---

### 8. Props / View Model Analysis

| Check                                | What to Validate                                                       | Status | Notes |
| ------------------------------------ | ---------------------------------------------------------------------- | ------ | ----- |
| Prop-driven model defined            | No hardcoded labels, values, messages, CTA text                        |        |       |
| Prop shape produced per component    | Every component has explicit prop table with source, type, detail      |        |       |
| Sitecore props identified            | Labels/copy/config from CMS                                            |        |       |
| API props identified                 | Runtime values from BFF/API                                            |        |       |
| Derived props identified             | FE-computed flags, visibility, active state                            |        |       |
| View model drafted                   | Clean props shape for view/display components                          |        |       |
| Mapper responsibility defined        | API/CMS data transformed before display                                |        |       |
| Optional/missing data handling noted | Avoid brittle UI assumptions                                           |        |       |
| Sitecore Helpers identified          | extractFormField, extractCTA, extractLink, etc. applied where relevant |        |       |

---

### 9. State, Behaviour and Interaction Analysis

| Check                          | What to Validate                            | Status | Notes |
| ------------------------------ | ------------------------------------------- | ------ | ----- |
| Default state analysed         | Initial render state documented             |        |       |
| Loading state analysed         | Required for API-driven sections            |        |       |
| Error state analysed           | Inline/error boundary/empty handling noted  |        |       |
| Empty state analysed           | No data / partial data behaviour            |        |       |
| Partial data state analysed    | Render available data where appropriate     |        |       |
| Visibility rules analysed      | Persona/role/config-driven visibility       |        |       |
| Interaction behaviour analysed | Tabs, CTA, navigation, expansion, selection |        |       |
| State ownership assigned       | Container/view/component ownership clear    |        |       |

---

### 10. Accessibility, RTL and Responsive Analysis

| Check                             | What to Validate                                      | Status | Notes |
| --------------------------------- | ----------------------------------------------------- | ------ | ----- |
| Semantic structure considered     | Headings, sections, labels, lists                     |        |       |
| Keyboard interaction considered   | Required for tabs/buttons/interactive UI              |        |       |
| ARIA requirements noted           | Only where interactive semantics need support         |        |       |
| RTL readiness considered          | Avoid left/right assumptions                          |        |       |
| Localisation readiness considered | No hardcoded text/copy                                |        |       |
| Responsive behaviour considered   | Desktop/mobile layout implications                    |        |       |
| Design tokens assumed             | Avoid hardcoded colours/spacing where DS tokens exist |        |       |

---

### 11. ANALYSIS_PLAN.md Content Compliance

| Check                                              | What to Validate                                                          | Status | Notes |
| -------------------------------------------------- | ------------------------------------------------------------------------- | ------ | ----- |
| No reference to DEV_REVIEW in ANALYSIS_PLAN.md     | Search for "DEV REVIEW", "DEV_REVIEW", "dev review" must not appear       |        |       |
| No open questions in ANALYSIS_PLAN.md              | No "please confirm", "needs developer approval", "option A or B"          |        |       |
| No deferred decisions in ANALYSIS_PLAN.md          | Every decision is finalised with a clear answer                           |        |       |
| Every uncertain decision recorded in DEV_REVIEW.md | Uncertainty captured with options, decision, reason, and confidence level |        |       |
| ANALYSIS_PLAN.md is 100% actionable                | Coding Agent can act on it without re-analysing the story                 |        |       |
| All 20 required sections present                   | All sections from the output template are populated                       |        |       |

---

### 12. Code Generation Readiness

| Check                               | What to Validate                                                    | Status | Notes |
| ----------------------------------- | ------------------------------------------------------------------- | ------ | ----- |
| Implementation plan created         | Ordered steps for Code Generation Agent                             |        |       |
| Files to create listed              | Every file identified with name and purpose                         |        |       |
| Component creation order defined    | Sequence from root to leaf components                               |        |       |
| Type/model creation order defined   | TypeScript interfaces/types ordered before components that use them |        |       |
| Mapper/helper creation defined      | Mapper files and visibility helpers identified                      |        |       |
| Component assembly sequence defined | How components are composed and wired together                      |        |       |
| State handling placement defined    | Which layer owns which state                                        |        |       |
| Visibility rule placement defined   | Where conditional rendering logic lives                             |        |       |
| Prop-driven wiring defined          | How props flow from Sitecore/API through mapper to display          |        |       |
| Things NOT to implement listed      | Explicit out-of-scope guardrails for Coding Agent                   |        |       |
| Design-system reuse wired           | Reuse decisions from Phase 6 incorporated into the plan             |        |       |
| Index exports included              | Barrel exports planned for all public components                    |        |       |
| Completion checklist referenced     | Plan ends with validate-against-checklist step                      |        |       |
| Component contracts ready           | Props/responsibilities clear                                        |        |       |
| API mapper plan ready               | Mapper/hook/container boundary clear                                |        |       |
| Sitecore prop mapping ready         | CMS fields mapped to FE props                                       |        |       |
| Reuse decisions finalised           | All components have a definitive reuse category                     |        |       |
| Gaps documented                     | Missing API/Sitecore/Figma decisions listed                         |        |       |

---

### 13. Final Analysis Quality Gate

| Check                           | What to Validate                                           | Status | Notes |
| ------------------------------- | ---------------------------------------------------------- | ------ | ----- |
| No unsupported assumptions      | Agent does not invent missing Sitecore/API fields          |        |       |
| No over-fragmentation           | Agent does not create unnecessary components/renderings    |        |       |
| No hardcoded implementation     | Labels/values/config remain prop-driven                    |        |       |
| Ownership boundaries clear      | Sitecore vs API vs FE ownership documented                 |        |       |
| Component hierarchy is readable | Developer and coding agent can follow it                   |        |       |
| Code agent can act on output    | Plan is actionable without re-analysing the story          |        |       |
| Three output files created      | ANALYSIS_PLAN.md, DEV_REVIEW.md, CODING_AGENT_CHECKLIST.md |        |       |
| All files saved to correct path | `.SS_WF/Agent/Analysis/` folder                            |        |       |

---

### Coverage Status Values

Mark each analysis area with one of:

| Status                         | Meaning                                                             |
| ------------------------------ | ------------------------------------------------------------------- |
| `Covered`                      | Analysis completed with sufficient information                      |
| `Partially Covered`            | Analysis done but some details are missing or unclear               |
| `Not Provided`                 | Required input was not available in the story/Figma/API spec        |
| `Derived`                      | Recommendation based on project best practices, not story-confirmed |
| `Not Applicable`               | This area does not apply to this story/component type               |
| `Needs Developer Confirmation` | Decision made but requires developer validation                     |

---

## PART B — ANALYSIS_PLAN.md Content Prohibition (Mandatory Pre-Generation Rule)

> **This check runs BEFORE generating each chunk — not as a post-write cleanup step.**
> Applying this rule before writing eliminates the need for any `sed`/`grep` repair pass.

Before generating content for ANY chunk of ANALYSIS_PLAN.md, confirm that the content you are about to write does NOT contain any of the following:

- `"DEV REVIEW"`, `"DEV_REVIEW"`, `"dev review"`
- `"see DEV REVIEW"`, `"confirm in DEV REVIEW"`, `"Check if supported in DEV REVIEW"`
- `"needs developer approval"`, `"to be confirmed"`, `"pending review"`, `"check with developer"`
- `"option A or B"`, any open question, or any deferred decision

**Every decision written into ANALYSIS_PLAN.md must be final and definitive.** Any uncertainty belongs in DEV_REVIEW.md only.

If you find yourself about to write any of the above phrases into ANALYSIS_PLAN.md, stop — make a definitive decision using the priority order below, write that decision into ANALYSIS_PLAN.md, and record the uncertainty in DEV_REVIEW.md instead:

```
Dev Notes → Project Guidelines → Figma → React/Frontend Best Practices
```

---

## PART C — Output Document Production

After all 13 self-validation checks pass, produce all three output documents in this order. Every section of every template MUST be fully populated — no empty sections, no placeholder text left unfilled.

---

## ⚠️ MANDATORY WRITE RULES — READ BEFORE WRITING ANY DOCUMENT

These rules are **absolute**. Violating any of them is the primary cause of Phase 8 cost overruns.

### Rule 1 — NEVER write a document in a single `write_file` call

This is an **absolute prohibition**. A single oversized `write_file` call will fail with an invalid input format error, forcing a full regeneration pass. Every document MUST be written in multiple chunks.

### Rule 2 — Write in strict ascending section order (1 → 20)

Maintain an explicit **section cursor** tracking the last section written. Before writing the next chunk, verify:

- Previous chunk's highest section = (next chunk's lowest section − 1)
- If a gap is detected: re-emit the missing chunk **in order** before proceeding
- **Never skip ahead to a later section** — write every section in sequence

The document is assembled **exclusively** through sequential `write_file` create/append calls in ascending section order. **Shell-based file reconstruction is prohibited.**

### Rule 3 — Use `create` for chunk 1, `append` for all subsequent chunks

- **First chunk** of each document → `write_file` with `mode: create`
- **Every later chunk** of the same document → `write_file` with `mode: append`

### Rule 4 — Retry cap: 3 attempts per chunk, then condense and continue

If a `write_file` chunk fails:

1. Retry the **same chunk with identical content** — attempt 2
2. If it fails again — retry once more — attempt 3
3. If it fails a third time: write a **condensed version** of that chunk (reduce tables to key rows only) and continue to the next chunk
4. Log inline: `[WRITE FAILED: Section X — condensed]` in the next successful chunk
5. **Never regenerate the entire document** on a chunk failure
6. **Never restart the analysis** or loop back to an earlier phase because of a write failure

### Rule 5 — Confirm each chunk before proceeding

After each `write_file` call, verify the tool returned success before writing the next chunk. If it did not return success, apply Rule 4.

### Rule 6 — No intermediate re-reads between chunks

Do **not** re-read the document between chunk writes. Rely on the section cursor (Rule 2) to track progress — not on reading the file back. This is the single biggest cost multiplier in Phase 8.

### Rule 7 — Shell/CLI file reconstruction is absolutely prohibited

Do **not** use `cat`, `cp`, `sed`, `head`, `tail`, temp-file merges, header-prepend tricks, or any other shell command to assemble, repair, or reorder documents. If a file is discovered to be out of order or incomplete, the only permitted recovery is:

- Overwrite from scratch: `write_file` with `mode: create` for chunk 1
- Then append chunks 2..N in order

Never patch a file with shell surgery.

### Rule 8 — One consolidated validation pass after ALL documents are written

Perform **at most one** final validation pass after all three documents are fully written. That single pass checks:

- All three files exist
- ANALYSIS_PLAN.md has all 20 section headers
- No prohibited phrases are present in ANALYSIS_PLAN.md

Do this in **one combined check** — not a series of separate commands. Remove all intermediate `cat`/`head`/`tail`/`wc`/`grep` inspection steps.

---

## Chunk Boundaries — Mandatory

### ANALYSIS_PLAN.md — 7 chunks

| Chunk | Mode     | Sections                                                                                          |
| ----- | -------- | ------------------------------------------------------------------------------------------------- |
| 1     | `create` | Header + Section 1 (Dev Notes Applied) + Section 2 (Story Summary)                                |
| 2     | `append` | Section 3 (Classification) + Section 4 (Derived Scope) + Section 5 (AC Analysis)                  |
| 3     | `append` | Section 6 (Agent Decisions) + Section 7 (Component Hierarchy) + Section 8 (Responsibility Matrix) |
| 4     | `append` | Section 9 (Container/View) + Section 10 (Folder Structure) + Section 11 (Code Generation Plan)    |
| 5     | `append` | Section 12 (Assumptions) + Section 13 (Interactions) + Section 14 (State/Edge Cases)              |
| 6     | `append` | Section 15 (Ownership) + Section 16 (Sitecore API Analysis) + Section 17 (BFF API Analysis)       |
| 7     | `append` | Section 18 (Prop Model) + Section 19 (Reuse Validation) + Section 20 (NFR Analysis)               |

**Section cursor after each chunk:**

- After Chunk 1: cursor = 2
- After Chunk 2: cursor = 5
- After Chunk 3: cursor = 8
- After Chunk 4: cursor = 11
- After Chunk 5: cursor = 14
- After Chunk 6: cursor = 17
- After Chunk 7: cursor = 20 ✓ COMPLETE

### DEV_REVIEW.md — 1 chunk

| Chunk | Mode     | Sections                                                             |
| ----- | -------- | -------------------------------------------------------------------- |
| 1     | `create` | Header + Section 1 + Section 2 + Section 3 (entire document — small) |

### CODING_AGENT_CHECKLIST.md — 2 chunks

| Chunk | Mode     | Sections                                                      |
| ----- | -------- | ------------------------------------------------------------- |
| 1     | `create` | Header + DN + AC + INT + STATE + SCOPE + PROP                 |
| 2     | `append` | CMS + API + COMP + DS + RESP + A11Y + RTL + NFR + FILE + TEST |

---

## Document 1: ANALYSIS_PLAN.md

**File path:** `.SS_WF/Agent/Analysis/{{ticket_id}}_ANALYSIS_PLAN.md`

> **ABSOLUTE PROHIBITION**: This document must NEVER reference DEV_REVIEW.md or contain any deferred decision. Apply the Part B prohibition check BEFORE generating each chunk's content.

**Required Sections (in order — ALL must be populated):**

```markdown
# ANALYSIS PLAN {{ticket_id}}

---

## 1. Developer Notes Applied

> ALWAYS first — even if no Dev Notes found.

| DN ID  | Dev Note (verbatim) | Applied Where | Impact on Analysis |
| ------ | ------------------- | ------------- | ------------------ |
| DN-001 |                     |               |                    |

> If no Dev Notes found: "No Developer Notes found in this story. Normal source priority order applies."

---

## 2. Story Summary

- **Story Title:** [exact JIRA title]
- **Page / Component:** [target page or component name]
- **User Goal:** [what the user is trying to achieve]
- **Business Intent:** [why this feature exists]
- **Journey Context:** [where this sits in the user journey]
- **Default View / State:** [what the user sees on first load]
- **Major UI Sections:** [named visible regions]
- **Personas / Roles:** [relevant personas if mentioned]
- **Dependencies:** [other stories, components, systems]

---

## 3. Classification Rationale

- **Classification:** Presentational / Transactional / Hybrid
- **Rationale:** [one clear sentence explaining why]
- **Data-Fetching Required:** Yes / No
- **CMS-Authored Required:** Yes / No
- **FE-Only Logic:** [local state, visibility, mapping, layout logic summary]

---

## 4. Derived Scope

**In Scope:**

- [item 1]
- [item 2]

**Out of Scope (Derived):**

- [item 1] — Reason: [why derived as out of scope]
- [item 2] — Reason: [why derived as out of scope]

---

## 5. Acceptance Criteria Analysis

| AC ID  | AC Statement | FE Implication | Owner Component | State / Interaction Impact | Agent Decision | Basis |
| ------ | ------------ | -------------- | --------------- | -------------------------- | -------------- | ----- |
| AC-001 |              |                |                 |                            |                |       |

---

## 6. Agent Decision Summary

| Decision Area | Decision Made | Basis | Confidence |
| ------------- | ------------- | ----- | ---------- |
|               |               |       |            |

---

## 7. Proposed Component Hierarchy
```

[ComponentName] [Sitecore-mapped]
[ComponentName] [container]
[ComponentName] [view]
[ComponentName] [feature]
[ComponentName] [design-system]
[ComponentName] [feature]

```

> Markers: `[design-system]` | `[feature]` | `[Sitecore-mapped]` | `[container]` | `[view]`
> No file paths in this diagram.

---

## 8. Component Responsibility Matrix

| Component | Type | Owns | Logic Allowed | Must NOT Own |
| --- | --- | --- | --- | --- |
| | | | | |

---

## 9. Container / View Decision

| Component | Container? | View? | Reason |
| --- | --- | --- | --- |
| | | | |

---

## 10. Folder Structure Proposal

```

Portals/Sme/Features/[DomainName]/[FeatureName]/
Components/
[ComponentName].tsx
Hooks/
use[FeatureName]Data.ts
Services/
[FeatureName]Service.ts
Types/
[FeatureName]Types.ts
Constants/
[FEATURE_NAME]_CONSTANTS.ts
index.ts

Packages/Cms/CmsComponents/[ComponentName]/
[ComponentName].tsx
index.ts

```

---

## 11. Code Generation Plan

> The generated code plan must be ordered and implementation-ready.

### Files to Create

| # | File Name | Path | Purpose |
| - | --- | --- | --- |
| 1 | | | |

### Ordered Implementation Steps

1. **Create root Sitecore-mapped component**
2. **Create type files**
3. **Create display components**
4. **Create container (if required)**
5. **Create view component (if required)**
6. **Create feature display components**
7. **Create mapper files**
8. **Create visibility helper (if needed)**
9. **Wire design-system reuse points**
10. **Add index exports**
11. **Validate against CODING_AGENT_CHECKLIST.md**

### State Handling Placement

| State | Owned By | Mechanism |
| --- | --- | --- |
| Loading | Container | `isLoading` from useQuery |
| Error | Container | `isError` from useQuery |
| Empty | Container | Check `data` length/null |

### Visibility Rule Placement

| Visibility Rule | Condition | Placed In | Passed As Prop? |
| --- | --- | --- | --- |
| | | | |

### Prop-Driven Wiring

| Prop Flow Step | From | To | Prop Name | Transformation |
| --- | --- | --- | --- | --- |
| | | | | |

### Things NOT to Implement

- [item 1 — with reason]
- [item 2 — with reason]

---

## 12. Assumptions and Decisions Made

| Area | Assumption / Decision | Basis | Confidence |
| --- | --- | --- | --- |
| | | | |

---

## 13. Interaction Analysis

| Interaction ID | Interaction Description | Trigger | Owner Component | State Impact | Confirmed In | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| INT-001 | | | | | Story / Figma / Derived | |

---

## 14. State, Error and Edge Case Analysis

| State / Edge Case | Applicable Component | Trigger / Condition | Expected FE Behaviour | Source |
| --- | --- | --- | --- | --- |
| Loading | | API call in progress | Show skeleton | Derived |

---

## 15. Sitecore / Backend / Frontend Ownership

| Area | Expected Source | Owner | Notes |
| --- | --- | --- | --- |
| | | | |

---

## 16. Sitecore API Analysis

> If not applicable: `SITECORE API NOT FOUND / NOT REQUIRED`

---

## 17. BFF API Analysis

> If not applicable: `BFF API NOT FOUND / NOT REQUIRED`

---

## 18. Prop-Driven Component Model

[For every component in the hierarchy:]

**Component: [ComponentName]**
Type: [Sitecore-mapped / Container / View / Feature Display / Design System]

| Prop Name | Type | Source | Source Detail (field/endpoint) | Required? | Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 19. Component Inventory & Reuse Validation

| Component | Atomic Level | Reuse Decision | Existing Component | Gap / Enhancement | New Component Name | Catalogue Update? |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## 20. Responsive / Accessibility / RTL / NFR Analysis

| NFR Category | Applies? | Agent Decision / Recommendation | Source |
| --- | --- | --- | --- |
| RTL | Yes/No | | Story / Figma / Derived |
| Accessibility | Yes/No | | Story / Figma / Derived |
| Responsive | Yes/No | | Story / Figma / Derived |
| Overflow & Scroll | Yes/No | | Story / Figma / Derived |
```

---

## Document 2: DEV_REVIEW.md

**File path:** `.SS_WF/Agent/Analysis/{{ticket_id}}_DEV_REVIEW.md`

> This document is for the developer to review **after** development is complete. It contains ONLY decisions made under uncertainty, assumptions due to missing information, and conflicts resolved.

**Write in 1 chunk (entire document is small — fits in a single `create` call).**

**Required Sections (ALL must be populated — write "None" if no items):**

```markdown
# DEV REVIEW {{ticket_id}}

---

## 1. Decisions Made Under Uncertainty

| Decision ID | Area | Options Considered | Decision Made | Reason | Confidence Level    |
| ----------- | ---- | ------------------ | ------------- | ------ | ------------------- |
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
```

---

## Document 3: CODING_AGENT_CHECKLIST.md

**File path:** `.SS_WF/Agent/Analysis/{{ticket_id}}_CODING_AGENT_CHECKLIST.md`

> A validation checklist the Code Generation Agent MUST complete before marking implementation done. Every item is derived from the analysis in ANALYSIS_PLAN.md.

**Write in 2 chunks:**

- **Chunk 1 (`create`):** Header + DN + AC + INT + STATE + SCOPE + PROP
- **Chunk 2 (`append`):** CMS + API + COMP + DS + RESP + A11Y + RTL + NFR + FILE + TEST

**Required Sections (ALL must be populated with story-specific items):**

```markdown
# CODING AGENT CHECKLIST {{ticket_id}}

> This checklist must be completed before marking implementation done.
> Every item is derived from the analysis in ANALYSIS_PLAN.md.

---

## DN — Developer Notes Compliance (ALWAYS first)

- [ ] DN-001: [verbatim dev note — confirm implemented as specified]

---

## AC — Acceptance Criteria

- [ ] AC-001: [AC statement] — [what FE must do to satisfy it]

---

## INT — Interaction Behaviour

- [ ] INT-001: [interaction] — [expected FE behaviour]

---

## STATE — State / Error / Empty Behaviour

- [ ] STATE-001: Loading state renders [skeleton/spinner] in [component]
- [ ] STATE-002: Error state renders [error message/boundary] in [component]
- [ ] STATE-003: Empty state renders [empty UI] in [component]

---

## SCOPE — Out-of-Scope Protection

- [ ] SCOPE-001: [out-of-scope item] NOT implemented in this story

---

## PROP — Prop-Driven Implementation

- [ ] PROP-001: No hardcoded labels, values, copy, or colours in any feature component

---

## CMS — Sitecore / Content Ownership

- [ ] CMS-001: [Sitecore field] mapped via [extractCTA/extractLink/extractFormField]

---

## API — Backend / API Ownership

- [ ] API-001: [endpoint] consumed via [HookName] + [ServiceName]
- [ ] API-002: Raw API response transformed by [MapperName] before reaching display components

---

## COMP — Component Responsibility

- [ ] COMP-001: [ComponentName] does NOT contain API calls
- [ ] COMP-002: [ComponentName] does NOT contain business logic
- [ ] COMP-003: Container/View separation maintained as specified

---

## DS — Design System Reuse

- [ ] DS-001: [ComponentName] reuses [DesignSystemComponent] with variant [variant]

---

## RESP — Responsive Behaviour

- [ ] RESP-001: Mobile-first implementation — base classes for mobile, `lg:` for desktop

---

## A11Y — Accessibility

- [ ] A11Y-001: [interactive element] has aria-label or visible label
- [ ] A11Y-002: All interactive elements are keyboard-navigable

---

## RTL — RTL / Localisation

- [ ] RTL-001: No `ml-`, `mr-`, `pl-`, `pr-` in layout-critical styles — logical properties used
- [ ] RTL-002: No `text-left` / `text-right` — `text-start` / `text-end` used

---

## NFR — Non-Functional Requirements

- [ ] NFR-001: [specific NFR requirement from analysis]

---

## FILE — Folder / File Structure

- [ ] FILE-001: All files created in correct folders per Folder Structure Proposal
- [ ] FILE-002: Naming conventions followed (PascalCase components, camelCase hooks, etc.)
- [ ] FILE-003: index.ts barrel exports added

---

## TEST — Testability / Validation

- [ ] TEST-001: All props are testable via prop injection — no hardcoded values
- [ ] TEST-002: All states (loading, error, empty, success) are testable via prop/mock
```

---

## Guardrails

### Always Do

- Complete ALL 13 self-validation checks before producing any document.
- If any check fails — complete the missing analysis first, then re-run the check.
- Populate EVERY section of EVERY template — no empty sections, no placeholder text left unfilled.
- Produce all three documents in order: ANALYSIS_PLAN.md → DEV_REVIEW.md → CODING_AGENT_CHECKLIST.md.
- Save all three files to `.SS_WF/Agent/Analysis/` with the correct ticket ID prefix.
- Populate the Code Generation Plan (Section 11) with story-specific files, order, state handling, visibility rules, prop wiring, and things NOT to implement.
- Derive CODING_AGENT_CHECKLIST.md items from the actual analysis — not generic boilerplate.
- **Apply the Part B prohibition check BEFORE generating each chunk's content** — not after writing.
- **Write ANALYSIS_PLAN.md in exactly 7 chunks** using the mandatory chunk boundaries above.
- **Write DEV_REVIEW.md in 1 chunk** (entire document — small).
- **Write CODING_AGENT_CHECKLIST.md in 2 chunks** using the mandatory chunk boundaries above.
- **Use `mode: create` for chunk 1 of each document; `mode: append` for all subsequent chunks.**
- **Maintain the section cursor** — write sections in strict ascending order (1 → 20), no exceptions.
- **Confirm each `write_file` call succeeded** before writing the next chunk.
- **If a chunk fails, retry the same chunk up to 2 more times (3 total)** before condensing.
- **After all three documents are written, run exactly one consolidated validation pass.**

### Never Do

- Never produce any document before completing all 13 self-validation checks.
- Never leave a template section empty or with placeholder text.
- Never reference DEV_REVIEW.md inside ANALYSIS_PLAN.md.
- Never write "DEV REVIEW", "DEV_REVIEW", "dev review", "see DEV REVIEW", "confirm in DEV REVIEW", "needs developer approval", "to be confirmed", "pending review", "option A or B", or any open question / deferred decision in ANALYSIS_PLAN.md.
- Never produce a Code Generation Plan that is generic — it must be specific to this story.
- Never omit the "Things NOT to Implement" section from the Code Generation Plan.
- Never omit the Data Fetching Pattern from the BFF API Analysis section.
- Never omit the Prop-Driven Component Model — every component must have its prop table.
- **Never write an entire document in a single `write_file` call** — always use the mandatory chunk boundaries.
- **Never write chunks out of order** — sections must be written in strict ascending order.
- **Never re-read the document between chunk writes** — use the section cursor, not file reads.
- **Never use shell commands (`cat`, `cp`, `sed`, `head`, `tail`, temp-file merges) to assemble or repair documents.**
- **Never retry a failed chunk more than 2 additional times** — condense and continue instead of looping.
- **Never regenerate the full analysis output after a write failure** — reuse already-computed content.
- **Never restart the analysis or loop back to an earlier phase** because of a write failure.
- **Never run more than one validation pass** — one combined check after all three documents are written.
- **Never re-open the raw API spec, full component catalogue, or raw Figma JSON trees during Phase 8.**
