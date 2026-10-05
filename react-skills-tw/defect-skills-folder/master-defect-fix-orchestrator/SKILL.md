---
name: master-defect-fix-orchestrator
description: Orchestrates the frontend defect workflow for a triaged defect ticket - intake, investigate and fix, report.
---

## Master Defect Fix Orchestrator

### Variables

- `{{$var[ticket_id]s}}`: the defect ticket
- `{{$var[parent_ticket_id]s}}`: the story it was raised on

### Principles

1. **The defect is real.** Every ticket in this workflow is triaged. The only outcomes are FIXED or BLOCKED.
2. **Unchanged contracts are fixed inputs.** If the ticket gives no BFF, Sitecore or Figma data, that contract has not changed and the fault is in the code.
3. **Reproduce before you reason.** A failing test comes before any conclusion about the code.
4. **Fix the behaviour, not the line.** Every scenario through the changed behaviour is verified.
5. **Evidence, not narrative.** Every claim is backed by a test verdict or `git diff --stat`.

### Phases

| #   | Phase                           | Skill                                                                                     |
| --- | ------------------------------- | ----------------------------------------------------------------------------------------- |
| 1   | Intake                          | `defect-intake-and-decomposition`                                                         |
| 2   | Investigate and fix (per issue) | `defect-investigate-and-fix` + coding standards for the issue category + `run-test-cases` |
| 3   | Report                          | `defect-reporting-and-learning`                                                           |

Only a missing defect ticket ends the run early (HALT). A BLOCKED issue does not stop the other issues.

Load only the coding-standards skill that matches each issue's category. Do not load generation, Storybook or catalogue skills.

### Working rules

- Run every command from the repository root (`git rev-parse --show-toplevel`). Do not `cd` elsewhere.
- Updating a todo list is not evidence. A phase is done only when its output block exists.

### Final report: this exact shape, nothing else

The first line is machine-read by the workflow. Do not change its format.

```text
DEFECT_VERDICT=<FIXED|BLOCKED|PARTIAL>
{{$var[ticket_id]s}}   <n> issues   <n> fixed   <n> blocked
  ISSUE-001  <FIXED|BLOCKED>  <file>: <root cause in one line>
    Reproduction: before FAIL, after PASS
    Scenarios:    <n> verified (<n> new tests, <n> existing)
  git diff --stat:
    <pasted output>
  Summary: <path> updated
```

- `FIXED`: all issues fixed. `BLOCKED`: all issues blocked. `PARTIAL`: a mix.
- The diff block is pasted from the command output. The report may not describe any change the diff does not show.

### Never

- Never output "not a defect", "already fixed" or "cannot reproduce".
- Never recommend closing the ticket or verifying an UNCHANGED contract externally.
- Never close, comment on or transition the ticket.
