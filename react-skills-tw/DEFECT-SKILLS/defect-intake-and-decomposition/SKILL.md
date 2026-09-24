---
name: defect-intake-and-decomposition
description: Use as Phase 1 of the FE Defect Fix workflow to parse a JIRA defect ticket, split it into discrete independently-fixable issues, extract Defect Dev Notes, categorise each issue, detect source-change signals, and capture reproduction evidence. Handles both enumerated lists and unstructured prose describing multiple problems. Triggers include defect intake, parse defect, split defect issues, or decompose defect.
disable-model-invocation: true
---

## Defect Intake and Decomposition

### Purpose

This skill is **Phase 1** of the FE Defect Fix Agent. It converts a defect ticket — whatever shape it arrives in — into a structured, stable set of independently-fixable issues that thread through the rest of the workflow.

⚠️ **Triage has already happened.** The developer decided this is a defect worth fixing. This skill does **not** re-litigate whether it is a defect — it decomposes, categorises, and flags source-change signals so the fix can proceed.

---

### Input

| Input | Source | Required? |
| --- | --- | --- |
| Defect ticket | `.SS_WF/{{ticket_id}}_JIRA_OUTPUT_.json` | **Mandatory** |

If the ticket is missing or unreadable → **HALT**. Report clearly. Do not proceed.

⚠️ **The parent story JIRA ticket is NOT read here.** Everything needed from the original story lives in the Analysis Plan and Code Generation Summary, loaded in Phase 2.

---

## ⚠️ TICKET CONTENT VARIES — PARSE BOTH SHAPES

A defect ticket may contain **one** defect or **several**. The developer may have enumerated them, or described them in prose. Both must be handled.

### Shape A — Enumerated

```text
1. Carousel arrows do not mirror in Arabic
2. Policy number shows blank on the card
3. Empty state message is hardcoded English
```

Straightforward: each numbered item is a candidate issue. **Still verify** each is genuinely single — a numbered item can itself contain two problems.

### Shape B — Unstructured Prose

```text
On the policy page the carousel arrows point the wrong way in Arabic and
the policy number is blank for some records. Also when there are no
policies the message appears in English even on the Arabic site.
```

⚠️ **The split is semantic, not list-parsing.** This paragraph contains **three** distinct issues with three different root causes in three different files. Read for *distinct failing behaviours*, not punctuation.

### Shape C — Mixed

Enumerated items where one entry buries a second problem in its description. Split it.

---

## The Splitting Test

Two symptoms are **separate issues** if any of these differ:

```text
✅ Different root cause          → separate
✅ Different file / layer        → separate
✅ Different category            → separate
✅ Fixable independently         → separate
```

They are **one issue** if:

```text
❌ Same root cause, multiple visible symptoms
   e.g. "title and subtitle both blank" caused by one missing mapper field
```

⚠️ **When uncertain, split.** Two issues that turn out to share a root cause merge naturally at RCA. One issue hiding two root causes produces a partial fix that reopens.

---

## Issue ID Assignment

Assign stable, sequential IDs: `ISSUE-001`, `ISSUE-002`, `ISSUE-003` …

These thread through **RCA → fix → test → §13 Change Log entry**. **Never renumber** them, even if an issue is later found to be blocked or a duplicate.

---

## ⚠️ Defect Dev Notes Extraction

Scan the ticket for developer instructions on **how** to fix:

```text
"Developer Notes" · "Dev Notes" · "Developer Note" · "Dev Note"
"Notes for Developer" · "Implementation Notes" · "Tech Notes"
"Fix Notes" · "How to Fix"
```

Extract **verbatim** and number as `DDN-001`, `DDN-002` …

⚠️ **Use the `DDN-` prefix, never `DN-`.** Story Dev Notes from the Analysis Plan keep the `DN-` chain. Two separate chains keep both traceable.

**Defect Dev Notes are TOP priority** — above story Dev Notes, the Analysis Plan, and every guideline. Apply the full `developer-notes-protocol` sacred-law rules.

Where a DDN clearly applies to a specific issue, associate it. Where it applies globally, mark it as applying to all issues.

---

## Issue Categorisation

Each issue gets exactly **one primary category**. This determines which coding skills load in Phase 4 **and** which artefact may be refetched in Phase 2.

| Category | Symptom pattern | Skills (Phase 4) | Refetch (Phase 2) |
| --- | --- | --- | --- |
| **UI / Visual** | Wrong layout, spacing, colour, variant, token | `presentational-ui-generation` | Figma |
| **RTL** | Wrong direction, unmirrored/over-mirrored icon, clipped Arabic | `presentational-ui-generation` | Figma |
| **Responsive** | Breaks at a breakpoint, wrong grid, overflow | `presentational-ui-generation` | Figma |
| **Accessibility** | Missing label, keyboard trap, wrong role, focus loss | `presentational-ui-generation` | None |
| **Media** | Image not loading, wrong size, layout shift, missing alt | `+ frontend-media-integration` | Figma |
| **Sitecore** | Authored content missing/wrong, placeholder empty, registry miss | `sitecore-rendering-integration` | Sitecore |
| **BFF / API** | Wrong/blank value, request wrong, error not handled | `frontend-logic-integration` | BFF |
| **State** | Wrong state renders, stale data, form misbehaviour | `+ frontend-state-and-form-management` | None |
| **Missing AC** | Requirement never implemented | depends on layer | None |
| **Regression** | Previously worked, broken by a later change | depends on layer | None |

### Categorisation Hints

```text
"blank" / "wrong value" / "not updating"     → BFF/API  (check §7 Data Flow Trace)
"authored text not showing"                   → Sitecore (check §5 field→prop)
"wrong thing shows when [state]"              → State    (check §8 State Matrix)
"looks wrong in Arabic"                       → RTL
"broken on mobile" / "at 390px"               → Responsive
"used to work"                                → Regression  (check §13 Change Log)
"doesn't match the design"                    → UI  (+ check for design-change signal)
```

⚠️ If an issue genuinely spans two categories, **assign the primary one** and note the secondary. A genuinely two-layer problem is usually **two issues** — re-check the splitting test.

---

## ⚠️ SOURCE-CHANGE SIGNAL DETECTION

An external source may have changed **after** code generation. When it has, the code is not necessarily wrong — the source moved. Phase 2 uses these flags as **Gate Condition 2** for a selective refetch.

⚠️ **Flag the signal; do not judge it.** Phase 2 decides whether to refetch. Phase 3 decides the fault origin.

### Design-Change Signals (→ Figma)

```text
Explicit phrases:
  "design updated" · "new Figma" · "per latest design" · "design changed"
  "as per updated design" · "matches new mockup" · "redesign"

Structural signals:
  A Figma URL present in the DEFECT ticket
  A design modification date referenced as later than generation
  "should now be…" phrasing implying a new target state
```

### Contract-Change Signals (→ Sitecore / BFF)

```text
Sitecore:
  "field renamed" · "new field added" · "rendering updated"
  "content type changed" · "placeholder changed"
  Authored content that exists in CMS but does not render at all

BFF:
  "API changed" · "response updated" · "new field in response"
  "endpoint updated" · "contract changed"
  A value that previously rendered and now does not
```

### Recording the Signal

```text
ISSUE-001
  Source-change signal:  FIGMA — ticket states "per updated design v2"
                         Figma URL present: yes
  → Phase 2 Gate Condition 2: SATISFIED

ISSUE-002
  Source-change signal:  NONE detected
  → Phase 2 Gate Condition 2: NOT satisfied — use existing on-disk artefact
```

⚠️ **Absence of a signal is a meaningful result.** A UI defect with no design-change signal is a genuine visual defect — the code does not match the design it was built against. That is an **agent miss**, and it must not trigger a Figma refetch.

---

## Reproduction Evidence Capture

For each issue, capture whatever the ticket provides. Missing evidence is recorded as missing — **never invented**.

```text
ISSUE-00N
  Summary:         [one line — the failing behaviour]
  Category:        [primary category]
  Steps:           [reproduction steps, or: Not provided]
  Expected:        [what should happen — from the ticket or the AC]
  Actual:          [what happens instead]
  Environment:     [browser / device / viewport, or: Not provided]
  Locale:          [en / ar, or: Not specified]   ← critical for RTL issues
  Persona/Role:    [if relevant, or: Not specified]
  Attachments:     [screenshots, recordings, logs referenced in the ticket]
  Related AC:      [AC-xxx if the ticket names one, else: To be determined in RCA]
  Applicable DDN:  [DDN-xxx, or: None]
  Source-change:   [FIGMA | SITECORE | BFF | NONE]  ← drives Phase 2 refetch gate
```

⚠️ **Locale matters disproportionately.** An RTL issue with no stated locale is ambiguous — record `Not specified` so RCA can flag it rather than assuming `ar`.

---

## Output — ISSUE_REGISTER

Hold in memory and report inline. **This skill writes no files.**

```text
DEFECT INTAKE — {{ticket_id}}

Parent story: {{parent_story_id}}

Defect Dev Notes:
  DDN-001  [verbatim text]  → applies to: ISSUE-002 | all issues
  (or: No Defect Dev Notes found)

Issues identified: N

ISSUE-001  [RTL]       [one-line summary]   source-change: NONE
ISSUE-002  [Sitecore]  [one-line summary]   source-change: SITECORE
ISSUE-003  [UI]        [one-line summary]   source-change: FIGMA

[full evidence block per issue]

Split rationale (where prose was decomposed):
  "[original sentence]" → ISSUE-001 + ISSUE-003
    different root cause and layer

Refetch candidates for Phase 2:
  ISSUE-002 → Sitecore   (contract-change signal present)
  ISSUE-003 → Figma      (design-change signal present)
```

The split rationale matters — it lets the reviewing developer confirm the decomposition was correct.

---

### Gate: Phase 1 Complete When

```text
- [ ] Defect ticket read from .SS_WF/{{ticket_id}}_JIRA_OUTPUT_.json
- [ ] Parent story ID identified
- [ ] Every distinct failing behaviour is its own ISSUE-xxx
- [ ] Splitting test applied — prose decomposed semantically, not by punctuation
- [ ] Split rationale recorded where decomposition was non-obvious
- [ ] Stable sequential IDs assigned; none will be renumbered
- [ ] Defect Dev Notes extracted verbatim as DDN-xxx (never DN-xxx)
- [ ] DDN associated with specific issues or marked global
- [ ] Every issue has exactly one primary category
- [ ] Source-change signal recorded per issue (FIGMA / SITECORE / BFF / NONE)
- [ ] Refetch candidates listed for Phase 2
- [ ] Reproduction evidence captured; missing items marked "Not provided"
- [ ] Locale recorded (critical for RTL issues)
- [ ] ISSUE_REGISTER reported inline
- [ ] No files written
```

### Never Do

- **Never read or re-analyse the parent story JIRA ticket** — the Analysis Plan carries it.
- **Never re-triage** — the developer already decided this is a defect to fix.
- **Never merge distinct root causes into one issue** to reduce the count.
- **Never split a single root cause into multiple issues** because it has several visible symptoms.
- **Never invent reproduction steps, environment, or locale** — mark them "Not provided".
- **Never use the `DN-` prefix for defect notes** — always `DDN-`.
- **Never renumber issue IDs** once assigned.
- **Never assume a source changed** without an explicit signal in the ticket.
- **Never decide the fault origin here** — that is Phase 3.
- **Never trigger a refetch here** — flag the signal; Phase 2 decides.
- **Never begin root cause analysis here** — that is Phase 3.
- **Never load coding skills here** — categorisation only determines what Phase 4 will load.
- Never write any file.
