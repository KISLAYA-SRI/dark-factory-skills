---
name: defect-reporting-and-learning
description: Use as Phase 6 of the FE Defect Fix workflow to update the parent CODE_GENERATION_SUMMARY.md in place — refreshing every state section the fix changed and appending a Change Log entry — and conditionally append to the Coding Agent Learnings file when the fault origin was an agent miss or regression. Triggers include defect report, update code gen summary, update learnings, or close out defect fix.
disable-model-invocation: true
---

## Defect Reporting and Learning

### Purpose

This skill is **Phase 6** — the final phase of the FE Defect Fix Agent. It has two responsibilities:

```text
6a  Update CODE_GENERATION_SUMMARY.md     → always
      · refresh state sections the fix changed
      · append a §13 Change Log entry recording the defect
6b  Append to CODING_AGENT_LEARNINGS.md   → ONLY for agent-miss / regression origins
```

⚠️ **There is no separate DEFECT_FIX_SUMMARY.md.** The parent summary is the single living record. A separate document would restate the same facts and immediately diverge.

---

## ⚠️ WHY THE SUMMARY MUST BE UPDATED

The Code Generation Summary is the **location index** every future defect run depends on. Left stale, it actively misleads.

```text
JIRA-1 §7:  policyNumber → PolicyMapper.ts:34 → null default '—'

DEF-123 fixes a bug in PolicyMapper.ts; line 34 becomes line 41
        → summary still says line 34

DEF-789: "policy number blank"
        → reads §7 → opens line 34 → wrong code
        → RCA locates the wrong branch, or confidence collapses
```

Worse, a stale §8 corrupts **fault-origin classification**:

```text
DEF-123 changed the empty state: EmptyState → SitecoreEmptyState
        §8 still records "EmptyState"

DEF-789 reports the empty state again
        → RCA sees code ≠ §8 → classifies AGENT MISS
        → but the code was fixed; §8 was stale
        → a wrong learning is written; the learnings file degrades
```

⚠️ A stale summary does not merely slow diagnosis — it poisons the learning loop.

---

## ⚠️ STATE SECTIONS vs HISTORICAL SECTIONS

The summary holds two kinds of content. **Only one kind is updated.**

| § | Section | Nature | On defect fix |
| --- | --- | --- | --- |
| 3 | File Inventory | Current state | ✅ **Update** |
| 4 | UI Components | Current state | ✅ Update if a component changed |
| 5 | Sitecore field → prop | Current state | ✅ Update if a mapping changed |
| 6 | Logic & API Integration | Current state | ✅ Update if a layer changed |
| 7 | Data Flow Trace | Current state | ✅ **Update** — per affected field |
| 8 | State → UI Matrix | Current state | ✅ **Update** — per affected state |
| 9 | Design & NFR Notes | Current state | ✅ Update if tokens/exceptions changed |
| 10 | Tests & Coverage | Current state | ✅ **Update** — add regression tests |
| 12.4 | Known Limitations | Current state | ✅ Update if a limitation was resolved |
| 11 | AC Evidence | Mixed | ⚠️ Update **status only** if an AC now passes |
| 1 | Developer Notes Applied | Historical | ❌ Leave — records the original build |
| 2 | Story & Classification | Historical | ❌ Leave |
| 12.1 | Decisions & Conflicts | Historical | ❌ Leave |
| 12.2 | Assumptions | Historical | ❌ Leave |
| 12.5 | Validation Exceptions | Historical | ❌ Leave |
| **13** | **Change Log** | **Append-only** | ✅ **Add one entry per defect** |

**Rule:** state sections must always describe the code as it is **now**. Provenance sections record what happened at original generation and never change.

---

## ⚠️ MINIMAL-CHANGE CONTRACT APPLIES HERE TOO

```text
Update ONLY the rows the fix actually touched.

❌ Never regenerate the summary
❌ Never rewrite unaffected rows
❌ Never reformat tables
❌ Never re-derive traces for fields the fix did not touch
❌ Never "improve" wording of existing entries
```

The same discipline that governs the code governs its record.

---

# PART 6a — UPDATE CODE_GENERATION_SUMMARY.md

**Path:** `.SS_WF/Agent/CODE/{{parent_story_id}}_CODE_GENERATION_SUMMARY.md`

⚠️ This is the **parent story's** summary — the story the defect was raised against. Update it in place.

## Step 1 — Tag Every Changed Row

Every row you modify carries the defect ID so provenance stays visible:

```markdown
## 7. Data Flow Trace

FIELD: policyNumber
  BFF getPolicyList → response.items[].policyNumber (string, nullable)
    → PolicyListService.fetchPolicies()          Services/PolicyListService.ts
    → usePolicyList()                            Hooks/usePolicyList.ts
    → PolicyMapper.mapPolicyResponse()           Mappers/PolicyMapper.ts:41   [DEF-123]
        null / undefined → "—"                                                [DEF-123]
    → PolicyListContainer                        Components/PolicyListContainer.tsx
    → PolicyCard (prop: policyNumber)            Components/PolicyCard.tsx
```

```markdown
## 8. State → UI Behaviour Matrix

| State | Trigger Condition | What Renders | Owning File |
| ----- | ----------------- | ------------ | ----------- |
| empty | `data.length === 0` | `SitecoreEmptyState` [DEF-123] | `PolicyListContainer.tsx:48` |
```

```markdown
## 3. File Inventory

| # | File Path | Type | Action | Purpose |
| - | --------- | ---- | ------ | ------- |
| 3 | `.../PolicyMapper.ts` | Mapper | Modified [DEF-123] | Response → ViewModel |
| 9 | `.../PolicyMapper.test.ts` | Test | Modified [DEF-123] | +1 regression test |
```

⚠️ A row touched by two defects carries both tags: `[DEF-123] [DEF-456]`.

## Step 2 — Update §10 Tests

Add each regression test; keep the existing rows intact:

```markdown
| Source File | Classification | Test File | Cases | Branch Coverage |
| ----------- | -------------- | --------- | ----- | --------------- |
| `PolicyMapper.ts` | Transactional | `PolicyMapper.test.ts` | 7 (+1 [DEF-123]) | 93% (targeted) |
```

## Step 3 — Resolve Known Limitations

If a fix closed a limitation, mark it — **do not delete the row**:

```markdown
| ID | Limitation | Root Cause | Impact | Owner | Status |
| -- | ---------- | ---------- | ------ | ----- | ------ |
| LIM-001 | Expiry badge never renders | GAP-003 | Users cannot see expiry | Backend | ✅ Resolved [DEF-123] |
```

## Step 4 — Append the §13 Change Log Entry

This is where the **defect-specific record** lives — what was reported, what was wrong, and how it was proven fixed.

```markdown
## 13. Change Log

> Append-only. Every defect fix and enhancement that modified this component.
> Sections 1–12 always describe the CURRENT state; this log records how it got there.

---

### DEF-123 — {{YYYY-MM-DD}} — Defect Fix

**Reported:** 3 issues · **Fixed:** 2 · **Blocked:** 1

#### Defect Dev Notes

| DDN ID | Instruction | Applied To | Status |
| ------ | ----------- | ---------- | ------ |
| DDN-001 | Use the Sitecore message, not a hardcoded string | ISSUE-002 | Implemented |

> Supersession: DDN-001 supersedes DN-004 (which allowed a generic fallback).

#### Context Refetch

| Artefact | Issue | Trigger | Diff Result |
| -------- | ----- | ------- | ----------- |
| Sitecore | ISSUE-002 | Field not rendering; §5 mismatch | `PolicyTitle` → `Title` (RENAMED) |

> `responsive_design_intent.json` stale after Figma refetch — not re-reconciled. *(omit if N/A)*

#### Issues

| Issue | Category | Status | Root Cause | Fault Origin | Fix | Regression Test | Failed First |
| ----- | -------- | ------ | ---------- | ------------ | --- | --------------- | ------------ |
| ISSUE-001 | RTL | ✅ Fixed | `CarouselPager.tsx:28` used `ml-2` (physical) — no RTL flip | Agent miss | `ml-2` → `ms-2`; added `rtl:rotate-180` | `CarouselPager.test.tsx` → "mirrors arrow in RTL" | ✅ |
| ISSUE-002 | Sitecore | ✅ Fixed | Contract renamed `PolicyTitle` → `Title` | Contract change | Updated field contract + mapping | `HeroBanner.test.tsx` → "renders Title field" | ✅ |
| ISSUE-003 | BFF | ⛔ Blocked | `expiryDate` absent from contract (GAP-003 / LIM-001) | Contract gap | — | — | — |

#### Sections Updated

| Section | Change |
| ------- | ------ |
| §3 | 4 rows updated (2 source, 2 test) |
| §5 | `PolicyTitle` → `Title` mapping corrected |
| §7 | `policyNumber` trace — mapper line 34 → 41 |
| §8 | `empty` state — owning file unchanged, renderer corrected |
| §10 | +2 regression tests |
| §12.4 | LIM-001 unchanged — still open |

#### Existing Tests Modified

| Test | Change | Reason |
| ---- | ------ | ------ |
| `HeroBanner.test.tsx:33` | Asserted `PolicyTitle` → now `Title` | Test encoded the old contract |

> If none: "None."

#### Observations — Not Fixed

| Source | Observation | Why Not Fixed |
| ------ | ----------- | ------------- |
| `usePolicyList.ts:22` | `staleTime` hardcoded rather than from constants | Outside every root cause |

> If none: "None."

#### Learnings

| Origin | Issues | Learning Written? |
| ------ | ------ | ----------------- |
| Agent miss | ISSUE-001 | ✅ `# UI LEARNINGS` — RTL logical properties (recurrence ×2) |
| Contract change | ISSUE-002 | ❌ External — nothing the agent could have done |
| Contract gap | ISSUE-003 | ❌ Upstream |

> ⚠️ SKILL GAP: [rule at recurrence ≥ 3, or: None]

#### Notes for the Developer

- ISSUE-003 requires a backend change before it can be fixed
- ISSUE-001's learning has fired twice — if it recurs, `presentational-ui-generation` needs a stronger RTL rule
```

⚠️ **Append below existing entries, newest last.** Never edit or remove a prior Change Log entry — the log is the audit trail that replaced the separate defect document.

## How to Write the Update

```text
1. Read the complete CODE_GENERATION_SUMMARY.md
2. Merge your targeted edits into the state sections
3. Append the new §13 entry
4. Write the COMPLETE file content back
```

⚠️ **Read → merge → write back.** Do not assume an append mode exists. Preserve every untouched section, row, and heading **byte for byte**.

⚠️ If the parent summary has no §13 section (generated before the Change Log existed), **create it** at the end with the standard header, then add the entry.

---

# PART 6b — LEARNING UPDATE (GATED)

**Path:** `./src/.project/learnings/CODING_AGENT_LEARNINGS.md`

## ⚠️ The Gate

```text
FOR EACH issue:

  IF fault origin is "Agent miss" OR "Regression from prior fix"
     → WRITE a learning

  ELSE (upstream gap | contract change | design change | ambiguous requirement)
     → DO NOT write a learning
     → Record the origin in the §13 Change Log entry instead
```

### Why the Gate Matters

The coding skills **read** this file. Every entry costs context on every future run.

```text
✅ "Mappers must apply the null default recorded in plan §11.2"
      → actionable; the agent can do this differently next time

❌ "Sitecore renamed PolicyTitle to Title in Sprint 14"
      → nothing the coding agent could have done; pure noise

❌ "Design v2 changed the card gap from 16px to 24px"
      → the agent built correctly against v1; nothing to learn
```

A learning must be something the coding agent **could have acted on at generation time**.

⚠️ **Design changes and contract changes never produce learnings.** The code was correct when written.

---

## Namespace Routing

| Issue category | Namespace |
| --- | --- |
| UI / RTL / Responsive / A11y / Media | `# UI LEARNINGS` |
| BFF / API / State / Sitecore / mapper | `# LOGIC LEARNINGS` |
| Test gap — a test should have caught it | `# TEST LEARNINGS` |
| Storybook / catalogue | `# STORYBOOK LEARNINGS` |

⚠️ If the defect reveals that a **test should have caught it**, write to **both** the behaviour namespace and `# TEST LEARNINGS`. Two failures occurred: the code was wrong, and the test did not cover it.

---

## ⚠️ Deduplication — Before Appending

```text
1. Search the target namespace for a SEMANTICALLY equivalent rule
     (not just string match — "use ms-* not ml-*" ≡ "use logical properties")

2. FOUND     → do NOT add a duplicate
                increment the recurrence counter
                append this defect ID to the existing entry

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

- Mappers must apply the null/missing default recorded in the Analysis Plan §11.2.
  Returning the raw DTO field leaves the prop undefined and renders blank.
  Refs: DEF-4102
```

**Rules for the entry text:**

```text
✅ Write a generalisable RULE
✅ State what to do AND what not to do
✅ Say briefly why it matters (the failure mode)
✅ Keep it 2–4 lines

❌ Never a war story ("In DEF-123 the arrows on the policy page…")
❌ Never story- or component-specific unless the rule genuinely only applies there
❌ Never restate a rule already embedded in a coding skill — unless recurrence
   proves the skill's version is not landing
```

---

## ⚠️ Skill-Gap Detection

```text
Recurrence ≥ 3  →  the SKILL is under-specified, not the learnings file
```

A rule that has fired three times is not being absorbed. The fix belongs **in the skill**, not in another learnings entry.

```text
⚠️ SKILL GAP DETECTED

  Rule:       RTL logical properties + directional icon mirroring
  Namespace:  # UI LEARNINGS
  Recurrence: 3  (DEF-4102, DEF-4380, DEF-123)
  Skill:      presentational-ui-generation

  RECOMMENDATION: strengthen the RTL section of presentational-ui-generation —
  the learnings entry is not preventing recurrence.
```

Surface this in the §13 Change Log entry. **Do not edit the skill** — that is a human decision.

---

## Writing to the Learnings File

```text
1. Read ./src/.project/learnings/CODING_AGENT_LEARNINGS.md
2. Locate the target namespace heading
3. Merge the new/updated entries into that namespace
4. Write the COMPLETE file content back
```

⚠️ Preserve every existing entry and all four namespace headings exactly. **Never delete or rewrite an existing learning** unless incrementing its recurrence and appending a defect ID.

---

### Gate: Phase 6 Complete When

```text
SUMMARY UPDATE
- [ ] Parent CODE_GENERATION_SUMMARY.md read in full before editing
- [ ] Every state section the fix touched is updated (§3 §4 §5 §6 §7 §8 §9 §10 §12.4)
- [ ] Historical sections left untouched (§1 §2 §12.1 §12.2 §12.5)
- [ ] §11 AC Evidence status updated only where an AC now passes
- [ ] Every changed row tagged with the defect ID
- [ ] ONLY rows the fix touched were modified — no regeneration, no reformatting
- [ ] §13 Change Log entry appended with all eight blocks
- [ ] §13 created with the standard header if the summary predates it
- [ ] Prior Change Log entries left untouched
- [ ] Untouched sections preserved byte for byte
- [ ] Written via read → merge → write back
- [ ] NO separate DEFECT_FIX_SUMMARY.md produced

LEARNINGS
- [ ] Every issue's fault origin evaluated against the gate
- [ ] Learning written ONLY for agent-miss / regression origins
- [ ] NO learning for design change, contract change, upstream gap, or ambiguity
- [ ] Namespace routing correct; test gaps also written to # TEST LEARNINGS
- [ ] Deduplication performed — semantic match, not string match
- [ ] Recurrence incremented where a rule already existed
- [ ] Entries written as generalisable RULES, not war stories
- [ ] Skill gap flagged at recurrence ≥ 3, recorded in the §13 entry
- [ ] File written via read → merge → write back; all namespaces preserved
- [ ] No existing learning deleted or rewritten
```

### Never Do

- **Never produce a separate `DEFECT_FIX_SUMMARY.md`** — the §13 Change Log replaced it.
- **Never regenerate the summary** — targeted row updates only.
- **Never modify historical sections** (§1, §2, §12.1, §12.2, §12.5).
- **Never edit or remove a prior §13 Change Log entry.**
- **Never delete a resolved Known Limitation row** — mark it Resolved.
- **Never leave a state section stale** after changing the code it describes.
- **Never update a trace or state row the fix did not touch.**
- **Never reformat, re-order, or reword untouched content.**
- **Never write a learning for upstream gaps, contract changes, design changes, or ambiguity.**
- **Never write a learning as a war story.**
- **Never append a duplicate rule** — increment recurrence instead.
- **Never delete or rewrite an existing learning.**
- **Never edit a coding skill** — flag the skill gap and let a human decide.
- **Never assume an append mode exists** — read, merge, write back.
- **Never close, transition, or comment on the defect ticket** — lifecycle belongs to the developer.
