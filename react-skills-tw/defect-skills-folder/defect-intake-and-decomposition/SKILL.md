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

## ⚠️ TICKET CONTENT VARIES — PARSE EVERY SHAPE

A defect ticket may contain **one** defect or **several**. The developer may have enumerated them, or described them in prose. Both must be handled.

### Shape A — Enumerated

```text
1. Carousel arrows do not mirror in Arabic
2. Policy number shows blank on the card
3. Empty state message is hardcoded English
```

Each numbered item is a candidate issue. **Still verify** each is genuinely single — a numbered item can contain two problems.

### Shape B — Unstructured Prose

```text
On the policy page the carousel arrows point the wrong way in Arabic and
the policy number is blank for some records. Also when there are no
policies the message appears in English even on the Arabic site.
```

⚠️ **The split is semantic, not list-parsing.** This paragraph contains **three** issues with three root causes in three files. Read for *distinct failing behaviours*, not punctuation.

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

⚠️ **When uncertain, split.** Two issues that share a root cause merge naturally at RCA. One issue hiding two root causes produces a partial fix that reopens.

---

## Issue ID Assignment

Stable, sequential IDs: `ISSUE-001`, `ISSUE-002` … These thread through **RCA → fix → test runs → §13 Change Log entry**. **Never renumber**, even if an issue is later blocked or found to be a duplicate.

---

## ⚠️ Defect Dev Notes Extraction

Scan the ticket for developer instructions on **how** to fix:

```text
"Developer Notes" · "Dev Notes" · "Developer Note" · "Dev Note"
"Notes for Developer" · "Implementation Notes" · "Tech Notes"
"Fix Notes" · "How to Fix"
```

Extract **verbatim** and number as `DDN-001`, `DDN-002` …

⚠️ **Use the `DDN-` prefix, never `DN-`.** Story Dev Notes keep the `DN-` chain.

**Defect Dev Notes are TOP priority** — above story Dev Notes, the Analysis Plan, and every guideline. Apply the full `developer-notes-protocol` sacred-law rules. Associate each DDN with specific issues, or mark it global.

---

## Issue Categorisation

Each issue gets exactly **one primary category**. It determines which coding skills load in Phase 4 **and** which artefact may be refetched in Phase 2.

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
"blank" / "wrong value" / "not updating"     → BFF/API  (§7 Data Flow Trace)
"authored text not showing"                   → Sitecore (§5 field→prop)
"wrong thing shows when [state]"              → State    (§8 State Matrix)
"looks wrong in Arabic"                       → RTL
"broken on mobile" / "at 390px"               → Responsive
"used to work"                                → Regression  (§13 Change Log)
"doesn't match the design"                    → UI  (+ check for design-change signal)
```

⚠️ A genuinely two-layer problem is usually **two issues** — re-check the splitting test.

---

## ⚠️ SOURCE-CHANGE SIGNAL DETECTION

An external source may have changed **after** code generation. Phase 2 uses these flags as **Gate Condition 2** for a selective refetch.

⚠️ **Flag the signal; do not judge it.** Phase 2 decides whether to refetch. Phase 3 decides the fault origin.

### Design-Change Signals (→ Figma)

```text
Phrases:  "design updated" · "new Figma" · "per latest design" · "design changed"
          "as per updated design" · "matches new mockup" · "redesign"
Signals:  A Figma URL in the DEFECT ticket · "should now be…" phrasing
```

### Contract-Change Signals (→ Sitecore / BFF)

```text
Sitecore: "field renamed" · "new field added" · "rendering updated"
          "placeholder changed" · authored content that does not render at all
BFF:      "API changed" · "response updated" · "new field in response"
          "contract changed" · a value that previously rendered and now does not
```

### Developer-Change Signals (→ recorded for RCA)

```text
"after the dev fix" · "since the last change" · "worked in the generated version"
"we modified" · a reference to a PR or commit
```

⚠️ These do not trigger a refetch. They tell RCA to look closely at **post-generation manual changes** — a distinct fault origin.

⚠️ **Absence of a signal is meaningful.** A UI defect with no design-change signal is a genuine visual defect and must not trigger a Figma refetch.

---

## Reproduction Evidence Capture

Missing evidence is recorded as missing — **never invented**.

```text
ISSUE-00N
  Summary:         [one line — the failing behaviour]
  Category:        [primary category]
  Steps:           [reproduction steps, or: Not provided]
  Expected:        [what should happen — from the ticket or the AC]
  Actual:          [what happens instead]
  Environment:     [browser / device / viewport, or: Not provided]
  Locale:          [en / ar, or: Not specified]   ← critical for RTL
  Persona/Role:    [if relevant, or: Not specified]
  Attachments:     [screenshots, recordings, logs referenced]
  Related AC:      [AC-xxx if named, else: To be determined in RCA]
  Applicable DDN:  [DDN-xxx, or: None]
  Source-change:   [FIGMA | SITECORE | BFF | NONE]
  Developer-change signal: [quoted text, or: None]
```

⚠️ **Reproduction conditions become test conditions.** Locale, persona, viewport and data shape recorded here are what the Phase 4 regression test must set up. Record them precisely.

---

## Output — ISSUE_REGISTER

Hold in memory and report inline. **This skill writes no files.**

```text
DEFECT INTAKE — {{ticket_id}}
Parent story: {{parent_story_id}}

Defect Dev Notes:
  DDN-001  [verbatim text]  → applies to: ISSUE-002 | all issues

Issues identified: N
ISSUE-001  [RTL]       [summary]   source-change: NONE
ISSUE-002  [Sitecore]  [summary]   source-change: SITECORE
ISSUE-003  [UI]        [summary]   source-change: FIGMA

[full evidence block per issue]

Split rationale:
  "[original sentence]" → ISSUE-001 + ISSUE-003 — different root cause and layer

Refetch candidates for Phase 2:
  ISSUE-002 → Sitecore · ISSUE-003 → Figma
```

---

### Gate: Phase 1 Complete When

```text
- [ ] Defect ticket read; parent story ID identified
- [ ] Every distinct failing behaviour is its own ISSUE-xxx
- [ ] Splitting test applied semantically; rationale recorded where non-obvious
- [ ] Stable IDs assigned; none will be renumbered
- [ ] DDN extracted verbatim (never DN-); associated or marked global
- [ ] Every issue has one primary category
- [ ] Source-change and developer-change signals recorded per issue
- [ ] Reproduction evidence captured; missing items marked "Not provided"
- [ ] ISSUE_REGISTER reported inline; no files written
```

### Never Do

- Never read or re-analyse the parent story JIRA ticket.
- Never re-triage — the developer already decided this is a defect to fix.
- Never merge distinct root causes, or split one root cause into several issues.
- Never invent reproduction steps, environment, or locale.
- Never use the `DN-` prefix for defect notes.
- Never renumber issue IDs.
- Never assume a source changed without an explicit signal.
- Never decide fault origin, trigger a refetch, begin RCA, or load coding skills here.
- Never write any file.
