---
name: master-static-code-quality
description: Use to run the static code quality gate over generated or modified code — prettier format, eslint fix, remaining lint errors, test suite, and build — fixing errors between gates with a bounded attempt policy and producing a short pass/pending report. Triggers include static code quality, quality gate, run lint and build, fix lint errors, fix failing tests, fix build errors, or pre-commit check.
disable-model-invocation: true
---

## Master Static Code Quality

### Purpose

Run every quality gate over the current working tree, fix the **errors** that appear between gates, and report what is green and what still needs a developer.

One skill. One script for the non-test gates. `run-test-cases` for the test gates.

---

## ⚠️ CORE RULES

```text
ERRORS are fixed.  WARNINGS are ignored.
TWO fix attempts per gate — then record and move on.
Minimal change only — no refactors, no redesigns, no unrelated files.
A failed gate never stops the run.
```

### Output discipline

One line per gate. No narration, no per-gate essays, no restating the plan.

```text
Gate 2  lint:fix   FAIL → 3 errors → attempt 1 → PASS
Gate 4  test       FAIL → 2 failing → attempt 1 → attempt 2 → 1 PENDING
```

Everything else goes in the summary document at the end.

---

## Gate Sequence

| # | Gate | Command | Agent action |
| --- | --- | --- | --- |
| 1 | **Format** | `run-quality-gate.sh format` | None — auto-fix |
| 2 | **Lint fix** | `run-quality-gate.sh lint:fix` | None — auto-fix |
| 3 | **Lint verify** | `run-quality-gate.sh lint` | **FIX LOOP** on remaining errors |
| 4 | **Test** | `run-test-cases --all` | — |
| 5 | **Test fix** | *(loop re-runs gate 4)* | **FIX LOOP** on failing tests |
| 6 | **Build** | `run-quality-gate.sh build` | **FIX LOOP** on build errors |
| 7 | **Final sweep** | format → lint → test → build | **Verify only — no fixing** |
| 8 | **Summary** | — | Write `STATIC_QUALITY_SUMMARY.md` |

⚠️ **Gate 3 is separate from gate 2.** `lint:fix` auto-fixes what it can; gate 3 reveals what it could not. Fixing before that verification wastes an attempt on already-fixed errors.

⚠️ **Gate 5's re-run IS the verification.** Each attempt ends with a fresh `run-test-cases --all`, so no extra step is needed.

### ⚠️ Gate 7 — why a final sweep

A test fix in gate 5 or a build fix in gate 6 edits source, which can reintroduce a formatting or lint error that gate 2 already cleared. Without a closing pass the run reports green on gates that were green *before* those edits.

```text
Gate 7 runs all four gates once, in order.
FAILS → record in the summary as a REGRESSION. Do NOT start a new fix loop.
```

Starting a loop here would make the attempt cap meaningless.

---

## Running the Gates

```bash
bash <skill-dir>/scripts/run-quality-gate.sh <script-name>
```

Any script in the root `package.json`. The script finds the repo root (including a nested `src/`), runs it with pnpm, and returns a parsed verdict.

| Verdict | Exit | Meaning |
| --- | --- | --- |
| `PASS` | 0 | Clean |
| `PASS_WITH_WARNINGS` | 0 | Warnings only — **ignore, do not fix** |
| `FAIL` | 1 | Errors present, or non-zero exit with nothing parseable |
| `SCRIPT_NOT_FOUND` | 4 | Not in root `package.json` — the output lists what is |
| `ENV_ERROR` | 4 | pnpm missing / root not found |
| `TIMEOUT` | 5 | Exceeded the limit |

Errors arrive pre-parsed:

```text
ERRORS_START
Portals/Sme/Features/Shared/Otp/OtpInput.tsx:8   @typescript-eslint/no-unused-vars  'useMemo' is defined but never used
Packages/Common/Utils/Format.ts:12               -                                  Cannot find module './Missing'
ERRORS_END
```

Full logs and a tab-separated `errors.txt` are written to `.SS_WF/Agent/QUALITY_RUNS/<gate>-<timestamp>/`.

⚠️ **Never build a `pnpm`/`eslint`/`tsc` command by hand.** If a call fails, read the verdict and reason — they name the cause.

### Tests use `run-test-cases`

```bash
python3 <run-test-cases>/scripts/run-tests.py --all --label quality-gate-test
```

It gives per-package status, per-test failure detail, and flags `PASSED_ON_RERUN` (flaky) — which a generic wrapper cannot.

⚠️ `PASSED_ON_RERUN` is **not a pass**. Record it as flaky; do not "fix" it.

---

## ⚠️ THE FIX LOOP — TWO ATTEMPTS, THEN STOP

```text
run gate
  PASS / PASS_WITH_WARNINGS → next gate
  FAIL → ATTEMPT 1: fix every error → re-run gate
           PASS → next gate
           FAIL → ATTEMPT 2: fix remaining → re-run gate
                    PASS → next gate
                    FAIL → RECORD AS PENDING → next gate
```

### Early stop — no progress

If attempt 2 returns the **same error count with the same signatures**, the agent is not converging. Stop immediately and record as PENDING with `stopped: no progress`. Spending the attempt changes nothing.

### Record, then continue

A gate that ends PENDING does **not** stop the run. One stubborn lint error must not hide a build failure.

⚠️ Record the **actual error text**, not a paraphrase — the developer needs the real message.

---

## Per-Gate Fix Rules

Shared across all gates: minimal change · no unrelated files · no architectural change · preserve approved behaviour · never suppress an error you do not understand.

### Lint (gate 3)

| Fix | Never |
| --- | --- |
| Unused imports and variables | Disable a rule |
| Missing hook dependency arrays | Add `any` to satisfy a type rule |
| Naming convention violations | Add a broad `eslint-disable` |
| Unstable callbacks (`useCallback`/`useMemo`) | Change behaviour to satisfy lint |
| Missing explicit types | Touch unrelated files |
| Physical → logical RTL properties | |

⚠️ If a lint error can only be silenced by disabling the rule, **record it as PENDING** instead. A suppressed rule hides the problem from the next run too.

### Test (gate 5)

**Read BOTH the failing test and the source it exercises, then decide.**

```text
Fix the SOURCE when:
  · the test asserts behaviour the code should have but does not
  · the test was written for this change and encodes the requirement

Fix the TEST when:
  · mock setup is wrong · wiring is wrong · async handling is missing
  · the assertion encodes behaviour that legitimately changed in this ticket

AMBIGUOUS — both look defensible:
  → record as PENDING. Do NOT guess.
```

```text
❌ Never delete a test to make the suite pass
❌ Never weaken an assertion to accommodate broken code
❌ Never redesign the feature to satisfy a test
```

⚠️ The ambiguous case is where an autonomous agent does the most damage. Recording beats a coin flip.

### Build (gate 6)

| Fix | Never |
| --- | --- |
| Import and export errors | Change build tooling |
| Wrong file paths | Change package versions |
| Missing modules | Suppress an error without understanding it |
| Type incompatibilities | Introduce a new implementation approach |
| Server/client boundary violations | Modify unrelated files |

⚠️ **Fix the first root-cause error, not the cascade.** One missing export can produce twenty downstream errors; re-run after fixing it before touching anything else.

---

## Summary Document

**Path:** `.SS_WF/Agent/CODE/{{ticket_id}}_STATIC_QUALITY_SUMMARY.md`

⚠️ **Informational only.** Short and factual — not a rebuild of the code-gen summary. If everything passed, it is a few lines.

```markdown
# Static Quality Summary — {{ticket_id}}

**Result:** PASS | PASS WITH PENDING ITEMS
**Run:** {{YYYY-MM-DD HH:MM}}

## Gates

| Gate | Result | Errors In → Out | Attempts |
| ---- | ------ | --------------- | -------- |
| Format   | ✅ PASS    | —      | — |
| Lint     | ✅ PASS    | 3 → 0  | 1 |
| Test     | ⚠️ PENDING | 2 → 1  | 2 |
| Build    | ✅ PASS    | 1 → 0  | 1 |
| Final sweep | ✅ PASS | —      | — |

## Fixed

| File | Gate | Change |
| ---- | ---- | ------ |
| `Otp/OtpInput.tsx` | Lint | Removed unused `useMemo`; typed `payload` |
| `Atoms/Button.tsx` | Lint | `ml-2` → `ms-2` |
| `Otp/OtpContainer.tsx` | Test | Added missing `onVerified` prop pass-through |
| `Common/Utils/Format.ts` | Build | Corrected import path `./Missing` → `./Missing/Index` |

## ⚠️ Pending — developer action required

| # | Gate | Where | Error | Why not fixed |
| - | ---- | ----- | ----- | ------------- |
| 1 | Test | `OtpInput.test.tsx › resends after timeout` | `expected 2 calls, received 1` | Ambiguous: the test may encode a changed requirement, or the debounce may be wrong. Needs a decision. |

> If none: "None — all gates passed."

## Notes

- 1 flaky test: `PolicyCard.test.tsx` passed on re-run — not fixed.
- 4 warnings ignored per policy.
```

**Rules:** state the real error text · say why a fix was not made · omit the Pending and Notes sections when empty · no narration of the process.

---

### Gate: Complete When

```text
- [ ] Gates 1–6 run in order; each verdict recorded
- [ ] Only ERRORS fixed; warnings ignored
- [ ] No gate exceeded 2 fix attempts
- [ ] No-progress early stop applied where it triggered
- [ ] Failed gates recorded and the run continued
- [ ] Ambiguous test failures recorded, not guessed
- [ ] Final sweep run; regressions recorded, not re-fixed
- [ ] STATIC_QUALITY_SUMMARY.md written with real error text
- [ ] One line of output per gate; nothing else narrated
```

### Never Do

- **Never fix warnings** — errors only.
- **Never exceed 2 attempts per gate.**
- **Never stop the run because a gate failed** — record and continue.
- **Never start a fix loop in the final sweep.**
- **Never disable a lint rule, add `any`, or add `eslint-disable` to pass a gate.**
- **Never delete a test or weaken an assertion** to make the suite pass.
- **Never guess on an ambiguous test failure** — record it.
- **Never change build tooling or package versions.**
- **Never refactor, rename, or reformat beyond the specific error.**
- **Never touch files unrelated to a reported error.**
- **Never build a pnpm/eslint/tsc/vitest command by hand** — use the script and `run-test-cases`.
- **Never treat `PASSED_ON_RERUN` as a pass.**
- **Never paraphrase an error** in the summary — quote it.
- Never narrate phases beyond one line per gate.
