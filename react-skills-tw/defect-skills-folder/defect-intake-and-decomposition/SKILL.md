---
name: defect-intake-and-decomposition
description: Turn a triaged defect ticket into issues, each with a symptom contract and a contract-change classification. Use in Phase 1 of the defect workflow.
---

## Defect Intake and Decomposition

Triage already happened. Do not question whether it is a defect.

### Input: one file

`.SS_WF/{{$var[ticket_id]s}}_JIRA_OUTPUT.json`

Read it directly. If it is missing or unreadable, HALT.
Read only this ticket. A prefix in the title (for example `ABC-123 ||`) is a label, not a ticket to look up.

### 1. Symptom contract per issue

Extract from the ticket, verbatim where possible:

- **TRIGGER**: the user action or event that produces the bug
- **OBSERVED**: the ticket's Actual Result
- **EXPECTED**: the ticket's Expected Result, or the AC it cites
- **SIGNALS**: concrete identifiers (error codes, API names, fields, screens, locale, viewport)

If Actual or Expected is missing, record `Not provided`. Never invent one.
The contract is fixed for the rest of the run.

### 2. Contract classification (per ticket)

For each of BFF, Sitecore and Figma:

- **DEVIATED** if the ticket supplies data for it (payload, field structure, new Figma link or node, changed copy)
- **UNCHANGED** otherwise

Mentioning a contract's name (for example an error code) is not supplying data.

### 3. Splitting

Split issues when root cause, layer or expected behaviour clearly differ. One issue when one behaviour produces several symptoms. Number `ISSUE-001`, `ISSUE-002`; never renumber.

### 4. Category (one per issue)

UI, RTL, Responsive, Accessibility, Media, Sitecore, BFF/API, State, Missing AC, Regression.
The category only decides which coding standards load. It is not a diagnosis.

### 5. Developer notes

Copy any Dev Notes, Fix Notes or Implementation Notes verbatim as hints. They are optional input, not proof.

### Output: one block, no narration

```text
INTAKE   {{$var[ticket_id]s}} (parent {{$var[parent_ticket_id]s}})
  CONTRACTS: BFF <UNCHANGED|DEVIATED>, Sitecore <...>, Figma <...>
  HINTS:     <verbatim dev notes> | none
  ISSUE-001 [<category>]
    TRIGGER:  ...
    OBSERVED: ...
    EXPECTED: ...
    SIGNALS:  ...
```

### Never

- Never read the parent story ticket or other `*_JIRA_OUTPUT.json` files.
- Never paraphrase OBSERVED or EXPECTED into something the ticket did not say.
- Never start investigating the code here. Write no files.
