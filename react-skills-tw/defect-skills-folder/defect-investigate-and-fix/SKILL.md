---
name: defect-investigate-and-fix
description: Reproduce a triaged frontend defect, find its root cause in the code, fix it, and verify every related scenario. Use in Phase 2 of the defect workflow.
---

## Defect Investigate and Fix

### Stance

The defect is real and already triaged. The ticket's Actual vs Expected is ground truth.
If the code looks correct to you, your understanding is incomplete, not the ticket.
There is no "not a defect", "already fixed" or "cannot reproduce" outcome.

### Goal

Make the ticket's expected behaviour true and keep every related scenario correct,
proven by tests that run in this workspace.

---

### 1. Context: baseline vs deviation

Baseline (agreed contract):

- `.SS_WF/Agent/Analysis/{{$var[parent_ticket_id]s}}_ANALYSIS_PLAN.md`: ACs, states, Sitecore fields and data, BFF endpoints and request/response/error samples - Read this only and only if you need more context.
- `figma-output/`: design context (desktop, mobile, responsive intent)
- `.SS_WF/Agent/CODE/{{$var[parent_ticket_id]s}}_CODE_GENERATION.md`: file map only, not proof - Read this to understand what all files were created/updated for parent jira ticket.

For each contract (BFF, Sitecore, Figma), use the intake's CONTRACTS line:

- **UNCHANGED** (the ticket gives no data for it): the baseline is a fixed, correct input.
  The fault is in how the code consumes, transforms, stores or renders it.
  Never attribute the defect to this contract, never recommend verifying it externally, never wait on it.
- **DEVIATED** (the ticket gives data for it): diff it against the baseline, record each
  difference, and make the code satisfy the ticket's version.

Load more on demand: any repo file, the analysis plan, figma-output, existing test fixtures,
git history. No permission needed. Record what you loaded beyond the minimum and why.
No live API, no running app, no external mock server. The baseline files and repo fixtures are your data.

Developer notes in the ticket are hints. Use them, but never treat them as proof or as a substitute for tracing.

---

### 2. Reproduce first

- Write a test that follows the ticket's steps at the level the user observes:
  render the screen or container, perform the action, assert what the user should see.
- Build fixtures from the baseline (or the ticket's version if DEVIATED). Reuse matching repo fixtures.
- Mock only the outermost boundary (network fetch, CMS props). Never mock a function on the path you are investigating.
- Run it with `run-test-cases`. If it passes, your reproduction is wrong, not the code.
  Make the data, sequence or state closer to the ticket until it fails.

### 3. Investigate the code

With the reproduction failing and the data fixed, the cause is in the code.
Read the path from the user action to what renders and explain the mechanism:
why the TRIGGER with this data produces the OBSERVED behaviour.
Verify each step against the data rather than assuming it: how a value is parsed,
which branch it takes, what state it sets, what clears or overrides that state later,
and what conditions gate the render.
If a step looks correct, prove it with the test (assert intermediate state or add temporary logging).

### 4. Fix the root cause, not the symptom

Fix at the layer where the behaviour is wrong. Do not patch downstream to hide an upstream fault.
Follow the coding standards for the issue's category. No unrelated refactors.

### 5. Scenario sweep (mandatory)

List every scenario that passes through the behaviour you changed, then verify each one:

- Sibling cases: other error codes, success path, missing or empty CMS content, fallbacks
- Related ACs and states from the analysis plan
- State transitions: error, retry, success; repeated failures; timers and resets
- Locale and responsive variants if the change touches UI
- Every consumer of the changed code (grep) and its existing tests
- New scenarios the fix itself introduces

Each scenario ends as one of: new test, existing test, gap found and fixed,
or gap outside FE (documented with evidence, DEVIATED contracts only).
If the sweep finds related bugs on the same behaviour, fix them in this run.

### 6. Done when

- The reproduction test failed before the fix and passes after it
- Scenario tests and existing related tests pass
- `git diff --stat` (run from the repo root) contains at least one non-test source file

### Never

- Never weaken, skip or delete an existing test. Update one only if it encoded the wrong behaviour, and say why.
- Never report a change the diff does not show.
- Never close, comment on or transition the ticket.

---

### Output (one block per issue)

```text
ISSUE-<n>   FIXED | BLOCKED
  Root cause:  <file>: <mechanism, in one or two sentences>
  Contracts:   BFF <UNCHANGED|DEVIATED>, Sitecore <...>, Figma <...>
  Extra context loaded: <file: reason> | none
  Reproduction: <test name>   before: FAIL   after: PASS
  Scenarios:
    <scenario>: <new test | existing test | gap fixed | outside FE: evidence>
  Diff:        <pasted git diff --stat>
```

BLOCKED is allowed only when a DEVIATED contract needs a backend, CMS or design change
the frontend cannot provide. State the exact baseline-vs-ticket difference.
An UNCHANGED contract can never be the reason for BLOCKED.
