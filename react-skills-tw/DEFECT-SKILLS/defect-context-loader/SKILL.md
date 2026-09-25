---
name: defect-context-loader
description: Use as Phase 2 of the FE Defect Fix workflow to load the Analysis Plan, the Code Generation Summary including its Change Log, and the Coding Agent Learnings once into working memory, record the dates needed for drift detection, and selectively refetch a changed external artefact (Sitecore, Figma, or BFF) via the context-gathering skill with snapshot-and-diff. Triggers include defect context load, load defect context, or refetch changed contract.
disable-model-invocation: true
---

## Defect Context Loader

### Purpose

This skill is **Phase 2** of the FE Defect Fix Agent. It loads everything needed to **locate** the fault — once — and, when an external source has genuinely changed, delegates a **selective** refetch to `context-gathering`.

⚠️ **This phase performs no analysis.** It loads, indexes, and diffs. Diagnosis happens in Phase 3.

---

## ⚠️ THE DOCUMENTS ARE A MAP — NOT THE TERRITORY

After generation, developers routinely change the code. The Analysis Plan and Code Generation Summary describe what the workflow **produced**, which may no longer be what is on disk.

| Document | What it is authoritative for | What it is NOT authoritative for |
| --- | --- | --- |
| **Analysis Plan** | What the behaviour **should** be (ACs, states, contracts) | What the code currently does |
| **Code Gen Summary** | **Where to look** — files, traces, states, tokens, prior fixes | What the code currently does |
| **Current code** | What the code **does now** | What it should do |

⚠️ Load both documents in full, but treat every file path, line number and trace in the summary as a **pointer to verify**, not a fact. Phase 3 reads the current code before relying on any of it.

---

## ⚠️ NO RE-ANALYSIS

```text
❌ Never read the parent story JIRA ticket — the Analysis Plan carries it
❌ Never re-run story analysis
❌ Never re-run Figma reconciliation
❌ Never read DEV_REVIEW.md
✅ Selective artefact refetch via context-gathering — under the gate below
```

---

### Inputs

| Input | Path | Required? |
| --- | --- | --- |
| Analysis Plan | `.SS_WF/Agent/Analysis/{{parent_story_id}}_ANALYSIS_PLAN.md` | **Mandatory** |
| Code Gen Summary | `.SS_WF/Agent/CODE/{{parent_story_id}}_CODE_GENERATION_SUMMARY.md` | **Mandatory*** |
| Coding Agent Learnings | `./src/.project/learnings/CODING_AGENT_LEARNINGS.md` | **Mandatory** |
| Component Catalogue | `./src/component-catalogue.json` | For blast radius |
| Sitecore API JSON | `./.SC_API_SPEC/sitecore-api.json` | Existing copy |
| BFF API specs | `./.BFF_API_SPEC/{operationId}.json` | Existing copies |
| Figma context | `figma-output/figma_design_{Node_id}_-context.json` | Existing copies |

*If missing, use Fallback Discovery below.

⚠️ If `ANALYSIS_PLAN.md` is missing → **HALT**. Without it there is no correctness oracle.

---

## 1. Load the Analysis Plan

Read all 13 sections. Index these for Phase 3:

| § | Why it matters |
| --- | --- |
| 1 | **Story Dev Notes (DN)** — still binding, below DDN |
| 3 | Classification |
| 4 | **Acceptance Criteria** — is the reported behaviour actually required? |
| 6 | Responsibility matrix — which layer *should* own this |
| 8 | **Things NOT to Implement** — deliberately excluded? |
| 10 | **States** — expected behaviour per state |
| 11 | API contracts |
| 12 | Prop model — `Source` / `Source Detail` per prop |
| 13 | Reuse decisions and NFR exceptions |

> **Summary answers *where*. Plan answers *whether*. Code answers *what is*.**

---

## 2. Load the Code Generation Summary — the Map

Load all 13 sections. Highest diagnostic weight:

| § | Section | Answers |
| --- | --- | --- |
| **3** | File Inventory | Which files could possibly cause this? |
| **5** | Sitecore field → prop | Why is authored content not appearing? |
| **7** | Data Flow Trace | Where does this value come from? |
| **8** | State → UI Matrix | Which file owns the wrong-looking state? |
| **9** | Design & NFR Notes | Which tokens were used? |
| **10** | Tests & Coverage | **Which test files already exist** — the starting point for blast-radius runs |
| **12.4** | Known Limitations | Known gap rather than a defect? |
| **12.1** | Decisions | Why was it built this way? |
| **13** | **Change Log** | Has this been fixed before? What changed? |

### ⚠️ Record the Dates Needed for Drift Detection

```text
Generated:        [date from the summary header]
Prior fixes (§13): DEF-4102 (2026-08-14) · DEF-4380 (2026-09-02)
```

Phase 3 compares these with git history. A line changed **after** generation and **not** by a §13 fix was changed by a developer — the **post-generation manual change** fault origin.

### ⚠️ §13 Change Log Is Diagnostic, Not History

```text
REGRESSION CANDIDATES  prior fix touched the same file/state/field → possible regression
TAGGED ROWS            [DEF-xxx] tags show which rows were last verified, and when
PRIOR OBSERVATIONS     a problem recorded but not fixed earlier may be what is reported now
RESOLVED LIMITATIONS   "✅ Resolved [DEF-xxx]" — do not block the issue against it
```

⚠️ **Check §12.4 and §2 Scope NOT Implemented early.** A match → candidate `BLOCKED — known limitation` or `BLOCKED — out of scope`, confirmed in RCA. The run continues.

---

## 3. Load the Coding Agent Learnings

**Path:** `./src/.project/learnings/CODING_AGENT_LEARNINGS.md` — READ all  namespaces.

1. **Diagnostic** — an existing learning may describe this exact failure mode.
2. **Deduplication** — Phase 6 needs to know what exists before appending.

⚠️ If a learning **already covers** the failure mode, note it — the rule existed and was not applied. Phase 6 tracks recurrence.

---

## 4. Load the Component Catalogue

**Path:** `./src/component-catalogue.json` — composition and imports for blast radius.

---

## 5. ⚠️ SELECTIVE ARTEFACT REFETCH — VIA `context-gathering`

### 5.1 — Which Artefact, By Category

| Issue category | Refetch |
| --- | --- |
| UI · RTL · Responsive · Media | **Figma only** |
| Sitecore | **Sitecore only** |
| BFF · API · mapper | **BFF only** |
| State · A11y · Missing AC · Regression | **None** |

⚠️ **Never invoke all three tasks.** Scope `context-gathering` to the one artefact the category requires.

### 5.2 — Two Gate Conditions, BOTH Required

```text
CONDITION 1 — Category match (table above)

CONDITION 2 — Evidence the source actually changed:
  Sitecore → authored field not appearing · placeholder empty · missing-component fallback
             · §5 mapping no longer matches behaviour
  Figma    → ticket says design changed · ticket contains a Figma URL
             · reported visual differs from §9
  BFF      → field absent or renamed · §7 trace no longer matches the contract
             · new error code the UI does not handle

EITHER fails → use the existing on-disk artefact. Do NOT refetch.
```

### 5.3 — ⚠️ Snapshot Before Refetching

`context-gathering` **overwrites** canonical paths. The diff is the diagnostic value.

```text
1. SNAPSHOT the current artefact (or the summary's §5 / §7 / §9 record)
2. INVOKE context-gathering — ONE artefact only
3. DIFF old vs new
4. Root cause FROM the diff
```

### 5.4 — Diff Formats

```text
SITECORE CONTRACT DIFF — ISSUE-002
Summary §5 recorded          Current contract         Status
PolicyTitle (Single-Line)    Title (Single-Line)      ⚠️ RENAMED
CtaLink (General Link)       CtaLink (General Link)   ✅ unchanged
ExpiryDate (Date)            — absent —               ⚠️ REMOVED
Fault origin candidate: CONTRACT CHANGE
```

```text
FIGMA DESIGN DIFF — ISSUE-001
Property        Old            New            Status        Scope
Card gap        gap-m (16px)   gap-l (24px)   ⚠️ CHANGED     ✅ reported → IN SCOPE
CTA button      — absent —     Primary CTA    ℹ️ ADDED       ⛔ not reported → OBSERVATION
Divider         present        — absent —     ⚠️ REMOVED     ⛔ not reported → OBSERVATION
Fault origin candidate: DESIGN CHANGE
```

⚠️ The **Scope** column is mandatory on a Figma diff.

### 5.5 — Reconciliation Is NOT Re-Run

If Figma is refetched, `responsive_design_intent.json` becomes stale. Do not re-reconcile — work from the raw viewport JSONs and record the staleness for the §13 entry. A changed responsive **strategy** is structural — escalate.

### 5.6 — Refetch Failure

Record `REFETCH FAILED — [artefact] — [reason]`, continue with the on-disk artefact. **Never invent** contract fields, design values, or tokens.

---

## 6. ⚠️ Fallback Discovery (No Prior Summary)

```text
1. Record: "NO PRIOR SUMMARY — fallback discovery mode"
2. Locate candidates via plan §5 component names, §7 ownership markers, §12 prop names
3. Read candidate files directly to build an ad-hoc location map
4. Flag REDUCED CONFIDENCE in every RCA; note regression detection is degraded (no §13)
```

---

## Output — DEFECT_CONTEXT

Hold in memory. **This skill writes no files** — `context-gathering` writes artefacts if a refetch occurred.

```text
DEFECT CONTEXT LOADED — {{ticket_id}}

Parent story:     {{parent_story_id}}
Analysis Plan:    loaded · classification: [X]
Code Gen Summary: loaded (13 sections) — treated as a MAP | NOT FOUND → fallback
Generated:        2026-07-30
Prior fixes (§13): DEF-4102 (2026-08-14) · DEF-4380 (2026-09-02)
                  ⚠️ DEF-4380 touched PolicyMapper.ts — overlaps ISSUE-002
Existing tests (§10): [test files relevant to issues in scope]
Learnings:        N entries across 4 namespaces
Story Dev Notes:  N found (below DDN)

REFETCH DECISIONS
  ISSUE-001 (RTL)      → Figma:    NOT REQUIRED — no design-change signal
  ISSUE-002 (Sitecore) → Sitecore: PERFORMED → diff attached

Pre-matched:
  ISSUE-004 → LIM-001 → candidate BLOCKED (confirm in RCA)
```

---

### Gate: Phase 2 Complete When

```text
- [ ] Analysis Plan loaded — all 13 sections indexed as the correctness oracle
- [ ] Code Gen Summary loaded — all 13 sections, treated as a map
- [ ] Generation date and §13 fix dates recorded for drift detection
- [ ] Existing test files from §10 indexed for blast-radius runs
- [ ] Learnings and catalogue loaded
- [ ] Issues cross-checked against §12.4, §2, and §13 prior fixes
- [ ] Refetch decision recorded per issue; performed only where both conditions met
- [ ] One artefact per refetch; snapshot taken first; diff produced
- [ ] Reconciliation NOT re-run
- [ ] No story re-read, no re-analysis, no files written
```

### Never Do

- Never treat summary paths, lines or traces as facts — they are pointers to verify.
- Never read the parent story JIRA ticket or re-run analysis.
- Never invoke all three `context-gathering` tasks; never refetch without both conditions.
- Never overwrite an artefact without a snapshot.
- Never re-run Figma reconciliation.
- Never invent contract fields, design values, or tokens.
- Never skip §13 — it is how regressions are detected.
- Never read `DEV_REVIEW.md`.
- Never begin RCA here.
- Never proceed without the Analysis Plan — HALT.
