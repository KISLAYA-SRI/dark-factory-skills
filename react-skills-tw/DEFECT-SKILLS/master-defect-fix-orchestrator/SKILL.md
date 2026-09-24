---
name: master-defect-fix-orchestrator
description: Use when orchestrating the end-to-end FE Defect Fix workflow that turns a JIRA defect ticket into surgical code fixes with regression tests. Defines the mandatory phase sequence, per-issue loop, selective context refetch, skill selection by issue category, minimal-change contract, failing-first test protocol, in-place summary update, and the learning feedback loop. Triggers include defect fix, bug fix, fix defect, defect workflow, or regression fix. Invoked when the user says something like "Fix defect <TICKET_ID>" or "Resolve DEF-1234".
disable-model-invocation: true
---

## Master Defect Fix Orchestrator

### Purpose

This is the **master orchestration skill** for the FE Defect Fix Agent. It defines:
- **What** the agent must do — locate, fix, prove, and record.
- **In what order** — the mandatory phase sequence with a per-issue loop.
- **Which skills load** — selected per issue category, never speculatively.
- **When external sources may be refetched** — selectively, via `context-gathering`.
- **What guardrails apply** — minimal-change contract and failing-first tests.
- **What is updated** — the parent summary stays current; the learnings loop closes.

---

## ⚠️ DEFECT FIXING IS NOT CODE GENERATION

| | Code Generation | Defect Fixing |
| --- | --- | --- |
| Input | Finalised plan | Ambiguous symptom |
| First task | Build | **Locate** |
| Scope | Whole story | **Minimal surgical change** |
| Biggest risk | Missing a requirement | **Regression + scope creep** |
| Prior context | None | Analysis Plan + Code Gen Summary |

You are **repairing existing code**, not generating new features. Every instinct toward completeness, refactoring, or improvement must be suppressed.

---

## ⚠️ EXECUTION CONTRACT — READ FIRST

### Rule 1 — Run all phases without stopping

When a phase gate passes, **immediately invoke the next phase in the same run**. Do not pause. Do not ask whether to continue.

### Rule 2 — EXACTLY THREE conditions stop the run

| # | Stop condition | Where | What happens |
| --- | --- | --- | --- |
| 1 | Defect ticket missing/unreadable | Phase 1 | HALT |
| 2 | ANALYSIS_PLAN.md missing | Phase 2 | HALT — cannot locate without context |
| 3 | **Phase 6 has updated CODE_GENERATION_SUMMARY.md** | Phase 6 | Run complete |

**No other event ends the run.** An issue classified as blocked does **not** stop the run — record it and continue with the remaining issues.

### Rule 3 — Announce transitions

```text
Phase 3 complete (ISSUE-002) → proceeding to Phase 4 (Fix + Regression Test)
```

---

## ⚠️ WRITE FILES, NOT DESCRIPTIONS

**The PRIMARY deliverable is modified source code and new regression tests written to disk.**

```text
✅ Every fix applied to the actual file at the exact path
✅ Every regression test written and proven to fail-then-pass
✅ The parent summary updated so it still describes the code accurately
❌ Describing what the fix would be
❌ Producing only an RCA or a plan
```

**The order is: locate → write failing test → fix → prove pass → update the record.**

---

## ⚠️ THE MINIMAL-CHANGE CONTRACT (NON-NEGOTIABLE)

This is the single most important rule in the workflow.

```text
CHANGE ONLY what Root Cause Analysis explicitly named.

❌ No refactoring of surrounding code
❌ No "while I'm here" improvements
❌ No renaming, reordering, or reformatting
❌ No dependency upgrades
❌ No unrelated file touches
❌ No adding features the defect did not ask for

If you notice an unrelated problem → record it as an observation in the
§13 Change Log entry for a SEPARATE ticket. Do NOT fix it.
```

⚠️ A defect fix that also refactors is **not** a defect fix — it is an untested change set masquerading as one.

⚠️ **This contract extends to the summary update.** Update only the rows the fix touched. Never regenerate, reformat, or reword untouched content.

---

## ⚠️ SINGLE LIVING RECORD — NO SEPARATE DEFECT DOCUMENT

```text
.SS_WF/Agent/CODE/{{parent_story_id}}_CODE_GENERATION_SUMMARY.md
   §1–§12   ALWAYS describe the code as it is NOW
   §13      Change Log — append-only record of every defect fix
```

There is **no** `DEFECT_FIX_SUMMARY.md`. A separate document would restate the same facts and immediately diverge from the code.

### Why the summary must stay current

The summary is the **location index** every future defect run depends on:

```text
DEF-123 moves PolicyMapper's null default from line 34 to 41
        → §7 still says line 34
DEF-789 "policy number blank" → reads §7 → opens line 34 → wrong code
```

Worse, a stale §8 corrupts **fault-origin classification** — RCA sees code ≠ summary, calls it an agent miss, and writes a learning for a defect that was already fixed.

⚠️ **State sections are updated. Historical sections are not.** See Phase 6 for the split.

---

## Inputs

| Input | Source | Required? |
| --- | --- | --- |
| Defect ticket | `.SS_WF/{{ticket_id}}_JIRA_OUTPUT_.json` | **Mandatory** |
| Defect Dev Notes (DDN) | Section inside the defect ticket | If present — **TOP priority** |
| Analysis Plan | `.SS_WF/Agent/Analysis/{{parent_story_id}}_ANALYSIS_PLAN.md` | **Mandatory** |
| Code Gen Summary | `.SS_WF/Agent/CODE/{{parent_story_id}}_CODE_GENERATION_SUMMARY.md` | **Mandatory*** |
| Coding Agent Learnings | `./src/.project/learnings/CODING_AGENT_LEARNINGS.md` | **Mandatory** |
| Component Catalogue | `./src/component-catalogue.json` | For blast-radius checks |
| Existing artefacts | `.SC_API_SPEC/` · `.BFF_API_SPEC/` · `figma-output/` | On-disk copies |

*If missing, fallback discovery applies — see Phase 2.

⚠️ **The parent story is whichever story the defect was raised against.** All documents come from that story ID.

⚠️ **The story JIRA output is NOT an input.** Everything needed is in the Analysis Plan.

⚠️ **`DEV_REVIEW.md` is NOT an input** — provenance for human reviewers only.

---

## ⚠️ DEV NOTES PRECEDENCE

```text
DDN-001…   Defect Dev Notes   ← TOP PRIORITY, from the defect ticket
DN-001…    Story Dev Notes    ← from Analysis Plan §1, still binding
```

Separate ID chains keep both traceable. If a DDN **contradicts** a DN, follow the DDN and **record the supersession explicitly** in the §13 Change Log entry.

### Full Priority Order

```text
Defect Dev Notes (DDN)
  → Story Dev Notes (DN)
    → Refetched artefact (if a source genuinely changed)
      → Analysis Plan
        → Code Gen Summary
          → Project Guidelines (embedded in coding skills)
            → React/Frontend Best Practices
```

---

## ⚠️ SELECTIVE CONTEXT REFETCH — VIA `context-gathering`

External sources can change after generation. When they do, the code is not necessarily wrong — the **source moved**. The defect agent reuses the **same acquisition skill as the coding workflow** so paths, scripts and formats never drift.

### Refetch is SELECTIVE — never wholesale

| Issue category | Refetch |
| --- | --- |
| UI · RTL · Responsive · Media | **Figma only** |
| Sitecore | **Sitecore only** |
| BFF · API · mapper | **BFF only** |
| State · A11y · Missing AC · Regression | **None** |

⚠️ **Never invoke all three tasks.** A blank-value BFF defect has no business refetching Figma.

### Two Gate Conditions — BOTH required

```text
1. Issue category matches the artefact type (table above)
2. Evidence suggests the source actually changed:
     Sitecore → field missing/renamed; §5 mapping no longer matches behaviour
     Figma    → ticket references a design change, new Figma URL, "per latest design"
     BFF      → field absent/renamed; §7 Data Flow Trace no longer matches contract

If EITHER fails → use the existing on-disk artefact. Do NOT refetch.
```

### ⚠️ Snapshot Before Refetching

`context-gathering` writes to canonical paths and **will overwrite** what is there. The diff is the entire diagnostic value.

```text
1. Snapshot the current artefact (or the summary's §5 / §7 / §9 record of it)
2. Invoke context-gathering for THAT ARTEFACT ONLY
3. DIFF old vs new
4. Root cause from the diff
```

### Fault Origins From Refetch — Neither Writes a Learning

| Source changed | Fault origin | Learning? |
| --- | --- | --- |
| Sitecore / BFF contract | **Contract change** | ❌ No — external |
| Figma design | **Design change** | ❌ No — code was correct for the old design |

⚠️ A Figma change means the code is **correct for the design it was built against**. Labelling it an agent miss would pollute the learnings file.

### Reconciliation Is NOT Re-Run

If Figma is refetched, `responsive_design_intent.json` becomes stale. **Do not re-reconcile** — that is an Analysis Agent responsibility. Work from raw viewport context JSONs and note the staleness in the §13 entry.

---

## Mandatory Execution Sequence

```text
PHASE 1  Intake + Decomposition     [defect-intake-and-decomposition]
PHASE 2  Context Load               [defect-context-loader]
          └─ selective refetch      [context-gathering]  ← reused, gated, per-artefact
──────────────── PER-ISSUE LOOP ────────────────
PHASE 3  Root Cause Analysis        [defect-root-cause-analysis]
PHASE 4  Fix + Regression Test      [defect-fix-and-regression-test]
          └─ delegates to coding skills by category
──────────────── CONVERGE ────────────────
PHASE 5  Validation                 [generated-code-self-validation]   (reused)
PHASE 6  Summary Update + Learning  [defect-reporting-and-learning]
```

Phases 3–4 run **per issue**. Phases 5–6 run once, across all issues.

---

### PHASE 1 — Intake and Decomposition

**Invoke: defect-intake-and-decomposition**

Parse the defect ticket and split it into discrete, independently-fixable issues.

- Ticket content varies — one defect, several enumerated, or prose describing multiple problems
- The split is **semantic**, not list-parsing: a single paragraph can contain three issues
- Assign stable `ISSUE-001`, `ISSUE-002` … IDs threading through RCA → fix → test → record
- Extract **Defect Dev Notes** as `DDN-001`, `DDN-002` …
- Categorise each issue
- **Detect source-change signals** — phrases indicating design or contract change, and any Figma URL
- Capture reproduction evidence: steps, expected vs actual, environment, locale

**Gate:** ticket parsed · every distinct problem is its own ISSUE-xxx · DDN extracted and numbered · every issue categorised · source-change signals flagged · evidence captured.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 2.**

---

### PHASE 2 — Context Load

**Invoke: defect-context-loader**

Load everything needed to locate the fault, **once**. Delegates all external acquisition to `context-gathering`.

**Always loaded:**
- Analysis Plan — all 13 sections
- Code Gen Summary — especially **§3 File Inventory**, **§5 field→prop**, **§7 Data Flow Trace**, **§8 State Matrix**, **§9 Design Notes**, **§12 Deviations/Limitations**, **§13 Change Log**
- Coding Agent Learnings from `./src/.project/learnings/CODING_AGENT_LEARNINGS.md`
- Component catalogue for blast-radius checks
- Existing on-disk artefacts

⚠️ **§13 Change Log is diagnostically valuable.** It shows which prior defects already touched this component — critical for spotting a regression from an earlier fix, and for knowing which rows carry defect tags.

**Conditionally refetched** — per the selective gate above, one artefact at a time, with snapshot-and-diff.

#### Fallback Discovery

If the Code Gen Summary is missing (legacy code, or a story predating this pipeline), record `NO PRIOR SUMMARY — fallback discovery` and locate by searching the repository. Flag **reduced confidence** in every RCA produced this way.

**Gate:** plan, summary (incl. §13) and learnings loaded · issues pre-matched against §12.4 Known Limitations and §2 Scope NOT Implemented · refetch performed only where both gate conditions met · snapshot and diff for every refetch · no re-analysis · reconciliation not re-run.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 3 for ISSUE-001.**

---

### PHASE 3 — Root Cause Analysis (Per Issue)

**Invoke: defect-root-cause-analysis**

Locate the exact cause. **Naming a file is not enough — name the line and the mechanism.**

#### Summary Lookup Map

| Symptom | Look in | Finds |
| --- | --- | --- |
| Value blank / wrong | **§7 Data Flow Trace** | Mapper + null default + file:line |
| Wrong UI on a state | **§8 State Matrix** | Owning file for that state |
| CMS text not appearing | **§5 field→prop** | Field name mismatch or missing helper |
| Visual differs from design | **§9 Design Notes** | Tokens used, discrepancies recorded |
| Which files could cause this | **§3 File Inventory** | Complete scoped surface |
| Was this touched before? | **§13 Change Log** | Prior defect fixes on this component |
| Should this even work? | **§12.4 + §2** | Known limitation or out of scope |
| Why built this way? | **§12.1 Decisions** | Original reasoning |

⚠️ **Check §13 for regressions.** If a prior defect touched the same file or state, the current issue may be a regression from that fix — a distinct fault origin that **does** write a learning.

#### ⚠️ Fault Origin Classification (Gates the Learning Update)

| Origin | Example | Learning? |
| --- | --- | --- |
| **Agent miss** | Used `ml-4` instead of `ms-4`; forgot empty state | ✅ **Yes** |
| **Regression from prior fix** | Earlier fix (see §13) broke this | ✅ **Yes** |
| Upstream gap | Analysis Plan omitted the state | ❌ Flag to developer |
| **Contract change** | Sitecore/BFF field renamed post-generation | ❌ External |
| **Design change** | Figma updated after generation | ❌ Code was correct for the old design |
| Ambiguous requirement | AC open to interpretation | ❌ Story issue |

Only the first two write a learning.

#### Blast Radius

Before proposing any fix, determine what else consumes the code being changed. **Critical for design-system components.** Use §3 and the catalogue.

**Gate (per issue):** root cause named to file + line + mechanism · fault origin classified · §13 checked for prior fixes on the same code · blast radius determined · blocked issues recorded (run continues).

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 4 for this issue.**

---

### PHASE 4 — Fix and Regression Test (Per Issue)

**Invoke: defect-fix-and-regression-test**

#### ⚠️ Failing-First Protocol (MANDATORY)

```text
1. Write a regression test expressing the EXPECTED behaviour
2. Run it → it MUST FAIL against current code          ← proves the RCA
3. Apply the minimal fix
4. Run it → it MUST PASS
5. Run the existing suite for touched files → no regressions
```

⚠️ **If the test does not fail at step 2, the root cause is wrong.** Return to Phase 3.

#### ⚠️ Scope-to-Diff (Refetched Sources)

When an artefact was refetched, the diff may contain **many** changes — only one of which the defect reports.

```text
Figma diff shows:
  ✅ gap 16px → 24px        ← defect mentions this → FIX
  ⛔ new CTA button added    ← not mentioned → OBSERVATION, separate ticket
  ⛔ heading token changed   ← not mentioned → OBSERVATION, separate ticket
```

⚠️ **A refreshed artefact is NOT licence to re-implement against the latest version.**

#### ⚠️ Structural-Change Escape Hatch

If a diff shows **structural** change — new components, removed sections, changed hierarchy, new endpoints:

```text
Record: "EXCEEDS DEFECT SCOPE — structural change detected.
         Requires re-analysis via the Analysis Agent."
Do NOT attempt it. Continue with the remaining issues.
```

#### Skill Selection by Category

| Category | Skills loaded |
| --- | --- |
| UI / RTL / Responsive / A11y | `presentational-ui-generation` |
| Media | `+ frontend-media-integration` |
| Sitecore | `sitecore-rendering-integration` |
| BFF / API / mapper | `frontend-logic-integration` |
| State / forms | `frontend-state-and-form-management` |
| Any file move or rename | `+ repository-structure-governance` |
| DS component changed | `+ storybook-and-component-catalogue` |
| **Always** | `developer-notes-protocol` · `frontend-test-generation` |

⚠️ Coding skills are loaded for their **standards, guidelines and conventions** — not as licence to regenerate the component. The minimal-change contract overrides any completeness instinct those skills carry.

**Gate (per issue):** regression test written and **proven to fail first** · minimal fix applied to disk · test now passes · existing tests still pass · only RCA-named code changed · scope-to-diff honoured · structural change escalated · observations recorded.

> **➡️ More issues → loop to PHASE 3. All done → IMMEDIATELY invoke PHASE 5.**

---

### PHASE 5 — Validation

**Invoke: generated-code-self-validation** *(reused from the coding workflow)*

Run the structural gate across all changed files, **scoped to what was touched** — there is no manifest in a defect run.

**Additional defect-specific checks:**

```text
- [ ] ONLY files named in RCA were modified — no collateral changes
- [ ] Every issue has a regression test that failed first
- [ ] No existing test was weakened, skipped, or deleted to make a fix pass
- [ ] Every DDN resolved to Implemented / Not Applicable / Blocked with evidence
- [ ] Blast radius consumers still behave correctly (DS component changes)
- [ ] No new hardcoded values, tokens bypassed, or guardrails broken
- [ ] Refetched-artefact fixes stayed scoped to the reported delta
```

⚠️ **Never weaken or delete an existing test to make a fix pass.** If an existing test now fails, either the fix is wrong or the test encoded the defect — investigate and record which.

**Gate:** all structural checks pass · no collateral modifications · every DDN resolved with evidence · no test weakened.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 6.**

---

### PHASE 6 — Summary Update and Learning

**Invoke: defect-reporting-and-learning**

#### 6a — Update the Parent CODE_GENERATION_SUMMARY.md

**Path:** `.SS_WF/Agent/CODE/{{parent_story_id}}_CODE_GENERATION_SUMMARY.md`

⚠️ **Updated in place. There is no separate defect document.**

**State sections — UPDATE (they must describe the code as it is now):**

```text
§3   File Inventory        → changed files + new test files
§4   UI Components         → if a component changed
§5   Sitecore field → prop → if a mapping changed
§6   Logic & API           → if a layer changed
§7   Data Flow Trace       → per affected field (line numbers, defaults)
§8   State → UI Matrix     → per affected state
§9   Design & NFR Notes    → if tokens or exceptions changed
§10  Tests & Coverage      → add regression tests
§12.4 Known Limitations    → mark Resolved if a fix closed one
§11  AC Evidence           → status only, if an AC now passes
```

**Historical sections — LEAVE UNTOUCHED:**

```text
§1   Developer Notes Applied   — records the original build
§2   Story & Classification
§12.1 Decisions & Conflicts
§12.2 Assumptions
§12.5 Validation Exceptions
```

**Tag every changed row** with the defect ID: `[DEF-123]`

#### 6a-2 — Append the §13 Change Log Entry

This carries the **defect-specific record** that a separate document would otherwise hold:

```text
DDN applied · context refetch + diff · per-issue table (category, status,
root cause, fault origin, fix, regression test, failed-first) · sections
updated · existing tests modified · observations not fixed · learnings
written · notes for the developer
```

⚠️ **Append below existing entries, newest last.** Never edit or remove a prior entry — this log is the audit trail. If the summary predates §13, create it.

#### 6b — Learning Update (Gated)

**Path:** `./src/.project/learnings/CODING_AGENT_LEARNINGS.md`

```text
IF fault origin is "Agent miss" OR "Regression from prior fix":
   1. Determine the namespace (UI / LOGIC / TEST / STORYBOOK LEARNINGS)
   2. Search for a semantically equivalent existing rule
   3. Found     → increment recurrence, append this defect ID
   4. Not found → append a new entry as a RULE, not a war story
   5. Recurrence ≥ 3 → flag "SKILL GAP: this rule keeps firing"
ELSE:
   Do NOT write a learning. Record the origin in the §13 entry instead.
```

⚠️ Both files updated via **read → merge → write back**. Do not assume an append mode exists.

**Gate:** every state section the fix touched is updated and tagged · historical sections untouched · §13 entry appended with all blocks · prior entries intact · untouched content preserved byte for byte · learning appended only for agent-miss/regression · deduplication performed · skill gap flagged at recurrence ≥ 3 · **no separate defect document produced**.

> **➡️ Gate passed → RUN COMPLETE.** Report the updated summary path and any skill-gap flags.

---

## Skill Invocation Map

| Phase | Skill | New / Reused | Writes files? |
| --- | --- | --- | --- |
| 1 | defect-intake-and-decomposition | 🆕 New | ❌ |
| 2 | defect-context-loader | 🆕 New | ❌ |
| 2r | **context-gathering** | ♻️ **Reused** | ✅ artefacts only, selective |
| 3 | defect-root-cause-analysis | 🆕 New | ❌ |
| 4 | defect-fix-and-regression-test | 🆕 New | ✅ fixes + tests |
| 4d | *(coding skills by category)* | ♻️ Reused | ✅ via the fix skill |
| 5 | generated-code-self-validation | ♻️ Reused | ❌ |
| 6 | defect-reporting-and-learning | 🆕 New | ✅ summary update + learnings |
| all | developer-notes-protocol | ♻️ Reused | ❌ |

**6 new skills. Eleven coding skills reusable** — which keeps fixes conforming to the same standards as generated code.

### Coding Skills NOT Reusable

| Skill | Why |
| --- | --- |
| `implementation-contract-loader` | Loads the plan *to build from*; `defect-context-loader` loads plan **+ summary** *to locate from* |
| `master-react-coding-orchestrator` | The defect orchestrator owns the sequence |

---

## Global Guardrails

### Always Do
- **Execute all phases in one continuous run**; loop 3–4 per issue.
- **Apply the minimal-change contract** to code AND to the summary update.
- **Write a failing test before every fix** and prove it fails first.
- **Classify fault origin** for every issue — it gates the learning update.
- **Check §13 Change Log** for prior fixes that may have caused a regression.
- **Refetch selectively** via `context-gathering` — one artefact, both gate conditions met.
- **Snapshot before refetching**; the diff is the diagnostic value.
- **Scope fixes to the reported delta** when an artefact was refetched.
- **Update every state section the fix changed** so the summary stays accurate.
- **Tag every changed summary row** with the defect ID.
- Determine blast radius before changing shared or design-system code.
- Apply DDN above DN; record any supersession.
- Load coding skills **by category only** — never speculatively.
- Record unrelated problems as observations in the §13 entry.
- Preserve ISSUE, DDN, DN, AC and GAP IDs exactly.
- Deduplicate learnings before appending.

### Never Do
- **Never produce a separate `DEFECT_FIX_SUMMARY.md`** — the §13 Change Log replaced it.
- **Never leave a state section stale** after changing the code it describes.
- **Never modify historical sections** (§1, §2, §12.1, §12.2, §12.5).
- **Never edit or remove a prior §13 Change Log entry.**
- **Never regenerate the summary** — targeted, tagged row updates only.
- **Never re-read or re-analyse the story JIRA ticket** — the Analysis Plan has it.
- **Never re-run story analysis.**
- **Never invoke all three `context-gathering` tasks** — selective only.
- **Never refetch** unless both gate conditions are met.
- **Never overwrite an artefact without snapshotting it first.**
- **Never re-run Figma reconciliation** — work from raw viewport JSONs.
- **Never re-implement a component against a refreshed design** — fix the reported delta only.
- **Never attempt a structural change** — escalate to the Analysis Agent.
- **Never read `DEV_REVIEW.md`.**
- **Never refactor, rename, reformat, or improve code outside the RCA finding.**
- **Never fix an unrelated problem you happen to notice.**
- **Never weaken, skip, or delete an existing test to make a fix pass.**
- **Never apply a fix without a test that failed first.**
- **Never write a learning for upstream gaps, contract changes, design changes, or ambiguous requirements.**
- **Never assume an append mode exists** — read, merge, write back.
- **Never close, transition, or comment on the defect ticket** — lifecycle is the developer's.

---

## Quick Reference

```text
PHASE 1  Intake            [defect-intake-and-decomposition]
          → split into ISSUE-001… · extract DDN-001… · categorise
          → flag source-change signals (design / contract)

PHASE 2  Context Load      [defect-context-loader]
          → Analysis Plan · Code Gen Summary (§3 §5 §7 §8 §9 §12 §13) · Learnings
          → §13 Change Log shows prior fixes on this component
          → SELECTIVE refetch via [context-gathering]:
               UI/RTL/Responsive/Media → Figma only
               Sitecore                → Sitecore only
               BFF/API/mapper          → BFF only
               State/A11y/Missing AC   → none
            both gate conditions required · SNAPSHOT first · DIFF after
          → NO reconciliation re-run · NO story re-read · NO re-analysis

┌──────────────── PER ISSUE ────────────────┐
PHASE 3  RCA               [defect-root-cause-analysis]
          → locate via §7/§8/§5/§9/§3 → file:line + mechanism
          → check §13 for a regression from a prior fix
          → classify FAULT ORIGIN (6 origins; 2 write learnings)
          → blast radius

PHASE 4  Fix + Test        [defect-fix-and-regression-test]
          → test FAILS first ← proves RCA
          → minimal fix (coding skills by category)
          → SCOPE TO DIFF if artefact refetched
          → structural change → ESCALATE, do not attempt
          → test PASSES · existing tests still pass
└───────────────────────────────────────────┘

PHASE 5  Validation        [generated-code-self-validation]  ← reused, scoped
          → structural + no collateral changes + no weakened tests

PHASE 6  Summary + Learning [defect-reporting-and-learning]
          → UPDATE parent CODE_GENERATION_SUMMARY.md IN PLACE:
               state sections (§3 §4 §5 §6 §7 §8 §9 §10 §11 §12.4) — tagged [DEF-xxx]
               historical sections (§1 §2 §12.1 §12.2 §12.5) — untouched
               §13 Change Log — append the defect entry
          → learnings ONLY if agent-miss/regression
          → dedupe · recurrence ≥3 = SKILL GAP flag
          → NO separate defect document
```
