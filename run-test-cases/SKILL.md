---
name: run-test-cases
description: Use to execute the monorepo's tests and get a machine-readable verdict — the full suite through the project's own package.json script (turbo run test --parallel), or targeted runs of specific test files, tests related to changed source files, or whole packages. Resolves each package's Vitest scan directory so file paths are written in the form Vitest expects, and distinguishes a real assertion failure from a load error or a file that was never collected. Shared by the Defect Fix workflow (failing-first proof, guard tests, blast radius) and the static code quality workflow (full-suite gate). Triggers include run tests, run all tests, test suite, test:parallel, run test cases, verify tests pass, failing-first, blast radius tests, or unit test run.
disable-model-invocation: true
---

## Run Test Cases

### Purpose

Execute tests and return a verdict the agent can act on. The agent decides **what** to test. The bundled script decides **how**.

```bash
python3 scripts/run-tests.py --all                                   # full suite
python3 scripts/run-tests.py --files <test files> [--expect fail]    # specific files
```

⚠️ **Always use the script. Never build a test command by hand.** A hand-built command can use the wrong path form, run from the wrong package, match no files, or produce output that cannot be parsed — and each of those can look like a pass.

---

## Two Engines — Pick by Question

| You want to know | Use | Engine | Used by |
| --- | --- | --- | --- |
| **Does the whole test suite pass?** | `--all` | **Suite** — runs `pnpm run test:parallel` exactly as developers do | Static code quality workflow |
| Does **this test file** pass or fail? | `--files` | **Targeted** — direct Vitest, JSON reporter | Defect workflow |
| Does **this one test** fail first? | `--files --name --expect fail` | Targeted | Defect workflow |
| What tests **import this changed file**? | `--related` | Targeted | Defect workflow (blast radius) |
| Does **this package** pass, with per-test detail? | `--package` | Targeted | Both |

```text
SUITE     fidelity  — the exact project command, turbo cache and all
TARGETED  precision — per-test status, load errors separated from assertion failures
```

The suite engine recovers precision when it needs it: **any failing package is automatically re-run with the targeted engine** to get per-test failure detail.

---

## ENGINE 1 — SUITE (`--all`)

Runs a root `package.json` script unchanged, and reads the result per package.

```bash
python3 scripts/run-tests.py --all                            # pnpm run test:parallel
python3 scripts/run-tests.py --all --force                    # bypass the turbo cache
python3 scripts/run-tests.py --all --script test              # pnpm run test (sequential)
python3 scripts/run-tests.py --all --coverage                 # pnpm run test:coverage
python3 scripts/run-tests.py --all --script test:sme          # one package, project script
```

| Root script | Runs |
| --- | --- |
| `test:parallel` *(default)* | `turbo run test --parallel` |
| `test` | `turbo run test` |
| `test:coverage` | `turbo run test:coverage` *(default when `--coverage` is given)* |
| `test:foundation` · `test:theme` · `test:cms-utils` · `test:cms-components` · `test:sme` | one package via turbo |

⚠️ The script validates the name against the root `package.json`. An unknown script exits **4** and lists the test scripts that exist.

### What it reads

```text
Turbo prefixes every line:   @dxp/sme-portal:test: <line>
Output from --parallel is interleaved; the prefix keeps each package separate.

Per package   → Vitest summary lines   "Test Files  1 failed | 24 passed (25)"
                                        "Tests  2 failed | 180 passed (182)"
              → FAIL lines, "No test files found", ELIFECYCLE / command errors
              → cache status: hit · miss · bypass
Turbo summary → "Tasks: N successful, N total" · "Cached: N" · "Failed: pkg#test"
```

### Turbo cache

A **cache hit is a valid result.** Turbo replays a task only when its hashed inputs are unchanged since a run that passed, so a hit means *the same code already passed*. Each package reports its cache status.

Use `--force` (sets `TURBO_FORCE=true`) when you need proof the tests **executed in this run** — for example a release gate, or when `turbo.json` inputs may be incomplete.

⚠️ If a package's `outputLogs` setting in `turbo.json` suppresses logs on cache hits, its counts show as `—`. Status still comes from turbo's `Failed:` line; re-run with `--force` for counts.

### Automatic drill-down

When a package fails, the script re-runs **only that package** with the targeted engine and attaches per-test detail:

| Drill-down result | Meaning |
| --- | --- |
| `FAILED` | Per-test failures and load errors listed — act on these |
| `PASSED_ON_RERUN` | Failed under turbo, passed alone — **possible flaky, order-dependent or parallelism-sensitive test**. Report it; do not treat the suite as green |
| `NO_REPORT` | The targeted run produced no report — rely on the log |

Skip it with `--no-drill-down` when you only need the gate result.

### Suite verdicts

| Verdict | Exit | Meaning |
| --- | --- | --- |
| `PASS` | 0 | Every test task passed |
| `FAIL` | 1 | One or more packages failed — see the package table and `failed_tests` |
| `NO_TASKS` | 3 | Turbo ran no test tasks — **never a pass** |
| `RUNNER_ERROR` | 5 | Timed out, or the command failed with no failing package identified (turbo/pnpm error) |

### Per-package status

| Status | Meaning |
| --- | --- |
| `PASSED` | Task succeeded |
| `FAILED` | Tests failed, a suite errored, or turbo marked the task failed |
| `NO_TEST_FILES` | Vitest found no test files and exited non-zero — usually an include-pattern or placement problem |
| `UNKNOWN` | No log output for the package and the run failed — read `suite.log` |

### Suite output

```text
TEST SUITE — quality-gate
  Command:   pnpm run test:parallel   →  turbo run test --parallel
  Verdict:   FAIL
  Reason:    1 package(s) failed: @dxp/sme-portal.
  Turbo:     4 successful · 5 total · 2 cached · 41.2s
  Tests:     612 passed · 2 failed · 3 skipped   ·   files 80 passed · 1 failed
  Package                 Status          Tests p/f/s     Files p/f   Cache
  @dxp/cms-components     PASSED          96/0/0          14/0        hit
  @dxp/foundation         PASSED          240/0/3         31/0        hit
  @dxp/sme-portal         FAILED          180/2/0         24/1        miss
  ✗ FAILED  [@dxp/sme-portal] Portals/Sme/features/Shared/…/OtpInput.test.tsx › handles invalid otp
      AssertionError: expected error message
  Output:    .SS_WF/Agent/TEST_RUNS/quality-gate-20260925-101500/summary.json
```

`summary.json` (suite): `verdict · reason · script · script_command · force · exit_code · duration_s · turbo{} · totals{} · packages[] · failed_tests[] · drill_down[] · log`

---

## ENGINE 2 — TARGETED (`--files` · `--related` · `--package`)

Runs Vitest directly inside the owning package with a JSON reporter:

```text
pnpm --filter <package> exec vitest run <files> [flags from the package's test script] --reporter=json …
```

Flags in the package's own `test` script that change where Vitest looks — `--config`, `--root`, `--dir` — are forwarded, so a targeted run uses the same config as `pnpm run test:<package>`.

### ⚠️ Path Form — Why Hand-Built Commands Fail

Vitest matches a file filter against paths **relative to its scan directory** (`test.dir`, else `root`), which is not always the package folder. For `@dxp/sme-portal` that directory is `features/`:

```text
pnpm run test:sme -- Portals/Sme/features/Shared/OtpVerification/Components/OtpVerificationContainer.test.tsx
  ✗ FAILS    — repo-relative; not found under features/

pnpm run test:sme -- ./Shared/OtpVerification/Components/OtpVerificationContainer.test.tsx
  ✓ PASSES   — relative to the scan directory
```

The script handles this:

```text
1. Accepts any path — pass the repo-relative path you have; do NOT convert it
2. Finds the owning package (nearest package.json)
3. Finds the scan directory: package test script flags → config `dir` → config `root`
4. Writes the filter relative to it:  ./Shared/…/X.test.tsx
5. Not collected? → retries as absolute, then package-relative; reports which worked
6. No form collects it → NOT_COLLECTED — never a pass
```

⚠️ **Vitest filters are substring matches.** `./Shared/X.test.tsx` also matches `Motor/Shared/X.test.tsx`. The script reports any unrequested file as `ℹ ALSO RAN` — check it did not mask or cause a result. Narrow with `--name` if needed.

### Targeted examples

```bash
# Specific files — files from different packages may be mixed
python3 scripts/run-tests.py --files Portals/Sme/features/Shared/OtpVerification/Components/OtpVerificationContainer.test.tsx

# Failing-first — the named test must fail on an assertion
python3 scripts/run-tests.py --files <test file> --name "DEF-123 / ISSUE-002" --expect fail \
  --label DEF-123-ISSUE-002-failing-first

# Blast radius — every test that imports the changed files
python3 scripts/run-tests.py --related Packages/DesignSystem/Foundation/Src/Atoms/Button/Button.tsx \
  --related-scope all        # design-system / common code: search every package

# Whole packages with per-test detail
python3 scripts/run-tests.py --package sme foundation
```

**Package aliases:** `foundation` · `theme` · `cms-utils` · `cms-components` · `sme` — or the full `@dxp/...` name.

### Targeted verdicts

| Verdict | Exit | Meaning | Action |
| --- | --- | --- | --- |
| `PASS` | 0 | Every executed test passed | Proceed |
| `EXPECTED_FAIL` | 0 | `--expect fail` and the target failed **on an assertion** | Root cause proven |
| `FAIL` | 1 | Tests failed or a suite errored | Read `failed_tests` |
| `PASSED_UNEXPECTEDLY` | 1 | `--expect fail`, but the test passed | Root cause is wrong — return to RCA |
| `FAILED_FOR_WRONG_REASON` | 1 | Load/import/setup error, or a *different* test failed | Not proof — fix the test **setup**, never the assertion |
| `NOT_COLLECTED` | 3 | A requested file never ran under any path form | **Never a pass** — check placement and include pattern |
| `RUNNER_ERROR` | 5 | Vitest crashed, timed out, or produced no report | Read the log tail |

### Targeted output

```text
TEST RUN — DEF-123-ISSUE-002-failing-first
  Verdict:   EXPECTED_FAIL   (expected: fail)
  Reason:    Target test failed on an assertion, as required.
  Totals:    1 passed · 1 failed · 0 skipped · 0 suite errors · 0 not collected
  Package:   @dxp/sme-portal   RAN   exit=1  3.8s
             scan dir: Portals/Sme/features  ·  path form: scan-dir-relative  ·  tried: scan-dir-relative✓
             reproduce: pnpm run test:sme -- ./Shared/…/OtpInput.test.tsx
  ✗ FAILED  Portals/Sme/features/Shared/…/OtpInput.test.tsx › handles invalid otp [DEF-123 / ISSUE-002]
      AssertionError: expected error message
```

⚠️ If `tried:` shows a fallback (`scan-dir-relative✗ → absolute✓`), the scan directory was not detected — the run is still valid, but check that package's vitest config.

`summary.json` (targeted): `verdict · reason · totals{} · failed_tests[] · suite_errors[] · not_collected[] · packages[]` — each package with `scan_dir · path_form · attempts[] · command · developer_equivalent · test_script · also_ran[]`.

---

## Common Flags

| Flag | Applies to | Purpose |
| --- | --- | --- |
| `--label` | all | Output folder name — e.g. `quality-gate`, `DEF-123-ISSUE-002-after-fix` |
| `--timeout` | all | Seconds — default **1800** suite, **600** targeted |
| `--coverage` | all | Suite: runs `test:coverage` unless `--script` is given · Targeted: adds `--coverage` |
| `--dry-run` | all | Print the resolved command, script, scan directory and path form — nothing runs |
| `--script` · `--force` · `--no-drill-down` | `--all` only | Suite controls |
| `--name` · `--expect` | targeted only | Test filter · failing-first |

**Output location:** `.SS_WF/Agent/TEST_RUNS/<label>-<timestamp>/` — `summary.json`, raw logs, JSON reports, and `drill-down/` for suite runs. The script creates `TEST_RUNS` but never `.SS_WF`; without it, output goes to a printed temp folder.

---

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Suite `NO_TEST_FILES` for a package | No tests match its include pattern | Check placement and `include`; a new package may need tests |
| Suite `PASSED_ON_RERUN` | Test depends on order, timing or shared state | Report as flaky; do not mark the gate green |
| Suite counts show `—` | turbo `outputLogs` hides cached logs | Re-run with `--force` |
| Suite `RUNNER_ERROR`, exit ≠ 0 | turbo or pnpm failed before tests ran | Read `suite.log` |
| Targeted `NOT_COLLECTED` | File outside `include`, or wrong casing | Check the package's vitest config; paths are case-sensitive on Linux/CI |
| Targeted `ALSO RAN` | Substring filter matched another file | Confirm the result; narrow with `--name` |
| Targeted `FAILED_FOR_WRONG_REASON` | Import, mock or syntax error | Fix the test setup; re-run |
| Exit 4 | pnpm missing, repo root, package or script not found | Pass `--repo-root`; check the script name |

---

## If Tests Cannot Run

Exit **4** or **5** that cannot be resolved → do **not** claim results:

```text
Verification level:  STATIC ONLY — tests were not executed
Reason:              [exit code + script message]
Developer action:    [the reproduce / developer_equivalent command from the output]
```

⚠️ A reasoned pass/fail is a prediction, not evidence.

---

### Rules

#### Always
- Run tests **through the script**; pass paths as you have them.
- Read the **verdict** and package statuses, not just the exit code.
- Use `--all` for "does everything pass"; targeted modes for specific files or tests.
- Use `--force` when the run must prove fresh execution.
- Treat `NOT_COLLECTED`, `NO_TASKS`, `FAILED_FOR_WRONG_REASON` and `PASSED_ON_RERUN` as **not proven**.
- Use `--label`; record the output folder as evidence.
- Use `--dry-run` when a package or script is new to the workflow.

#### Never
- Never build a `vitest`, `turbo` or `pnpm test` command by hand for a verdict.
- Never convert paths to scan-dir-relative form yourself.
- Never report `NOT_COLLECTED` or `NO_TASKS` as a pass.
- Never treat `PASSED_ON_RERUN` as a green suite.
- Never accept a load error as failing-first proof, or edit an assertion to change a verdict.
- Never claim results when the script could not run.
- Never delete or edit anything in `TEST_RUNS/` after a run.
