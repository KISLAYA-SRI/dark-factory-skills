---
name: run-test-cases
description: Use to execute the monorepo's tests and get a verdict the agent can always read — the full suite via the project's package.json script (turbo run test --parallel), or targeted runs of specific test files, tests related to changed source files, or whole packages. Finds the repo root and resolves any path form itself. Shared by the Defect Fix workflow (failing-first proof, guard tests, blast radius) and the static code quality workflow (full-suite gate). Triggers include run tests, run all tests, test suite, test:parallel, run test cases, failing-first, blast radius tests, or unit test run.
disable-model-invocation: true
---

## Run Test Cases

Execute tests and return a verdict. The agent decides **what** to test; the script decides **how**.

---

## ⚠️ THE OUTPUT CONTRACT — HOW TO READ A RESULT

```text
1. The FIRST line of stdout is always   VERDICT=<value>
2. The script exits 0 whenever it ran — even for FAIL or PASSED_UNEXPECTEDLY
3. Every run writes   <repo>/.SS_WF/Agent/TEST_RUNS/LATEST.json
```

**Read the VERDICT line. Act on it.**

⚠️ **If your tool reports "Command failed" or shows no output** — do NOT conclude the environment is broken. Read the result file:

```bash
cat <repo>/.SS_WF/Agent/TEST_RUNS/LATEST.json
```

`STATIC ONLY` is allowed **only** when you have actually seen `VERDICT=ENV_ERROR` (pnpm missing, no repo root). A failed tool call is not an environment error.

---

## ONE COMMAND SHAPE

```bash
python3 <script> --files <path> [--name "<pattern>"] [--expect fail] --label <label>
```

Locate the script **once** per run, confirm the layout **once**, reuse both:

```bash
find . -path '*/run-test-cases/scripts/run-tests.py' -not -path '*/node_modules/*' | head -1
python3 <script> --where
```

Any path form works, from any working directory — repo-relative, `src/`-prefixed, scan-dir-relative, absolute.

⚠️ **Do not retry with a different path form, working directory, `--repo-root`, or a hand-built `pnpm`/`vitest` command.** If a path is wrong, the script says so (`VERDICT=USAGE_ERROR`) and lists same-named files it found.

---

## Modes

| You want to know | Use |
| --- | --- |
| Does the whole suite pass? | `--all` (runs `pnpm run test:parallel`) |
| Does this test file pass? | `--files <path>` |
| Does this one test fail first? | `--files <path> --name "<pattern>" --expect fail` |
| Which tests import this changed file? | `--related <source> [--related-scope all]` |
| Does this package pass, per test? | `--package sme` |

Flags: `--label` (always set) · `--timeout` · `--coverage` · `--dry-run` · `--where` · `--force` / `--script` / `--no-drill-down` (suite only) · `--strict-exit` (CI exit codes).

---

## Verdicts

| Verdict | Meaning | Action |
| --- | --- | --- |
| `PASS` | All executed tests passed | Proceed |
| `EXPECTED_FAIL` | `--expect fail` and the named test failed on an assertion | Root cause proven |
| `FAIL` | Tests failed or a suite errored | Read the ✗ FAILED lines |
| `PASSED_UNEXPECTEDLY` | `--expect fail` but the test passed against current code | **Root cause is wrong — return to RCA** |
| `FAILED_FOR_WRONG_REASON` | Load/import/setup error, or a different test failed | Fix the test **setup**, never the assertion |
| `NOT_COLLECTED` | Requested file never ran | Never a pass — check placement / include pattern |
| `NO_TASKS` | Turbo ran nothing | Never a pass |
| `RUNNER_ERROR` | Crash / timeout / no report | Read the log tail |
| `USAGE_ERROR` | Bad arguments or path | Read the message — it lists what was tried |
| `ENV_ERROR` | pnpm missing / root not found | Only verdict that justifies STATIC ONLY |

Suite: a turbo cache hit is a valid pass (use `--force` for fresh execution); failing packages are re-run alone; `PASSED_ON_RERUN` = possible flaky test, not a pass.

---

### Rules

**Always** — read the VERDICT line · set `--label` · record the output folder · on a failed tool call read `LATEST.json`.

**Never**
- Never conclude "environment unavailable" from a failed tool call — read `LATEST.json`.
- Never claim STATIC ONLY without having seen `VERDICT=ENV_ERROR`.
- Never retry with a different path form or a hand-built command.
- Never treat `NOT_COLLECTED`, `NO_TASKS`, `FAILED_FOR_WRONG_REASON` or `PASSED_ON_RERUN` as passes.
- Never edit an assertion to change a verdict.
