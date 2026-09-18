---
name: code-generation-reporting
description: Use to produce the SINGLE consolidated code-generation summary document covering UI, Storybook, Logic, and Tests in one file — written with the Chunked Write Protocol (write first chunk, append the rest) to conserve tokens. Replaces the four legacy per-agent documents. Triggers include code generation summary, consolidated report, final document, or write the summary.
disable-model-invocation: true
---

## Code Generation Reporting

### Purpose

Generate ONE consolidated summary of everything the Coding Agent produced — UI, Storybook, Logic/Sitecore/State, and Tests. No multiple documents. This replaces the legacy `CODE_GENERATION.md` + `TEST_GENERATION.md` + Storybook handoff with a single file.

**File path:** `.SS_WF/Agent/Coding/{{ticket_id}}_CODE_GENERATION_SUMMARY.md`

### Chunked Write Protocol (Mandatory — Token/Cost Optimisation)

Follow the same chunked approach as the Analysis Orchestrator:

```text
- Write 2–3 sections per write_file call.
- Chunk 1 uses WRITE (create) mode.
- Every subsequent chunk uses APPEND mode.
- Max 2-retry guard per chunk. If a chunk fails twice → write a condensed version of that chunk and continue.
- NEVER write the whole document in one call.
- NEVER restart the build to regenerate the summary — only re-attempt the failed chunk.
```

Suggested chunking:

```text
Chunk 1 (write) : Sections 1–3   (Dev Notes, Story/Classification, UI Components)
Chunk 2 (append): Sections 4–6   (Responsive/RTL/A11y, Media, Sitecore)
Chunk 3 (append): Sections 7–9   (Logic/API, State/Forms, Storybook/Catalogue)
Chunk 4 (append): Sections 10–13 (Tests, AC Evidence, Self-Validation, Deviations)
```

### Consolidated Summary Template (13 Sections)

```markdown
# Code Generation Summary — {{ticket_id}}

## 1. Developer Notes Applied
| DN ID | Instruction | Files Affected | How Applied |

## 2. Story & Classification Summary
- Classification: Presentational | Transactional | Hybrid
- Component(s): …
- Scope built / Scope explicitly NOT implemented (from plan Section 11)

## 3. UI Components Generated
| Component | Owner (DS/CMS/Feature/Shared) | Reuse (reuse/enhance/new) | File Path |

## 4. Responsive / RTL / Accessibility Implementation
- Breakpoint strategy, token mapping, RTL handling, a11y roles/keyboard
- Token/source discrepancies recorded

## 5. Media Integration
- Assets handled + optimization; or "Not Applicable"

## 6. Sitecore Rendering Integration
- Field contracts, rendering entry, registry, placeholders; or "Not Applicable"

## 7. Logic & API Integration
- Types, constants/query keys, mapper, service, hook, container
- States orchestrated (loading/error/empty/partial); or "Not Applicable — Presentational"

## 8. State & Form Management
- State homes, stores, forms/validation; or "Not Applicable"

## 9. Storybook & Catalogue Updates
| Component | Story File | Catalogue Action (new/enhanced) |

## 10. Test Generation Summary
| Source File | Test File | Strategy | Branch/Coverage (intended %) |
- Overall intended coverage: NN% (state measured only if a run occurred)

## 11. Acceptance Criteria Evidence
| AC ID | Implemented In (files) | Verified By (tests) |

## 12. Self-Validation Result
| Checklist Item | Status (Covered/NA) | Evidence (file) |

## 13. Deviations & Assumptions Made
- Conflicts resolved (with priority order applied)
- Assumptions due to missing detail
- Token/design discrepancies
- (Write "None" if empty)
```

### Content Rules

- Populate every section with **story-specific** detail (real file paths, real component names) — no boilerplate.
- **Presentational runs:** mark Sections 6, 7, 8 as `Not Applicable` (and Section 5 if no media).
- Pull all content from the in-memory manifest + each skill's outputs; do not re-open source files.
- Keep it a summary — link file paths, do not paste full source code.
- This is the ONLY document produced. Do not emit `CODE_GENERATION.md`, `TEST_GENERATION.md`, or a separate Storybook doc.

### Gate: Complete When

```text
- [ ] Single file written via chunked write/append (chunk 1 write, rest append).
- [ ] All 13 sections present and populated with story-specific detail.
- [ ] Presentational runs mark Sections 6–8 (and 5 if no media) as Not Applicable.
- [ ] AC Evidence and Self-Validation tables reference real files/tests.
- [ ] Saved to .SS_WF/Agent/Coding/{{ticket_id}}_CODE_GENERATION_SUMMARY.md.
```

### Never Do

- Never produce more than one document.
- Never write the summary in a single write_file call.
- Never restart the whole build to regenerate the summary — re-attempt only the failed chunk.
- Never paste full source code into the summary.
- Never leave a section empty — use "Not Applicable" or "None".
