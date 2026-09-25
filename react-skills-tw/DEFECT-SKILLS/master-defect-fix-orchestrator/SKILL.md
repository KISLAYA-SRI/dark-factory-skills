---
name: master-defect-fix-orchestrator
description: Use when orchestrating the end-to-end FE Defect Fix workflow that turns a JIRA defect ticket into surgical code fixes proven by executed tests. Defines the mandatory phase sequence, per-issue loop, current-code-first diagnosis, selective context refetch, skill selection by issue category, minimal-change contract, fix impact analysis, executed failing-first and blast-radius tests, in-place summary update, and the learning feedback loop. Triggers include defect fix, bug fix, fix defect, defect workflow, or regression fix. Invoked when the user says something like "Fix defect <TICKET_ID>" or "Resolve DEF-1234".
disable-model-invocation: true
---

## Master Defect Fix Orchestrator

### Purpose

This is the **master orchestration skill** for the FE Defect Fix Agent. It defines:
- **What** the agent must do — locate, fix, prove, and record.
- **In what order** — the mandatory phase sequence with a per-issue loop.
- **What counts as truth** — the current code for what exists; the plan and Dev Notes for what is required.
- **Which skills load** — selected per issue category, never speculatively.
- **When external sources may be refetched** — selectively, via `context-gathering`.
- **How fixes are proven** — tests are **executed** via `run-test-cases`, never predicted.
- **What is updated** — the parent summary stays current; the learnings loop closes.

---

## ⚠️ DEFECT FIXING IS NOT CODE GENERATION

| | Code Generation | Defect Fixing |
| --- | --- | --- |
| Input | Finalised plan | Ambiguous symptom |
| First task | Build | **Locate** |
| Scope of change | Whole story | **Minimal surgical change** |
| Scope of checking | Generated files | **Everything the change can affect** |
| Biggest risk | Missing a requirement | **Regression + scope creep** |
| Tests | Written, not run | **Written and executed** |

You are **repairing existing code**, not generating new features.

---

## ⚠️ THREE GOVERNING PRINCIPLES

### 1. The current code is the territory. The documents are the map.

After generation, developers routinely change the code — the generated version did not always work, or the logic needed adjusting. **The Analysis Plan and Code Generation Summary describe what the workflow produced, not necessarily what is on disk today.**

```text
WHAT EXISTS NOW        → the CURRENT CODE is the authority
                         (summary is a map to find it — verify every claim against the file)

WHAT IS REQUIRED       → DDN → DN → Analysis Plan ACs/states
                         (the code does not define correctness)
```

```text
❌ Never assume the code matches the summary
❌ Never revert a developer's change because it differs from the summary
❌ Never treat a difference from the summary as a defect by itself
✅ Read the current code for every file in scope before diagnosing
✅ Record every divergence as DRIFT and reconcile the summary rows you touch
```

⚠️ A divergence from the summary is **information, not a bug**. It may be a deliberate developer fix. Only a divergence from the **requirement** is a defect.

### 2. Change narrowly. Verify widely.

```text
CHANGE  → only what Root Cause Analysis named          (minimal-change contract)
VERIFY  → everything the change can affect              (fix impact analysis)
```

The minimal-change contract limits what you **edit**. It never limits what you **check**. Every fix must be tested against the edge cases, branches, locales, states and consumers that pass through the changed lines.

### 3. Tests are executed, not predicted.

Every test claim is backed by a run of `run-test-cases`. A test you *reason* would pass is a prediction; a run that passes is evidence. If tests cannot be executed, the record says **STATIC ONLY** — it never claims a result.

---

## ⚠️ EXECUTION CONTRACT

### Rule 1 — Run all phases without stopping

When a phase gate passes, **immediately invoke the next phase in the same run**. Do not pause. Do not ask whether to continue.

### Rule 2 — EXACTLY THREE conditions stop the run

| # | Stop condition | Where | What happens |
| --- | --- | --- | --- |
| 1 | Defect ticket missing/unreadable | Phase 1 | HALT |
| 2 | ANALYSIS_PLAN.md missing | Phase 2 | HALT — no correctness oracle |
| 3 | Phase 6 has updated CODE_GENERATION_SUMMARY.md | Phase 6 | Run complete |

**No other event ends the run.** A blocked issue does not stop the run — record it and continue.

### Rule 3 — Announce transitions

```text
Phase 3 complete (ISSUE-002) → proceeding to Phase 4 (Fix + Regression Test)
```

---

## ⚠️ WRITE FILES, NOT DESCRIPTIONS

```text
✅ Every fix applied to the actual file at the exact path
✅ Every regression and guard test written AND executed
✅ The parent summary updated so it describes the code accurately
❌ Describing what the fix would be
❌ Producing only an RCA or a plan
❌ Claiming a test passed without a run
```

**Order: read current code → locate → write failing test → RUN (must fail) → fix → RUN (must pass) → run guards + blast radius → update the record.**

---

## ⚠️ THE MINIMAL-CHANGE CONTRACT (NON-NEGOTIABLE)

```text
CHANGE ONLY what Root Cause Analysis explicitly named.

❌ No refactoring of surrounding code
❌ No "while I'm here" improvements
❌ No renaming, reordering, or reformatting
❌ No dependency upgrades
❌ No unrelated file touches
❌ No adding features the defect did not ask for
❌ No reverting developer changes to match the summary

Unrelated problem noticed → record as an observation in the §13 entry. Do NOT fix it.
```

⚠️ This contract also governs the **summary update** — only the rows the fix touched, plus drift reconciliation for rows RCA inspected.

---

## Inputs

| Input | Source | Required? |
| --- | --- | --- |
| Defect ticket | `.SS_WF/{{ticket_id}}_JIRA_OUTPUT_.json` | **Mandatory** |
| Defect Dev Notes (DDN) | Section inside the defect ticket | If present — **TOP priority** |
| **Current source code** | The repository, as it is now | **Mandatory — authority for what exists** |
| Analysis Plan | `.SS_WF/Agent/Analysis/{{parent_story_id}}_ANALYSIS_PLAN.md` | **Mandatory — authority for what is required** |
| Code Gen Summary | `.SS_WF/Agent/CODE/{{parent_story_id}}_CODE_GENERATION_SUMMARY.md` | **Mandatory*** — the map |
| Coding Agent Learnings | `./src/.project/learnings/CODING_AGENT_LEARNINGS.md` | **Mandatory** |
| Component Catalogue | `./src/component-catalogue.json` | For blast radius |
| Git history | `git log` / `git blame` | If available — drift evidence |
| Existing artefacts | `.SC_API_SPEC/` · `.BFF_API_SPEC/` · `figma-output/` | On-disk copies |

*If missing, fallback discovery applies — see Phase 2.

⚠️ **The parent story** is the story the defect was raised against. All documents come from that story ID.
⚠️ **The parent story JIRA output is NOT an input** — the Analysis Plan carries it.
⚠️ **`DEV_REVIEW.md` is NOT an input.**

---

## ⚠️ DEV NOTES AND AUTHORITY

```text
DDN-001…   Defect Dev Notes   ← TOP PRIORITY, from the defect ticket
DN-001…    Story Dev Notes    ← from Analysis Plan §1, still binding
```

If a DDN contradicts a DN, follow the DDN and record the supersession in the §13 entry.

### Two Questions, Two Authorities

| Question | Authority, highest first |
| --- | --- |
| **What should the behaviour be?** | DDN → DN → refetched artefact (if a source changed) → Analysis Plan (§4 ACs, §10 states, §11 contracts) → project guidelines |
| **What does the code do now?** | **Current code** → git history → Code Gen Summary (map only) |

⚠️ Never answer the first question from the code, and never answer the second from the summary.

---

## ⚠️ SELECTIVE CONTEXT REFETCH — VIA `context-gathering`

External sources can change after generation. When they do, the code is not necessarily wrong — **the source moved**.

| Issue category | Refetch |
| --- | --- |
| UI · RTL · Responsive · Media | **Figma only** |
| Sitecore | **Sitecore only** |
| BFF · API · mapper | **BFF only** |
| State · A11y · Missing AC · Regression | **None** |

**Both gate conditions required:** (1) category matches the artefact; (2) evidence the source actually changed. Otherwise use the on-disk artefact.

⚠️ Never invoke all three tasks. ⚠️ **Snapshot before refetching** — the diff is the diagnostic value. ⚠️ Never re-run Figma reconciliation; work from raw viewport JSONs.

---

## ⚠️ FAULT ORIGINS — SEVEN, TWO WRITE LEARNINGS

| Origin | Meaning | Learning? |
| --- | --- | --- |
| **Agent miss** | Coding agent had what it needed and got it wrong | ✅ Yes |
| **Regression from prior fix** | An earlier defect fix (see §13) broke this | ✅ Yes |
| Upstream gap | Analysis Plan omitted or mis-specified it | ❌ |
| Contract change | Sitecore/BFF contract changed after generation | ❌ |
| Design change | Figma updated after generation | ❌ |
| **Post-generation manual change** | A developer modified the code after generation and the defect lives in that change | ❌ |
| Ambiguous requirement | AC open to interpretation | ❌ |

⚠️ **Post-generation manual change** exists because the agent is not the only author. If the failing line was written by a developer after generation (evidence: git history, drift from the summary with no `[DEF-xxx]` tag), the coding agent did not produce the fault and must not be "taught" a rule for it.

---

## Mandatory Execution Sequence

```text
PHASE 1  Intake + Decomposition     [defect-intake-and-decomposition]
PHASE 2  Context Load               [defect-context-loader]
          └─ selective refetch      [context-gathering]  ← reused, gated, per-artefact
──────────────── PER-ISSUE LOOP ────────────────
PHASE 3  Root Cause + Impact        [defect-root-cause-analysis]
          └─ current code read first · drift detected · edge-case matrix built
PHASE 4  Fix + Tests (EXECUTED)     [defect-fix-and-regression-test]
          ├─ coding skills by category
          └─ test execution         [run-test-cases]
──────────────── CONVERGE ────────────────
PHASE 5  Validation                 [generated-code-self-validation] + [run-test-cases]
PHASE 6  Summary Update + Learning  [defect-reporting-and-learning]
```

---

### PHASE 1 — Intake and Decomposition

**Invoke: defect-intake-and-decomposition**

Split the ticket into independently-fixable issues (`ISSUE-001…`), extract Defect Dev Notes (`DDN-001…`), categorise each issue, flag source-change signals, capture reproduction evidence. The split is **semantic** — one paragraph can hold three issues.

**Gate:** every distinct problem is its own ISSUE · DDN extracted · categorised · source-change signals flagged · evidence captured.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 2.**

---

### PHASE 2 — Context Load

**Invoke: defect-context-loader**

Load the Analysis Plan (all 13 sections), the Code Gen Summary (all 13 sections, including the **§13 Change Log**), the learnings, the catalogue, and the on-disk artefacts. Record the summary's generation date and the dates of §13 entries — Phase 3 uses them for drift evidence. Refetch selectively only where both gate conditions hold.

⚠️ **The summary is loaded as a map.** Phase 3 verifies every location against the current code.

**Gate:** plan, summary and learnings loaded · generation and §13 dates recorded · issues cross-checked against §12.4 and §2 · refetch only where gated, with snapshot and diff · no re-analysis.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 3 for ISSUE-001.**

---

### PHASE 3 — Root Cause and Impact Analysis (Per Issue)

**Invoke: defect-root-cause-analysis**

1. **Read the current code first** for every file the summary points to. Establish what the code actually does.
2. **Detect drift** — where current code differs from the summary, record it; use git history to tell a developer change from a prior defect fix.
3. **Locate** the root cause to file + line + mechanism.
4. **Classify fault origin** (seven origins).
5. **Blast radius** — who consumes the changed code, and **which test files cover them**.
6. **Fix Impact Analysis** — the edge-case matrix for everything that flows through the lines about to change.
7. **Test plan** — regression test, guard tests, blast-radius test files, for Phase 4 to execute.

**Gate (per issue):** current code read · drift recorded · root cause named to file + line + mechanism · origin classified · §13 checked for regressions · blast radius with concrete test files · edge-case matrix built · test plan written.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 4 for this issue.**

---

### PHASE 4 — Fix and Tests, Executed (Per Issue)

**Invoke: defect-fix-and-regression-test** — which runs tests via **run-test-cases**.

```text
1. Write the regression test
2. RUN  --expect fail --name "<DEF / ISSUE>"   → verdict EXPECTED_FAIL      ← proves the RCA
3. Apply the minimal fix on top of the CURRENT code
4. RUN  the regression test                     → verdict PASS
5. Write guard tests for the edge-case matrix
6. RUN  guard tests                             → verdict PASS
7. RUN  blast radius: co-located tests of every changed file
        + consumer test files from RCA + --related on changed sources → PASS
```

| Verdict at step 2 | Meaning | Action |
| --- | --- | --- |
| `EXPECTED_FAIL` | Root cause proven | Continue |
| `PASSED_UNEXPECTEDLY` | Root cause is wrong | Return to Phase 3 |
| `FAILED_FOR_WRONG_REASON` | Load error or a different test failed | Fix the test **setup**, re-run |
| `NOT_COLLECTED` | File never ran | Fix placement/path, re-run |

⚠️ Guard tests **may pass before the fix** — they protect neighbouring behaviour. Only the regression test must fail first.

⚠️ If tests cannot run (script exit 4 or 5), record **STATIC ONLY** with the exact command for the developer. Never claim a result.

**Gate (per issue):** regression test EXPECTED_FAIL then PASS · guard tests PASS · blast-radius tests PASS · minimal fix on current code · no developer change reverted · no test weakened · run output folders recorded.

> **➡️ More issues → loop to PHASE 3. All done → IMMEDIATELY invoke PHASE 5.**

---

### PHASE 5 — Validation

**Invoke: generated-code-self-validation** (scoped to changed files) **and run-test-cases** (final consolidated run).

```text
Final run: every test file touched in this defect + every blast-radius test file,
           in ONE run-test-cases invocation, label "{{ticket_id}}-final" → must PASS
```

A per-issue pass does not prove the combined set passes — two fixes can interact.

**Defect-specific checks:**

```text
- [ ] ONLY RCA-named files modified — no collateral changes
- [ ] No developer change reverted to match the summary
- [ ] Every issue: regression test EXPECTED_FAIL then PASS (executed)
- [ ] Every issue: guard tests and blast-radius tests PASS (executed)
- [ ] Final consolidated run PASS
- [ ] No existing test weakened, skipped, or deleted
- [ ] Every DDN resolved with evidence
- [ ] No hardcoded values, tokens bypassed, or guardrails broken
- [ ] Refetched-artefact fixes stayed scoped to the reported delta
```

**Gate:** structural checks pass · final consolidated run PASS (or STATIC ONLY recorded) · no collateral changes.

> **➡️ Gate passed → IMMEDIATELY invoke PHASE 6.**

---

### PHASE 6 — Summary Update and Learning

**Invoke: defect-reporting-and-learning**

**6a — Update the parent CODE_GENERATION_SUMMARY.md in place.** State sections (§3 §4 §5 §6 §7 §8 §9 §10 §12.4, §11 status only) updated for what the fix changed **and** reconciled for drift in the rows RCA inspected. Historical sections (§1 §2 §12.1 §12.2 §12.5) untouched. Rows tagged `[DEF-xxx]` or `[DEF-xxx · drift]`.

**6a-2 — Append the §13 Change Log entry**: DDN · refetch · per-issue table · **drift reconciled** · **edge cases verified** · **test execution evidence** · sections updated · tests modified · observations · learnings · developer notes.

**6b — Learning update**, gated: **only** agent miss or regression from prior fix. Deduplicate; recurrence ≥ 3 flags a skill gap.

⚠️ No separate defect document. Both files via read → merge → write back.

**Gate:** state sections current and tagged · drift reconciled for inspected rows · §13 entry complete with execution evidence · learning only for the two origins · no separate document.

> **➡️ Gate passed → RUN COMPLETE.** Report the summary path, verification level, and any skill-gap flags.

---

## Skill Invocation Map

| Phase | Skill | Source | Writes files? |
| --- | --- | --- | --- |
| 1 | defect-intake-and-decomposition | 🆕 Defect | ❌ |
| 2 | defect-context-loader | 🆕 Defect | ❌ |
| 2r | context-gathering | ♻️ Analysis | ✅ artefacts, selective |
| 3 | defect-root-cause-analysis | 🆕 Defect | ❌ |
| 4 | defect-fix-and-regression-test | 🆕 Defect | ✅ fixes + tests |
| 4d | *(coding skills by category)* | ♻️ Coding | ✅ via the fix skill |
| 4t / 5 | **run-test-cases** | 🆕 **Shared** | ✅ `TEST_RUNS/` evidence only |
| 5 | generated-code-self-validation | ♻️ Coding | ❌ |
| 6 | defect-reporting-and-learning | 🆕 Defect | ✅ summary + learnings |
| all | developer-notes-protocol | ♻️ Analysis | ❌ |

⚠️ `run-test-cases` is a **shared** skill — the static code quality workflow will use it for package-level runs.

---

## Global Guardrails

### Always Do
- **Read the current code before diagnosing** — the summary is a map, not the territory.
- **Record drift** between the code and the summary; use git history to explain it.
- **Change narrowly, verify widely.**
- **Execute every test claim** via `run-test-cases`; record the output folder.
- **Prove the root cause** with an `EXPECTED_FAIL` verdict before fixing.
- **Build the edge-case matrix** and cover it with guard tests.
- **Run blast-radius tests** — co-located, consumer, and `--related`.
- **Run a final consolidated test run** across all issues.
- Classify fault origin for every issue — seven origins, two write learnings.
- Check §13 for regressions from prior fixes.
- Refetch selectively via `context-gathering`; snapshot first; scope fixes to the reported delta.
- Apply DDN above DN; record supersession.
- Load coding skills by category only.
- Record unrelated problems as observations.
- Update state sections the fix touched; reconcile drift in rows RCA inspected.

### Never Do
- **Never assume the code matches the summary.**
- **Never revert a developer's change to match the summary.**
- **Never treat drift from the summary as a defect by itself.**
- **Never claim a test result without executing it** — label STATIC ONLY instead.
- **Never accept `PASSED_UNEXPECTEDLY`, `FAILED_FOR_WRONG_REASON` or `NOT_COLLECTED` as proof.**
- **Never build test commands by hand** — use `run-test-cases`.
- **Never write a learning for a post-generation manual change**, upstream gap, contract change, design change, or ambiguity.
- Never produce a separate `DEFECT_FIX_SUMMARY.md`.
- Never modify historical summary sections or prior §13 entries.
- Never re-read the parent story ticket or re-run analysis.
- Never invoke all three `context-gathering` tasks; never refetch without both gate conditions.
- Never re-run Figma reconciliation.
- Never re-implement a component against a refreshed design.
- Never attempt a structural change — escalate to the Analysis Agent.
- Never read `DEV_REVIEW.md`.
- Never refactor, rename, reformat, or improve code outside the RCA finding.
- Never weaken, skip, or delete an existing test to make a fix pass.
- Never assume an append mode exists — read, merge, write back.
- Never close, transition, or comment on the defect ticket.

---

## Quick Reference

```text
PHASE 1  Intake            → ISSUE-001… · DDN-001… · category · source-change signals

PHASE 2  Context Load      → Plan (what is required) · Summary + §13 (the map) · Learnings
                           → selective refetch via context-gathering (gated, snapshot, diff)

┌──────────────── PER ISSUE ────────────────┐
PHASE 3  RCA + Impact      → READ CURRENT CODE FIRST · drift vs summary (git evidence)
                           → file:line + mechanism · 7 fault origins · §13 regression check
                           → blast radius WITH test files · EDGE-CASE MATRIX · test plan

PHASE 4  Fix + Tests       → regression test → run-test-cases --expect fail → EXPECTED_FAIL
                           → minimal fix on current code
                           → regression PASS · guard tests PASS · blast radius PASS
└───────────────────────────────────────────┘

PHASE 5  Validation        → scoped structural gate · FINAL consolidated run → PASS

PHASE 6  Record            → summary state sections updated + drift reconciled, tagged
                           → §13 entry incl. drift · edge cases · execution evidence
                           → learnings ONLY for agent miss / regression
```
