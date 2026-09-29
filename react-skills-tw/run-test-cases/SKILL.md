---
name: run-test-cases
description: Use to execute the monorepo's tests and get a machine-readable verdict — the full suite through the project's own package.json script, or targeted runs of specific test files, tests related to changed source files, or whole packages. Finds the repo root and resolves any path form itself, so no path guessing is needed. Shared by the Defect Fix workflow (failing-first proof, guard tests, blast radius) and the static code quality workflow (full-suite gate). Triggers include run tests, run all tests, test suite, test:parallel, run test cases, verify tests pass, failing-first, blast radius tests, or unit test run.
disable-model-invocation: true
---

## Run Test Cases

### Purpose

Execute tests and return a verdict the agent can act on. The agent decides **what** to test. The script decides **how**.

---

## ⚠️ ONE COMMAND SHAPE — DO NOT EXPERIMENT

```bash
python3 <skill-dir>/scripts/run-tests.py --files <path> [--name "<pattern>"] [--expect fail] --label <label>
```

**The script finds the repo root and fixes the path form itself.** Every one of these works, from any working directory:

```text
--files Portals/Sme/Features/Shared/X.test.tsx        repo-relative
--files src/Portals/Sme/Features/Shared/X.test.tsx    with the workspace prefix
--files ./Features/Shared/X.test.tsx                  scan-dir-relative
--files /abs/path/X.test.tsx                          absolute
```

⚠️ **If the first call fails, do NOT retry with a different path form, a different working directory, `--repo-root`, or a hand-built `pnpm`/`vitest` command.** The script has already tried the alternatives internally. Read its error — it prints the repo root, every path it tried, and any same-named file it found (which catches casing mistakes).

### Locate the script once, at the start of the run

```bash
find . -path '*/run-test-cases/scripts/run-tests.py' -not -path '*/node_modules/*' 2>/dev/null | head -1
```

Then confirm the layout with a single call, and reuse both values for the rest of the run:

```bash
python3 <script> --where
```

```text
repo root:  /workspace/src
script:     /workspace/.agents/skills/run-test-cases/scripts/run-tests.py
cwd:        /workspace
packages:
  @dxp/sme-portal   dir=Portals/Sme   scan=Portals/Sme   (vitest.config.ts)
```

⚠️ The repo root is often **not** the workspace folder — `package.json` and `pnpm-workspace.yaml` may live in a sub-folder such as `src/`. The script detects this; `--where` shows you what it found.

---

## Two Engines

| You want to know | Use |
| --- | --- |
| Does the **whole suite** pass? | `--all` — runs `pnpm run test:parallel` |
| Does **this test file** pass or fail? | `--files` |
| Does **this one test** fail first? | `--files --name "<pattern>" --expect fail` |
| What tests **import this changed file**? | `--related` |
| Does **this package** pass, per test? | `--package sme` |

```bash
python3 <script> --all                        # full suite (quality gate)
python3 <script> --all --force                # bypass the turbo cache
python3 <script> --all --script test:coverage # any root test script
python3 <script> --files <path> --expect fail --name "DEF-123 / ISSUE-001"
python3 <script> --related <changed source> [--related-scope all]
python3 <script> --package sme foundation
```

**Package aliases:** `foundation` · `theme` · `cms-utils` · `cms-components` · `sme`

| Flag | Purpose |
| --- | --- |
| `--label` | Output folder name — always set it (e.g. `DEF-123-ISSUE-001-failing-first`) |
| `--timeout` | Seconds — default 1800 suite, 600 targeted |
| `--coverage` | Suite: runs `test:coverage` · Targeted: adds `--coverage` |
| `--dry-run` | Print the resolved command without running |
| `--where` | Print repo root, script path and package scan dirs |
| `--force` · `--script` · `--no-drill-down` | `--all` only |

---

## ⚠️ Verdicts — Read These, Not the Exit Code

| Verdict | Exit | Meaning | Action |
| --- | --- | --- | --- |
| `PASS` | 0 | Every executed test passed | Proceed |
| `EXPECTED_FAIL` | 0 | `--expect fail` and the target failed **on an assertion** | Root cause proven |
| `FAIL` | 1 | Tests failed or a suite errored | Read `failed_tests` |
| `PASSED_UNEXPECTEDLY` | 1 | `--expect fail` but it passed | Root cause is wrong — return to RCA |
| `FAILED_FOR_WRONG_REASON` | 1 | Load/import/setup error, or a different test failed | Not proof — fix the test **setup**, never the assertion |
| `NOT_COLLECTED` | 3 | File never ran under any path form | **Never a pass** — check placement and include pattern |
| `NO_TASKS` | 3 | Turbo ran no test tasks | **Never a pass** |
| `RUNNER_ERROR` | 5 | Crashed, timed out, or no report | Read the log tail |
| — | 2 | Usage error | Read the message; it lists what was tried |
| — | 4 | pnpm missing, root/package/script not found | Read the message |

### Suite specifics

- A **turbo cache hit is a valid pass** — inputs unchanged since a passing run. Use `--force` when you need proof of fresh execution.
- A failing package is **automatically re-run alone** for per-test detail.
- `PASSED_ON_RERUN` = failed in the suite, passed alone → **possible flaky test**. Report it; do not call the suite green.

---

## Output

```text
TEST RUN — DEF-123-ISSUE-001-failing-first
  Verdict:   EXPECTED_FAIL   (expected: fail)
  Reason:    Target test failed on an assertion, as required.
  Totals:    1 passed · 1 failed · 0 skipped · 0 suite errors · 0 not collected
  Package:   @dxp/sme-portal   RAN   exit=1  3.8s
             scan dir: Portals/Sme  ·  form: scan-dir-relative  ·  tried: scan-dir-relative✓
             reproduce: pnpm run test:sme -- --run ./Features/Shared/…/X.test.tsx -t "DEF-123 / ISSUE-001"
  ✗ FAILED  Portals/Sme/Features/…/X.test.tsx › should not display toast [DEF-123 / ISSUE-001]
  Output:    .SS_WF/Agent/TEST_RUNS/DEF-123-ISSUE-001-failing-first-20260929-064500/summary.json
```

Record the **output folder** as evidence. `summary.json` holds per-test detail; raw logs sit beside it.

⚠️ `ℹ ALSO RAN` means the filter matched an extra file — Vitest filters are substring matches. Confirm it did not affect the verdict; narrow with `--name`.

---

## Troubleshooting — Read the Error, Do Not Guess

| Message | Cause | Action |
| --- | --- | --- |
| `Test file not found` + `files with the same name` | Wrong folder casing or prefix | Use the path the error prints |
| `Repository root not found` | No `pnpm-workspace.yaml`/`turbo.json` above or below cwd | Run `--where`; pass `--repo-root` only if that fails |
| `NOT_COLLECTED` | File outside the package's `include` pattern | Check the package's vitest config and folder casing |
| `FAILED_FOR_WRONG_REASON` + suite error | Import, mock or syntax error | Fix the test setup; re-run |
| `Package not found` | Wrong alias | The message lists known packages |
| Exit 4, pnpm missing | Environment | Report STATIC ONLY; do not claim results |

---

## If Tests Cannot Run

```text
Verification level:  STATIC ONLY — tests were not executed
Reason:              [exit code + message]
Developer action:    [the reproduce: line from the output]
```

⚠️ A reasoned pass/fail is a prediction, not evidence.

---

### Rules

#### Always
- Locate the script once with `find`, confirm with `--where`, reuse both for the whole run.
- Pass the path you already have — any form.
- Read the **verdict**; set `--label`; record the output folder.
- Treat `NOT_COLLECTED`, `NO_TASKS`, `FAILED_FOR_WRONG_REASON`, `PASSED_ON_RERUN` as **not proven**.

#### Never
- **Never retry with a different path form** — the script already did.
- **Never fall back to a hand-built `pnpm`/`vitest`/`turbo` command** for a verdict.
- **Never pass `--repo-root` speculatively** — only after `--where` fails.
- Never convert paths to scan-dir-relative form yourself.
- Never report `NOT_COLLECTED` or `NO_TASKS` as a pass.
- Never edit an assertion to change a verdict.
- Never claim results the script did not produce.
