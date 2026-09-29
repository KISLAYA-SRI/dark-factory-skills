---
name: master-defect-fix-orchestrator
description: Use when orchestrating the end-to-end FE Defect Fix workflow that turns a JIRA defect ticket into surgical code fixes proven by executed tests. Defines the phase sequence, per-issue loop, lean context policy, current-code-first diagnosis, minimal-change contract, executed failing-first and blast-radius tests, in-place summary update, and the learning feedback loop. Triggers include defect fix, bug fix, fix defect, defect workflow, or regression fix. Invoked when the user says something like "Fix defect <TICKET_ID>" or "Resolve DEF-1234".
disable-model-invocation: true
---

## Master Defect Fix Orchestrator

### Purpose

Master orchestration skill for the FE Defect Fix Agent — what to do, in what order, with which context, and what must be written back.

---

## ⚠️ VARIABLES

```text
{{$var[ticket_id]s}}          the DEFECT ticket            e.g. TAW-486
{{$var[parent_ticket_id]s}}   the story it was raised on   e.g. TAW-311
```



---

## ⚠️ OUTPUT DISCIPLINE

**Source files, tests and document updates are the deliverable. Narration is not.**

```text
Per phase, emit ONE line:
  Phase 3 (ISSUE-001) — root cause: PolicyMapper.ts → mapPolicyResponse() :41 · agent miss

At the end, emit the final report ONCE.
```

```text
❌ No "Phase N complete" summaries
❌ No restating what a phase does before doing it
❌ No listing files read, or echoing their contents
❌ No per-phase recaps of findings already recorded in the summary
❌ No narrating tool calls ("Now I'll run the tests…")
```

⚠️ Everything a reviewer needs ends up in the **§13 Change Log entry**. Saying it in chat as well is duplication.

**Final report — at most:**

```text
DEF-486 — 2 issues · 2 fixed · 0 blocked · tests EXECUTED
  ISSUE-001  RTL        CarouselPager.tsx → ms-2         agent miss      ✅
  ISSUE-002  BFF        PolicyMapper.ts → null default   contract change ✅
  Summary:   .SS_WF/Agent/CODE/TAW-311_CODE_GENERATION_SUMMARY.md (§13 updated)
  Learnings: 1 entry added to # UI LEARNINGS (recurrence ×2)
  ⚠️ SKILL GAP: none
```

---

## ⚠️ LEAN CONTEXT POLICY — LOAD ON DEMAND

Most defects are small. **Do not pre-load the whole paper trail.**

### Always loaded (Phase 1–2)

```text
1. Defect ticket        .SS_WF/{{$var[ticket_id]s}}_JIRA_OUTPUT_.json
2. Parent code summary  .SS_WF/Agent/CODE/{{$var[parent_ticket_id]s}}_CODE_GENERATION_SUMMARY.md
                        → §3 File Inventory · §5 field→prop · §7 Data Flow · §8 States
                          §12.4 Known Limitations · §13 Change Log
3. The current source files those sections point to
```

That is the default working set. **Nothing else is read unless a trigger below fires.**

### Loaded ONLY when a trigger fires

| Source | Load only when |
| --- | --- |
| **Analysis Plan** `{{$var[parent_ticket_id]s}}_ANALYSIS_PLAN.md` | You must decide whether the reported behaviour is **actually wrong** (code and summary disagree with the report), OR classify fault origin as agent miss vs upstream gap, OR the issue is "missing AC". **Read only the sections needed** — §4 ACs · §10 states · §1 Dev Notes · §8 out-of-scope |
| **Learnings** `./src/.project/learnings/CODING_AGENT_LEARNINGS.md` | Phase 6, before writing — and earlier only if the failure mode looks familiar |
| **Component catalogue** `./src/component-catalogue.json` | The fix touches a design-system or shared component (blast radius) |
| **Git history** | Current code differs from the summary and you must tell a developer change from a prior fix |
| **Refetched artefact** (Sitecore / Figma / BFF) | Both refetch gate conditions hold — see below |

⚠️ **Never read the parent story's JIRA ticket.** Never read `DEV_REVIEW.md`. Never re-run story analysis.

⚠️ **Trade-off, stated plainly:** the Analysis Plan is the only record of what was *required*. Skipping it by default keeps simple defects cheap, but means a reported behaviour is assumed wrong unless something contradicts it. When in doubt about correctness, load §4 and §10 — that is exactly what the trigger is for.

---

## ⚠️ THREE GOVERNING PRINCIPLES

**1. The current code is the territory; the summary is the map.**
Developers change generated code. Verify every location against the file. A difference from the summary is **drift** — information, not a defect. Never revert it.

**2. Change narrowly; verify widely.**
The minimal-change contract limits what you **edit**, never what you **check**.

**3. Tests are executed, not predicted.**
Every test claim comes from `run-test-cases`. If it cannot run, the record says **STATIC ONLY**.

---

## ⚠️ MINIMAL-CHANGE CONTRACT

```text
CHANGE ONLY what Root Cause Analysis named.

❌ No refactoring · renaming · reformatting · dependency changes
❌ No unrelated file touches · no features the defect did not ask for
❌ No reverting developer changes to match the summary

Unrelated problem noticed → record as an observation in §13. Do NOT fix it.
```

Applies to the summary update too: only the rows the fix touched, plus drift in rows RCA inspected.

---

## ⚠️ DEV NOTES

```text
DDN-001…   Defect Dev Notes (defect ticket)   ← TOP priority
DN-001…    Story Dev Notes (Analysis Plan §1) ← binding; load only if the plan is loaded
```

If a DDN contradicts a DN, follow the DDN and record the supersession.

---

## ⚠️ SELECTIVE REFETCH — VIA `context-gathering`

| Issue category | Refetch |
| --- | --- |
| UI · RTL · Responsive · Media | Figma only |
| Sitecore | Sitecore only |
| BFF · API · mapper | BFF only |
| State · A11y · Missing AC · Regression | None |

**Both conditions required:** category matches **and** there is evidence in the ticket that the source changed. Otherwise use the on-disk artefact.

⚠️ Never invoke all three tasks. **Snapshot before refetching** — the diff is the diagnostic value. Never re-run Figma reconciliation.

---

## ⚠️ FAULT ORIGINS — SEVEN, TWO WRITE LEARNINGS

| Origin | Learning? |
| --- | --- |
| **Agent miss** — code as generated, agent had what it needed | ✅ |
| **Regression from prior fix** — a §13 fix broke it | ✅ |
| Upstream gap — plan omitted it | ❌ |
| Contract change — Sitecore/BFF changed after generation | ❌ |
| Design change — Figma changed after generation | ❌ |
| **Post-generation manual change** — a developer wrote the faulty line | ❌ |
| Ambiguous requirement | ❌ |

⚠️ Classify **"is this code still as generated?" first.** Otherwise a developer's bug teaches the coding agent a rule for code it never wrote.

---

## Phase Sequence

```text
PHASE 1  Intake                [defect-intake-and-decomposition]
PHASE 2  Context Load          [defect-context-loader]  (+ context-gathering if gated)
──────── PER ISSUE ────────
PHASE 3  RCA + Impact          [defect-root-cause-analysis]
PHASE 4  Fix + Tests           [defect-fix-and-regression-test] → [run-test-cases]
──────── CONVERGE ────────
PHASE 5  Validation            [generated-code-self-validation] + [run-test-cases]
PHASE 6  Record + Learning     [defect-reporting-and-learning]
```

Run continuously. **Only two things end the run:** a missing defect ticket (HALT), or Phase 6 completing. A blocked issue does not stop the run.

### PHASE 1 — Intake
Split the ticket into `ISSUE-001…` semantically (one paragraph can hold three issues). Extract `DDN-001…`. Categorise. Flag source-change signals. Capture reproduction conditions — **they become the test conditions**.

### PHASE 2 — Context Load
Load the default working set. Record the summary's generation date and §13 fix dates for drift detection. Refetch only if gated.

### PHASE 3 — RCA + Impact (per issue)
Read the current code first; find symbols **by name, not line number**. Record drift. Name the root cause to **file + symbol + mechanism**. Classify fault origin. Determine blast radius **with the test files that cover it**. Build the **edge-case matrix** (data · branches · locale · state · consumers · developer-introduced behaviour). Write the test plan.

### PHASE 4 — Fix + Tests (per issue)

```text
1. Write the regression test
2. RUN --expect fail --name "…"  → EXPECTED_FAIL      ← proves the RCA
3. Apply the minimal fix on the CURRENT code
4. RUN                            → PASS
5. RUN guard tests (edge-case matrix)  → PASS
6. RUN blast radius (co-located + consumers + --related) → PASS
```

⚠️ Guard tests **may pass before the fix** — only the regression test must fail first.

Load coding skills by category for standards only — **never to regenerate the component**.

### PHASE 5 — Validation
Structural gate scoped to changed files, plus **one final consolidated run** across every touched and blast-radius test file. Two fixes can interact.

### PHASE 6 — Record + Learning
Update the parent summary in place; append the §13 entry; write learnings if gated. **Both files must be modified on disk — see below.**

---

## ⚠️ PHASE 6 MUST WRITE FILES

Identifying a learning is not the same as recording one.

```text
❌ "This should be added to # UI LEARNINGS: …"
❌ Printing the proposed entry and moving on
✅ Read the file → merge the entry → write the complete file back → confirm the write
```

The Phase 6 gate is **not satisfied** until:

```text
- [ ] CODE_GENERATION_SUMMARY.md written — state sections updated, §13 entry appended
- [ ] CODING_AGENT_LEARNINGS.md written — IF any issue was agent miss / regression
- [ ] Both writes confirmed (tool reported success)
```

If no issue qualifies for a learning, the learnings file is correctly left untouched — **say so explicitly** in the final report.

---

## Skill Map

| Phase | Skill | Source |
| --- | --- | --- |
| 1 | defect-intake-and-decomposition | Defect |
| 2 | defect-context-loader | Defect |
| 2r | context-gathering | Analysis *(gated)* |
| 3 | defect-root-cause-analysis | Defect |
| 4 | defect-fix-and-regression-test | Defect |
| 4d | coding skills by category | Coding *(standards only)* |
| 4t/5 | **run-test-cases** | Shared |
| 5 | generated-code-self-validation | Coding *(scoped)* |
| 6 | defect-reporting-and-learning | Defect |
| all | developer-notes-protocol | Analysis |

---

## Global Guardrails

### Always
- Use `{{$var[ticket_id]s}}` and `{{$var[parent_ticket_id]s}}`.
- Load the **default working set only**; pull more when a trigger fires.
- One line per phase; one final report.
- Read current code before diagnosing; record drift.
- Execute every test claim; record the output folder.
- Prove the root cause with `EXPECTED_FAIL` before fixing.
- Cover the edge-case matrix with guard tests; run the blast radius.
- **Write both documents in Phase 6 and confirm the writes.**

### Never
- **Never use `parent_story_id`.**
- **Never narrate phases** or restate findings already in §13.
- **Never pre-load the Analysis Plan, learnings, or catalogue** without a trigger.
- **Never read the parent story JIRA ticket or `DEV_REVIEW.md`.**
- **Never suggest a learning instead of writing it.**
- **Never claim a test result without an executed run.**
- **Never retry a failed test command with a different path form** — read the error.
- Never revert a developer's change; never treat drift as the defect.
- Never refactor while fixing; never fix unrelated problems.
- Never weaken, skip or delete an existing test.
- Never write a learning for a developer's change, contract change, design change, upstream gap, or ambiguity.
- Never produce a separate defect document — the §13 Change Log is the record.
- Never close or comment on the ticket.
