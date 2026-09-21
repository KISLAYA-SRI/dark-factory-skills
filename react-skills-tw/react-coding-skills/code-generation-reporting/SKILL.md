---
name: code-generation-reporting
description: Use to produce the SINGLE consolidated code-generation summary document covering UI, Storybook, Logic, and Tests in one file. Replaces the four legacy per-agent documents. Triggers include code generation summary, consolidated report, final document, or write the summary.
disable-model-invocation: true
---

## Code Generation Reporting

### Purpose

Generate **ONE** consolidated summary of everything the Coding Agent produced — UI, Storybook, Logic/Sitecore/State, and Tests. This replaces the legacy `CODE_GENERATION.md` + `TEST_GENERATION.md` + Storybook handoff with a single file.

**File path:** `.SS_WF/Agent/CODE/{{ticket_id}}_CODE_GENERATION_SUMMARY.md`

⚠️ This is the **only** document the Coding Agent produces. Source files, stories and tests are implementation artefacts, not reports.

---

## ⚠️ HOW TO WRITE IT

**This skill defines WHAT the summary must contain. You decide HOW to write it using your available file-writing tool.**

Write the summary **completely, in a single write operation**, using the template below.

### If a single write fails or is rejected for size

1. Write the document with the leading sections first, creating the file.
2. To add the remaining sections: **read the file's current content, concatenate the new sections onto it, and write the complete combined content back.** Repeat until all 13 sections are present.
3. Choose your own split points. Keep sections whole — never split mid-section or mid-table.
4. Always write sections in ascending order, so the final file reads 1 → 13.

⚠️ **Do not assume an append mode exists.** If your write tool only creates or overwrites files, the read-concatenate-rewrite sequence above is the correct way to grow a document.

### Non-negotiable outcomes

| Outcome | Requirement |
| --- | --- |
| **Single file** | Exactly one document produced |
| **Completeness** | All 13 sections present and populated with story-specific detail |
| **Order** | Sections in ascending numerical order, 1 → 13 |
| **Integrity** | No duplicated, truncated, or orphaned sections; no partial tables |
| **No loss** | If rewriting to add sections, preserve all previously written content verbatim |

### Efficiency rules

- **Reuse computed content.** If a write fails, reuse what you already generated — never re-run the build.
- **Do not re-read a file you just wrote** to confirm success — rely on the tool's result.
- **Never restart the build** because of a write failure.
- **Do not use shell commands** (`cat`, `cp`, `sed`, `head`, `tail`, temp-file merges) to assemble or repair the document.
- **If content must be reduced to fit**, condense tables to their essential rows rather than dropping a section. Note the reduction inline as `[Condensed: Section X]`.

---

## Consolidated Summary Template (13 Sections)

```markdown
# Code Generation Summary — {{ticket_id}}

---

## 1. Developer Notes Applied

| DN ID | Instruction | Files Affected | How Applied | Status |
| ----- | ----------- | -------------- | ----------- | ------ |
| DN-001 |            |                |             | Implemented / Not Applicable / Blocked |

> Every DN must resolve to Implemented (with file evidence), Not Applicable (with reason),
> or Blocked (by a named unavailable dependency). "Considered" is not evidence.
> If none: "No Developer Notes. Normal priority order applied."

---

## 2. Story & Classification Summary

- **Classification:** Presentational | Transactional | Hybrid
- **Component(s) built:** [names]
- **Execution path:** lean | full
- **Scope explicitly NOT implemented:** [from plan §8 Things NOT to Implement]

---

## 3. UI Components Generated

| Component | Owner | Reuse Decision | File Path |
| --------- | ----- | -------------- | --------- |
|           | DS / CMS / Feature / Shared | reuse / enhance / new | |

---

## 4. Responsive / RTL / Accessibility Implementation

- **Breakpoint strategy:** [mobile-first approach applied]
- **Grid usage:** [columns={12} responsive / columns={4} mobile-only]
- **Token mapping:** [Figma values → project tokens]
- **New tokens created:** [list, or: None] ⚠️ mandatory if any primitive was added
- **RTL handling:** [logical properties, mirrored directional elements]
- **Accessibility:** [roles, labels, keyboard support]
- **NFR exceptions applied:** [from plan §13.2, or: None]
- **Token/design discrepancies:** [recorded, or: None]

---

## 5. Media Integration

[Assets handled + optimisation applied, or: "Not Applicable — no media in this story"]

---

## 6. Sitecore Rendering Integration

[Field contracts, rendering entry, registry key, placeholders, registry build commands run,
 or: "Not Applicable — no CMS-mapped components"]

---

## 7. Logic & API Integration

[Types, constants/query keys, mapper, service, hook, container.
 States orchestrated: loading / error / empty / partial / success.
 Data fetching config applied (staleTime/gcTime/retry).
 or: "Not Applicable — Presentational component"]

---

## 8. State & Form Management

[State homes (server / local / shared), stores created with justification,
 forms and validation utilities, or: "Not Applicable"]

---

## 9. Storybook & Catalogue Updates

| Component | Story File | JSDoc Added | Catalogue Action |
| --------- | ---------- | ----------- | ---------------- |
|           |            | Yes / No    | new / enhanced / unchanged |

> Catalogue path: ./src/component-catalogue.json

---

## 10. Test Generation Summary

| Source File | Classification | Test File | Strategy | Branch Coverage |
| ----------- | -------------- | --------- | -------- | --------------- |
|             | Presentational / Transactional / Hybrid | | | |

- **Overall coverage:** NN% — **targeted** | **measured**
- ⚠️ State "measured" only if a coverage command was actually executed. Otherwise "targeted".
- **Files excluded from testing:** [barrels, type-only, stories, configs, primitive constants]

---

## 11. Acceptance Criteria Evidence

| AC ID | Implemented In (files) | Verified By (tests) |
| ----- | ---------------------- | ------------------- |
| AC-001 |                       |                     |

---

## 12. Self-Validation Result

| Checklist Item | Status | Evidence (file) |
| -------------- | ------ | --------------- |
| DN-001         | Covered / Not Applicable | |
| AC-001         | Covered / Not Applicable | |

> Every CODING_AGENT_CHECKLIST.md item must appear with concrete evidence.

---

## 13. Deviations & Assumptions Made

- **Conflicts resolved:** [with the priority order applied]
- **Assumptions made:** [due to missing detail]
- **Upstream contract gaps encountered:** [e.g. plan §10 empty, or a prop marked
  "Unknown — source contract not provided" that remained prop-driven]
- **New design tokens created:** [name + value + why no existing token matched]
- **Token/design discrepancies:** [recorded during UI generation]
- **Scope deviations:** [any departure from the ordered plan, with reason]

> Write "None" if there were no deviations.
```

---

## Content Rules

- Populate every section with **story-specific** detail — real file paths, real component names. No boilerplate.
- **Presentational runs:** mark Sections 6, 7 and 8 as `Not Applicable` (and Section 5 if no media).
- Pull all content from the in-memory manifest and each skill's outputs — do **not** re-open source files.
- Keep it a summary — reference file paths, do not paste source code.
- **Gapped props:** if a prop was marked `Unknown — source contract not provided` in the plan, confirm in Section 13 that it remained prop-driven with no hardcoded substitute.
- **New tokens:** every primitive or semantic token created during UI generation must appear in Sections 4 and 13.
- Preserve DN IDs exactly as numbered by the Analysis Agent — never renumber.
- Record every conflict resolution with the priority order applied.

---

### Gate: Complete When

```text
- [ ] Exactly one summary file written at .SS_WF/Agent/CODE/{{ticket_id}}_CODE_GENERATION_SUMMARY.md
- [ ] All 13 sections present, in ascending order, populated with story-specific detail
- [ ] No duplicated, truncated, or orphaned sections; no partial tables
- [ ] Presentational runs mark Sections 6–8 (and 5 if no media) as Not Applicable
- [ ] Every DN resolved to Implemented / Not Applicable / Blocked with evidence
- [ ] New design tokens recorded in Sections 4 and 13
- [ ] Coverage labelled "targeted" or "measured" — never claimed without a run
- [ ] AC Evidence and Self-Validation tables reference real files and tests
- [ ] Section 13 records every deviation, or states "None"
```

### Never Do

- Never produce more than one document.
- Never emit `CODE_GENERATION.md`, `TEST_GENERATION.md`, or a separate Storybook doc.
- **Never assume an append mode exists** — read, concatenate, write the complete content back.
- **Never lose previously written content** when rewriting to add sections.
- **Never split a section or table across two writes.**
- **Never write sections out of ascending order.**
- **Never restart the build** to regenerate the summary — reuse already-computed content.
- **Never use shell commands** to assemble or repair the document.
- Never re-read a file you just wrote merely to confirm the write succeeded.
- Never paste full source code into the summary.
- Never leave a section empty — use "Not Applicable" or "None".
- Never claim measured coverage without an actual test run.
- Never renumber DN, AC, INT or STATE IDs.
