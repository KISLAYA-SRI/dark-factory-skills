---
name: defect-context-loader
description: Use as Phase 2 of the FE Defect Fix workflow to load the minimum context needed to locate a fault — the parent Code Generation Summary and the current source files it points to — and to pull additional sources only when a specific trigger fires. Also performs a gated selective refetch of a changed external artefact via context-gathering. Triggers include defect context load, load defect context, or refetch changed contract.
disable-model-invocation: true
---

## Defect Context Loader

### Purpose

Load the **minimum** context needed to locate the fault. Pull more only when a trigger fires.

⚠️ This phase loads and indexes. Diagnosis happens in Phase 3.

---

## ⚠️ VARIABLES

```text
{{$var[ticket_id]s}}          the DEFECT ticket
{{$var[parent_ticket_id]s}}   the story it was raised on
```

---

## ⚠️ DEFAULT WORKING SET — LOAD EXACTLY THIS

```text
1. Parent code summary
   .SS_WF/Agent/CODE/{{$var[parent_ticket_id]s}}_CODE_GENERATION_SUMMARY.md

   Index these sections only:
     §3   File Inventory        which files could cause this
     §5   Sitecore field → prop authored content not appearing
     §7   Data Flow Trace       where a value comes from, and its null default
     §8   State → UI Matrix     which file owns a state
     §12.4 Known Limitations    is this a known gap, not a defect?
     §13  Change Log            was this code fixed before? (regression check)

2. The CURRENT source files those sections point to
```

The defect ticket itself was already read in Phase 1.

⚠️ **That is the whole default load.** Most defects need nothing more.

### Do NOT load by default

```text
❌ Analysis Plan            — trigger-gated (below)
❌ Coding Agent Learnings   — Phase 6, or if the failure mode looks familiar
❌ Component catalogue      — only for design-system / shared blast radius
❌ Git history              — only when drift must be explained
❌ Parent story JIRA ticket — never
❌ DEV_REVIEW.md            — never
```

---

## ⚠️ TRIGGERS — WHEN TO LOAD MORE

| Load | Only when |
| --- | --- |
| **Analysis Plan §4 (ACs)** | You must confirm the reported behaviour is actually wrong, or the issue is "missing AC" |
| **Analysis Plan §10 (states)** | A state renders differently from what the summary records and you need the required behaviour |
| **Analysis Plan §1 (Dev Notes)** | A DN may constrain the fix approach |
| **Analysis Plan §8 (out of scope)** | The issue may be deliberately excluded |
| **Learnings file** | Phase 6 (always), or earlier if the failure mode looks like a known rule |
| **Component catalogue** | The fix will touch a design-system or shared component |
| **Git history** | Current code differs from the summary and the source of that change matters |

⚠️ **Load only the sections named**, not the whole plan.

⚠️ **The correctness question matters.** The summary says what was *built*; only the plan says what was *required*. If the code matches the summary and the ticket still reports a problem, you cannot tell defect from change-request without §4/§10 — that is the trigger. When unsure, load them.

---

## Record for Drift Detection

From the summary header and §13:

```text
Generated:         2026-07-30
Prior fixes (§13): DEF-4102 (2026-08-14) · DEF-4380 (2026-09-02)
```

Phase 3 compares these with git. A line changed after generation with **no** §13 entry was changed by a developer — the *post-generation manual change* fault origin.

⚠️ **§13 is also the regression check.** If a prior fix touched the same file, state or field, the current issue may be a regression from it — one of only two origins that write a learning.

⚠️ **§12.4 and §2 are the not-a-defect check.** A match → `BLOCKED — known limitation LIM-xxx` or `BLOCKED — out of scope`. A row marked `✅ Resolved [DEF-xxx]` is closed; do not block against it.

---

## ⚠️ SELECTIVE REFETCH — VIA `context-gathering`

### Which artefact

| Issue category | Refetch |
| --- | --- |
| UI · RTL · Responsive · Media | **Figma only** |
| Sitecore | **Sitecore only** |
| BFF · API · mapper | **BFF only** |
| State · A11y · Missing AC · Regression | **None** |

⚠️ Never invoke all three tasks.

### Both conditions required

```text
1. Category matches the artefact
2. Evidence the source actually changed:
     Sitecore → authored field not rendering · placeholder empty ·
                §5 mapping no longer matches behaviour
     Figma    → ticket says design changed · contains a Figma URL ·
                reported visual differs from §9
     BFF      → field absent/renamed · §7 trace no longer matches the contract

EITHER fails → use the on-disk artefact. Do NOT refetch.
```

### Snapshot first

`context-gathering` **overwrites** canonical paths, and the diff is the whole diagnostic value.

```text
1. SNAPSHOT the current artefact (or the summary's §5 / §7 / §9 record of it)
2. INVOKE context-gathering — ONE artefact
3. DIFF old vs new
4. Root cause FROM the diff
```

```text
FIGMA DIFF — ISSUE-001
Property      Old            New            Status       Scope
Card gap      gap-m (16px)   gap-l (24px)   ⚠ CHANGED    ✅ reported → IN SCOPE
CTA button    — absent —     Primary CTA    ℹ ADDED      ⛔ not reported → OBSERVATION
Fault origin candidate: DESIGN CHANGE
```

⚠️ The **Scope** column is mandatory on a Figma diff — a refreshed design usually carries changes the defect never mentioned.

⚠️ Refetched Figma makes `responsive_design_intent.json` stale. **Do not re-reconcile** — use the raw viewport JSONs and note the staleness.

⚠️ Refetch failure → record it, continue with the on-disk artefact, **never invent** fields or tokens.

---

## Fallback — No Prior Summary

```text
Record: "NO PRIOR SUMMARY — fallback discovery"
Locate candidates by searching the repo for the component/prop names in the ticket.
Load Analysis Plan §5 / §7 / §12 to guide the search.
Flag REDUCED CONFIDENCE in every RCA; regression detection is degraded (no §13).
```

---

## Output — one block, no narration

```text
CONTEXT — {{$var[ticket_id]s}} (parent {{$var[parent_ticket_id]s}})
  Summary:   loaded §3 §5 §7 §8 §12.4 §13 · generated 2026-07-30
  Prior fix: DEF-4380 touched PolicyMapper.ts → overlaps ISSUE-002 (regression check)
  Plan:      not loaded | §4 §10 loaded — [trigger]
  Refetch:   ISSUE-002 Sitecore PERFORMED → diff attached · others none
  Blocked:   ISSUE-004 matches LIM-001 (confirm in RCA)
```

---

### Gate

```text
- [ ] Default working set loaded — nothing more without a trigger
- [ ] Generation date and §13 fix dates recorded
- [ ] Issues cross-checked against §12.4, §2, and §13 prior fixes
- [ ] Any extra source loaded has its trigger named
- [ ] Refetch only where both conditions held; snapshot taken; diff produced
- [ ] No parent story ticket, no DEV_REVIEW.md, no re-analysis
- [ ] No files written (except artefacts via context-gathering)
```

### Never

- Never load the Analysis Plan, learnings or catalogue without a named trigger.
- Never load the whole Analysis Plan when two sections answer the question.
- Never read the parent story JIRA ticket or `DEV_REVIEW.md`.
- Never treat summary paths or line numbers as facts — they are pointers to verify.
- Never invoke all three `context-gathering` tasks; never refetch without both conditions.
- Never overwrite an artefact without a snapshot; never re-run Figma reconciliation.
- Never invent contract fields, design values or tokens.
- Never begin RCA here.
- Never narrate what was loaded beyond the single output block.
