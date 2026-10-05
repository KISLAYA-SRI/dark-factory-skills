---
name: defect-context-loader
description: Use as Phase 2 of the FE Defect Fix workflow to orient the agent — read the parent code generation document, use it to identify which files implement the feature the symptom lives in, and pick the entry file for tracing. Context is orientation only, never evidence. Includes a gated selective refetch via context-gathering. Triggers include defect context load or load defect context.
disable-model-invocation: true
---

## Defect Context Loader

**Purpose: orientation.** Answer one question — *which files implement the feature where the symptom occurs, and where does the trigger enter the code?* Nothing more.

⚠️ **Context is a map, not evidence.** Documents and code comments describe intent, history and other tickets. They do not tell you what is broken. Diagnosis happens in Phase 3, from the code path the trigger actually executes.

---

## 1. Input — one file

```text
.SS_WF/Agent/CODE/{{$var[parent_ticket_id]s}}_CODE_GENERATION.md
```

Read it directly. Do not search for it or for other documents.

If it is missing → search the repo for the screen / component named in the issue SIGNALS and continue.

⚠️ Do not `ls` or `grep` across `.SS_WF` looking for other documents. Validation reports, remediation summaries, checklists, other tickets' JSON — none of these are inputs.

---

## 2. Read it for orientation only

Extract just this:

```text
FEATURE MAP
  Feature:        OtpVerification (TAW-229)
  Files:          Container  Components/OtpVerificationContainer.tsx
                  Hooks      Hooks/useOtpVerify.ts · useOtpSend.ts
                  Services   Services/OtpVerifyService.ts
                  View       Components/OtpVerificationView.tsx
                  Helpers    SitecoreHelpers → resolveToastFromErrorCode
  Trigger entry:  "Verify click" → OtpVerificationContainer → handleVerify
```

Use whatever the document provides — file lists, data flow, error-code-to-UI mapping, state handling. These are shortcuts to the right files.

⚠️ **If a section is absent — including a Change Log — that is fine.** Do not search for it, do not create it here, do not record it as a gap. The document's only job is to point at files.

---

## 3. Other sources — only on a named trigger

| Source | Load only when |
| --- | --- |
| Analysis Plan `.SS_WF/Agent/Analysis/{{$var[parent_ticket_id]s}}_ANALYSIS_PLAN.md` (§4 ACs, §10 states) | The ticket's EXPECTED is missing or ambiguous and an AC is needed |
| Learnings file | Phase 6 |
| Component catalogue | The fix will touch a design-system / shared component |
| Git history | Phase 3 needs to know who last changed a line on the trigger path |
| Refetch (Sitecore / Figma / BFF) | Category matches **and** the ticket says the source changed. Snapshot first, one artefact only. |

⚠️ Never read the parent story ticket or `DEV_REVIEW.md`.

---

## Output — one block, no narration

```text
CONTEXT — TAW-516 (parent TAW-229)
  Code-gen doc:   .SS_WF/Agent/CODE/TAW-229_CODE_GENERATION.md
  Feature map:    [files as above]
  Trigger entry:  OtpVerificationContainer → handleVerify
  Extra sources:  none
```

### Gate
```text
- [ ] .SS_WF/Agent/CODE/{{$var[parent_ticket_id]s}}_CODE_GENERATION.md read
- [ ] Feature map and trigger entry identified
- [ ] No other .SS_WF documents read; no missing-section hunting
- [ ] Any extra source loaded has its trigger named
- [ ] No diagnosis performed; no files written
```

### Never
- Never search for the code-gen document — read the path above.
- Never treat a document statement or a code comment as evidence of the defect.
- Never search for sections that are not there.
- Never read validation reports, remediation summaries, or other tickets' files.
- Never begin RCA here.
