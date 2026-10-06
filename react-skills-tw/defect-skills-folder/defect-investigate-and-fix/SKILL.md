---
name: defect-investigate-and-fix
description: Phase 2 of the FE defect workflow. Reproduces a triaged defect with a failing test, traces the code to the root cause, fixes it at the right layer, and verifies every related scenario. Loads coding-standard skills on demand. Use for every issue produced by defect-intake-and-decomposition.
---

## Defect Investigate and Fix

### Stance

- The defect is real and already triaged. The ticket's Actual vs Expected is ground truth.
- If the code looks correct to you, your understanding is incomplete, not the ticket.
  Find what you have not read, not run, or not verified.
- There is no "not a defect", "already fixed", "working as designed" or "cannot reproduce" outcome.
- You are free to read any file, follow any call and run tests as often as needed.
  This skill defines the goal and the rules, not every step.

### Goal

Make the ticket's expected behaviour true **and** keep every related scenario correct,
proven by tests that run in this workspace.

---

## 1. Context

### 1.1 Starting context (minimum, already available)

| Source                   | Path                                                                 | Use it for                                                                           |
| ------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Intake block             | from Phase 1                                                         | Symptom contract, contracts classification, dev notes                                |
| Analysis plan            | `.SS_WF/Agent/Analysis/{{$var[parent_ticket_id]s}}_ANALYSIS_PLAN.md` | ACs, states, Sitecore fields and data, BFF endpoints, request/response/error samples |
| Figma output             | `figma-output/`                                                      | Design intent: desktop, mobile, responsive, RTL                                      |
| Code-generation document | `.SS_WF/Agent/CODE/{{$var[parent_ticket_id]s}}_CODE_GENERATION.md`   | File map only. It is not proof of behaviour                                          |

The code-generation document and analysis plan are large. Search them (`grep -n`) for the
feature, file or field you need and read only those sections. Never read either one end to end.

### 1.2 Baseline vs deviation

Use the intake's CONTRACTS line for each of BFF, Sitecore and Figma.

**UNCHANGED** (the ticket gives no data or reference for it)

- The baseline in the analysis plan / figma-output is a fixed, correct input. It has not changed and will not change.
- The fault is in how the code consumes, transforms, stores or renders that data.
- Never attribute the defect to this contract. Never recommend verifying it in Sitecore, the BFF or Figma. Never wait on it.

**DEVIATED** (the ticket gives data or a reference for it)

- Treat it as a change from the baseline. Diff the ticket's version against the baseline and record every difference.
- Make the code satisfy the ticket's version.
- If the ticket gives a reference (endpoint, Sitecore path, Figma link or node) instead of the data,
  load `context-gathering` and fetch **only that artefact**. Never fetch for UNCHANGED contracts.

### 1.3 Developer notes (DDN) — highest priority

- Dev notes are the highest-priority instruction. Only the ticket's Expected Result outranks them.
- They outrank the analysis plan, the code-generation document and your own judgement.
- If a dev note says where to look or how to fix, do that first.
- If a defect dev note conflicts with a parent-story developer note, the defect's note wins. Record it.
- Limits: a dev note never proves the code is correct, and having no dev notes never blocks or narrows the investigation.

### 1.4 Load more on demand

Open any repo file, more of the analysis plan, figma-output, existing test fixtures or mock files,
or git history whenever you need it. No permission needed. Record what you loaded beyond the
minimum and why.

### 1.5 Data you do not have

No live API, no running app, no external mock server. Your data is the baseline files
(or the ticket's DEVIATED version) plus fixture/mock files already in the repo.

---

## 2. Coding-standard skills: load on demand

Skills supply **standards only**. Never regenerate a component, page or feature.
Load a skill the first time the work needs it, whatever the issue's category. Load each one at most once per run.
Do not load skills speculatively.

| Load this skill                      | When                                                                                                                                                                 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend-test-generation`           | Always, before writing the reproduction test (test conventions, file placement, render helpers)                                                                      |
| `run-test-cases`                     | Always, to run any test. Never run raw `pnpm`/`vitest`/`jest` commands                                                                                               |
| `presentational-ui-generation`       | The fix touches markup, styles, Tailwind classes, layout, spacing, typography, RTL, responsive behaviour, accessibility attributes, or design-system component usage |
| `frontend-logic-integration`         | The fix touches hooks, services, API calls, containers, mappers, error handling, response parsing, toasts/notifications driven by API results                        |
| `frontend-state-and-form-management` | The fix touches local or global state, stores, form fields, validation, timers, counters, enable/disable logic                                                       |
| `sitecore-rendering-integration`     | The fix touches Sitecore field mapping, datasource props, rendering registration, dictionary or CMS message lookup                                                   |
| `frontend-media-integration`         | The fix touches images, icons, SVGs, video, DAM assets, lazy loading or media sizing                                                                                 |
| `repository-structure-governance`    | Before creating, moving or renaming **any** file or folder (component, hook, util, test, fixture)                                                                    |
| `context-gathering`                  | A contract is DEVIATED and the ticket gives a reference instead of the data (see 1.2)                                                                                |

A single fix often needs more than one (for example logic + state). Load each as soon as the
fix enters its area. Record each loaded skill and the reason in the output block.

---

## 3. Reproduce first

Before changing any source file:

1. Write a test that follows the ticket's TRIGGER at the level the user observes:
   render the screen or container, perform the user action, assert what the user should see (EXPECTED).
2. Build fixtures from the baseline, or the ticket's version if DEVIATED. Reuse matching repo fixtures and mock files.
3. **Mock only the outermost boundary**: the network request (fetch/axios/BFF client) and the CMS props.
   Never mock a hook, service, mapper or helper that sits on the path you are investigating.
   A mocked function on the path makes the test agree with your assumption instead of the code.
4. Run it with `run-test-cases`. Label the run `<ticket>-<issue>-reproduction`.
5. **If it passes, your reproduction is wrong, not the code.** Make it closer to the ticket:
   the real response shape from the baseline, the real CMS data, the real sequence of actions,
   timers, re-renders and state changes. Repeat until it fails for the reason in OBSERVED.

---

## 4. Investigate the code

With the reproduction failing and the contract data fixed, the cause is in the code.

### 4.1 Trace the whole path

Trace from the user action to what the user sees, for example:
event handler → hook/container → service/API client → response parsing/mapper → state update →
anything that later clears or overrides that state → render condition → rendered output.

- **Open every hop. Do not stop at a layer and assume what the layers below or above do.**
- **Every boundary where data enters the code must be opened**: the service/API client that
  turns the HTTP response into what the hook receives, the mapper that turns CMS fields into props,
  any adapter or normaliser in between. Check the real shape at that boundary against the baseline sample.
- A file that appears in a grep result but was not opened has not been verified.

### 4.2 Verify, do not assume

At each hop check, against the fixed data:

- how a value is parsed and which shape it actually has
- which branch it takes, including defaults, `??`/`||` fallbacks and empty values
- what state it sets
- what later clears, resets or overrides that state (timers, effects, unmounts, other handlers)
- which conditions gate the render

If a step looks correct, prove it with the test: assert intermediate state, or add temporary
logging and re-run. Remove all temporary logging before the fix is final.

### 4.3 Explain the mechanism

State in one or two sentences why the TRIGGER with this data produces the OBSERVED behaviour.
If you cannot explain it, the trace is not finished.

### 4.4 Fault origin

Once the root-cause lines are known, classify the origin from git history on those lines only
(`git log -L :<symbol>:<file>` or `git blame` on the range):
agent miss · regression from prior fix · post-generation manual change · contract change ·
design change · upstream gap · ambiguous requirement · unknown (no history).

---

## 5. Fix the root cause, not the symptom

- Fix at the layer where the behaviour is wrong. Do not patch a downstream layer to hide an upstream fault.
- Do not aim for the smallest diff. Aim for the change that makes the behaviour correct for every
  scenario in section 6, including scenarios the ticket did not mention.
- Apply the coding standards of every skill loaded in section 2.
- Load `repository-structure-governance` before creating, moving or renaming any file.
- No unrelated refactors. Keep the public API of shared components unless the fix requires a change; if it does, update every consumer.

---

## 6. Scenario sweep (mandatory)

The defect is one scenario of a behaviour. List every scenario that passes through the behaviour
you changed, then verify each one:

- **Sibling cases**: other error codes or response types on the same path, success path,
  empty/missing/null data, missing or empty CMS content, fallback messages
- **Related ACs and states** from the analysis plan (for example thresholds, counters, expiry,
  disabled states, retries) — the code must match the AC, not just the ticket
- **State transitions**: error → retry → success; repeated failures; timers starting, ending and resetting;
  navigation away and back
- **Locale and layout**: EN/AR and RTL, mobile/tablet/desktop, if the change touches UI
- **Consumers**: every place that uses the changed code (`grep`), and their existing tests
- **New scenarios the fix introduces**

Each scenario ends as exactly one of:
`new test` · `existing test` · `gap found and fixed` · `outside FE` (DEVIATED contracts only, with evidence).

If the sweep finds related bugs on the same behaviour, fix them in this run and record them.

---

## 7. Run and verify

Use `run-test-cases` for every run, from the repo root. Required runs per issue:

| Run label                                                                  | Expected verdict             |
| -------------------------------------------------------------------------- | ---------------------------- |
| `<ticket>-<issue>-reproduction` (before fix)                               | FAIL for the OBSERVED reason |
| `<ticket>-<issue>-after-fix`                                               | PASS                         |
| `<ticket>-<issue>-scenarios`                                               | PASS                         |
| `<ticket>-<issue>-related` (existing tests of changed files and consumers) | PASS                         |

A test counts only if its run output folder exists. Never report a verdict without one.

---

## 8. Done when (per issue)

- [ ] Reproduction failed before the fix and passes after it
- [ ] Root-cause mechanism explained, with every hop on the path opened
- [ ] Scenario sweep complete; every scenario has an outcome
- [ ] Scenario and related existing tests pass
- [ ] Temporary logging removed
- [ ] `git diff --stat` (from the repo root) includes at least one non-test source file

Updating a todo list is not evidence. The issue is done only when its output block is filled from real runs and the real diff.

---

## Outcomes

- **FIXED**: all of section 8 is true.
- **BLOCKED**: only when a **DEVIATED** contract needs a backend, CMS or design change the frontend
  cannot provide. State the exact baseline-vs-ticket difference as evidence.
  An UNCHANGED contract can never be the reason for BLOCKED.

## Output (one block per issue)

```text
ISSUE-<n>   FIXED | BLOCKED
  Root cause:   <file → symbol>: <mechanism in one or two sentences>
  Trace:        <hop> → <hop> → … (every hop opened)
  Origin:       <fault origin> (<commit or "no history">)
  Dev notes:    <DDN-id: how applied> | none
  Contracts:    BFF <UNCHANGED|DEVIATED>, Sitecore <…>, Figma <…>
  Deviations:   <contract: baseline vs ticket> | none
  Skills loaded: <skill: reason>
  Extra context: <file: reason> | none
  Reproduction: <test name>   before: FAIL   after: PASS
  Scenarios:
    <scenario>: <new test | existing test | gap fixed | outside FE: evidence>
  Test runs:    <label: verdict: output folder>
  Tests modified: <test: was asserting → why changed> | none
  Diff:         <pasted git diff --stat>
```

## Never

- Never conclude the code is correct, the defect is fixed, or the ticket is invalid.
- Never mock a function on the path under investigation.
- Never stop the trace at a layer and assume the rest.
- Never blame an UNCHANGED contract or recommend verifying it externally.
- Never weaken, skip or delete an existing test. Update one only if it encoded the wrong behaviour, and say why.
- Never `cd` out of the repo root. Never run tests without `run-test-cases`.
- Never report a change the diff does not show.
- Never close, comment on or transition the ticket.
