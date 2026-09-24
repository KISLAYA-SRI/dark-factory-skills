---
name: defect-context-loader
description: Use as Phase 2 of the FE Defect Fix workflow to load the Analysis Plan, Code Generation Summary including its Change Log, and Coding Agent Learnings once into working memory, and to selectively refetch a changed external artefact (Sitecore, Figma, or BFF) via the context-gathering skill with snapshot-and-diff. Triggers include defect context load, load defect context, or refetch changed contract.
disable-model-invocation: true
---

## Defect Context Loader

### Purpose

This skill is **Phase 2** of the FE Defect Fix Agent. It loads everything needed to **locate** the fault — once — and, when an external source has genuinely changed, delegates a **selective** refetch to the `context-gathering` skill.

⚠️ **This phase performs no analysis.** It loads, indexes, and diffs. Diagnosis happens in Phase 3.

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
| Component Catalogue | `./src/component-catalogue.json` | For blast-radius checks |
| Sitecore API JSON | `./.SC_API_SPEC/sitecore-api.json` | Existing on-disk copy |
| BFF API specs | `./.BFF_API_SPEC/{operationId}.json` | Existing on-disk copies |
| Figma context | `figma-output/figma_design_{Node_id}_-context.json` | Existing on-disk copies |

*If missing, use Fallback Discovery below.

⚠️ **The parent story is whichever story the defect was raised against.** All documents come from that story ID.

⚠️ If `ANALYSIS_PLAN.md` is missing → **HALT**. Without it there is no reliable way to locate the fault or distinguish a defect from an intentional decision.

---

## 1. Load the Analysis Plan

Read all 13 sections. Index these for Phase 3:

| § | Why it matters for defect fixing |
| --- | --- |
| 1 | **Story Dev Notes (DN)** — still binding, below DDN |
| 3 | Classification — Presentational / Transactional / Hybrid |
| 4 | **Acceptance Criteria** — is the reported behaviour actually required? |
| 6 | Responsibility matrix — which layer *should* own this |
| 8 | **Things NOT to Implement** — was this deliberately excluded? |
| 10 | **States** — expected behaviour per state |
| 11 | API contracts — Sitecore fields and BFF slice |
| 12 | Prop model — `Source` / `Source Detail` per prop |
| 13 | Reuse decisions and NFR exceptions |

> **Summary answers *where*. Plan answers *whether*.** The plan is the correctness oracle — it tells you if the reported behaviour is actually wrong, and whether a miss was the agent's or an upstream gap.

---

## 2. Load the Code Generation Summary

This is the **primary location index**. Load all 13 sections; these carry the most diagnostic weight:

| § | Section | Answers |
| --- | --- | --- |
| **3** | **File Inventory** | *"Which files could possibly cause this?"* |
| **5** | **Sitecore field → prop** | *"Why is authored content not appearing?"* |
| **7** | **Data Flow Trace** | *"Where does this value come from and where could it break?"* |
| **8** | **State → UI Matrix** | *"Which file owns the wrong-looking state?"* |
| **9** | **Design & NFR Notes** | *"Which tokens were used? What discrepancies were recorded?"* |
| **12.4** | **Known Limitations** | *"Is this a known gap rather than a defect?"* |
| **12.1** | **Decisions** | *"Why was it built this way?"* |
| **13** | **Change Log** | *"Has this component been fixed before? What changed?"* |

### ⚠️ §13 Change Log Is a Primary Diagnostic Source, Not History

```text
- REGRESSION CANDIDATES — if a prior defect touched the same file, state, or
  field, the current issue may be a regression from that fix. That is a distinct
  fault origin, and unlike contract or design changes it DOES write a learning.

- TAGGED ROWS — state sections carry [DEF-xxx] tags showing which rows were
  updated by which fix, and therefore how recently that line reference was verified.

- PRIOR OBSERVATIONS — a problem recorded but not fixed in an earlier run may be
  exactly what is now being reported.

- RESOLVED LIMITATIONS — a §12.4 row marked "✅ Resolved [DEF-xxx]" means the gap
  is closed; do not block the issue against it.
```

⚠️ **Sections 1–12 always describe the CURRENT state**, because every defect fix updates them in place. §13 records how they got that way.

⚠️ **Check §12.4 and §2 Scope NOT Implemented early.** If an issue matches a known limitation or an explicit exclusion, record it as `BLOCKED — known limitation (LIM-xxx)` or `BLOCKED — out of scope` and carry it to the §13 entry. The run continues.

---

## 3. Load the Coding Agent Learnings

**Path:** `./src/.project/learnings/CODING_AGENT_LEARNINGS.md`

Read all namespaces: `# UI LEARNINGS` · `# LOGIC LEARNINGS` · `# TEST LEARNINGS` · `# STORYBOOK LEARNINGS`

Two purposes:

1. **Diagnostic** — an existing learning may describe exactly this failure mode.
2. **Deduplication** — Phase 6 must know what exists before appending. Loading now avoids a second read.

⚠️ If a learning **already covers** the failure mode being diagnosed, note it — the rule existed and was not applied. Phase 6 tracks recurrence.

---

## 4. Load the Component Catalogue

**Path:** `./src/component-catalogue.json`

Used for **blast radius** — if a fix touches a design-system component, the catalogue shows which components compose it.

---

## 5. ⚠️ SELECTIVE ARTEFACT REFETCH — VIA `context-gathering`

External sources change after generation. When they do, the code is not necessarily wrong — **the source moved**. Reuse the same acquisition skill as the coding workflow so paths, scripts and formats never drift.

### 5.1 — Which Artefact, By Category

| Issue category | Refetch |
| --- | --- |
| UI · RTL · Responsive · Media | **Figma only** |
| Sitecore | **Sitecore only** |
| BFF · API · mapper | **BFF only** |
| State · A11y · Missing AC · Regression | **None** |

⚠️ **Never invoke all three tasks.** `context-gathering` runs Sitecore, BFF and Figma by default — the defect agent must scope it to the **one artefact** the category requires.

### 5.2 — Two Gate Conditions, BOTH Required

```text
CONDITION 1 — Category match (table above)

CONDITION 2 — Evidence the source actually changed:

  Sitecore → authored field value not appearing at all
           → field appears empty despite being authored
           → placeholder renders nothing
           → component falls back to the missing-component placeholder
           → summary §5 field→prop mapping no longer matches behaviour

  Figma    → ticket says "design updated", "new Figma", "per latest design"
           → ticket contains a Figma URL
           → reported visual differs from what summary §9 records

  BFF      → field absent or renamed in the response
           → summary §7 Data Flow Trace no longer matches the contract
           → new error code the UI does not handle

If EITHER condition fails → use the existing on-disk artefact. Do NOT refetch.
```

⚠️ Without Condition 2, every visual defect would trigger a Figma fetch. **The ticket must indicate the source changed.**

### 5.3 — ⚠️ SNAPSHOT BEFORE REFETCHING

`context-gathering` writes to canonical paths and **will overwrite** what is there. The diff is the entire diagnostic value.

```text
1. SNAPSHOT the current artefact — read and hold its content in memory
     (or, if the file is gone, use the summary's §5 / §7 / §9 record of it)
2. INVOKE context-gathering — scoped to that ONE artefact
3. DIFF old vs new
4. Root cause FROM the diff
```

⚠️ Lose the old copy and you lose the ability to say *"`PolicyTitle` was renamed to `Title`"* — which is the whole point.

### 5.4 — Diff Output Format

```text
SITECORE CONTRACT DIFF — ISSUE-002

Summary §5 recorded          Current contract         Status
─────────────────────────────────────────────────────────────
PolicyTitle (Single-Line)    Title (Single-Line)      ⚠️ RENAMED
CtaLink (General Link)       CtaLink (General Link)   ✅ unchanged
ExpiryDate (Date)            — absent —               ⚠️ REMOVED
—                            Subtitle (Single-Line)   ℹ️ ADDED

ROOT CAUSE CANDIDATE:
  PolicyTitle → Title rename explains ISSUE-002 (title not rendering).
  Fault origin: CONTRACT CHANGE (external) — not an agent miss.
```

```text
FIGMA DESIGN DIFF — ISSUE-001

Property              Summary §9 / old context    New context     Status
────────────────────────────────────────────────────────────────────────
Card gap              gap-m (16px)                gap-l (24px)    ⚠️ CHANGED
Heading token         heading3                    heading3        ✅ unchanged
CTA button            — absent —                  Primary CTA     ℹ️ ADDED
Divider               present                     — absent —      ⚠️ REMOVED

DEFECT SCOPE:
  ✅ Card gap change   → reported in the ticket → IN SCOPE
  ⛔ CTA button added   → not reported → OBSERVATION, separate ticket
  ⛔ Divider removed    → not reported → OBSERVATION, separate ticket

  Fault origin: DESIGN CHANGE — code was correct for the original design.
```

⚠️ The **scope column is mandatory** on a Figma diff. A refreshed design typically carries several changes; only the reported one is in scope.

### 5.5 — Fault Origins From Refetch

| Source changed | Fault origin | Learning? |
| --- | --- | --- |
| Sitecore / BFF contract | **Contract change** | ❌ No — external |
| Figma design | **Design change** | ❌ No — code was correct for the old design |

⚠️ A Figma change means the code is **correct for the design it was built against**. Never classify it as an agent miss — that pollutes the learnings file with a rule nobody can act on.

### 5.6 — ⚠️ Reconciliation Is NOT Re-Run

If Figma is refetched, `figma-output/responsive_design_intent.json` becomes stale.

```text
❌ Do NOT re-reconcile — that is an Analysis Agent responsibility
✅ Work from the RAW viewport context JSONs for the specific property reported
✅ Record in the §13 entry: "responsive_design_intent.json is stale after refetch"
```

If the responsive **strategy itself** changed — layout restructured, breakpoint behaviour altered — that is a structural change and must be escalated, not fixed here.

### 5.7 — Refetch Failure

```text
Record: "REFETCH FAILED — [artefact] — [reason from context-gathering]"
Proceed with the existing on-disk artefact and the summary's recorded values.
NEVER invent contract fields, design values, or tokens.
```

---

## 6. ⚠️ Fallback Discovery (No Prior Summary)

If `CODE_GENERATION_SUMMARY.md` does not exist — legacy code, or a story predating this pipeline:

```text
1. Record: "NO PRIOR SUMMARY — fallback discovery mode"
2. Locate candidate files by searching the repository:
     - component names from Analysis Plan §5
     - ownership markers from §7 → resolved paths
     - prop names from §12
3. Read the candidate files directly to build an ad-hoc location map
4. Flag REDUCED CONFIDENCE in every RCA produced this way
```

⚠️ Without §5/§7/§9, a refetch diff has nothing recorded to compare against. Diff against the **existing on-disk artefact** instead, and note the reduced confidence.

⚠️ Without §13, prior-fix history is unavailable — regression detection is degraded. Note this explicitly.

---

## Output — DEFECT_CONTEXT

Hold in memory. **This skill writes no files** — `context-gathering` writes artefacts if a refetch occurred.

```text
DEFECT CONTEXT LOADED — {{ticket_id}}

Parent story:     {{parent_story_id}}
Analysis Plan:    loaded · classification: [X]
Code Gen Summary: loaded (13 sections) | NOT FOUND → fallback discovery
Learnings:        loaded · N entries across 4 namespaces
Catalogue:        loaded · N components

Story Dev Notes (DN):  N found  ← lower priority than DDN
Known Limitations:     LIM-xxx …  ← issues cross-checked
Scope NOT Implemented: [items]    ← issues cross-checked

Prior fixes (§13):     DEF-4102 (2026-08-14) · DEF-4380 (2026-09-02)
                       ⚠️ DEF-4380 touched PolicyMapper.ts — overlaps ISSUE-002
                          → check for regression in RCA

REFETCH DECISIONS
  ISSUE-001 (RTL)       → Figma:    NOT REQUIRED — no design-change signal
  ISSUE-002 (Sitecore)  → Sitecore: PERFORMED → diff attached
  ISSUE-003 (BFF)       → BFF:      NOT REQUIRED — §7 trace still matches

Reconciliation: not re-run (stale after Figma refetch) | N/A

Pre-matched issues:
  ISSUE-004 → matches LIM-001 → candidate BLOCKED (confirm in RCA)
```

---

### Gate: Phase 2 Complete When

```text
- [ ] Analysis Plan loaded — all 13 sections indexed
- [ ] Code Gen Summary loaded (§3 §5 §7 §8 §9 §12 §13) OR fallback recorded
- [ ] §13 Change Log loaded; prior fixes listed
- [ ] Issues cross-checked against prior fixes for regression candidates
- [ ] Learnings loaded from ./src/.project/learnings/CODING_AGENT_LEARNINGS.md
- [ ] Component catalogue loaded for blast-radius checks
- [ ] Story Dev Notes (DN) indexed below DDN
- [ ] Issues cross-checked against §12.4 Known Limitations and §2 Scope NOT Implemented
- [ ] Refetch decision recorded PER ISSUE with the reason
- [ ] Refetch performed ONLY where both gate conditions met
- [ ] Refetch scoped to ONE artefact — never all three tasks
- [ ] Snapshot taken BEFORE any refetch
- [ ] Diff produced with a scope column (Figma) or status column (contract)
- [ ] Fault origin candidate identified from each diff
- [ ] Reconciliation NOT re-run; staleness recorded if Figma was refetched
- [ ] No story re-read, no re-analysis
```

### Never Do

- **Never read the parent story JIRA ticket.**
- **Never re-run story analysis.**
- **Never invoke all three `context-gathering` tasks** — one artefact, by category.
- **Never refetch** unless both gate conditions are met.
- **Never refetch "just to check"** — Condition 2 requires positive evidence.
- **Never overwrite an artefact without snapshotting it first.**
- **Never re-run Figma reconciliation.**
- **Never invent contract fields, design values, or tokens** if a refetch fails.
- **Never skip §13** — it is how regressions from prior fixes are detected.
- **Never read `DEV_REVIEW.md`.**
- **Never begin root cause analysis here** — index and diff only.
- **Never skip the Known Limitations cross-check.**
- **Never proceed without the Analysis Plan** — HALT instead.
- Never write any file directly — only `context-gathering` writes artefacts.
