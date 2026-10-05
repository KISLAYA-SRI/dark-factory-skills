---
name: defect-reporting-and-learning
description: Use as Phase 6 of the FE Defect Fix workflow to update the parent CODE_GENERATION_SUMMARY.md in place — refreshing state sections, reconciling drift, appending a Change Log entry with edge-case and test-execution evidence — and to WRITE an entry into the Coding Agent Learnings file when the fault origin was an agent miss or a regression from a prior fix. Triggers include defect report, update code gen summary, update learnings, or close out defect fix.
disable-model-invocation: true
---

## Defect Reporting and Learning

### Purpose

```text
6a  Update CODE_GENERATION_SUMMARY.md     → always
6b  Write CODING_AGENT_LEARNINGS.md       → ONLY for agent miss / regression
```

⚠️ **Both are file writes, not recommendations.** This phase is not complete until the files on disk have changed.

---

## ⚠️ VARIABLES

```text
Summary:    .SS_WF/Agent/CODE/{{$var[parent_ticket_id]s}}_CODE_GENERATION.md
Learnings:  ./src/.project/learnings/CODING_AGENT_LEARNINGS.md
Defect ID:  {{$var[ticket_id]s}}
```

Never `parent_story_id`.

---

## ⚠️ THE MOST COMMON FAILURE: IDENTIFYING A LEARNING WITHOUT WRITING IT

```text
❌ "This should be added to # UI LEARNINGS: RTL logical properties…"
❌ Printing the proposed entry in the response and moving on
❌ Listing it under "Notes for the developer"
❌ Saying "the learnings file should be updated"

✅ Read the learnings file
✅ Merge the entry into the right namespace
✅ Write the COMPLETE file back
✅ Confirm the write succeeded
```

**Drafting is step one of four.** A learning that exists only in the response is lost the moment the run ends — the coding agent reads the _file_, not the transcript.

⚠️ If you catch yourself describing what the file should contain, **stop and write it**.

---

## PART 6a — UPDATE THE SUMMARY

### State vs historical sections

| §                                     | Nature                       | On defect fix           |
| ------------------------------------- | ---------------------------- | ----------------------- |
| 3 · 4 · 5 · 6 · 7 · 8 · 9 · 10 · 12.4 | **State** — what the code IS | ✅ Update               |
| 11 AC Evidence                        | Mixed                        | ⚠️ Status only          |
| 1 · 2 · 12.1 · 12.2 · 12.5            | **Historical**               | ❌ Never change         |
| **13 Change Log**                     | **Append-only**              | ✅ One entry per defect |

⚠️ A stale §7 or §8 misleads the next defect run and can cause a wrong fault-origin classification.

### Minimal-change applies here too

```text
Update ONLY:
  · rows the fix touched
  · rows RCA inspected and found drifted

❌ Never regenerate the summary · never resync the whole codebase
❌ Never reformat or reword untouched rows
```

Drift found **outside** the rows RCA inspected → record in §13 as _observed, not reconciled_.

### Tags

| Tag                 | Meaning                                                      |
| ------------------- | ------------------------------------------------------------ |
| `[DEF-xxx]`         | Changed by this fix                                          |
| `[DEF-xxx · drift]` | Reconciled to match a developer change found during this fix |

Prefer **symbol + line** over a bare line number, so the location survives future edits.

### §12.4 — mark, never delete

```markdown
| LIM-001 | Expiry badge never renders | GAP-003 | … | Backend | ✅ Resolved [DEF-486] |
```

### §13 entry — the defect record

```markdown
### DEF-486 — 2026-09-29 — Defect Fix

**Reported:** 2 issues · **Fixed:** 2 · **Blocked:** 0
**Verification:** EXECUTED _(or: STATIC ONLY — reason)_

#### Defect Dev Notes

| DDN ID | Instruction | Applied To | Status |
| DDN-001 | Use the Sitecore message | ISSUE-002 | Implemented |

> Supersession: DDN-001 supersedes DN-004. _(or: None)_

#### Context Refetch

| Artefact | Issue | Trigger | Diff Result |
| Sitecore | ISSUE-002 | Field not rendering | `PolicyTitle` → `Title` RENAMED |

> _(or: No artefacts refetched.)_

#### Drift From Summary

| Location | Summary Said | Code Did | Source | Reconciled? |
| `PolicyMapper.ts → mapPolicyResponse()` | null → "—" | null → `legacyNumber ?? ""` | Developer, a1b2c3 (2026-08-21) | ✅ §7 updated |

> _(or: No drift found.)_

#### Issues

| Issue | Category | Status | Root Cause | Fault Origin | Fix |
| ISSUE-001 | RTL | ✅ Fixed | `CarouselPager.tsx → Pager` used `ml-2` | Agent miss | `ml-2` → `ms-2` |
| ISSUE-002 | BFF | ✅ Fixed | Developer fallback returned `""` | Post-generation manual change | `""` → `"—"`, legacy fallback kept |

#### Edge Cases Verified

| Issue | Case | Expected | Result |
| ISSUE-002 | null _(reported)_ | "—" | ✅ |
| ISSUE-002 | undefined / "" / whitespace | "—" | ✅ |
| ISSUE-002 | legacyNumber present _(developer behaviour)_ | legacyNumber | ✅ |
| ISSUE-001 | LTR still correct after RTL fix | left spacing | ✅ |

#### Test Execution

| Run | Verdict | Output |
| ISSUE-002 failing-first | EXPECTED_FAIL | `.SS_WF/Agent/TEST_RUNS/DEF-486-ISSUE-002-failing-first-…/` |
| ISSUE-002 after fix | PASS | `…/DEF-486-ISSUE-002-after-fix-…/` |
| Guards (6) | PASS | `…/DEF-486-ISSUE-002-guards-…/` |
| Blast radius (3 files) | PASS | `…/DEF-486-ISSUE-002-blast-radius-…/` |
| Final consolidated | PASS | `…/DEF-486-final-…/` |

#### Sections Updated

| §3 | 4 rows [DEF-486] |
| §7 | `policyNumber` trace — fix + drift reconciled |
| §10 | +1 regression, +6 guard tests |

#### Existing Tests Modified

| `HeroBanner.test.tsx` | asserted `PolicyTitle` → now `Title` | Test encoded the old contract |

> _(or: None.)_

#### Observations — Not Fixed

| `usePolicyList.ts` | `staleTime` hardcoded | Outside every root cause |

> _(or: None.)_

#### Learnings Written

| Origin | Issues | Written? |
| Agent miss | ISSUE-001 | ✅ `# UI LEARNINGS` — recurrence ×2 |
| Post-generation manual change | ISSUE-002 | ❌ Developer-authored code |

> ⚠️ SKILL GAP: [rule at recurrence ≥ 3, or: None]

#### Notes for the Developer

- ISSUE-002 lived in code changed after generation; your legacy fallback was preserved
```

⚠️ Append below existing entries. **Never edit a prior entry.** If §13 is missing (summary predates it), create it with the standard header.

### How to write

```text
1. Read the complete summary
2. Merge targeted edits into the state sections
3. Append the §13 entry
4. Write the COMPLETE file back
5. Confirm the write succeeded
```

⚠️ Do not assume an append mode exists. Preserve untouched content byte for byte.

---

## PART 6b — WRITE THE LEARNING (GATED)

### The gate

```text
Agent miss · Regression from prior fix                      → WRITE
Upstream gap · Contract change · Design change ·
Post-generation manual change · Ambiguous requirement       → DO NOT WRITE
                                                              record the origin in §13
```

A learning must be something the coding agent **could have acted on at generation time**.

```text
✅ "Mappers must apply the null default recorded in plan §11.2"
❌ "Sitecore renamed PolicyTitle to Title"        — external
❌ "Design v2 changed the card gap"               — external
❌ "The developer's fallback returned empty"      — not the agent's code
```

### Namespace

| Category                              | Namespace               |
| ------------------------------------- | ----------------------- |
| UI · RTL · Responsive · A11y · Media  | `# UI LEARNINGS`        |
| BFF · API · State · Sitecore · mapper | `# LOGIC LEARNINGS`     |
| A test should have caught it          | `# TEST LEARNINGS`      |
| Storybook · catalogue                 | `# STORYBOOK LEARNINGS` |

⚠️ If a test should have caught it, write to **both** the behaviour namespace and `# TEST LEARNINGS`.

### The four steps — all four, every time

```text
STEP 1  READ    ./src/.project/learnings/CODING_AGENT_LEARNINGS.md
STEP 2  DEDUPE  search the namespace for a SEMANTICALLY equivalent rule
                  found     → increment recurrence, append this defect ID
                  not found → compose a new entry
STEP 3  WRITE   merge into the namespace, write the COMPLETE file back
STEP 4  CONFIRM the write succeeded; report the namespace and new/recurrence
```

⚠️ Steps 1–2 without 3–4 is the failure this section exists to prevent.

### Entry format

```text
# UI LEARNINGS

- RTL: use logical properties (ms-/me-/ps-/pe-) — never physical (ml-/mr-/pl-/pr-).
  Mirror directional icons with rtl:rotate-180; never mirror neutral icons
  (eye, help, search, calendar), symmetric icons, or brand logos.
  Refs: DEF-4380, DEF-486  (recurrence ×2)
```

```text
✅ A generalisable rule · what to do and not do · why it matters · 2–4 lines
❌ A war story ("In DEF-486 the arrows on the policy page…")
```

⚠️ Preserve every existing entry and all four namespace headings. Never delete or rewrite a learning except to increment recurrence.

### Skill gap

```text
Recurrence ≥ 3 → the SKILL is under-specified, not the learnings file

⚠️ SKILL GAP DETECTED
  Rule: [rule] · Namespace: [ns] · Recurrence: 3 ([refs])
  Skill: [coding skill] — RECOMMENDATION: strengthen [section]
```

Record it in §13. **Do not edit the skill** — that is a human decision.

---

### Gate — Phase 6 is NOT complete until

```text
SUMMARY
- [ ] Summary read in full before editing
- [ ] State sections the fix touched updated and tagged [DEF-xxx]
- [ ] Drift in RCA-inspected rows reconciled, tagged [DEF-xxx · drift]
- [ ] Historical sections untouched; prior §13 entries untouched
- [ ] §13 entry appended with all blocks incl. test-execution output folders
- [ ] FILE WRITTEN and the write confirmed

LEARNINGS
- [ ] Every issue's origin evaluated against the gate
- [ ] For each qualifying issue: file READ → deduped → MERGED → WRITTEN → confirmed
- [ ] No learning for developer changes, contract/design changes, upstream gaps, ambiguity
- [ ] Skill gap flagged at recurrence ≥ 3
- [ ] If NO issue qualified: file correctly untouched, and this is stated explicitly
```

⚠️ **"Identified but not written" fails this gate.**

### Never

- **Never suggest a learning instead of writing it.**
- **Never end the phase with an unwritten entry.**
- Never write a learning for a post-generation manual change, contract change, design change, upstream gap, or ambiguity.
- Never write a learning as a war story; never append a duplicate.
- Never delete or rewrite an existing learning.
- Never edit a coding skill — flag the gap.
- Never produce a separate defect document — §13 is the record.
- Never regenerate the summary; never modify historical sections.
- Never record a test as passed without a run output folder.
- Never write "measured" coverage without a `--coverage` run.
- Never assume an append mode exists.
- Never close or comment on the ticket.
