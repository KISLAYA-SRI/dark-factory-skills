---
name: run-test-cases
description: Run FE tests through the project test script and read the verdict. Loading this skill does NOT run tests - run the command below with the shell tool
---

# Run Test Cases

Run from the workspace root (contains `.agents/` and `src/`). Never `cd`. Never search for the script.

```bash
python3 ./.agents/skills/run-test-cases/scripts/run-tests.py --files <test-file> --label <label> [--name "<it pattern>"] [--expect fail]
python3 ./.agents/skills/run-test-cases/scripts/run-tests.py --related <source-file> --label <label>
```

Any path form works (`src/Portals/...`, `Portals/...`, absolute). Never hand-build `pnpm`/`vitest`; never retry with another path form.

First stdout line is `VERDICT=<value>`; exit code is 0 even for FAIL.
`Output:` is relative to `src/` → read `src/.SS_WF/Agent/TEST_RUNS/<label>-<time>/summary.json`.
Tool shows "Command failed"/no output → read `src/.SS_WF/Agent/TEST_RUNS/LATEST.json`.

| Verdict                  | Action                                |
| ------------------------ | ------------------------------------- |
| PASS                     | proceed                               |
| EXPECTED_FAIL            | reproduction proven                   |
| FAIL                     | read failed tests                     |
| PASSED_UNEXPECTEDLY      | test not realistic — fix the test     |
| FAILED_FOR_WRONG_REASON  | fix setup, never the assertion        |
| NOT_COLLECTED / NO_TASKS | never a pass — check placement        |
| PASSED_ON_RERUN          | flaky — not a pass; record it         |
| RUNNER_ERROR             | retry once, then BLOCKED: environment |
| USAGE_ERROR              | read the message                      |
| ENV_ERROR                | retry once, then BLOCKED: environment |
