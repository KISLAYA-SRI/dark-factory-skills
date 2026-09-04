---
name: developer-notes-protocol
description: Use when extracting and enforcing Developer Notes from a Jira user story before any analysis begins. Developer Notes are sacred law and override all other sources. Triggers include developer notes, dev notes, DN extraction, implementation notes, tech notes, or notes for developer.
---

# Developer Notes Protocol — SACRED LAW

## Purpose

Developer Notes are the **single highest-priority input** in the entire analysis pipeline. They represent direct, authoritative instructions from the developer who owns the feature. Every word must be followed exactly — without interpretation, override, or exception.

---

## Step 0 — Mandatory Pre-Analysis: Extract All Developer Notes First

Before reading Figma context, Sitecore API specs, BFF API specs, or any other source, you MUST:

1. Scan the Jira user story for any Developer Notes / Dev Notes section.
2. Extract every instruction verbatim and number them: `DN-001`, `DN-002`, `DN-003` …
3. Record them in a working list that is kept active throughout the entire analysis.
4. For EVERY analysis decision made, check: "Does a Dev Note cover this topic?"
   - If YES → The Dev Note answer IS the answer. Do not produce an alternative.
   - If NO → Proceed with normal source priority order.

This step is **non-negotiable**. If Developer Notes are not extracted first, the analysis is invalid.

---

## How to Identify Developer Notes

Look for any of the following headings (case-insensitive) inside the Jira user story:

- "Developer Notes"
- "Dev Notes"
- "Developer Note"
- "Dev Note"
- "Notes for Developer"
- "Implementation Notes"
- "Tech Notes"

If ANY such section exists, treat its entire content as SACRED LAW.

---

## Rules for Applying Developer Notes

1. **READ FIRST** — Developer Notes must be read BEFORE reading Figma context, Sitecore API specs, BFF API specs, or any other source. They set the frame for everything else.

2. **OVERRIDE AUTHORITY** — Developer Notes override:
   - Figma context (visual design decisions, component choices)
   - responsive_design_intent.json (responsive behaviour)
   - Any other guideline, rule, or convention
     If Developer Notes say to do X, do X — even if every other source says Y.

3. **NO INTERPRETATION** — Apply Developer Notes literally. Do not paraphrase, interpret, or "improve" on the developer's instructions. If a note says "use ComponentX", use ComponentX — do not substitute a similar component.

4. **NO OMISSION** — Every instruction in Developer Notes must be applied. Do not skip any note because it seems minor, redundant, or already covered by another source.

5. **NO OVERRIDE BY AGENT** — The agent MUST NOT produce a conflicting recommendation, an alternative suggestion, or a "better approach" for any topic already covered by a Developer Note. The Developer Note is the final, authoritative answer. Framing an override as a "suggestion" or "recommendation" is equally prohibited.

6. **CONFLICT RESOLUTION** — If Developer Notes conflict with Figma or other sources:
   - Follow Developer Notes.
   - Record the conflict and resolution in the Gaps Section of the output document.
   - Do NOT silently override Developer Notes in favour of other sources.

7. **PARTIAL NOTES** — If Developer Notes only address part of the implementation, apply Developer Notes for what they cover and use the normal source priority order for everything else.

8. **AMBIGUOUS NOTES** — If a Developer Note is ambiguous or unclear, apply the most literal interpretation possible. Record the ambiguity and your interpretation in the Gaps Section. Do NOT silently guess.

9. **TRACEABILITY** — Every analysis output item influenced by a Developer Note MUST reference the Dev Note ID (e.g., "Per DN-002") so reviewers can trace the decision back to the source.

---

## Source Priority Order (When No Dev Note Covers a Topic)

```
Dev Notes → Project Guidelines → Figma → React/Frontend Best Practices
```

---

## Required Output: Developer Notes Applied Table

Section 1 of the output document MUST always be the Developer Notes Applied table — even if no notes were found. This section must appear before all other analysis sections.

```markdown
## 1. Developer Notes Applied

| DN ID  | Developer Note (verbatim) | How It Was Applied   | Sections Affected | Files / Components Affected |
| ------ | ------------------------- | -------------------- | ----------------- | --------------------------- |
| DN-001 | [exact note text]         | [exact action taken] | [section numbers] | [file paths]                |
```

If no Developer Notes were found in the user story, write:

```markdown
## 1. Developer Notes Applied

No Developer Notes / Dev Notes section found in the user story. Normal source priority order applied.
```

---

## Post-Analysis Self-Check (Mandatory Before Finalising Output)

After completing all analysis sections, the agent MUST verify:

- [ ] Every DN-xxx item from the extracted list appears in the "Developer Notes Applied" table.
- [ ] No analysis section contains a recommendation that contradicts a Dev Note.
- [ ] Every analysis item influenced by a Dev Note is labelled with the DN ID.

If any check fails, the agent MUST correct the output before producing the final document.

---

## Agent Self-Enforcement Rule

> ⚠️ The agent MUST NOT produce its own analysis, alternative suggestion, or "better recommendation" for any topic that is already addressed by a Developer Note. The Developer Note IS the final answer for that topic. Producing a conflicting or overriding recommendation — even if framed as a suggestion — is a **critical failure**.
