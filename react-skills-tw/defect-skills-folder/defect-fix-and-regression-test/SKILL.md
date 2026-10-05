---
name: defect-fix-and-regression-test
description: Use as Phase 4 of the FE Defect Fix workflow to write a regression test that reproduces the trigger, prove it fails, apply the minimal fix on the current code, then prove the regression, guard and blast-radius tests pass — with every claim backed by an executed run-test-cases verdict and a git diff. Runs once per issue. Triggers include apply fix, fix defect, regression test, failing-first test.
disable-model-invocation: true
---

## Defect Fix and Regression Test

```text
regression test → RUN (EXPECTED_FAIL) → minimal fix → RUN (PASS)
→ guards → RUN (PASS) → blast radius → RUN (PASS) → git diff --stat
```

Every claim is backed by a **verdict** or a **diff**. Nothing else counts as evidence.

---

## ⚠️ READING TEST RESULTS

```bash
python3 <script> --files <test> --name "<DEF / ISSUE>" --expect fail --label <label>
```

- The first stdout line is `VERDICT=…`. Act on it.
- **Tool says "Command failed" or shows nothing?** Read `<repo>/.SS_WF/Agent/TEST_RUNS/LATEST.json`. Do not conclude the environment is broken.
- `STATIC ONLY` is allowed **only** after seeing `VERDICT=ENV_ERROR`.

| Failing-first verdict | Action |
| --- | --- |
| `EXPECTED_FAIL` | Root cause proven → fix |
| `PASSED_UNEXPECTEDLY` | **Root cause is wrong → back to Phase 3.** Do not fix anything. |
| `FAILED_FOR_WRONG_REASON` | Fix the test setup (imports, mocks) — never the assertion — re-run |
| `NOT_COLLECTED` / `USAGE_ERROR` | Fix the path as the message says — re-run |

⚠️ `PASSED_UNEXPECTEDLY` is the most valuable verdict in the workflow — it is how a wrong diagnosis is caught. Never route around it.

---

## 1 · Regression test

```text
✅ Reproduces the TRIGGER from the symptom contract — not a neighbouring behaviour
✅ Asserts EXPECTED from the ticket
✅ Co-located; added to the existing test file; .test.* naming
✅ Defect reference in the name:  it("shows API error on invalid OTP [TAW-516 / ISSUE-001]", …)
```

## 2 · RUN → must be `EXPECTED_FAIL`

## 3 · Minimal fix on the current code

```text
Change ONLY the lines RCA named.
❌ No refactor · rename · reformat · unrelated files · unmentioned features
❌ No reverting developer changes
✅ Tokens · logical RTL · typed · prop-driven · correct layer
```

Coding skills by category supply **standards only** — never regenerate a component.

## 4 · RUN regression → must be `PASS`

## 5 · Guards → `PASS`   (may pass before the fix — they protect working behaviour)

## 6 · Blast radius → `PASS`

```bash
python3 <script> --files <co-located> <consumer tests> --label <…>-blast
python3 <script> --related <changed sources> [--related-scope all] --label <…>-related
```

## 7 · ⚠️ Evidence gate — `git diff --stat`

```bash
git diff --stat
```

An issue may be marked **FIXED** only if the diff shows:

```text
✅ at least one NON-TEST source file changed (the RCA-named file)
✅ the regression test file changed
```

```text
❌ Only test files changed           → the fix was not applied. Not FIXED.
❌ Files outside the RCA changed     → scope creep. Revert them.
```

⚠️ The final report quotes this diff. **Never describe a change the diff does not show.**

---

## Never weaken an existing test

No delete / `.skip` / loosened assertion. If an existing test fails after the fix: either the fix is wrong, or the test encoded the old behaviour — update it and record why.

---

## Output — one block per issue

```text
FIX — ISSUE-001 · FIXED · EXECUTED
  Diff:        Hooks/useOtpVerify.ts | 3 +-
               Hooks/useOtpVerify.test.ts | 24 +
  Runs:        failing-first EXPECTED_FAIL · after-fix PASS · guards(3) PASS · blast(2) PASS
  Output:      .SS_WF/Agent/TEST_RUNS/TAW-516-ISSUE-001-*/
```

### Gate (per issue)
```text
- [ ] Regression test reproduces the TRIGGER and asserts EXPECTED
- [ ] EXPECTED_FAIL seen before fixing (or STATIC ONLY after a seen ENV_ERROR)
- [ ] Regression PASS · guards PASS · blast PASS — verdicts seen
- [ ] git diff --stat shows the RCA-named source file AND the test file
- [ ] Nothing outside the RCA changed; no test weakened
```

### Never
- **Never fix after `PASSED_UNEXPECTEDLY`** — return to Phase 3.
- **Never declare STATIC ONLY from a failed tool call** — read `LATEST.json`.
- **Never mark FIXED when the diff shows only test files.**
- **Never report a change the diff does not show.**
- Never change an assertion to make failing-first succeed.
- Never refactor, fix unrelated problems, or regenerate a component.
