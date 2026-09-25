---
name: defect-fix-and-regression-test
description: Use as Phase 4 of the FE Defect Fix workflow to write a regression test, execute it and prove it fails, apply the minimal fix on top of the current code, then execute the regression, edge-case guard and blast-radius tests and prove they pass. Enforces the minimal-change contract, preserves developer changes, and uses run-test-cases for every test claim. Runs once per issue. Triggers include apply fix, fix defect, regression test, guard tests, or failing-first test.
disable-model-invocation: true
---

## Defect Fix and Regression Test

### Purpose

This skill is **Phase 4** of the FE Defect Fix Agent, run **once per issue**. Fix and tests are a **single atomic unit** — and every test claim is backed by an **executed run** of `run-test-cases`.

```text
write regression test → RUN (must fail) → minimal fix → RUN (must pass)
→ write guard tests → RUN guards → RUN blast radius → record evidence
```

---

## ⚠️ ALL TESTS ARE EXECUTED — VIA `run-test-cases`

```bash
python3 scripts/run-tests.py --files <test files> [--name "<pattern>"] [--expect pass|fail] --label <label>
```

⚠️ **Never build a vitest, turbo or pnpm test command by hand.** The script resolves the owning package, runs from its context, and distinguishes a real assertion failure from a load error or a file that never ran.

⚠️ **A reasoned result is not a result.** If you did not run it, you cannot say it passed.

### Labels — Make Every Run Traceable

```text
{{ticket_id}}-ISSUE-002-failing-first
{{ticket_id}}-ISSUE-002-after-fix
{{ticket_id}}-ISSUE-002-guards
{{ticket_id}}-ISSUE-002-blast-radius
```

Record each run's output folder — it is the evidence in the §13 entry.

---

## ⚠️ BUILD ON THE CURRENT CODE

Phase 3 read the file as it is now. The fix is applied **to that**, not to the version the summary describes.

```text
❌ Never revert a developer's change to match the summary
❌ Never restore the generated version of a function
❌ Never "tidy" a developer's code while fixing next to it
✅ Make the minimal change on top of what is there
✅ Preserve developer-introduced behaviour unless the requirement contradicts it
✅ If a DDN tells you to undo a developer change, follow it and record why
```

The edge-case matrix contains **preserve-rows** for developer-introduced behaviour. Those guard tests prove the fix did not undo it.

---

## THE SEQUENCE

### Step 1 — Write the Regression Test

Expresses the **expected** behaviour for the reported condition.

```text
✅ Co-located with the source file; added to the existing test file if one exists
✅ .test.* naming — never .spec.*, never a __tests__ folder
✅ Defect reference in the name:
     it("handles null policyNumber [DEF-123 / ISSUE-002]", ...)
✅ Reproduces the exact reported condition:
     RTL → dir="rtl" · locale → the reported locale · state → hook mocked into it
     null data → the field null/absent · persona → the reported role · viewport → the size
```

Conventions (explicit Vitest imports, `userEvent`, accessible queries, package include patterns) come from **`frontend-test-generation`**. The failing-first protocol is owned here.

### Step 2 — RUN It: It MUST Fail

```bash
python3 scripts/run-tests.py \
  --files Portals/Sme/Features/Motor/PolicyList/Mappers/PolicyMapper.test.ts \
  --name "DEF-123 / ISSUE-002" --expect fail \
  --label DEF-123-ISSUE-002-failing-first
```

| Verdict | Meaning | Action |
| --- | --- | --- |
| `EXPECTED_FAIL` | Root cause proven | → Step 3 |
| `PASSED_UNEXPECTEDLY` | Test passes against current code — **root cause is wrong** | Return to Phase 3 |
| `FAILED_FOR_WRONG_REASON` | Load/import/setup error, or a different test failed | Fix the test **setup** (imports, mocks, rendering) — **never the assertion** — and re-run |
| `NOT_COLLECTED` | File never ran — outside the vitest include pattern | Fix placement/path; re-run |
| exit 4 / 5 | Environment or runner error | See *If Tests Cannot Run* |

⚠️ **Never adjust the assertion until the test fails.** That shapes the test around an assumption and proves nothing.

### Step 3 — Apply the Minimal Fix

```text
CHANGE ONLY what Root Cause Analysis named.
For every line you are about to change: "Did RCA name this line?"
  YES → change it      NO → do not touch it; record an observation if relevant
```

The fix conforms to project standards — load the coding skill for the category:

| Category | Skills |
| --- | --- |
| UI · RTL · Responsive · A11y | `presentational-ui-generation` |
| Media | `+ frontend-media-integration` |
| Sitecore | `sitecore-rendering-integration` |
| BFF · API · mapper | `frontend-logic-integration` |
| State · forms | `+ frontend-state-and-form-management` |
| File move/rename | `+ repository-structure-governance` |
| DS component public API changed | `+ storybook-and-component-catalogue` |
| **Always** | `developer-notes-protocol` · `frontend-test-generation` · `run-test-cases` |

⚠️ Coding skills supply **how** to write the fix correctly — tokens, logical properties, layering, typing. They are **not** licence to regenerate the component, add unmentioned states, or restructure. The minimal-change contract overrides their completeness instincts.

```text
✅ Tokens, never raw hex/px          ✅ Logical properties for RTL
✅ cn() for classes                  ✅ Typed — no `any`
✅ Prop-driven — no hardcoded copy   ✅ Constants for endpoints / keys
✅ Correct layer (mapper defaults in the mapper)
```

⚠️ A hardcoded value used to fix a defect creates a new defect. No source for the value → record a contract gap. Missing token → create it and record it.

⚠️ **Scope-to-diff:** if an artefact was refetched, apply only the reported delta. Other diff changes are observations.

⚠️ **Structural change** flagged in Phase 3 → do not attempt; record the escalation.

### Step 4 — RUN the Regression Test: It MUST Pass

```bash
python3 scripts/run-tests.py --files <same test file> --name "DEF-123 / ISSUE-002" \
  --label DEF-123-ISSUE-002-after-fix
```

`PASS` required. Anything else → the fix is incomplete or wrong; revise the fix (within the RCA lines) and re-run.

### Step 5 — Write and RUN the Guard Tests

One test per **GUARD** row in the Phase 3 edge-case matrix — including preserve-rows for developer-introduced behaviour.

```bash
python3 scripts/run-tests.py --files <test files holding the guard tests> \
  --label DEF-123-ISSUE-002-guards
```

⚠️ **Guard tests do not need to fail first.** They protect behaviour that is already correct, so they typically pass before and after the fix. Only the regression test carries the failing-first requirement.

A guard test that **fails after the fix** means the fix broke a neighbour → revise the fix, re-run all of Steps 4–5.

### Step 6 — RUN the Blast Radius

```bash
# Co-located tests of every changed file + consumer test files from RCA
python3 scripts/run-tests.py --files <co-located tests> <consumer tests> \
  --label DEF-123-ISSUE-002-blast-radius

# Plus anything the module graph finds that RCA's search missed
python3 scripts/run-tests.py --related <changed source files> \
  [--related-scope all]   # for design-system / common code
  --label DEF-123-ISSUE-002-related
```

⚠️ Use `--related-scope all` whenever the changed file is in `Packages/DesignSystem` or `Packages/Common` — its consumers live in other packages.

| Result | Action |
| --- | --- |
| `PASS` | Done |
| `FAIL` in a consumer test | Did the fix break it, or does the test encode the old (wrong) behaviour? Investigate — see below |
| `NOT_COLLECTED` | A consumer test was never run — resolve before claiming the blast radius is clean |
| `FAILED_FOR_WRONG_REASON` on an **untouched** file | Pre-existing breakage — record as an observation; do not fix |

---

## ⚠️ Never Weaken an Existing Test

```text
❌ Never delete, .skip, or comment out an existing test to make a fix pass
❌ Never loosen an assertion to accommodate the fix
❌ Never change expected values to match new, wrong behaviour
```

If an existing test fails after the fix, exactly one of these is true:

| Situation | Action |
| --- | --- |
| The fix is wrong | Revise the fix, or return to Phase 3 |
| The test encoded the defect / old contract / old design | Update it **and record the change and reasoning** for the §13 entry |

⚠️ A silently-updated test is how defects get reintroduced.

---

## If Tests Cannot Run

If `run-test-cases` exits **4** or **5** and it cannot be resolved:

```text
Verification level:  STATIC ONLY — tests were not executed
Reason:              [exit code + script message]
Failing-first:       reasoned, not proven
Blast radius:        reviewed by reading, not run
Developer action:    [the exact run-tests.py commands, and the pnpm run test:<package> equivalent]
```

⚠️ Continue the workflow, but **never** write "passed" or "failed first ✅" for a test that did not run. This label travels into the §13 entry and the final report.

---

## Output — FIX_RESULT (Per Issue)

```text
FIX APPLIED — ISSUE-00N
  Status:              FIXED | BLOCKED (see RCA) | NOT A DEFECT
  Verification level:  EXECUTED | STATIC ONLY (reason)

  ── Fix ─────────────────────────────────────────────────────
  File / symbol:       [path] → [symbol]
  Change:              [precise minimal edit, against the current code]
  Developer changes:   preserved | overridden per DDN-xxx (why)
  Skills used:         [coding skills that supplied the standards]
  DDN applied:         [DDN-xxx, or: None]
  New token:           [name · value · why — or: None]

  ── Test Execution ──────────────────────────────────────────
  Regression (fail-first):  EXPECTED_FAIL   .SS_WF/Agent/TEST_RUNS/DEF-123-ISSUE-002-failing-first-…/
  Regression (after fix):   PASS            …/DEF-123-ISSUE-002-after-fix-…/
  Guards (N tests):         PASS            …/DEF-123-ISSUE-002-guards-…/
  Blast radius (N files):   PASS            …/DEF-123-ISSUE-002-blast-radius-…/
  Related sweep:            PASS | NO_RELATED_TESTS

  ── Edge Cases Verified ─────────────────────────────────────
  [matrix rows → test name → result]

  ── Scope ───────────────────────────────────────────────────
  Files touched:            [count] — matches RCA ✅
  Diff changes not applied: [list → observations]
  Existing tests modified:  NO | YES → [which · why]
  Observations (not fixed): [list, or: None]
  Untested consumers:       [list, or: None]

  ── Summary Rows For Phase 6 ────────────────────────────────
  Update for fix:  §3 · §7 · §8 · §10 … [rows]
  Reconcile drift: [rows from RCA]
```

---

### Gate: Phase 4 Complete (Per Issue) When

```text
- [ ] Regression test written, co-located, defect-referenced, reproducing the exact condition
- [ ] Regression test RUN → EXPECTED_FAIL (or STATIC ONLY recorded)
- [ ] Minimal fix applied on top of the CURRENT code
- [ ] Only RCA-named lines changed; no developer change reverted (unless a DDN says so)
- [ ] Regression test RUN → PASS
- [ ] Guard test for every GUARD row, including developer preserve-rows
- [ ] Guard tests RUN → PASS
- [ ] Blast-radius tests RUN → PASS; --related sweep run (scope all for DS/Common code)
- [ ] No NOT_COLLECTED left unresolved
- [ ] No existing test weakened, skipped, or deleted; any modification recorded with reason
- [ ] Fix conforms to token / RTL / typing / prop-driven standards
- [ ] Output folder recorded for every run
- [ ] Observations and untested consumers recorded
```

### Never Do

- **Never claim a test result without a `run-test-cases` run.**
- **Never build test commands by hand.**
- **Never accept `PASSED_UNEXPECTEDLY`, `FAILED_FOR_WRONG_REASON` or `NOT_COLLECTED` as proof.**
- **Never change an assertion to make a failing-first run succeed.**
- **Never revert or tidy a developer's change** while fixing.
- **Never skip guard or blast-radius runs** because the regression test passed.
- Never change code RCA did not name; never refactor while fixing.
- Never fix unrelated problems — record them.
- Never re-implement against a refreshed design; never attempt a structural change.
- Never regenerate a component because a coding skill was loaded.
- Never weaken, skip, or delete an existing test.
- Never hardcode a value to resolve a defect.
- Never override a DDN with your own approach.
- Never close or transition the defect ticket.
