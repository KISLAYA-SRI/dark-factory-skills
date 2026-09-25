---
name: defect-reporting-and-learning
description: Use as Phase 6 of the FE Defect Fix workflow to update the parent CODE_GENERATION_SUMMARY.md in place — refreshing every state section the fix changed, reconciling drift from developer changes in the rows inspected, and appending a Change Log entry with edge-case and test-execution evidence — and to append to the Coding Agent Learnings only when the fault origin was an agent miss or a regression from a prior fix. Triggers include defect report, update code gen summary, update learnings, or close out defect fix.
disable-model-invocation: true
---

## Defect Reporting and Learning

### Purpose

This skill is **Phase 6** — the final phase of the FE Defect Fix Agent.

```text
6a  Update CODE_GENERATION_SUMMARY.md     → always
      · refresh state sections the fix changed
      · reconcile drift in rows RCA inspected
      · append a §13 Change Log entry
6b  Append to CODING_AGENT_LEARNINGS.md   → ONLY for agent miss / regression from prior fix
```

⚠️ **There is no separate DEFECT_FIX_SUMMARY.md.** The parent summary is the single living record.

---

## ⚠️ WHY THE SUMMARY MUST BE UPDATED

The summary is the **map** every future defect run starts from. Two things make it stale:

```text
1. THIS FIX       — lines move, defaults change, states render differently
2. DEVELOPER EDITS — code changed after generation that the summary never recorded
```

A stale map misleads the next run — and a stale §8 corrupts fault-origin classification: RCA sees code ≠ summary and mislabels the cause, writing a wrong learning.

⚠️ Phase 3 already found the drift. Recording it here means the next defect run starts from an accurate map.

---

## ⚠️ STATE SECTIONS vs HISTORICAL SECTIONS

| § | Section | Nature | On defect fix |
| --- | --- | --- | --- |
| 3 | File Inventory | State | ✅ Update — incl. files developers added |
| 4 | UI Components | State | ✅ If a component changed |
| 5 | Sitecore field → prop | State | ✅ If a mapping changed or drifted |
| 6 | Logic & API | State | ✅ If a layer changed or drifted |
| 7 | Data Flow Trace | State | ✅ Per affected or drifted field |
| 8 | State → UI Matrix | State | ✅ Per affected or drifted state |
| 9 | Design & NFR Notes | State | ✅ If tokens/exceptions changed |
| 10 | Tests & Coverage | State | ✅ Add regression + guard tests |
| 12.4 | Known Limitations | State | ✅ Mark Resolved if closed |
| 11 | AC Evidence | Mixed | ⚠️ Status only, if an AC now passes |
| 1 · 2 · 12.1 · 12.2 · 12.5 | Historical | — | ❌ Never change |
| **13** | **Change Log** | **Append-only** | ✅ One entry per defect |

**Rule:** state sections describe the code as it is **now**. Historical sections record the original build.

---

## ⚠️ MINIMAL-CHANGE CONTRACT — FOR THE SUMMARY TOO

```text
Update ONLY:
  · rows the fix touched
  · rows RCA inspected and found drifted

❌ Never regenerate the summary
❌ Never re-survey the whole codebase to "resync" every section
❌ Never reformat, reorder, or reword untouched rows
```

Drift found **outside** the rows RCA inspected is not reconciled — record it in the §13 entry as *observed drift, not reconciled*.

---

# PART 6a — UPDATE CODE_GENERATION_SUMMARY.md

**Path:** `.SS_WF/Agent/CODE/{{parent_story_id}}_CODE_GENERATION_SUMMARY.md`

## Step 1 — Tag Every Changed Row

| Tag | Meaning |
| --- | --- |
| `[DEF-123]` | Changed by this fix |
| `[DEF-123 · drift]` | Reconciled to match a developer change found during this fix |

```markdown
FIELD: policyNumber
  BFF getPolicyList → response.items[].policyNumber (string, nullable)
    → PolicyMapper.mapPolicyResponse()    Mappers/PolicyMapper.ts:52   [DEF-123]
        null / undefined / "" → legacyNumber, else "—"                 [DEF-123 · drift]
    → PolicyCard (prop: policyNumber)     Components/PolicyCard.tsx
```

⚠️ A row touched by several defects carries every tag: `[DEF-123] [DEF-456]`.

⚠️ Where the summary cites a line number, prefer **symbol + current line** so the next run can find it even after further edits.

## Step 2 — Update §10 Tests

```markdown
| Source File | Classification | Test File | Cases | Branch Coverage |
| `PolicyMapper.ts` | Transactional | `PolicyMapper.test.ts` | 13 (+1 regression, +6 guards [DEF-123]) | 95% (measured) |
```

⚠️ Say **measured** only if `run-test-cases` was run with `--coverage`; otherwise keep **targeted**.

## Step 3 — Resolve Known Limitations

Mark closed — **never delete the row**:

```markdown
| LIM-001 | Expiry badge never renders | GAP-003 | Users cannot see expiry | Backend | ✅ Resolved [DEF-123] |
```

## Step 4 — Append the §13 Change Log Entry

```markdown
### DEF-123 — {{YYYY-MM-DD}} — Defect Fix

**Reported:** 3 issues · **Fixed:** 2 · **Blocked:** 1
**Verification level:** EXECUTED | STATIC ONLY — [reason]

#### Defect Dev Notes

| DDN ID | Instruction | Applied To | Status |
| ------ | ----------- | ---------- | ------ |
| DDN-001 | Use the Sitecore message, not a hardcoded string | ISSUE-002 | Implemented |

> Supersession: DDN-001 supersedes DN-004. *(or: None)*

#### Context Refetch

| Artefact | Issue | Trigger | Diff Result |
| -------- | ----- | ------- | ----------- |
| Sitecore | ISSUE-002 | Field not rendering | `PolicyTitle` → `Title` (RENAMED) |

> *(or: No artefacts refetched.)* Note stale `responsive_design_intent.json` if Figma was refetched.

#### Drift From Summary

> Where the current code differed from what this summary recorded.

| Location | Summary Said | Code Actually Did | Source | Reconciled? |
| -------- | ------------ | ----------------- | ------ | ----------- |
| `PolicyMapper.ts → mapPolicyResponse()` | null → "—" | null → `legacyNumber ?? ""` | Developer, commit a1b2c3 (2026-08-21) | ✅ §7 updated |
| `PolicyCard.tsx → formatDate()` | not recorded | added by developer | Developer, commit d4e5f6 | ⛔ Observed only — outside RCA scope |

> *(or: No drift found.)*

#### Issues

| Issue | Category | Status | Root Cause | Fault Origin | Fix |
| ----- | -------- | ------ | ---------- | ------------ | --- |
| ISSUE-001 | RTL | ✅ Fixed | `CarouselPager.tsx → Pager` used `ml-2` — no RTL flip | Agent miss | `ml-2` → `ms-2`; `rtl:rotate-180` on arrow |
| ISSUE-002 | BFF | ✅ Fixed | Developer fallback returned `""` for null — blank render | Post-generation manual change | Empty fallback → `"—"`, legacy fallback preserved |
| ISSUE-003 | BFF | ⛔ Blocked | `expiryDate` absent from contract | Contract gap | — |

#### Edge Cases Verified

| Issue | Case | Expected | Test | Result |
| ----- | ---- | -------- | ---- | ------ |
| ISSUE-002 | null policyNumber *(reported)* | "—" | `handles null policyNumber [DEF-123 / ISSUE-002]` | ✅ |
| ISSUE-002 | undefined / "" / whitespace | "—" | 3 guard tests | ✅ |
| ISSUE-002 | valid value (untouched path) | unchanged | guard | ✅ |
| ISSUE-002 | legacyNumber present *(developer behaviour)* | legacyNumber | guard — preserve | ✅ |
| ISSUE-002 | Arabic locale | inside `<bdi>` | guard | ✅ |
| ISSUE-001 | LTR still correct after RTL fix | `ms-2` resolves left in LTR | guard | ✅ |

#### Test Execution Evidence

| Run | Scope | Verdict | Output |
| --- | ----- | ------- | ------ |
| ISSUE-002 failing-first | regression test | EXPECTED_FAIL | `.SS_WF/Agent/TEST_RUNS/DEF-123-ISSUE-002-failing-first-…/` |
| ISSUE-002 after fix | regression test | PASS | `…/DEF-123-ISSUE-002-after-fix-…/` |
| ISSUE-002 guards | 6 guard tests | PASS | `…/DEF-123-ISSUE-002-guards-…/` |
| ISSUE-002 blast radius | 3 files + related sweep | PASS | `…/DEF-123-ISSUE-002-blast-radius-…/` |
| Final consolidated | all touched + blast-radius files | PASS | `…/DEF-123-final-…/` |

> Developer reproduction: `pnpm run test:sme` · `pnpm run test:foundation`
> ⚠️ If STATIC ONLY: list the exact commands the developer must run before merging.

#### Sections Updated

| Section | Change |
| ------- | ------ |
| §3 | 4 rows updated [DEF-123] |
| §7 | `policyNumber` trace — fix + drift reconciled |
| §10 | +1 regression, +6 guard tests |

#### Existing Tests Modified

| Test | Change | Reason |
| ---- | ------ | ------ |
| `HeroBanner.test.tsx` | asserted `PolicyTitle` → now `Title` | Test encoded the old contract |

> *(or: None.)*

#### Observations — Not Fixed

| Source | Observation | Why Not Fixed |
| ------ | ----------- | ------------- |
| `usePolicyList.ts` | `staleTime` hardcoded | Outside every root cause |

> *(or: None.)*

#### Untested Consumers

| Consumer | Uses | Why no test |
| -------- | ---- | ----------- |
| `PolicyExport.tsx` | `mapPolicyResponse()` | No test file exists — recommend adding |

> *(or: None.)*

#### Learnings

| Origin | Issues | Learning Written? |
| ------ | ------ | ----------------- |
| Agent miss | ISSUE-001 | ✅ `# UI LEARNINGS` — RTL logical properties (recurrence ×2) |
| Post-generation manual change | ISSUE-002 | ❌ Developer-authored code — nothing for the coding agent to learn |
| Contract gap | ISSUE-003 | ❌ Upstream |

> ⚠️ SKILL GAP: [rule at recurrence ≥ 3, or: None]

#### Notes for the Developer

- ISSUE-002 lived in code changed after generation; your legacy fallback was preserved
- ISSUE-003 needs a backend change
- `PolicyExport.tsx` consumes the changed mapper and has no tests
```

⚠️ Append below existing entries, newest last. **Never edit or remove a prior entry.** If the summary has no §13 (generated before the Change Log existed), create it with the standard header first.

## How to Write the Update

```text
1. Read the complete CODE_GENERATION_SUMMARY.md
2. Merge targeted edits into the state sections
3. Append the §13 entry
4. Write the COMPLETE file back
```

⚠️ Read → merge → write back. Do not assume an append mode exists. Preserve untouched content **byte for byte**.

---

# PART 6b — LEARNING UPDATE (GATED)

**Path:** `./src/.project/learnings/CODING_AGENT_LEARNINGS.md`

## ⚠️ The Gate

```text
FOR EACH issue:
  Agent miss · Regression from prior fix                        → WRITE a learning
  Upstream gap · Contract change · Design change ·
  Post-generation manual change · Ambiguous requirement         → DO NOT write
                                                                  record the origin in §13
```

⚠️ **Post-generation manual change never produces a learning.** The coding agent did not write that code. Teaching it a rule would train it against a mistake it never made.

⚠️ **Design and contract changes never produce learnings.** The code was correct when written.

A learning must be something the coding agent **could have acted on at generation time**.

## Namespace Routing

| Issue category | Namespace |
| --- | --- |
| UI · RTL · Responsive · A11y · Media | `# UI LEARNINGS` |
| BFF · API · State · Sitecore · mapper | `# LOGIC LEARNINGS` |
| A test should have caught it | `# TEST LEARNINGS` |
| Storybook · catalogue | `# STORYBOOK LEARNINGS` |

⚠️ If a test should have caught it, write to **both** the behaviour namespace and `# TEST LEARNINGS`.

⚠️ If the edge-case matrix found cases the original generated tests missed (e.g. no test for `undefined`), that is a `# TEST LEARNINGS` entry — **only** if the code was agent-generated.

## ⚠️ Deduplication

```text
1. Search the namespace for a SEMANTICALLY equivalent rule
2. FOUND     → increment recurrence, append this defect ID
3. NOT FOUND → append a new entry
4. Recurrence ≥ 3 → flag SKILL GAP
```

### Entry Format

```text
# UI LEARNINGS

- RTL: use logical properties (ms-/me-/ps-/pe-) — never physical (ml-/mr-/pl-/pr-).
  Mirror directional icons with rtl:rotate-180; never mirror neutral icons
  (eye, help, search, calendar), symmetric icons, or brand logos.
  Refs: DEF-4380, DEF-123  (recurrence ×2)

# TEST LEARNINGS

- Mapper tests must cover null, undefined, empty string and whitespace for every
  nullable field — not only null. Blank renders hide in the untested variants.
  Refs: DEF-123
```

```text
✅ Generalisable rule · what to do AND not do · why it matters · 2–4 lines
❌ War stories · component-specific trivia · restating a skill rule without recurrence proof
```

## ⚠️ Skill-Gap Detection

```text
Recurrence ≥ 3  →  the SKILL is under-specified, not the learnings file

⚠️ SKILL GAP DETECTED
  Rule:       [rule] · Namespace: [ns] · Recurrence: 3 ([refs])
  Skill:      [coding skill]
  RECOMMENDATION: strengthen [section] of [skill]
```

Surface it in the §13 entry. **Do not edit the skill** — that is a human decision.

## Writing the Learnings File

Read → locate namespace → merge → write the complete file back. Preserve every entry and all four headings. Never delete or rewrite a learning except to increment recurrence and append a ref.

---

### Gate: Phase 6 Complete When

```text
SUMMARY
- [ ] Parent summary read in full before editing
- [ ] Every state section the fix touched updated, tagged [DEF-xxx]
- [ ] Drift in rows RCA inspected reconciled, tagged [DEF-xxx · drift]
- [ ] Drift outside RCA scope recorded as observed, not reconciled
- [ ] Historical sections untouched
- [ ] §13 entry appended with: verification level · DDN · refetch · drift · issues ·
      edge cases verified · test execution evidence · sections updated ·
      tests modified · observations · untested consumers · learnings · developer notes
- [ ] Every test claim backed by a run output folder, or the entry says STATIC ONLY
- [ ] Prior §13 entries untouched; untouched content preserved byte for byte
- [ ] NO separate DEFECT_FIX_SUMMARY.md

LEARNINGS
- [ ] Learning written ONLY for agent miss / regression from prior fix
- [ ] NO learning for post-generation manual change, design, contract, upstream, ambiguity
- [ ] Namespace routing correct; test gaps also in # TEST LEARNINGS
- [ ] Semantic deduplication; recurrence incremented
- [ ] Skill gap flagged at recurrence ≥ 3
- [ ] Written via read → merge → write back; all namespaces preserved
```

### Never Do

- Never produce a separate `DEFECT_FIX_SUMMARY.md`.
- Never regenerate or fully resync the summary.
- Never modify historical sections or prior §13 entries.
- Never delete a resolved Known Limitation row.
- Never leave a state section stale after changing or inspecting its code.
- **Never record a test as passed without a run output folder.**
- **Never write "measured" coverage without a `--coverage` run.**
- **Never write a learning for a post-generation manual change.**
- Never write a learning for upstream gaps, contract changes, design changes, or ambiguity.
- Never write a learning as a war story; never append a duplicate rule.
- Never edit a coding skill — flag the skill gap.
- Never assume an append mode exists.
- Never close, transition, or comment on the defect ticket.
