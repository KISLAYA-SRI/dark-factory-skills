---
name: defect-intake-and-decomposition
description: Use as Phase 1 of the FE Defect Fix workflow to parse a JIRA defect ticket, split it into discrete independently-fixable issues, extract Defect Dev Notes, categorise each issue, detect source-change signals, and capture reproduction conditions. Handles enumerated lists and unstructured prose describing multiple problems. Triggers include defect intake, parse defect, split defect issues, or decompose defect.
disable-model-invocation: true
---

## Defect Intake and Decomposition

### Purpose

Turn the defect ticket into a structured set of independently-fixable issues.

⚠️ **Triage already happened.** The developer decided this is a defect. Do not re-litigate — decompose and categorise.

---

### Input — one file only

```text
.SS_WF/{{$var[ticket_id]s}}_JIRA_OUTPUT_.json
```

Missing or unreadable → **HALT**.

⚠️ **The parent story ticket is NOT read** — here or anywhere in this workflow. Use `{{$var[parent_ticket_id]s}}` only to build document paths in Phase 2. Never `parent_story_id`.

---

## Splitting — semantic, not list-parsing

A ticket may hold one defect or several, enumerated or in prose.

```text
"The carousel arrows point the wrong way in Arabic and the policy number is
 blank for some records. Also the empty message shows in English on the Arabic site."
   → THREE issues · three root causes · three files
```

Separate issues if **any** differ: root cause · file/layer · category · fixable independently.
One issue if: **same root cause, several visible symptoms** (e.g. title and subtitle both blank from one missing mapper field).

⚠️ **When uncertain, split.** Two issues sharing a root cause merge naturally at RCA; one issue hiding two root causes produces a partial fix that reopens.

Assign `ISSUE-001`, `ISSUE-002`… — stable through RCA → fix → test runs → §13. **Never renumber.**

---

## Defect Dev Notes

Scan for: `Developer Notes` · `Dev Notes` · `Notes for Developer` · `Implementation Notes` · `Tech Notes` · `Fix Notes` · `How to Fix`.

Extract **verbatim** as `DDN-001`, `DDN-002`…

⚠️ **`DDN-` prefix, never `DN-`** — story Dev Notes keep the `DN-` chain. DDN is top priority over everything, including the Analysis Plan.

---

## Categorisation — one primary category per issue

Drives which coding skills load in Phase 4 and which artefact may be refetched in Phase 2.

| Category | Symptom | Skills (Phase 4) | Refetch |
| --- | --- | --- | --- |
| UI / Visual | Wrong layout, spacing, colour, token | `presentational-ui-generation` | Figma |
| RTL | Wrong direction, mirrored icon, clipped Arabic | `presentational-ui-generation` | Figma |
| Responsive | Breaks at a breakpoint, wrong grid, overflow | `presentational-ui-generation` | Figma |
| Accessibility | Missing label, keyboard trap, wrong role | `presentational-ui-generation` | None |
| Media | Image missing, wrong size, layout shift | `+ frontend-media-integration` | Figma |
| Sitecore | Authored content missing, placeholder empty | `sitecore-rendering-integration` | Sitecore |
| BFF / API | Wrong/blank value, error not handled | `frontend-logic-integration` | BFF |
| State | Wrong state renders, stale data, form issue | `+ frontend-state-and-form-management` | None |
| Missing AC | Requirement never implemented | depends on layer | None |
| Regression | Previously worked | depends on layer | None |

```text
"blank" / "wrong value"        → BFF/API   (§7 Data Flow Trace)
"authored text not showing"    → Sitecore  (§5 field→prop)
"wrong thing shows when X"     → State     (§8 State Matrix)
"looks wrong in Arabic"        → RTL
"broken at 390px"              → Responsive
"used to work"                 → Regression (§13 Change Log)
"doesn't match the design"     → UI + check for a design-change signal
```

⚠️ A genuinely two-layer problem is usually **two issues** — re-check the splitting test.

---

## Source-change signals

Phase 2 uses these as refetch **Gate Condition 2**. Flag the signal; do not judge it.

```text
DESIGN  (→ Figma)     "design updated" · "new Figma" · "per latest design"
                      · a Figma URL in the DEFECT ticket · "should now be…"

CONTRACT (→ Sitecore) "field renamed" · "rendering updated" · "placeholder changed"
         (→ BFF)      "API changed" · "response updated" · "new field in response"

DEVELOPER (→ RCA only, no refetch)
                      "after the dev fix" · "since the last change"
                      · "worked in the generated version" · a PR/commit reference
```

⚠️ **Absence of a signal is meaningful.** A UI defect with no design-change signal is a genuine visual defect — an agent miss — and must not trigger a Figma refetch.

---

## Reproduction evidence

⚠️ **These become the Phase 4 test conditions.** Record precisely; never invent.

```text
ISSUE-00N
  Summary / Category
  Steps · Expected · Actual
  Environment · Locale (en/ar) · Persona      ← "Not provided" if absent
  Attachments · Related AC · Applicable DDN
  Source-change: FIGMA | SITECORE | BFF | NONE
  Developer-change signal: [quote, or None]
```

⚠️ Locale matters disproportionately for RTL. Unstated → record `Not specified`; never assume `ar`.

---

## Output — one block, no narration

```text
INTAKE — {{$var[ticket_id]s}} (parent {{$var[parent_ticket_id]s}})
  DDN-001  [verbatim]  → ISSUE-002 | all
  ISSUE-001  [RTL]       [summary]   source-change: NONE
  ISSUE-002  [Sitecore]  [summary]   source-change: SITECORE
  Split: "[sentence]" → ISSUE-001 + ISSUE-003 (different root cause and layer)
  Refetch candidates: ISSUE-002 → Sitecore
```

Evidence blocks are held in working memory, not printed in full.

---

### Gate

```text
- [ ] Ticket read; every distinct failing behaviour is its own ISSUE-xxx
- [ ] Splitting applied semantically; rationale noted where non-obvious
- [ ] DDN extracted verbatim (never DN-); associated or marked global
- [ ] One primary category per issue
- [ ] Source-change and developer-change signals recorded
- [ ] Reproduction conditions captured; missing marked "Not provided"
- [ ] No files written
```

### Never

- Never read the parent story JIRA ticket.
- Never use `parent_story_id`.
- Never re-triage.
- Never merge distinct root causes, or split one root cause into several issues.
- Never invent steps, environment or locale.
- Never use the `DN-` prefix for defect notes; never renumber issue IDs.
- Never assume a source changed without an explicit signal.
- Never decide fault origin, trigger a refetch, begin RCA, or load coding skills here.
- Never narrate beyond the single output block.
