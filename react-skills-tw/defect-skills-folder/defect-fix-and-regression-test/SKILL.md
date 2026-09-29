---
name: defect-fix-and-regression-test
description: Use as Phase 4 of the FE Defect Fix workflow to write a regression test, execute it and prove it fails, apply the minimal fix on top of the current code, then execute the regression, edge-case guard and blast-radius tests and prove they pass. Enforces the minimal-change contract, preserves developer changes, and uses run-test-cases for every test claim. Runs once per issue. Triggers include apply fix, fix defect, regression test, guard tests, or failing-first test.
disable-model-invocation: true
---

## Defect Fix and Regression Test

### Purpose

Fix and tests are one atomic unit, once per issue. **Every test claim comes from an executed `run-test-cases` run.**

```text
write regression test → RUN (must fail) → minimal fix → RUN (must pass)
→ guard tests → RUN → blast radius → RUN
```

---

## ⚠️ RUNNING TESTS — ONE COMMAND SHAPE

```bash
python3 <script> --files <path> [--name "<pattern>"] [--expect fail] --label <label>
```

Locate the script **once per run**, then reuse the path:

```bash
find . -path '*/run-test-cases/scripts/run-tests.py' -not -path '*/node_modules/*' | head -1
python3 <script> --where        # confirms repo root and package scan dirs
```

⚠️ **The script resolves the repo root and the path form itself.** Pass the path you already have — repo-relative, workspace-prefixed, or absolute.

⚠️ **If a call fails, read the error. Do NOT retry with a different path form, a different working directory, `--repo-root`, or a hand-built `pnpm`/`vitest` command.** The script already tried the alternatives and its error names what it attempted — including same-named files, which catches casing mistakes.

---

## ⚠️ BUILD ON THE CURRENT CODE

```text
❌ Never revert a developer's change to match the summary
❌ Never restore the generated version of a function
❌ Never tidy a developer's code while fixing next to it
✅ Minimal change on top of what is there
✅ Preserve developer-introduced behaviour unless the requirement contradicts it
✅ A DDN may direct you to undo a developer change — follow it, record why
```

The matrix contains **preserve-rows** for developer behaviour; their guard tests prove the fix did not undo it.

---

## ⚠️ MINIMAL-CHANGE CONTRACT

```text
For every line you are about to change: "Did RCA name this line?"
  YES → change it      NO → leave it; record an observation if relevant

❌ No refactoring · renaming · reformatting · import tidying
❌ No dependency changes · no unrelated files · no unmentioned features
```

Unrelated problems are recorded in the FIX_RESULT and carried to §13 — **never fixed**.

---

## The sequence

### 1 · Write the regression test

```text
✅ Co-located; added to the existing test file if one exists
✅ .test.* naming — never .spec.*, never a __tests__ folder
✅ Defect reference in the name:
     it("handles null policyNumber [DEF-486 / ISSUE-002]", …)
✅ Reproduces the EXACT reported condition — locale · state · data shape ·
   persona · viewport, from the Phase 1 evidence
```

Conventions come from `frontend-test-generation`. **The failing-first protocol is owned here.**

### 2 · RUN it — it MUST fail

```bash
python3 <script> --files <test file> --name "DEF-486 / ISSUE-002" --expect fail \
  --label DEF-486-ISSUE-002-failing-first
```

| Verdict | Action |
| --- | --- |
| `EXPECTED_FAIL` | Root cause proven → step 3 |
| `PASSED_UNEXPECTEDLY` | **Root cause is wrong** → return to Phase 3 |
| `FAILED_FOR_WRONG_REASON` | Load/import/setup error, or a different test failed → fix the **setup**, never the assertion; re-run |
| `NOT_COLLECTED` | File outside the include pattern → fix placement; re-run |
| exit 4 / 5 | See *If tests cannot run* |

⚠️ **Never adjust the assertion until the test fails.** That shapes the test around an assumption and proves nothing.

### 3 · Apply the minimal fix

Load coding skills by category for **standards only**:

| Category | Skills |
| --- | --- |
| UI · RTL · Responsive · A11y | `presentational-ui-generation` |
| Media | `+ frontend-media-integration` |
| Sitecore | `sitecore-rendering-integration` |
| BFF · API · mapper | `frontend-logic-integration` |
| State · forms | `+ frontend-state-and-form-management` |
| File move/rename | `+ repository-structure-governance` |
| DS public API changed | `+ storybook-and-component-catalogue` |
| Always | `developer-notes-protocol` · `frontend-test-generation` |

⚠️ These skills are written for *generation* and carry completeness instincts — "implement every state", "cover every variant". **The minimal-change contract overrides all of it.** Use them for *how* to write the fix correctly, never to regenerate the component or add unmentioned states.

⚠️ Load per issue; discard before the next.

```text
✅ Tokens, never raw hex/px          ✅ Logical properties for RTL
✅ cn() for classes                  ✅ Typed — no `any`
✅ Prop-driven — no hardcoded copy   ✅ Constants for endpoints / keys
✅ Correct layer — mapper defaults in the mapper
```

⚠️ A hardcoded value used to fix a defect creates a new defect. No source for the value → record a contract gap. Missing token → create it and record it.

⚠️ **Scope-to-diff:** if an artefact was refetched, apply only the reported delta. Other diff changes are observations — a refreshed design is not licence to re-implement.

⚠️ **Structural change** flagged in Phase 3 → do not attempt; record the escalation.

### 4 · RUN the regression test — it MUST pass

```bash
python3 <script> --files <test file> --name "DEF-486 / ISSUE-002" \
  --label DEF-486-ISSUE-002-after-fix
```

Anything but `PASS` → the fix is wrong or incomplete; revise within the RCA lines and re-run.

### 5 · Guard tests — one per GUARD row

```bash
python3 <script> --files <test files> --label DEF-486-ISSUE-002-guards
```

⚠️ **Guard tests do not need to fail first** — they protect behaviour that is already correct and typically pass before and after. A guard that **fails after the fix** means the fix broke a neighbour → revise, re-run steps 4–5.

### 6 · Blast radius

```bash
python3 <script> --files <co-located> <consumer tests> --label DEF-486-ISSUE-002-blast-radius
python3 <script> --related <changed sources> [--related-scope all] --label DEF-486-ISSUE-002-related
```

⚠️ Use `--related-scope all` when the changed file is in `Packages/DesignSystem` or `Packages/Common` — its consumers live in other packages.

| Result | Action |
| --- | --- |
| `PASS` | Done |
| `FAIL` in a consumer | Did the fix break it, or did the test encode old behaviour? Investigate |
| `NOT_COLLECTED` | Resolve before claiming the blast radius is clean |
| Pre-existing failure in an untouched file | Record as an observation; do not fix |

---

## ⚠️ Never weaken an existing test

```text
❌ Never delete, .skip or comment out an existing test
❌ Never loosen an assertion · never change expected values to match wrong behaviour
```

If an existing test fails after the fix, exactly one is true:

| Situation | Action |
| --- | --- |
| The fix is wrong | Revise, or return to Phase 3 |
| The test encoded the defect / old contract / old design | Update it **and record the change and reasoning** for §13 |

⚠️ A silently-updated test is how defects get reintroduced.

---

## If tests cannot run

```text
Verification: STATIC ONLY — tests were not executed
Reason:       [exit code + script message]
Developer:    [the reproduce: line from the script output]
```

⚠️ Continue the workflow, but **never** write "passed" or "failed first ✅" for a test that did not run.

---

## Output — one block per issue, no narration

```text
FIX — ISSUE-002 · FIXED · EXECUTED
  Change:      PolicyMapper.ts → mapPolicyResponse() :47   "" → "—"
               developer legacy fallback preserved
  DDN:         none          New token: none
  Runs:        failing-first EXPECTED_FAIL  …/DEF-486-ISSUE-002-failing-first-…/
               after-fix     PASS           …/…-after-fix-…/
               guards (5)    PASS           …/…-guards-…/
               blast (3)     PASS           …/…-blast-radius-…/
  Edge cases:  6/6 verified
  Scope:       2 files touched — matches RCA ✅
  Existing test modified: none
  Observations: usePolicyList.ts staleTime hardcoded — separate ticket
  §6 updates:  §3 rows · §7 trace · §10 +6 tests
```

---

### Gate (per issue)

```text
- [ ] Regression test written, co-located, defect-referenced, exact condition reproduced
- [ ] RUN → EXPECTED_FAIL (or STATIC ONLY recorded)
- [ ] Minimal fix on the CURRENT code; only RCA-named lines changed
- [ ] No developer change reverted (unless a DDN directs it)
- [ ] RUN → PASS
- [ ] Guard test per GUARD row, incl. developer preserve-rows → PASS
- [ ] Blast radius + --related run → PASS; no NOT_COLLECTED left unresolved
- [ ] No existing test weakened; any modification recorded with reason
- [ ] Fix conforms to token / RTL / typing / prop-driven standards
- [ ] Output folder recorded for every run
- [ ] Observations and untested consumers recorded
```

### Never

- **Never claim a test result without an executed run.**
- **Never retry a failed test command with a different path form or a hand-built command.**
- **Never accept `PASSED_UNEXPECTEDLY`, `FAILED_FOR_WRONG_REASON` or `NOT_COLLECTED` as proof.**
- **Never change an assertion to make a failing-first run succeed.**
- **Never revert or tidy a developer's change.**
- **Never skip guard or blast-radius runs** because the regression test passed.
- Never change code RCA did not name; never refactor while fixing.
- Never fix unrelated problems — record them.
- Never re-implement against a refreshed design; never attempt a structural change.
- Never regenerate a component because a coding skill was loaded.
- Never weaken, skip or delete an existing test.
- Never hardcode a value to resolve a defect.
- Never override a DDN with your own approach.
- Never narrate beyond the per-issue output block.
