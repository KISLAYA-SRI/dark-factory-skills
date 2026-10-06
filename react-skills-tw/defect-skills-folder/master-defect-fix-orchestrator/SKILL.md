---
name: master-defect-fix-orchestrator
description: Orchestrates the FE defect workflow for a triaged defect ticket in three phases - intake, investigate and fix, report - and loads coding-standard skills on demand. Use at the start of every defect run.
---

## Master Defect Fix Orchestrator

### Variables

- `{{$var[ticket_id]s}}`: the defect ticket
- `{{$var[parent_ticket_id]s}}`: the story the defect was raised on

### Principles

1. **The defect is real.** Every ticket here is triaged. The only outcomes are FIXED or BLOCKED.
2. **If the code looks correct, the understanding is incomplete.** Find the gap; never conclude "not a defect" or "already fixed".
3. **Unchanged contracts are fixed inputs.** If the ticket gives no BFF, Sitecore or Figma data, that contract has not changed and the fault is in the code.
4. **Developer notes come first.** Highest-priority instruction after the ticket's Expected Result. Their absence never limits the investigation.
5. **Reproduce before you reason.** A failing test comes before any conclusion about the code.
6. **Trace every hop.** No layer is assumed correct without being opened.
7. **Fix the behaviour, not the line.** Every related scenario, including ones the ticket did not mention, is verified.
8. **Evidence, not narrative.** Every claim is backed by a test run output or `git diff --stat`.

### Phases

| #   | Phase                           | Skill                                                 | Output                                              |
| --- | ------------------------------- | ----------------------------------------------------- | --------------------------------------------------- |
| 1   | Intake                          | `defect-intake-and-decomposition`                     | `INTAKE` block                                      |
| 2   | Investigate and fix (per issue) | `defect-investigate-and-fix` + on-demand skills below | `ISSUE-<n>` block per issue                         |
| 3   | Report                          | `defect-reporting-and-learning`                       | Code-generation document and learnings file written |

- Only a missing or unreadable defect ticket ends the run early (HALT).
- A BLOCKED issue does not stop the other issues.
- Phase 3 always runs, even if every issue is BLOCKED.

### On-demand skills

Coding skills supply **standards only**; never regenerate a component.
The issue's category picks the first skill to load. After that, load any skill the moment the
work enters its area, whatever the category. Load each skill at most once per run. Never load speculatively.

**Starting skill by category**
| Category | Load first |
| --- | --- |
| UI, RTL, Responsive, Accessibility | `presentational-ui-generation` |
| Media | `frontend-media-integration` |
| BFF/API | `frontend-logic-integration` |
| State | `frontend-state-and-form-management` |
| Sitecore | `sitecore-rendering-integration` |
| Missing AC, Regression | Whichever area the root cause is in |

**Load when the work needs it**
| Skill | Load when |
| --- | --- |
| `frontend-test-generation` | Always, before writing the reproduction test |
| `run-test-cases` | Always, for every test run |
| `presentational-ui-generation` | Markup, styles, layout, spacing, typography, RTL, responsive, accessibility, design-system usage |
| `frontend-logic-integration` | Hooks, services, API calls, containers, mappers, error handling, API-driven toasts |
| `frontend-state-and-form-management` | State, stores, forms, validation, timers, counters, enable/disable logic |
| `sitecore-rendering-integration` | Sitecore field mapping, datasource props, rendering registration, CMS message lookup |
| `frontend-media-integration` | Images, icons, SVGs, video, DAM assets, media sizing or loading |
| `repository-structure-governance` | Before creating, moving or renaming any file or folder |
| `context-gathering` | A contract is DEVIATED and the ticket gives a reference (endpoint, Sitecore path, Figma link) instead of data |

### Working rules

- Run every command from the repository root (`git rev-parse --show-toplevel`). Never `cd` elsewhere.
- Run tests only through `run-test-cases`.
- Search large documents (`grep -n`) and read only the needed sections; never read the code-generation document or analysis plan end to end.
- A todo item is complete only when its phase output block exists. Updating the list is not evidence.

### Final report: this exact shape, nothing else

The first line is machine-read by the workflow. Do not change its format.

```text
DEFECT_VERDICT=<FIXED|BLOCKED|PARTIAL>
{{$var[ticket_id]s}}   <n> issues   <n> fixed   <n> blocked
  ISSUE-001  <FIXED|BLOCKED>  <file → symbol>: <root cause in one line>
    Reproduction: before FAIL, after PASS
    Scenarios:    <n> verified (<n> new tests, <n> existing, <n> gaps fixed)
  Skills loaded: <list>
  git diff --stat:
    <pasted output>
  Code-generation document: updated · Learnings: <written | none qualified>
```

- `FIXED`: all issues fixed. `BLOCKED`: all blocked. `PARTIAL`: a mix.
- The diff is pasted from the command. The report may not describe a change the diff does not show.

### Never

- Never output "not a defect", "already fixed", "working as designed" or "cannot reproduce".
- Never recommend closing the ticket or verifying an UNCHANGED contract externally.
- Never close, comment on or transition the ticket.
