---
name: developer-notes-protocol
description: Use to extract, activate and trace Developer Notes consistently during story analysis or React code generation. Developer Notes are sacred law and override all other sources. Triggers include developer notes, dev notes, DN extraction, implementation notes, tech notes, or notes for developer.
---

## Developer Notes Protocol — SACRED LAW

### Purpose

Developer Notes are the **single highest-priority input** in the entire pipeline. They represent direct, authoritative instructions from the developer who owns the feature. Every word must be followed exactly — without interpretation, override, or exception.

### Dual Mode — One Skill, Two Consumers

This skill is shared. Do **not** create a coding-specific duplicate.

| Mode | Invoked By | Responsibility |
| --- | --- | --- |
| **Extraction** | Analysis Agent — **Phase 1** | Scan the JIRA story, extract notes verbatim, assign `DN-001`, `DN-002` …, keep the list active through Phases 2–9 |
| **Enforcement** | Coding Orchestrator — **Phase 2** | Consume the numbered DN table from ANALYSIS_PLAN.md Section 1, apply each note as the highest-priority constraint during generation, and attach file-level evidence |

**Preserve IDs across modes.** A note numbered `DN-002` during analysis remains `DN-002` for the whole life of the story — through code generation and into the final summary. Never renumber.

---

### ⚠️ ANALYSIS DEPTH vs OUTPUT WIDTH

Perform **every** step below in full. What is trimmed is only what gets written into ANALYSIS_PLAN.md.

| Work Performed (always, in full) | Where It Is Emitted |
| --- | --- |
| Scan story for all DN heading variants | Internal |
| Extract every note verbatim, assign stable IDs | **ANALYSIS_PLAN.md §1** |
| Map each note to affected decisions / components / files | **ANALYSIS_PLAN.md §1** |
| Check every analysis decision against the active DN list | Internal — governs all other sections |
| Detect and resolve DN-vs-source conflicts | **DEV_REVIEW.md §3** |
| Record ambiguity and the literal interpretation chosen | **DEV_REVIEW.md §4** |
| Post-analysis traceability self-check | Internal gate |

⚠️ Never write a conflict, ambiguity note, or confidence rating into ANALYSIS_PLAN.md. §1 states **what the note is and where it was applied** — nothing else.

---

### Extraction Mode — Analysis Agent Phase 1

This is the **first phase of the entire workflow**. It runs **before Context Gathering (Phase 2)** — Developer Notes may govern which endpoints are used, which components are built, and how design is interpreted, so they must be active before anything is fetched.

Before reading Figma context, Sitecore API specs, BFF API specs, or any other source:

- Scan the JIRA user story for any Developer Notes / Dev Notes section.
- Extract every instruction verbatim and number them: DN-001, DN-002, DN-003 …
- Record them in a working list kept active throughout the entire analysis.
- For EVERY decision made in Phases 2–9, check: "Does a Dev Note cover this topic?"
  - If YES → The Dev Note answer IS the answer. Do not produce an alternative.
  - If NO → Proceed with normal source priority order.

This step is **non-negotiable**. If Developer Notes are not extracted first, the analysis is invalid.

### How to Identify Developer Notes

Look for any of the following headings (case-insensitive) inside the JIRA user story:

- "Developer Notes" · "Dev Notes" · "Developer Note" · "Dev Note"
- "Notes for Developer" · "Implementation Notes" · "Tech Notes"

If ANY such section exists, treat its entire content as SACRED LAW.

### Rules for Applying Developer Notes

- **READ FIRST** — Developer Notes must be read BEFORE any context is fetched or any other source is consulted. They set the frame for everything else.
- **OVERRIDE AUTHORITY** — Developer Notes override Figma context, `responsive_design_intent.json`, API contracts, and any other guideline, rule, or convention. If Developer Notes say to do X, do X — even if every other source says Y.
- **NO INTERPRETATION** — Apply literally. If a note says "use ComponentX", use ComponentX — do not substitute a similar component.
- **NO OMISSION** — Every instruction must be applied. Do not skip a note because it seems minor, redundant, or already covered.
- **NO OVERRIDE BY AGENT** — Never produce a conflicting recommendation, alternative suggestion, or "better approach" for a topic already covered by a Developer Note. Framing an override as a "suggestion" is equally prohibited.
- **CONFLICT RESOLUTION** — If Developer Notes conflict with Figma or another source: follow the Developer Note, then record the conflict and resolution in **DEV_REVIEW.md §3 (Conflicts Resolved)**. Never silently override.
- **PARTIAL NOTES** — Apply Developer Notes for what they cover; use normal source priority for everything else.
- **AMBIGUOUS NOTES** — Apply the most literal interpretation possible. Record the ambiguity and your interpretation in **DEV_REVIEW.md §4 (Derived Items and Provenance)**. Never silently guess.
- **TRACEABILITY** — Every output item influenced by a Developer Note MUST reference its ID (e.g., "Per DN-002").

### Source Priority Order (When No Dev Note Covers a Topic)

```text
Dev Notes → Project Guidelines → Figma → React/Frontend Best Practices
```

---

### Required Output: Developer Notes Applied Table

**Section 1 of ANALYSIS_PLAN.md MUST always be this table** — even if no notes were found. It appears before all other sections.

```markdown
## 1. Developer Notes Applied

| DN ID  | Dev Note (verbatim) | Applied Where | Files / Components Affected |
| ------ | ------------------- | ------------- | --------------------------- |
| DN-001 | [exact note text]   | [exact action taken] | [component / file] |
```

If no Developer Notes were found:

```markdown
## 1. Developer Notes Applied

No Developer Notes / Dev Notes section found in the user story. Normal source priority order applied.
```

⚠️ **Column discipline.** Exactly these four columns.
- Do **not** add `Sections Affected` — section numbers are unstable across template revisions and are not actionable for the Coding Agent.
- Do **not** add `Basis`, `Confidence`, or `Impact if Wrong` — those belong to DEV_REVIEW.md.

The `Files / Components Affected` column is the one the Coding Agent uses to pre-identify which generation phases each note governs. Populate it precisely.

---

### Enforcement Mode — Coding Orchestrator Phase 2

When invoked by the Coding Agent, the DN table already exists and is already numbered. Do not re-extract or renumber.

- Load the Developer Notes Applied table from the implementation manifest.
- Use `Files / Components Affected` to map each note to the generation phases it touches.
- For EVERY file generated, check: "Does a DN cover this?" If YES → the DN IS the answer; implement it verbatim.
- Tag each affected output with its DN ID in the final summary (e.g. "Per DN-002").

#### Evidence Requirement

Each DN must resolve to one of:

- **Implemented** — with concrete evidence: generated/updated file, symbol, or configuration.
- **Not Applicable** — with a stated reason.
- **Blocked** — by a genuinely unavailable dependency, explicitly named.

A statement such as "considered" or "reviewed" is **not** evidence. No silent omission is permitted.

---

### Post-Analysis Self-Check (Mandatory Before Finalising Output)

- [ ] Every DN-xxx item from the extracted list appears in the Developer Notes Applied table.
- [ ] No analysis section contains a recommendation that contradicts a Dev Note.
- [ ] Every item influenced by a Dev Note is labelled with its DN ID.
- [ ] Every DN conflict is recorded in DEV_REVIEW.md §3 — not in ANALYSIS_PLAN.md.
- [ ] Every DN ambiguity and chosen interpretation is recorded in DEV_REVIEW.md §4.
- [ ] The §1 table uses exactly the four required columns.
- [ ] `Files / Components Affected` is populated for every note.

If any check fails, correct the output before producing the final document.

### Agent Self-Enforcement Rule

⚠️ The agent MUST NOT produce its own analysis, alternative suggestion, or "better recommendation" for any topic already addressed by a Developer Note. The Developer Note IS the final answer for that topic. Producing a conflicting or overriding recommendation — even framed as a suggestion — is a **critical failure**.
