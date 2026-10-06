---
name: defect-reporting-and-learning
description: Phase 3 of the FE defect workflow. Updates the parent code-generation document in place with the defect fix and appends a Defect Change Log entry, then writes a Coding Agent Learning when the fault origin is an agent miss or a regression from a prior fix. Runs after defect-investigate-and-fix, even if every issue is BLOCKED.
---

## Defect Reporting and Learning

### Purpose

- **A. Update the code-generation document**: always
- **B. Write a coding-agent learning**: only for agent miss or regression from a prior fix

Both are **file writes**. This phase is not done until the files on disk have changed and the write is confirmed.
A learning or update that exists only in your response is lost when the run ends.

### Inputs

| Item      | Value                                                                           |
| --------- | ------------------------------------------------------------------------------- |
| Document  | `.SS_WF/Agent/CODE/{{$var[parent_ticket_id]s}}_CODE_GENERATION.md`              |
| Learnings | `.project/learnings/CODING_AGENT_LEARNINGS.md` (from the repo root)             |
| Defect ID | `{{$var[ticket_id]s}}` (never the parent ID)                                    |
| Facts     | The `INTAKE` block, the `ISSUE-<n>` blocks from this run, and `git diff --stat` |

Use only facts from those blocks and the diff. Never describe a change the diff does not show.

---

## PART A: Update the code-generation document

### Find sections by role, not by number

Layouts differ between stories. Identify sections by heading and content:

| Role                             | Typical headings                                                                                                                                                                   | On a defect fix                                           |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| **State** (what the code is now) | Files created/updated, components, props, integration files, API/BFF integration, mappers, containers, state, routing, timers, error handling, design tokens, responsive/RTL notes | Update only rows the fix touched                          |
| **AC coverage**                  | AC coverage, AC evidence                                                                                                                                                           | Update status and evidence for affected ACs               |
| **Gaps / limitations**           | Gaps, blockers, limitations                                                                                                                                                        | Mark resolved `Resolved [<defect id>]`; never delete rows |
| **Historical**                   | Developer notes applied, reuse decisions, generation summary                                                                                                                       | Never change                                              |
| **Defect Change Log**            | `## Defect Change Log`                                                                                                                                                             | Append one entry per defect                               |

- If `## Defect Change Log` does not exist, create it at the end of the document.
- If the fix created files, add them to the files section, tagged `[<defect id>]`.

### Minimal change

- Update only rows the fix touched, or rows the investigation found had drifted from the code.
- Tag changed rows `[<defect id>]`; tag drift reconciliations `[<defect id> · drift]`.
- Prefer `file → symbol` over line numbers.
- Never regenerate the document, reformat untouched rows, or edit a prior change-log entry.
- Drift noticed but not inspected goes in the entry as _observed, not reconciled_.

### Change-log entry

```markdown
### <defect id> — <YYYY-MM-DD> — Defect Fix

**Issues:** <n> · **Fixed:** <n> · **Blocked:** <n>
**Contracts:** BFF <UNCHANGED|DEVIATED> · Sitecore <…> · Figma <…>

#### Developer Notes

| Note | Applied to | How applied |
| ---- | ---------- | ----------- |

> or: None

#### Issues

| Issue | Category | Status | Root cause (file → mechanism) | Fault origin | Fix |
| ----- | -------- | ------ | ----------------------------- | ------------ | --- |

#### Contract deviations

| Contract | Baseline | Ticket | Handled by |
| -------- | -------- | ------ | ---------- |

> or: None (all contracts unchanged)

#### Scenarios verified

| Issue     | Scenario                                | Evidence                              |
| --------- | --------------------------------------- | ------------------------------------- |
| ISSUE-001 | <reported scenario>                     | reproduction: before FAIL, after PASS |
| ISSUE-001 | <sibling / AC / state / consumer / new> | new test · existing test · gap fixed  |

#### Test runs

| Run | Verdict | Output folder |
| --- | ------- | ------------- |

#### Diff

<pasted git diff --stat>

#### Sections updated

| Section | Change |
| ------- | ------ |

#### Existing tests modified

| Test | Was asserting | Why changed |
| ---- | ------------- | ----------- |

> or: None

#### Observations, not fixed

> or: None

#### Learnings written

| Origin | Issues | Written? |
| ------ | ------ | -------- |
```

### How to write

1. Read the sections you will edit (search with `grep -n`; read the whole file only if it is small).
2. Make the targeted edits to state, AC coverage and gap sections.
3. Append the change-log entry.
4. Write the file back without an append mode; preserve untouched content exactly.
5. Re-read and confirm the entry is present.

---

## PART B: Write the learning (gated)

### Gate (origin from the ISSUE block)

| Origin                                                                                                      | Action                                            |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Agent miss                                                                                                  | Write                                             |
| Regression from prior fix                                                                                   | Write                                             |
| Post-generation manual change, contract change, design change, upstream gap, ambiguous requirement, unknown | Do not write; record the origin in the change log |

A learning must be something the coding agent could have acted on at generation time.

- Yes: "A lockout or block state must start only at the AC's failure threshold, never on the first failure."
- No: "Sitecore renamed a field" (external); "the developer's fallback returned empty" (not agent code).

### Namespace

| Category                                      | Namespace                                                  |
| --------------------------------------------- | ---------------------------------------------------------- |
| UI · RTL · Responsive · Accessibility · Media | `# UI LEARNINGS`                                           |
| BFF/API · State · Sitecore · mappers          | `# LOGIC LEARNINGS`                                        |
| A test should have caught it                  | `# TEST LEARNINGS` (also write to the behaviour namespace) |
| Storybook · catalogue                         | `# STORYBOOK LEARNINGS`                                    |

### Steps (all four, every time)

1. **Read** the learnings file. If it does not exist, create it with the four headings.
2. **Dedupe**: look for a semantically equivalent rule. Found → increment recurrence, add this defect ID. Not found → compose a new entry.
3. **Write** the complete file back with the entry merged into its namespace.
4. **Confirm** the write; report namespace and new/recurrence.

### Entry format

```markdown
- <Area>: <rule — what to do and not do>. <why it matters, one line>.
  Refs: <defect ids> (recurrence ×<n>)
```

Two to four lines. A general rule, never a story about this defect.
Preserve every existing entry and all four headings.

### Skill gap

At recurrence ≥ 3 the coding skill is under-specified. Record in the change log:
`SKILL GAP: <rule> · <namespace> · recurrence <n> (<refs>) · skill: <coding skill> — strengthen <section>`.
Do not edit the skill; that is a human decision.

---

### Done when

- [ ] Targeted sections updated and tagged; historical sections and prior entries untouched
- [ ] Change-log entry appended; file written and confirmed
- [ ] Every issue's origin checked against the gate
- [ ] Each qualifying learning read, deduped, written and confirmed — or "no issue qualified" stated explicitly

### Never

- Never describe a learning or update instead of writing it.
- Never write a learning for a non-qualifying origin.
- Never delete or rewrite an existing learning except to increment recurrence.
- Never record a test as passed without its run output folder.
- Never create a separate defect document; the change log is the record.
- Never close, comment on or transition the ticket.
