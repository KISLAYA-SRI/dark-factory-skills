---
name: master-defect-fix-orchestrator
description: Use when orchestrating the FE Defect Fix workflow that turns a JIRA defect ticket into a surgical, test-proven code fix. Defines the phase sequence, symptom-anchored diagnosis, orientation-only context, executed tests, evidence gates, in-place summary update and the learning loop. Triggers include defect fix, bug fix, fix defect, defect workflow. Invoked as "Fix defect <TICKET_ID>".
disable-model-invocation: true
---

## Master Defect Fix Orchestrator

### Variables

```text
{{$var[ticket_id]s}}          the DEFECT ticket
{{$var[parent_ticket_id]s}}   the story it was raised on
```

---

## ⚠️ FOUR GOVERNING PRINCIPLES

**1. The symptom is the anchor.** Every issue has a contract — TRIGGER · OBSERVED · EXPECTED — taken from the ticket. The root cause is the mechanism that turns that TRIGGER into that OBSERVED. A cause on a different trigger is wrong, however plausible.

**2. Context orients; it never diagnoses.** The code-gen document says which files implement the feature. Comments, ticket tags, docs and prior fixes describe history and intent. Only the code path the trigger executes is evidence.

**3. Change narrowly; verify widely.** Edit only what RCA names; test everything the edit can reach.

**4. Evidence, not narrative.** Every claim is backed by a `VERDICT=` line or a `git diff --stat`. If neither exists, the claim is not made.

---

## Output discipline

One line per phase. One final report. No narration, no file listings, no recaps.

---

## Phase Sequence

```text
1  Intake          [defect-intake-and-decomposition]   symptom contract per issue
2  Context         [defect-context-loader]             feature map + trigger entry
── per issue ──
3  RCA             [defect-root-cause-analysis]        trace → symptom-fit → origin → plan
4  Fix + Tests     [defect-fix-and-regression-test]    → [run-test-cases]  → git diff
── converge ──
5  Validation      [generated-code-self-validation] + one consolidated test run
6  Record          [defect-reporting-and-learning]
```

Only two things end the run: missing defect ticket (HALT), or Phase 6 complete. A BLOCKED issue does not stop the run.

### 1 · Intake
Locate the ticket **by pattern**. Extract TRIGGER · OBSERVED · EXPECTED · SIGNALS per issue. Ignore ticket-title prefixes. Read no other ticket.

### 2 · Context
Locate the parent code-gen document **by pattern**; any format is fine. Build the feature map and identify the trigger entry. Missing sections (including §13) are not a problem. Read no other `.SS_WF` documents.

### 3 · RCA
Trace the trigger path from the entry, opening every hop. Apply the relevance filter — comments, tags and off-path code are noise. Pass the four-question symptom-fit test or mark the issue BLOCKED. Then origin, blast radius, edge-case matrix, test plan.

### 4 · Fix + Tests
Regression test reproduces the TRIGGER → `EXPECTED_FAIL` → minimal fix → `PASS` → guards → blast radius → `git diff --stat`.
`PASSED_UNEXPECTEDLY` → return to Phase 3; nothing is fixed.

### 5 · Validation
Scoped structural gate + one consolidated run across every touched and blast-radius test file.

### 6 · Record
Update the parent summary and write learnings per `defect-reporting-and-learning`.

---

## ⚠️ EVIDENCE GATES — A PHASE IS NOT DONE WITHOUT THESE

| Phase | Done only when |
| --- | --- |
| 1 | Every issue has a symptom contract quoted from the ticket |
| 3 | Symptom-fit test answered YES ×4 — or the issue is BLOCKED with traced hops |
| 4 | `EXPECTED_FAIL` seen, then `PASS` seen · `git diff --stat` shows the RCA-named **source** file |
| 5 | Consolidated run verdict seen |
| 6 | Summary write confirmed |

⚠️ **Never mark a phase complete without its evidence.** Updating a todo list is not evidence.

### Reading test results

- First stdout line is `VERDICT=…`.
- Tool reports "Command failed" or no output → read `.SS_WF/Agent/TEST_RUNS/LATEST.json`.
- `STATIC ONLY` only after seeing `VERDICT=ENV_ERROR`.

---

## Final report — at most this

```text
TAW-516 — 1 issue · 1 fixed · 0 blocked · tests EXECUTED
  ISSUE-001  BFF/API  useOtpVerify.ts → onError: BE_OTP_INVALID not surfaced   agent miss  ✅
  git diff --stat:
    Portals/Sme/Features/Shared/OtpVerification/Hooks/useOtpVerify.ts      |  3 +-
    Portals/Sme/Features/Shared/OtpVerification/Hooks/useOtpVerify.test.ts | 24 +
  Tests:     failing-first EXPECTED_FAIL · after-fix PASS · guards PASS · blast PASS · final PASS
  Summary:   <path> updated
```

⚠️ The `git diff --stat` block is pasted from the command output. **The report may not describe any change that block does not show.**

---

## Skill Map

| Phase | Skill |
| --- | --- |
| 1 | defect-intake-and-decomposition |
| 2 | defect-context-loader (+ context-gathering if gated) |
| 3 | defect-root-cause-analysis |
| 4 | defect-fix-and-regression-test · coding skills by category (standards only) · run-test-cases |
| 5 | generated-code-self-validation (scoped) · run-test-cases |
| 6 | defect-reporting-and-learning |
| all | developer-notes-protocol |

---

## Global Guardrails

### Always
- Anchor every issue on its TRIGGER · OBSERVED · EXPECTED.
- Locate files by pattern; trace code by following calls.
- Back every claim with a verdict or a diff.

### Never
- **Never diagnose from a comment, a ticket tag, a document claim, or a keyword match.**
- **Never accept a cause that runs at a different time than the trigger.**
- **Never fix after `PASSED_UNEXPECTEDLY`.**
- **Never declare STATIC ONLY from a failed tool call.**
- **Never mark FIXED when the diff shows only test files.**
- **Never report a change the diff does not show.**
- Never read the parent story ticket, other defects' tickets, or `DEV_REVIEW.md`.
- Never hunt for missing document sections.
- Never use `parent_story_id`.
- Never refactor, fix unrelated problems, revert developer changes, or weaken a test.
- Never close or comment on the ticket.
