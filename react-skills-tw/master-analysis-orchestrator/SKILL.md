---
name: master-analysis-orchestrator
description: Use when orchestrating the complete end-to-end FE Story Analysis workflow. Defines the mandatory phase sequence, decision gates between phases, skill invocation map, and quality standards the final output must meet before being passed to the Coding Agent. Triggers include story analysis, analysis agent, FE analysis workflow, or analysis orchestration. Invoked when the user says something like "Implement JIRA <TICKET_ID>" or "Analyse JIRA <TICKET_ID>"
---

# Master Analysis Orchestrator

## Purpose

This is the **master orchestration skill** for the FE Story Analysis Agent. It defines:

1. **What** the Analysis Agent must do — the complete analysis scope.
2. **In what order** — the mandatory execution sequence of all sub-skills.
3. **How** each skill's output feeds into the next skill.
4. **What quality gates** must pass before the final output is produced.
5. **What three documents** must be generated at the end.

The Analysis Agent MUST follow this master skill as its primary execution blueprint. All other skills are invoked from within this master skill at the correct phase.

---

## Core Mandate

You are the **FE Story Analysis Agent**. Your job is to:

- Analyse a frontend user story end-to-end.
- Make every decision yourself — no open questions, no deferred approvals, no options to choose from.
- Produce three output documents that go **directly to the Code Generation Agent** (no developer review beforehand).
- Apply the priority order at all times: **Dev Notes → Figma → React/Frontend Best Practices**.

> ⚠️ **CRITICAL**: The Coding Agent receives your output BEFORE any developer sees it. Every decision must be finalised. Zero ambiguity is permitted in ANALYSIS_PLAN.md.

---

## Inputs Available to the Analysis Agent

Before starting, confirm what inputs are available:

| Input                       | Source                                           | Required?                         |
| --------------------------- | ------------------------------------------------ | --------------------------------- |
| JIRA User Story             | `.SS_WF/{{$var[ticket_id]s}}_jira_output.json`   | **Mandatory**                     |
| Developer Notes / Dev Notes | Section inside the JIRA story                    | If present — SACRED LAW           |
| Sitecore API Spec           | Cloned under `{{$var[BITBUCKET_SC_CLONE_DIR]s}}` | If Sitecore endpoints in story    |
| BFF API Spec (YAML)         | Cloned under `{{$var[BITBUCKET_CLONE_DIR]s}}`    | If BFF endpoints in story         |
| Component Catalogue         | `component-catalogue.json` at repo root          | **Mandatory** for reuse decisions |

---

## Mandatory Execution Sequence

The Analysis Agent MUST execute all phases in the exact order below. No phase may be skipped. No phase may be reordered.

```
PHASE 0  →  PHASE 1  →  PHASE 2  →  PHASE 4  →  PHASE 3  →  PHASE 5  →  PHASE 6  →  PHASE 8  →  OUTPUT
```

Run phases strictly in order. Load ONE sub-skill's context per phase and discard it before the next phase to conserve tokens.

---

## PHASE 0 — Pre-Analysis Setup (Mandatory Before Everything Else)

### 0.1 — Folder Pre-Check

Before writing any file:

1. Confirm `/.SS_WF/` already exists — do NOT create a new `.SS_WF` folder.
2. Confirm `/.SS_WF/Agent/Analysis/` exists — create only if missing.
3. All three output files will be saved to `.SS_WF/Agent/Analysis/`.

### 0.2 — Context Reuse Rule

Read and process each referenced file, document, or specification **only once** per execution. Once loaded into working context, reuse the already-available content. Do not re-fetch, re-read, or re-process the same source again.

### 0.3 — Confirm Inputs Available

Scan and record which inputs are available. Do not invent missing inputs. If an input is missing, mark the relevant analysis section as `Not Provided`.

---

## PHASE 1 — Developer Notes Extraction

> **Invoke: `developer-notes-protocol`**

This is the **first and highest-priority phase**. It MUST complete before any other analysis begins.

### What to Do

1. Scan the JIRA user story for any Developer Notes / Dev Notes section.
2. Extract every instruction verbatim and number them: `DN-001`, `DN-002`, `DN-003` …
3. Store them as an active working list that remains live throughout ALL subsequent phases.
4. For EVERY decision made in Phases 2–7, check: "Does a Dev Note cover this topic?"
   - If YES → The Dev Note IS the answer. Do not produce an alternative.
   - If NO → Proceed with normal source priority order.

### Gate: Phase 1 Complete When

- [ ] JIRA story scanned for Developer Notes.
- [ ] All Dev Notes extracted, numbered, and stored in working list.
- [ ] If no Dev Notes found — explicitly recorded: "No Developer Notes found. Normal source priority order applies."

> ⚠️ **If this phase is skipped, the entire analysis is invalid.**

---

## PHASE 2 — Figma Fetch, Reconcile, and Analyse

> **Invoke: `figma-fetch-reconcile-and-analyse`**

This phase runs BEFORE story analysis so that Figma context is available to inform component planning.

### What to Do

**Step 2.1 — Check Figma Availability**

Check whether Figma context JSON files already exist under `/figma-output/`:

- If they exist → skip Phase 1 of `figma-fetch-reconcile-and-analyse` (Figma fetch) and use the existing files.
- If they do not exist → execute Phase 1 of `figma-fetch-reconcile-and-analyse` to fetch Figma design intent from all Figma URLs in the JIRA story.

**Step 2.2 — Reconciliation (Conditional)**

- If BOTH mobile and desktop Figma context files are available → execute Phase 2 of `figma-fetch-reconcile-and-analyse` (reconciliation) to produce `responsive_design_intent.json`.
- If only one viewport is available → skip reconciliation. Use the single context file directly.
- If `responsive_design_intent.json` already exists → do NOT re-reconcile. Use the existing file.

**Step 2.3 — Figma Context Ready**

After this phase, the following are available for use in all subsequent phases:

- Mobile Design Context JSON (if available)
- Desktop Design Context JSON (if available)
- Responsive Reconciliation JSON (if both viewports were provided)

### Gate: Phase 2 Complete When

- [ ] Figma context files confirmed or fetched.
- [ ] Reconciliation performed if both viewports available.
- [ ] Figma inputs are ready for use in story analysis.

---

## PHASE 4 — API Analysis

> **Invoke: `api-analysis-sitecore-and-bff`**

> ⚠️ **This phase runs BEFORE Phase 3 (Story Analysis).** Both Sitecore and BFF API contracts must be fetched and fully analysed first, so that API data, request/response scenarios, and field contracts are available to inform and correlate with the story analysis in Phase 3.

This phase performs BOTH Sitecore API and BFF API analysis. There is no separate API analysis agent.

### What to Do

**Step 4.1 — Sitecore API Analysis**

1. Identify Sitecore endpoints from the JIRA story.
2. If no Sitecore endpoints found → mark section as `SITECORE API NOT FOUND / NOT REQUIRED`.
3. If found → look up ONLY the exact endpoint in `{{$var[BITBUCKET_SC_CLONE_DIR]s}}`.
   - Do NOT browse folders, list files, or fall back to similar files.
   - If exact file not found → mark as `SITECORE API CONTRACT NOT FOUND — endpoint [name] could not be located.`
4. Analyse: CMS rendering to FE component mapping, CMS-authored props, missing fields.

**Step 4.2 — BFF API Analysis**

1. Identify BFF endpoints from the JIRA story.
2. If no BFF endpoints found → mark section as `BFF API NOT FOUND / NOT REQUIRED`.
3. If found → look up ONLY the exact endpoint in `{{$var[BITBUCKET_CLONE_DIR]s}}`.
   - Do NOT browse folders, list files, or fall back to similar files.
   - If exact file not found → mark as `BFF API CONTRACT NOT FOUND — endpoint [name] could not be located.`
4. Read the **complete** YAML/JSON spec file — do NOT skim.
5. Extract and analyse:
   - ALL request scenarios (every variant, optional vs required fields)
   - ALL response scenarios (2xx, 4xx, 5xx, empty, partial data)
   - ALL error codes and messages
   - ALL conditional / nullable fields
   - ALL example payloads

> ⚠️ **MANDATORY**: Every request scenario and every response scenario MUST be individually listed. Omitting any scenario is a critical failure.

### Gate: Phase 4 Complete When

- [ ] Sitecore API section completed (or marked NOT REQUIRED).
- [ ] BFF API section completed (or marked NOT REQUIRED).
- [ ] All request scenarios individually listed.
- [ ] All response scenarios individually listed.
- [ ] All error codes listed.
- [ ] All conditional/nullable fields listed.
- [ ] Strict endpoint lookup rule followed — no folder browsing.
- [ ] API analysis output is ready to be used in Phase 3 story analysis.

---

## PHASE 3 — Story Analysis End to End

> **Invoke: `story-analysis-end-to-end`**

> ⚠️ **Prerequisite**: Phase 4 (API Analysis) MUST be complete before this phase begins. The API contracts fetched in Phase 4 must be actively used during story analysis to correlate API data with story functionality, ACs, ownership, and prop models.

This phase performs complete end-to-end analysis of the user story. All 11 steps of `story-analysis-end-to-end` must be executed in order. No step may be skipped.

### What `story-analysis-end-to-end` Covers (in order)

1. **Story Understanding** — title, goal, intent, journey context, major UI sections, persona/role variations, dependencies
2. **Component Classification** — Presentational / Transactional / Hybrid with rationale
3. **Scope Derivation** — in-scope and out-of-scope items derived from story wording, ACs, Figma, and missing detail
4. **Acceptance Criteria Analysis** — every AC assigned a stable ID, FE implication, owner component, state/interaction impact, and agent decision
5. **Interaction Analysis** — all interactions from story and Figma; Figma-only interactions labelled separately
6. **State and Edge Case Analysis** — all states and edge cases analysed; derived ones marked clearly
7. **Ownership Separation** — Sitecore, API, and FE ownership clearly separated for every content/data item; correlated with Phase 4 API contracts
8. **NFR Analysis** — RTL, Accessibility, Responsive Design, Overflow & Scroll Handling (Sections 6, 7, 9, 10 of `react-nextjs-best-practices` only)

### Gate: Phase 3 Complete When

- [ ] Story fully understood — title, goal, intent, journey context, major sections recorded.
- [ ] Component classified as Presentational / Transactional / Hybrid with rationale.
- [ ] In-scope and out-of-scope items clearly listed.
- [ ] All ACs analysed with FE implications, owner components, and state/interaction impact.
- [ ] All interactions identified — story-confirmed and Figma-visible ones labelled separately.
- [ ] All states and edge cases analysed.
- [ ] Ownership table produced — Sitecore, API, and FE ownership clearly separated.
- [ ] NFR analysis completed for RTL, Accessibility, Responsive Design, and Overflow & Scroll Handling.
- [ ] Every Dev Note applied and labelled with DN ID
- [ ] Every uncertain decision recorded in DEV_REVIEW.md, not in ANALYSIS_PLAN.md

---

## PHASE 5 — Component Breakdown and Hierarchy

> **Invoke: `component-breakdown-and-hierarchy`**

This phase produces the complete component hierarchy and folder structure.

### What to Do

**Step 5.1 — Apply Breakdown Logic**

Based on the classification from Phase 3:

- If **Presentational** → apply Presentational Breakdown Rules (P1–P8 from `component-breakdown-and-hierarchy`).
- If **Transactional** → apply Transactional Breakdown Rules (T1–T8 from `component-breakdown-and-hierarchy`).
- If **Hybrid** → apply both sets of rules to the appropriate sections.

**Step 5.2 — Build Component Hierarchy**

Produce a clean tree diagram of the component hierarchy:

- Use approved markers: `[design-system]`, `[feature]`, `[Sitecore-mapped]`, `[container]`, `[view]`.
- Do NOT include file paths in the hierarchy diagram.
- Separate containers from display components.
- Do not create a component for every icon, label, or text row.

**Step 5.3 — Component Responsibility Matrix**

For every component in the hierarchy, define:

- Responsibility (what it owns)
- Logic allowed (rendering / state / API / layout only)
- What it must NOT own

**Step 5.4 — Folder Structure Proposal**

Propose the folder/file structure following the rules in `component-breakdown-and-hierarchy`:

- Reusable UI elements → `Packages/DesignSystem/Foundation/Src/{Atoms,Molecules,Organisms}/`
- Sitecore-mapped components → `Packages/Cms/CmsComponents/<ComponentName>/`
- Domain-specific features → `Portals/Sme/Features/<DomainName>/<FeatureName>/`
  - Sub-folders: `Components/`, `Hooks/`, `Services/`, `Types/`, `Constants/`
  - Barrel: `index.ts`
- Cross-domain shared → `Portals/Sme/Features/Shared/<ComponentName>/`

Apply naming conventions:

- Component files (`.tsx`) → PascalCase
- Hook files (`.ts`) → camelCase, starts with `use`
- Service files (`.ts`) → PascalCase, ends with `Service`
- Type files (`.ts`) → PascalCase, ends with `Types`
- Constants files (`.ts`) → SCREAMING_SNAKE_CASE, ends with `_CONSTANTS`
- Test files → same as source + `.test.tsx` / `.test.ts`

### Gate: Phase 5 Complete When

- [ ] Component hierarchy tree produced.
- [ ] Component responsibility matrix completed.
- [ ] Folder/file structure proposed with correct naming conventions.
- [ ] No file paths inside hierarchy diagram.
- [ ] Containers separated from display components.

---

## PHASE 6 — Component Reuse Validation

> **Invoke: `component-reuse-validation`**

This phase validates every component against `component-catalogue.json`. There is no separate Component Reuse Agent — all reuse analysis is performed here.

### What to Do

For every applicable component identified in Phase 5, execute the **4-Step Component Reuse Decision Workflow** in this exact sequence:

**Step 6.1 — Classify Atomic Level (ALWAYS first)**

Classify as: Atom / Molecule / Organism.
Record: `Component: [Name] | Atomic Level: Atom/Molecule/Organism | Reason: [one-line justification]`

**Step 6.2 — Exact Match Check Against `component-catalogue.json`**

- Check whether the component exists with an exact match (name/purpose, visual pattern, required variant/state/config).
- If exact match found → assign `Reuse existing variant`. Specify component name, variant/config, props. **STOP.**
- If no exact match → proceed to Step 6.3.

**Step 6.3 — Partial Match Check (Catalogue + Code Verification)**

- Check whether a related component covers the same pattern but is missing a specific variant, state, prop, or configuration.
- If partial match found in catalogue:
  > ⚠️ **MANDATORY CODE CHECK**: Before assigning `Enhance existing component`, check the component's actual source code to verify the required variant/state does NOT already exist in code.
  - If variant/state IS found in code → treat as exact match. Assign `Reuse existing variant`. **STOP.**
  - If variant/state IS NOT found in code → assign `Enhance existing component`. Specify: existing component name, current gap, proposed new prop/variant/slot/state, backward compatibility impact, approval required: Yes. **STOP.**
- If no partial match → proceed to Step 6.4.

**Step 6.4 — No Match: Evaluate Reuse Potential**

Evaluate:

- Is the pattern generic and business-neutral? → Propose as reusable design-system component.
- Could it be used in more than one feature or page? → Propose as reusable (atom/molecule/organism).
- Is it tightly coupled to a specific business domain or API shape? → Propose as feature-specific component.

Assign:

- `Create new reusable component` — with proposed name, atomic level, expected props, expected variants, expected states, Storybook required: Yes, catalogue update required: Yes.
- `Create feature-specific component` — with feature component name, reason it is feature-specific, which existing catalogue/design-system components it reuses internally, expected props.

### Exclusions — Do NOT validate for reuse:

- Containers / controllers
- Mapper files
- Hook files
- Type files
- Visibility utilities
- API service files

### Gate: Phase 6 Complete When

- [ ] Every applicable component has gone through all 4 steps.
- [ ] No step skipped for any component.
- [ ] Every component has a definitive reuse category assigned.
- [ ] Code check performed for every partial match (Step 6.3).
- [ ] Containers/controllers excluded from reuse check.
- [ ] `component-catalogue.json` used as the ONLY source of truth for existence validation.

---

## PHASE 8 — Self-Validation and Output Production

> **Invoke: `analysis-output-contract`**

This phase has **two mandatory responsibilities** executed in sequence:

1. **Part A: Self-Validation** — Run the complete 13-section checklist to verify all analysis areas are complete and correct.
2. **Part B: ANALYSIS_PLAN.md Content Prohibition Check** — Scan for and remove any prohibited phrases.
3. **Part C: Output Production** — Generate all three output documents using the mandatory templates from `analysis-output-contract`, with full detail populated from Phases 1–7.

> ⚠️ **CRITICAL**: No output document may be produced until ALL self-validation checks pass. If any check fails, the agent must complete the missing analysis before proceeding.

### What to Do

**Step 8A — Self-Validation (13 Sections)**

Run through all 13 checklist sections from `analysis-output-contract` Part A:

1. Story Understanding
2. Story Classification
3. Developer Notes Compliance
4. Sitecore / CMS Analysis
5. Backend / API Analysis (including Data Fetching Pattern per endpoint)
6. Figma / Design Context Analysis
7. Component Breakdown Analysis
8. Props / View Model Analysis (including prop shape per component)
9. State, Behaviour and Interaction Analysis
10. Accessibility, RTL and Responsive Analysis
11. ANALYSIS_PLAN.md Content Compliance
12. Code Generation Readiness (including ordered plan with files, state handling, visibility rules, prop wiring, things NOT to implement)
13. Final Analysis Quality Gate

For each check, mark as: `Covered` / `Partially Covered` / `Not Provided` / `Derived` / `Not Applicable` / `Needs Developer Confirmation`.

**Step 8B — ANALYSIS_PLAN.md Content Prohibition Check**

Before producing ANALYSIS_PLAN.md, search the entire analysis output for:

- `"DEV REVIEW"`, `"DEV_REVIEW"`, `"dev review"`
- `"Check if supported in DEV REVIEW"`, `"Confirm in DEV REVIEW"`, `"See DEV REVIEW"`
- `"needs developer approval"`, `"to be confirmed"`, `"pending review"`, `"check with developer"`
- Any open question, option to choose from, or deferred decision

If ANY of these are found → remove them and replace with a definitive decision based on the priority order: Dev Notes → Figma → best practices.

**Step 8C — Output Production (Three Documents)**

Using the mandatory templates from `analysis-output-contract` Part C, produce all three documents with FULL detail using the **Chunked Write Protocol** defined in `analysis-output-contract`:

> ⚠️ **MANDATORY**: Do NOT write any document in a single write_file call. Follow the Chunked Write Protocol — write 2–3 sections per call, use append mode after the first chunk, and apply a maximum 2-retry guard per chunk. If a chunk fails twice, write a condensed version and continue. Never restart the analysis.

1. **ANALYSIS_PLAN.md** — All 20 sections populated across 7 sequential write_file chunks. Code Generation Plan with ordered steps, files, state handling, visibility rules, prop wiring, things NOT to implement.
2. **DEV_REVIEW.md** — All 3 sections populated in 1 write_file call (write "None" if no items).
3. **CODING_AGENT_CHECKLIST.md** — All prefix categories populated with story-specific items across 2 sequential write_file chunks.

### Gate: Phase 8 Complete When

- [ ] All 13 self-validation checklist sections completed.
- [ ] ANALYSIS_PLAN.md scanned for prohibited phrases — none found.
- [ ] Every uncertain decision is in DEV_REVIEW.md, not in ANALYSIS_PLAN.md.
- [ ] Every DN-xxx item appears in the Developer Notes Applied table.
- [ ] No analysis section contradicts a Dev Note.
- [ ] ANALYSIS_PLAN.md produced with all 20 sections fully populated.
- [ ] Code Generation Plan (Section 11) includes: ordered steps, files to create, state handling placement, visibility rule placement, prop-driven wiring, things NOT to implement.
- [ ] DEV_REVIEW.md produced with all 3 sections.
- [ ] CODING_AGENT_CHECKLIST.md produced with story-specific items for all prefix categories.
- [ ] All three files saved to `.SS_WF/Agent/Analysis/` with correct ticket ID prefix.

---

## OUTPUT PHASE — Generate Three Documents

> **Executed as Part C of `analysis-output-contract`.**

After all 8 phases are complete and all self-validation checks pass, generate the three output documents using the **mandatory templates defined in `analysis-output-contract` Part C**. Every section of every template must be fully populated with story-specific detail.

### Document 1: ANALYSIS_PLAN.md

**File path:** `.SS_WF/Agent/Analysis/{{$var[ticket_id]s}}_ANALYSIS_PLAN.md`

This document goes **directly to the Code Generation Agent**. It must be 100% actionable, decisive, and complete — all 20 sections populated per `analysis-output-contract` Part C template.

> ⚠️ **ABSOLUTE PROHIBITION**: ANALYSIS_PLAN.md must NEVER reference DEV_REVIEW.md or contain any deferred decision.

**Required Sections (in order — see `analysis-output-contract` Part C for full templates):**

```
1.  Developer Notes Applied (ALWAYS first — even if no Dev Notes found)
2.  Story Summary
3.  Classification Rationale
4.  Derived Scope
5.  Acceptance Criteria Analysis
6.  Agent Decision Summary
7.  Proposed Component Hierarchy
8.  Component Responsibility Matrix
9.  Container / View Decision
10. Folder Structure Proposal
11. Code Generation Plan (ordered steps, files, state handling, visibility rules,
    prop-driven wiring, things NOT to implement, design-system reuse wiring)
12. Assumptions and Decisions Made
13. Interaction Analysis
14. State, Error and Edge Case Analysis
15. Sitecore / Backend / Frontend Ownership
16. Sitecore API Analysis (or: SITECORE API NOT FOUND / NOT REQUIRED)
17. BFF API Analysis including Data Fetching Pattern per endpoint
    (or: BFF API NOT FOUND / NOT REQUIRED)
18. Prop-Driven Component Model (prop table per component with source and detail)
19. Component Inventory & Reuse Validation
20. Responsive / Accessibility / RTL / NFR Analysis
```

### Document 2: DEV_REVIEW.md

**File path:** `.SS_WF/Agent/Analysis/{{$var[ticket_id]s}}_DEV_REVIEW.md`

This document is for the developer to review **after** development is complete. Contains ONLY decisions made under uncertainty, assumptions due to missing information, and conflicts resolved. Do NOT duplicate content from ANALYSIS_PLAN.md.

**Required Sections (see `analysis-output-contract` Part C for full templates):**

```
1. Decisions Made Under Uncertainty
2. Assumptions Made (Missing Information)
3. Conflicts Resolved
```

### Document 3: CODING_AGENT_CHECKLIST.md

**File path:** `.SS_WF/Agent/Analysis/{{$var[ticket_id]s}}_CODING_AGENT_CHECKLIST.md`

A validation checklist the Code Generation Agent must use before completing implementation. Every item must be story-specific — not generic boilerplate.

**Checklist prefix categories (in order see `analysis-output-contract` Part C for full templates):**

| Prefix | Category                                     |
| ------ | -------------------------------------------- |
| DN     | Developer Notes compliance (ALWAYS first)    |
| AC     | Acceptance criteria                          |
| INT    | Interaction behaviour                        |
| STATE  | State/error/empty behaviour                  |
| SCOPE  | Out-of-scope protection                      |
| PROP   | Prop-driven implementation                   |
| CMS    | Sitecore/content ownership                   |
| API    | Backend/API ownership                        |
| COMP   | Component responsibility                     |
| DS     | Design-system reuse and catalogue validation |
| RESP   | Responsive behaviour                         |
| A11Y   | Accessibility                                |
| RTL    | RTL/localisation                             |
| NFR    | Non-functional requirement                   |
| FILE   | Folder/file structure                        |
| TEST   | Testability / validation                     |

---

## Skill Invocation Map

This table shows which skill is invoked at each phase:

| Phase   | Skill Invoked                       | Purpose                                                                                                                                                                                   |
| ------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Phase 1 | `developer-notes-protocol`          | Extract Dev Notes as SACRED LAW before all analysis                                                                                                                                       |
| Phase 2 | `figma-fetch-reconcile-and-analyse` | Fetch Figma context, reconcile viewports, prepare design inputs                                                                                                                           |
| Phase 4 | `api-analysis-sitecore-and-bff`     | Complete Sitecore and BFF API analysis — runs BEFORE Phase 3; includes Data Fetching Pattern per endpoint (hook, service, query key, state rules)                                         |
| Phase 3 | `story-analysis-end-to-end`         | Complete story analysis: classification, ACs, interactions, states, ownership separation + prop-driven model per component (Step 7.1 + 7.2), NFR (Sections 6,7,9,10 only)                 |
| Phase 5 | `component-breakdown-and-hierarchy` | Breakdown rules, hierarchy, responsibility matrix, folder/file structure and naming conventions                                                                                           |
| Phase 6 | `component-reuse-validation`        | Component reuse validation against catalogue — 4-step workflow for every applicable component                                                                                             |
| Phase 8 | `analysis-output-contract`          | Part A: 13-section self-validation checklist. Part B: ANALYSIS_PLAN.md prohibition check. Part C: Production of all 3 documents using mandatory templates with full story-specific detail |

---

## Priority Order (Applied at Every Decision Point)

```
Dev Notes   →  Figma  →  React/Frontend Best Practices
```

This priority order is non-negotiable. When two sources conflict, the higher-priority source wins. The conflict and resolution must be recorded in DEV_REVIEW.md.

---

## Global Guardrails

### Always Do

- Execute all 8 phases in order. No skipping, no reordering.
- Extract Dev Notes FIRST — before any other analysis.
- Make every decision yourself — no open questions, no deferred approvals.
- Apply the priority order at every decision point.
- Mark every derived recommendation clearly: `Derived from project frontend best practices.`
- Mark every missing input clearly: `Not Provided.`
- Record every uncertain decision in DEV_REVIEW.md — never in ANALYSIS_PLAN.md.
- Label every analysis item influenced by a Dev Note with its DN ID (e.g., "Per DN-002").
- Keep all components prop-driven — no hardcoded labels, values, or copy.
- Separate Sitecore, API, and FE ownership clearly.
- Perform component reuse validation directly — no separate reuse agent.
- Perform API analysis directly — no separate API analysis agent.
- Perform Figma fetch and reconciliation directly — no separate Figma agent.
- Save all three output files to `.SS_WF/Agent/Analysis/`.

### Never Do

- Never skip Phase 1 (Dev Notes extraction).
- Never reference DEV_REVIEW.md inside ANALYSIS_PLAN.md.
- Never write "needs developer approval", "to be confirmed", "option A or B" in ANALYSIS_PLAN.md.
- Never write "Check if supported in DEV REVIEW" or any equivalent phrase.
- Never override a Dev Note — not even as a "suggestion" or "recommendation".
- Never browse folders or fall back to similar files when looking up API endpoints.
- Never skim or partially read a BFF YAML spec — read the complete file.
- Never skip any step in the 4-Step Component Reuse Workflow.
- Never assign a reuse category without completing all applicable prior steps.
- Never hardcode labels, values, copy, or colours inside feature components.
- Never generate implementation code (that is the Coding Agent's job).
- Never include file paths inside component hierarchy diagrams.
- Never create containers for purely presentational sections.
- Never place API calls inside feature display components.
- Never place business logic inside design-system components.
- Never re-reconcile Figma if `responsive_design_intent.json` already exists.
- Never use raw mobile/desktop context JSONs to override the Responsive Reconciliation JSON.

---

## Quick Reference: Phase Execution Summary

```
PHASE 0  Pre-Analysis Setup
         → Confirm folder structure, confirm inputs available

PHASE 1  Developer Notes Extraction          [developer-notes-protocol]
         → Extract all Dev Notes, number them, keep active list

PHASE 2  Figma Fetch, Reconcile, Analyse     [figma-fetch-reconcile-and-analyse]
         → Fetch Figma context, reconcile if both viewports, prepare design inputs

PHASE 4  API Analysis                        [api-analysis-sitecore-and-bff]  ← Runs BEFORE Phase 3
         → Sitecore API + BFF API — strict endpoint lookup, full YAML analysis
         → Data Fetching Pattern produced per endpoint (hook, service, query key factory,
           endpoint constant, state rendering rules, mutation/infinite scroll flags)
         → API contracts + fetching patterns made available for Phase 3 story analysis

PHASE 3  Story Analysis End to End           [story-analysis-end-to-end]
         → Story understanding, classification, ACs, interactions, states
         → Step 7.1: Ownership separation (Sitecore / API / FE)
         → Step 7.2: Prop-driven model per component (explicit prop table with source,
           type, source detail, Sitecore Helper functions identified)
         → NFR: RTL, a11y, Responsive, Overflow (Sections 6,7,9,10 only)
         → Uses Phase 4 API contracts to correlate API data with story functionality

PHASE 5  Component Breakdown and Hierarchy   [component-breakdown-and-hierarchy]
         → Breakdown rules, hierarchy, responsibility matrix, folder structure

PHASE 6  Component Reuse Validation          [component-reuse-validation]
         → 4-step reuse workflow for every applicable component

PHASE 8  Output Contract Framework           [analysis-output-contract]
         → Part A: 13-section self-validation checklist
         → Part B: ANALYSIS_PLAN.md prohibition check
         → Part C: Production of all 3 documents using mandatory templates
           → ANALYSIS_PLAN.md — all 20 sections, Code Generation Plan with full detail
           → DEV_REVIEW.md — all 3 sections
           → CODING_AGENT_CHECKLIST.md — all prefix categories, story-specific items
```
