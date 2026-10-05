---
name: defect-intake-and-decomposition
description: Use as Phase 1 of the FE Defect Fix workflow to read the JIRA defect ticket, split it into independently-fixable issues, extract Defect Dev Notes, and capture for each issue a precise symptom contract — trigger, observed result, expected result — that root cause analysis must explain. Triggers include defect intake, parse defect, split defect issues, or decompose defect.
disable-model-invocation: true
---

## Defect Intake and Decomposition

Turn the defect ticket into issues, each with a **symptom contract** that Phase 3 must explain.

⚠️ Triage already happened. Do not re-litigate whether it is a defect.

---

## Input — one file

```text
.SS_WF/{{$var[ticket_id]s}}_JIRA_OUTPUT.json
```

Read it directly. If it is missing or unreadable → **HALT**.

⚠️ Read only this ticket. **Never** read the parent story ticket or any other `*_JIRA_OUTPUT.json` in `.SS_WF` — other defects' tickets may be present; they are not context.

⚠️ **Ticket titles may carry a prefix** such as `TAW-175 || …`. It is a label, not a ticket to look up. Do not search for it.

---

## The Symptom Contract — the most important output

For every issue, extract these from the ticket **verbatim where possible**:

```text
ISSUE-001
  TRIGGER    the user action / event that produces the bug
             e.g. "enter incorrect OTP 1111 → click Verify"
  OBSERVED   what actually happens (ticket's Actual Result)
             e.g. "API returns BE_OTP_INVALID; no error message shown on UI"
  EXPECTED   what should happen (ticket's Expected Result, or the AC it cites)
             e.g. "error message returned by the API is shown on Verify Account screen"
  SIGNALS    concrete identifiers in the ticket: error codes, API names, field names,
             screen names, locale, viewport
             e.g. BE_OTP_INVALID · Verify OTP API · Verify Account screen
```

⚠️ **The contract is fixed for the rest of the run.** Phase 3 must find a mechanism that, when TRIGGER happens, produces OBSERVED. A cause that involves a different trigger is wrong by definition.

⚠️ If the ticket gives no Actual or Expected Result, record `Not provided` — never invent one.

---

## Splitting — semantic

Separate issues if root cause, file/layer, category, or fixability differ. One issue if one root cause produces several symptoms. When unsure, split. Assign `ISSUE-001…`; never renumber.

## Defect Dev Notes

Scan for `Dev Notes` · `Developer Notes` · `Fix Notes` · `How to Fix` · `Implementation Notes`. Extract verbatim as `DDN-001…` (never `DN-`). Top priority.

## Category (one per issue)

UI · RTL · Responsive · Accessibility · Media · Sitecore · BFF/API · State · Missing AC · Regression — drives which coding skills load and which artefact may be refetched.

```text
"error/message not shown after <action>"   → BFF/API or State (error path)
"blank / wrong value"                      → BFF/API
"authored text missing"                    → Sitecore
"looks wrong in Arabic"                    → RTL
"used to work"                             → Regression
```

## Source-change signals

Flag only if the ticket says so: design updated / new Figma URL (→ Figma); field renamed / API changed (→ Sitecore/BFF). Absence = no refetch.

---

## Output — one block

```text
INTAKE — {{$var[ticket_id]s}} (parent {{$var[parent_ticket_id]s}})
  DDN:      none
  ISSUE-001 [BFF/API]
    TRIGGER:  incorrect OTP → Verify
    OBSERVED: BE_OTP_INVALID returned; no error message on UI
    EXPECTED: API error message shown on Verify Account screen
    SIGNALS:  BE_OTP_INVALID · Verify OTP API · Verify Account screen
```

### Gate
```text
- [ ] .SS_WF/{{$var[ticket_id]s}}_JIRA_OUTPUT.json read; no other ticket read
- [ ] Every issue has TRIGGER · OBSERVED · EXPECTED · SIGNALS (or "Not provided")
- [ ] DDN extracted verbatim; one category per issue
- [ ] No files written
```

### Never
- Never search for the ticket file — read the path above.
- Never read the parent story ticket or other defects' tickets.
- Never look up a ticket ID found in the title prefix.
- Never paraphrase OBSERVED/EXPECTED into something the ticket did not say.
- Never begin RCA here.
