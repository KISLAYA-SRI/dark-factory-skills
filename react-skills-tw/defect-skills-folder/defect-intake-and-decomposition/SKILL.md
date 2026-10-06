---
name: defect-intake-and-decomposition
description: Phase 1 of the FE defect workflow. Turns a triaged defect ticket into issues, each with a symptom contract, category, contract-change classification and developer notes. Reads only the defect ticket JSON.
---

## Defect Intake and Decomposition

Triage already happened. Do not question whether it is a defect.

### Input: one file

`.SS_WF/{{$var[ticket_id]s}}_JIRA_OUTPUT.json`

- Read it directly. If it is missing or unreadable, HALT.
- Read only this ticket. A prefix in the title (for example `ABC-123 ||`) is a label, not a ticket to look up.
- Read the description, all comments and attachment names; dev notes are often in comments.

### 1. Symptom contract per issue

Extract from the ticket, verbatim where possible:

- **TRIGGER**: the user action or event that produces the bug (include steps to reproduce)
- **OBSERVED**: the ticket's Actual Result
- **EXPECTED**: the ticket's Expected Result, or the AC it cites
- **SIGNALS**: concrete identifiers (error codes, API names, fields, screens, locale, viewport, device)

If Actual or Expected is missing, record `Not provided`. Never invent one.
The contract is fixed for the rest of the run.

### 2. Contract classification

For each of BFF, Sitecore and Figma:

- **DEVIATED** if the ticket supplies data or a reference for it: payload, response sample, field structure,
  endpoint, Sitecore path or item, new Figma link or node, screenshot of changed design, changed copy.
- **UNCHANGED** otherwise.

Mentioning a name (an error code, a field, a component) is not supplying data.
For DEVIATED, record what the ticket supplied and whether it is data or a reference.

### 3. Splitting

- Split when root cause, layer or expected behaviour clearly differ.
- Keep one issue when one behaviour produces several symptoms.
- Number `ISSUE-001`, `ISSUE-002`; never renumber.

### 4. Category (one per issue)

UI · RTL · Responsive · Accessibility · Media · Sitecore · BFF/API · State · Missing AC · Regression.
The category only decides which coding-standard skill loads first. It is not a diagnosis and not a limit.

### 5. Developer notes

- Copy any Dev Notes, Developer Notes, Fix Notes, How to Fix, Implementation Notes or dev comments verbatim as `DDN-001`, `DDN-002`.
- Map each to the issue it applies to.
- They are the highest-priority instruction for the fix, after the Expected Result.
- If none are present, record `none`. That never limits the investigation.

### Output: one block, no narration

```text
INTAKE   {{$var[ticket_id]s}} (parent {{$var[parent_ticket_id]s}})
  CONTRACTS: BFF <UNCHANGED|DEVIATED: data|reference>, Sitecore <…>, Figma <…>
  DEV NOTES: DDN-001 → ISSUE-001: "<verbatim>" | none
  ISSUE-001 [<category>]
    TRIGGER:  …
    OBSERVED: …
    EXPECTED: …
    SIGNALS:  …
```

### Never

- Never read the parent story ticket or any other `*_JIRA_OUTPUT.json`.
- Never paraphrase OBSERVED or EXPECTED into something the ticket did not say.
- Never start investigating code here. Write no files.
