---
name: defect-root-cause-analysis
description: Use as Phase 3 of the FE Defect Fix workflow to read the current code first, detect drift from the Code Generation Summary, locate the exact cause of an issue to file and line, classify fault origin across seven categories to gate the learning update, determine blast radius with concrete test files, and build the Fix Impact Analysis edge-case matrix and test plan that Phase 4 executes. Runs once per issue. Triggers include root cause analysis, RCA, locate defect, diagnose issue, or impact analysis.
disable-model-invocation: true
---

## Defect Root Cause and Impact Analysis

### Purpose

This skill is **Phase 3** of the FE Defect Fix Agent, run **once per issue**. It answers five questions:

```text
1. WHAT does the code do NOW?        → current code, read first; drift recorded
2. WHERE is the fault?               → file + line + mechanism
3. WHY did it happen?                → fault origin (gates the learning update)
4. WHAT ELSE does it touch?          → blast radius, with the test files that cover it
5. WHAT MUST STILL WORK after a fix? → Fix Impact Analysis — the edge-case matrix
```

⚠️ **Naming a file is not a root cause.** A root cause names the **line** and the **mechanism**: *"`PolicyMapper.ts:41` returns `undefined` for null `policyNumber` instead of `'—'`, so `PolicyCard` renders an empty span."*

⚠️ **No fix is written in this phase.** No source edits, no tests. The output is precise enough for Phase 4 to write a test that **fails** against current code, and a set of guard tests that must still pass after the fix.

---

## STEP 1 — ⚠️ READ THE CURRENT CODE FIRST

Developers change code after generation. The summary tells you **where to look**; only the file tells you **what is there**.

```text
For every file the summary points to for this issue (§3, §5, §7, §8):
  1. OPEN the file as it is now
  2. FIND the symbol the summary names — by name, not by line number
  3. READ the actual logic: branches, defaults, conditions, rendered output
  4. COMPARE with what the summary records
```

⚠️ **Find by symbol, never by line number.** Line numbers drift with every edit. `mapPolicyResponse()` is still findable after the file grows; `line 34` is not.

### Drift Detection

Record every place the current code differs from the summary:

```text
DRIFT — ISSUE-002
  Location:     Mappers/PolicyMapper.ts → mapPolicyResponse()
  Summary §7:   null policyNumber → "—"  (line 34)
  Current code: null policyNumber → policy.legacyNumber ?? ""   (line 47)
  Explained by: git — changed 2026-08-21 by a developer commit; no §13 entry
  Classification: POST-GENERATION MANUAL CHANGE
```

### Explaining Drift With Git (When Available)

```bash
git log --follow --format="%h %ad %an %s" --date=short -- <file>
git log -L :<symbolName>:<file> --format="%h %ad %an %s" --date=short
git blame -L <start>,<end> --date=short -- <file>
```

| Evidence | Meaning |
| --- | --- |
| Line changed **after** generation date, matching a §13 `[DEF-xxx]` fix | Changed by a prior defect fix → regression candidate |
| Line changed **after** generation date, **no** §13 entry | Changed by a developer → post-generation manual change |
| Line unchanged since generation | Code is as the agent generated it |
| No git available | Record `drift source: unknown`; do not guess |

⚠️ **Drift is information, not a defect.** A developer may have changed the code deliberately — often because the generated version did not work.

```text
❌ Never revert code to match the summary
❌ Never "restore" the generated behaviour unless the requirement says so
❌ Never classify drift itself as the defect
✅ Diagnose against the REQUIREMENT (plan §4/§10/§11, DDN, DN)
✅ Build the fix on top of the CURRENT code
✅ Record drift for Phase 6 to reconcile in the summary
```

### The Two Questions

| Question | Answer from |
| --- | --- |
| What **should** happen? | DDN → DN → refetched artefact → Analysis Plan §4 · §10 · §11 |
| What **does** happen? | Current code → git history → summary (map only) |

---

## STEP 2 — Locate the Root Cause

### Summary Lookup Map (then verify in the code)

| Symptom | Start at | Then verify |
| --- | --- | --- |
| Value blank / wrong / stale | §7 Data Flow Trace | The mapper/service/hook as it is now |
| Wrong UI shown for a state | §8 State Matrix | The container's current state guards |
| Authored content missing | §5 field → prop | The current field access and helper |
| Visual differs from design | §9 Design Notes | The current classes and tokens |
| Which files could cause this | §3 File Inventory | Plus any files the developer added since |
| Touched before? | §13 Change Log | The prior fix's changes in the current file |
| Should this even work? | §12.4 + §2 | — |
| Which test should have caught it | §10 AC → test mapping | The current test file |

⚠️ **Files the developer added after generation are not in §3.** If the code imports something the summary never mentions, follow it.

### If an Artefact Was Refetched

The diff is the primary evidence:

```text
Relevant change in diff   → root cause is the source change
NO relevant change        → source did NOT change → code is wrong → not a design/contract change
```

⚠️ A negative diff is evidence, not a dead end.

### Diagnostic Paths by Category

```text
BFF / API     §7 trace → current mapper default → field path vs §11.2 → query key
              → §13 (prior fix?) → git (developer change?) → confirm the branch
Sitecore      §5 → current field name (case-sensitive) → helper used? → registry key
              → refetch diff if performed
State         §8 → current trigger conditions → guard ordering → plan §10 expectation
RTL           current classes → physical properties (ml-/mr-/pl-/pr-/text-left/right)
              → neutral icon mirrored? → symmetric/brand mirrored? → fixed widths clipping Arabic
UI / Visual   design-change signal? YES → diff · NO → current tokens vs design → agent miss
Responsive    manual grid classes vs Grid columns={12} · desktop-first classes · hardcoded px
Missing AC    plan §4 → §11 evidence claimed? → what is actually in the code now
Regression    §13 entry → what that fix changed → still present in current code?
```

---

## STEP 3 — ⚠️ Classify Fault Origin (Seven Origins)

| Origin | Definition | Learning? |
| --- | --- | --- |
| **Agent miss** | Code is as generated, and the agent had what it needed | ✅ Yes |
| **Regression from prior fix** | A §13 fix changed this and broke it | ✅ Yes |
| Upstream gap | Plan omitted or mis-specified it | ❌ |
| Contract change | Sitecore/BFF contract changed after generation | ❌ |
| Design change | Figma changed after generation | ❌ |
| **Post-generation manual change** | A developer changed the code after generation; the fault is in that change | ❌ |
| Ambiguous requirement | AC open to interpretation | ❌ |

### The Classification Test

```text
1. Is the faulty code still as the agent generated it?
     NO, changed by a §13 fix        → REGRESSION FROM PRIOR FIX       ✅
     NO, changed by a developer      → POST-GENERATION MANUAL CHANGE   ❌
     YES → continue
2. Given the plan, the embedded guidelines, and the contracts/designs available
   AT GENERATION TIME, could the agent have got this right?
     YES → AGENT MISS                ✅
     NO  → upstream gap · contract change · design change · ambiguous   ❌
```

⚠️ **Step 1 comes first.** Without it, a developer's bug is classified as an agent miss and the learnings file is taught a rule for code the agent never wrote.

⚠️ **Design change vs agent miss:** if a refetch shows the reported property **unchanged**, the design never changed — agent miss, regardless of what the ticket claimed.

⚠️ **Be honest in both directions.** Mislabelling an agent miss loses the learning; mislabelling anything else pollutes the learnings file.

### Learning Candidate (Agent Miss / Regression Only)

```text
LEARNING CANDIDATE
  Namespace:  # UI LEARNINGS | # LOGIC LEARNINGS | # TEST LEARNINGS | # STORYBOOK LEARNINGS
  Rule:       [generalisable rule — not a description of this defect]
  Why missed: [what the agent did instead]
  Defect ref: {{ticket_id}} / ISSUE-00N
```

If an existing learning already covers it → **recurrence**; flag for Phase 6.

---

## STEP 4 — Blast Radius, With Test Files

Identify **who consumes** the code about to change **and which test files cover them**. Phase 4 executes these.

| Change location | Consumers | How to find consumer tests |
| --- | --- | --- |
| Design-system component | ⚠️ every consumer | catalogue composition + search imports of the symbol; `--related --related-scope all` |
| Design token | every component using it | search the token name |
| Shared feature component | 2+ features | catalogue + import search |
| Mapper / service | every consumer of that data | §7 + import search |
| Container / feature component | usually that feature | co-located tests |
| Sitecore entry | that rendering | co-located tests |

```bash
# Find consumers of a changed symbol (then take their co-located .test files)
grep -rl --include=*.ts --include=*.tsx "PolicyMapper\|mapPolicyResponse" Portals/ Packages/
```

```text
BLAST RADIUS — ISSUE-002
  Changing:        Mappers/PolicyMapper.ts → mapPolicyResponse()
  Consumers:       PolicyListContainer.tsx · PolicySummary.tsx
  Consumer tests:  PolicyListContainer.test.tsx · PolicySummary.test.tsx
  Co-located:      PolicyMapper.test.ts
  Related sweep:   --related Mappers/PolicyMapper.ts
  Risk:            MEDIUM — behaviour change for null input only
```

⚠️ **A consumer without a test is a gap.** Record it — Phase 4 adds a guard test for the consumer's use of the changed behaviour, or the §13 entry flags it as unverified.

---

## STEP 5 — ⚠️ FIX IMPACT ANALYSIS — THE EDGE-CASE MATRIX

> **Change narrowly. Verify widely.**
> The minimal-change contract limits what you edit. It never limits what you check.

Before any fix is written, enumerate **every case that flows through the lines about to change**, and state the expected behaviour after the fix. Each row becomes a **guard test** in Phase 4.

### Checklist by Dimension

| Dimension | Always check |
| --- | --- |
| **Data** | `null` · `undefined` · `""` · whitespace-only · `0` / `false` · empty array · single item · many items · overlong value · unexpected type |
| **Branches** | **Both sides** of every conditional the fix touches — especially the path that was already correct |
| **Locale** | `en` **and** `ar` — an RTL fix must not break LTR, and vice versa |
| **Numbers/IDs in RTL** | LTR content inside RTL text needs `<bdi>` |
| **Responsive** | 390 · 1024 · 1700 when layout is involved |
| **State** | Transitions **into and out of** the changed state (loading → empty → populated) |
| **Interaction** | Rapid repeat · keyboard as well as pointer · disabled path |
| **Persona / role** | Every role variant the plan defines |
| **Consumers** | Each blast-radius consumer's use of the changed behaviour |
| **Prior fixes** | Behaviour a §13 fix established on the same code |
| **Developer changes** | Behaviour a post-generation manual change introduced — **must be preserved** unless the requirement says otherwise |

⚠️ The last row matters: a fix built on top of a developer's change must not quietly undo what the developer intended.

### Matrix Format

```text
FIX IMPACT ANALYSIS — ISSUE-002
Changed lines: PolicyMapper.ts → mapPolicyResponse(), policyNumber fallback

| # | Case                              | Input / Condition            | Expected after fix        | Test type  |
| - | --------------------------------- | ---------------------------- | ------------------------- | ---------- |
| 1 | Reported defect                   | policyNumber = null          | "—"                       | REGRESSION |
| 2 | Undefined field                   | policyNumber absent          | "—"                       | GUARD      |
| 3 | Empty string                      | ""                           | "—"                       | GUARD      |
| 4 | Whitespace                        | "   "                        | "—"                       | GUARD      |
| 5 | Valid value (untouched path)      | "POL-001"                    | "POL-001"                 | GUARD      |
| 6 | Developer's legacy fallback       | null + legacyNumber = "L-9"  | "L-9"  (preserve DEV change) | GUARD   |
| 7 | Arabic locale                     | "POL-001", dir="rtl"         | rendered inside <bdi>     | GUARD      |
| 8 | Consumer: PolicySummary           | null                         | shows "—", no crash       | BLAST      |
```

⚠️ **Only row type REGRESSION must fail first.** GUARD and BLAST rows protect behaviour that is already correct, so they will usually pass both before and after the fix.

### Scope of the Matrix

| Finding while building the matrix | Action |
| --- | --- |
| The planned fix would handle a case wrongly | Adjust the fix direction — still within the RCA-named lines |
| The fix newly exposes a case (e.g. crash on `undefined`) | **In scope** — the fix must handle it; add a guard row |
| A pre-existing bug unrelated to the changed lines | **Observation** for a separate ticket — not a matrix row |

---

## STEP 6 — Test Plan for Phase 4

```text
TEST PLAN — ISSUE-002
  Regression test (must FAIL first, then PASS):
    file:  Mappers/PolicyMapper.test.ts
    name:  "handles null policyNumber [DEF-123 / ISSUE-002]"
    sets:  policyNumber = null

  Guard tests (must PASS after the fix):
    Mappers/PolicyMapper.test.ts   rows 2–7

  Blast-radius runs (must PASS after the fix):
    --files PolicyMapper.test.ts PolicyListContainer.test.tsx PolicySummary.test.tsx
    --related Portals/Sme/Features/Motor/PolicyList/Mappers/PolicyMapper.ts

  Untested consumers (gap): [list, or: None]
```

---

## STEP 7 — Structural Change and Non-Defects

```text
STRUCTURAL (escalate, do not fix):
  Figma    → new components · removed sections · changed hierarchy · changed responsive strategy
  Contract → new or removed endpoints · changed response shape (not just a renamed field)
  Record: "EXCEEDS DEFECT SCOPE — requires re-analysis via the Analysis Agent."
```

| Discovery | Status |
| --- | --- |
| Matches an **open** §12.4 limitation | `BLOCKED — known limitation LIM-xxx` |
| Matches §2 Scope NOT Implemented | `BLOCKED — out of scope` |
| Upstream contract gap | `BLOCKED — contract gap GAP-xxx` |
| Structural change | `BLOCKED — structural` |
| Behaviour matches the requirement | `NOT A DEFECT — behaves as specified` |

⚠️ A §12.4 row marked `✅ Resolved [DEF-xxx]` is closed — do not block against it. A blocked issue does **not** stop the run.

---

## Output — RCA_RESULT (Per Issue)

```text
ROOT CAUSE ANALYSIS — ISSUE-00N
  Category / Status:  [category] · DIAGNOSED | BLOCKED (reason) | NOT A DEFECT

  ── Current Code vs Summary ─────────────────────────────────
  Files read:        [list, as they are now]
  Drift:             [location · summary says · code does · explained by] | None
  Drift source:      prior fix DEF-xxx | developer (commit, date) | unknown

  ── Refetch Evidence (if any) ───────────────────────────────
  Artefact / Diff:   [artefact] · RELEVANT CHANGE | NO RELEVANT CHANGE

  ── Location & Mechanism ────────────────────────────────────
  File / Symbol:     [path] → [symbol]   (current line: N)
  Mechanism:         [what the code does vs what the requirement says]
  Expected:          [from DDN / DN / plan §4 §10 §11 / diff]
  Actual:            [observed in current code]

  ── Fault Origin ────────────────────────────────────────────
  Origin:            [one of seven]
  Reasoning:         [classification test answers]
  Learning:          YES → [rule + namespace] | NO → [why]
  Recurrence:        NEW | EXISTING RULE NOT APPLIED

  ── Blast Radius ────────────────────────────────────────────
  Consumers / tests: [consumer → test file]
  Untested:          [list, or: None]
  Risk:              LOW | MEDIUM | HIGH

  ── Fix Impact Analysis ─────────────────────────────────────
  [edge-case matrix]

  ── Test Plan ───────────────────────────────────────────────
  [regression test · guard tests · blast-radius runs]

  ── Dev Notes ───────────────────────────────────────────────
  DDN / DN / supersession

  ── Fix Direction (no code) ─────────────────────────────────
  [the minimal change, stated against the CURRENT code]

  ── Summary Rows For Phase 6 ────────────────────────────────
  Update for fix:    [§ rows]
  Reconcile drift:   [§ rows inspected that no longer match the code]
```

---

### Gate: Phase 3 Complete (Per Issue) When

```text
- [ ] Current code read for every file in scope — symbols found by name, not line
- [ ] Drift recorded, with its source from git (or "unknown")
- [ ] No drift treated as the defect itself
- [ ] Root cause named to file + symbol + mechanism, against the CURRENT code
- [ ] Expected behaviour sourced from DDN / DN / plan / diff — never from the code
- [ ] Fault origin classified; "is the code still as generated?" answered first
- [ ] Learning candidate drafted as a rule (agent miss / regression only)
- [ ] Blast radius lists consumers AND their test files; untested consumers flagged
- [ ] Edge-case matrix built across every applicable dimension
- [ ] Developer-introduced behaviour included as preserve-rows
- [ ] Test plan written: regression · guards · blast-radius runs
- [ ] Summary rows to update and to reconcile identified for Phase 6
- [ ] Structural change escalated; blocked issues recorded — run continues
- [ ] NO source file modified; NO test written
```

### Never Do

- **Never diagnose from the summary without reading the current file.**
- **Never locate code by summary line number** — find the symbol.
- **Never revert, or plan to revert, a developer's change** to match the summary.
- **Never treat drift as the defect.**
- **Never take expected behaviour from the code** — take it from the requirement.
- **Never classify a developer's change as an agent miss.**
- **Never skip the edge-case matrix** — a fix that passes the reported case can still break its neighbours.
- **Never leave a consumer's tests out of the plan.**
- Never name a file without the symbol and mechanism.
- Never ignore a refetch diff; never treat a negative diff as inconclusive.
- Never write a learning as a war story.
- Never diagnose a structural change as fixable.
- Never modify source or write tests in this phase.
- Never close or transition the defect ticket.
