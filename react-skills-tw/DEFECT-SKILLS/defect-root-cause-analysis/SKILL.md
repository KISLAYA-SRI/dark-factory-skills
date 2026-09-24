---
name: defect-root-cause-analysis
description: Use as Phase 3 of the FE Defect Fix workflow to locate the exact cause of an issue to file and line, classify fault origin across six categories to gate the learning update, and determine blast radius before any fix is proposed. Runs once per issue. Triggers include root cause analysis, RCA, locate defect, diagnose issue, or find the cause.
disable-model-invocation: true
---

## Defect Root Cause Analysis

### Purpose

This skill is **Phase 3** of the FE Defect Fix Agent, run **once per issue**. It answers three questions:

```text
1. WHERE is the fault?        → file + line + mechanism
2. WHY did it happen?          → fault origin (gates the learning update)
3. WHAT ELSE does it touch?    → blast radius
```

⚠️ **Naming a file is not a root cause.** *"The bug is in `PolicyCard.tsx`"* is a location, not a diagnosis. A root cause names the **line** and the **mechanism**: *"`PolicyMapper.ts:41` returns `undefined` for null `policyNumber` instead of the `'—'` default, so `PolicyCard` renders an empty span."*

---

## ⚠️ NO FIX IS WRITTEN IN THIS PHASE

This phase **diagnoses only**. Do not modify any source file. Do not write tests. The fix and its failing-first test belong to Phase 4.

The output must be precise enough that Phase 4 can write a test that **fails** against current code.

---

## 1. Locate — Use the Summary as an Index

The Code Generation Summary was designed for exactly this lookup. Start there, not in the codebase.

| Symptom | Look in | Finds |
| --- | --- | --- |
| Value blank / wrong / stale | **§7 Data Flow Trace** | Source → service → hook → mapper (null default + line) → prop |
| Wrong UI shown for a state | **§8 State Matrix** | Trigger condition + what renders + owning file |
| Authored content not appearing | **§5 Sitecore field → prop** | Field name, helper used, fallback when missing |
| Visual differs from design | **§9 Design Notes** | Tokens used, discrepancies recorded with deltas |
| Which files could cause this | **§3 File Inventory** | Complete scoped surface |
| **Was this touched before?** | **§13 Change Log** | **Prior defect fixes on this component** |
| Should this even work? | **§12.4 + §2** | Known limitation or explicit out-of-scope |
| Why was it built this way? | **§12.1 Decisions** | Original conflict resolution and reasoning |
| Which test should have caught it | **§10 AC → test mapping** | The test that exists but did not cover this path |

⚠️ **Sections 1–12 describe the CURRENT state** — every prior fix updated them in place. Rows carry `[DEF-xxx]` tags showing when they were last verified.

### ⚠️ Check §13 First for Regression Candidates

```text
IF a prior defect in §13 touched the same file, state, or field:
   → the current issue may be a REGRESSION from that fix
   → read that entry's "Sections Updated" and "Existing Tests Modified" blocks
   → if the prior fix's change plausibly caused this symptom:
        fault origin = REGRESSION FROM PRIOR FIX  ✅ writes a learning
```

This distinction matters enormously — regression is one of only **two** origins that write a learning. Without checking §13, a regression looks identical to a fresh agent miss and produces a wrong learning.

### If an Artefact Was Refetched in Phase 2

The **diff is the primary evidence**. Start there before opening any source file.

```text
Contract diff shows a renamed/removed field  → root cause is the rename
Design diff shows a changed property         → root cause is the design change
Diff shows NO relevant change                → the source did NOT change
                                                → the code is genuinely wrong
                                                → reclassify as an AGENT MISS
```

⚠️ A refetch that produces **no relevant diff** is a meaningful result: it disproves the source-change hypothesis. Record this explicitly — a negative diff is evidence, not a dead end.

### Diagnostic Paths by Category

**BFF / API — value blank or wrong**
```text
§7 Data Flow Trace for that field
  → check the mapper's null/missing default        ← most common cause
  → check the field path against §11.2 contract    ← renamed/absent field
  → check the query key in §6                      ← cache collision
  → check §13 — did a prior fix touch this mapper?
  → if refetched: check the diff first
  → open the mapper file and confirm the branch
```

**Sitecore — authored content missing**
```text
§5 field → prop mapping
  → field name mismatch (case-sensitive)           ← most common cause
  → helper not used (raw field access)
  → registry key vs folder name mismatch
  → if refetched: check the diff first
```

**State — wrong thing renders**
```text
§8 State Matrix → owning file for that state
  → check the trigger condition in the container
  → check ordering of state guards (isLoading before isError, etc.)
  → check §13 — did a prior fix change this state's renderer?
  → confirm against plan §10 expected behaviour
```

**RTL — wrong direction or mirroring**
```text
§3 File Inventory → the component
  → physical property used (ml-/mr-/pl-/pr-/text-left/text-right)
  → neutral icon incorrectly mirrored (eye/help/search/calendar)
  → symmetric icon or brand logo mirrored
  → Arabic text clipped by a fixed width
```

**UI / Visual — does not match design**
```text
FIRST: was a design-change signal flagged in intake?
  YES → check the Figma diff → design change, not an agent miss
  NO  → §9 Design Notes: which token was used vs which the design specifies
        → the code does not match the design it was BUILT against
        → AGENT MISS
```

**Responsive — breaks at a breakpoint**
```text
§3 → component · §9 → NFR exceptions
  → manual grid classes instead of Grid columns={12}
  → desktop-first classes instead of mobile-first
  → hardcoded px instead of token
```

**Missing AC**
```text
Plan §4 → the AC
  → Summary §11 AC Evidence: was it marked ✅ or ❌?
  → ❌ already → known, check §12 for the reason
  → ✅ claimed → the evidence was wrong; find what was actually built
```

**Regression**
```text
§13 Change Log → which prior fix introduced it
  → read that entry's Sections Updated and Existing Tests Modified
  → was an existing test weakened or removed by that fix?
```

⚠️ **Open the actual file and confirm.** The summary points you there; it does not replace reading the code. A root cause asserted from the summary alone is a guess.

---

## 2. ⚠️ Classify Fault Origin — This Gates the Learning Update

**Every issue must be classified into exactly one of six origins.** This is the most consequential output of this phase.

| Origin | Definition | Example | Learning? |
| --- | --- | --- | --- |
| **Agent miss** | The coding agent had everything needed and still got it wrong | Used `ml-4` instead of `ms-4`; forgot the empty state; skipped a null default | ✅ **Yes** |
| **Regression from prior fix** | An earlier defect fix broke this (see §13) | Fix for DEF-4380 removed a guard | ✅ **Yes** |
| **Upstream gap** | The Analysis Plan omitted or mis-specified it | Plan §10 never listed the empty state | ❌ Flag to developer |
| **Contract change** | Sitecore/BFF contract changed after generation | Field renamed post-generation | ❌ External |
| **Design change** | Figma updated after generation | Spacing token changed in a design revision | ❌ Code was correct for the old design |
| **Ambiguous requirement** | The AC was open to interpretation | "Show a friendly message" — no copy source specified | ❌ Story issue |

### The Classification Test

```text
Ask: "Given the Analysis Plan, the guidelines embedded in the coding skills,
      and the contracts/designs available AT GENERATION TIME —
      could the coding agent have got this right?"

  YES → Agent miss                          ✅ learning
  NO  → upstream / contract / design / ambiguous   ❌ no learning

Then ask: "Did a prior fix in §13 break this?"
  YES → Regression from prior fix           ✅ learning
```

### ⚠️ Distinguishing Design Change From Agent Miss

This is the hardest call and the one most likely to go wrong in both directions.

```text
Code matches the ORIGINAL Figma, design has since changed
  → DESIGN CHANGE. Code was correct. No learning.
  → Evidence: Figma diff shows the property changed

Code NEVER matched the original Figma
  → AGENT MISS. Code was always wrong. Learning required.
  → Evidence: §9 records a token the original design did not specify,
              OR a Figma diff shows NO change to the reported property
```

⚠️ **The decisive evidence is the diff.** If Phase 2 refetched and the reported property is **unchanged**, the design never changed — the code was wrong from the start. Classify as an agent miss regardless of what the ticket claimed.

⚠️ **Be honest in both directions.** Classifying an agent miss as a design or contract change loses the learning and the mistake repeats. Classifying an external change as an agent miss pollutes the learnings file.

### Learning Candidate (Agent Miss / Regression Only)

Draft the learning **now** — the mechanism is freshest here:

```text
LEARNING CANDIDATE
  Namespace:  # UI LEARNINGS | # LOGIC LEARNINGS | # TEST LEARNINGS | # STORYBOOK LEARNINGS
  Rule:       [the generalisable rule — NOT a description of this defect]
  Why missed: [what the agent did instead]
  Defect ref: {{ticket_id}} / ISSUE-00N
```

Write it as a **rule**, not a war story:

```text
✅ "RTL: carousel pager arrows must use rtl:rotate-180. Directional icons
    mirror; neutral icons (eye/help/search/calendar) never do."

❌ "In DEF-4521 the carousel arrows were pointing the wrong way in Arabic
    on the policy page and we had to fix them."
```

### Check Against Existing Learnings

The learnings file was loaded in Phase 2. If an existing rule **already covers** this failure mode:

```text
⚠️ RECURRENCE — the rule existed and was not applied.
   Flag for Phase 6 recurrence tracking.
   At recurrence ≥ 3 the SKILL itself is under-specified, not the learnings file.
```

---

## 3. Blast Radius — Before Proposing Any Fix

| Change location | Blast radius | How to determine |
| --- | --- | --- |
| **Design-system component** | ⚠️ **Every consumer** | `./src/component-catalogue.json` → composition + imports |
| Design token | ⚠️ Every component using it | Search token name |
| Shared feature component | 2+ features | §3 + catalogue |
| Mapper / service | All consumers of that data | §7 Data Flow Trace |
| Container | That feature only | §3 |
| Feature display component | Usually isolated | §3 |
| Sitecore entry | That rendering only | §5 |

```text
BLAST RADIUS — ISSUE-00N
  Changing:     Packages/DesignSystem/Foundation/Src/Atoms/Button.tsx
  Consumed by:  PolicyCard · ClaimForm · HeroBanner  (from catalogue)
  Risk:         MEDIUM — prop addition is backward compatible
  Must verify:  existing Button tests still pass
```

⚠️ **A design-system change is never low risk.** If the minimal fix for one component requires changing a shared component, consider whether the fix belongs at the consumer instead — and record the reasoning either way.

---

## 4. ⚠️ Structural-Change Detection

If a Phase 2 diff shows **structural** change, the issue exceeds surgical repair.

```text
STRUCTURAL indicators:
  Figma     → new components, removed sections, changed hierarchy,
              altered responsive strategy, new breakpoint behaviour
  Contract  → new endpoints, removed endpoints, changed response shape
              (not just a renamed field)

Record: "EXCEEDS DEFECT SCOPE — structural change detected.
         Requires re-analysis via the Analysis Agent."

Status: BLOCKED — structural
Do NOT propose a fix. The run continues with remaining issues.
```

⚠️ A renamed field is surgical. A restructured response shape is not. **The test:** *can this be fixed by changing existing code, or does it require new components, new layers, or a new plan?*

---

## 5. Handle Non-Defects Discovered During RCA

Triage already happened, but RCA can still reveal an issue is not fixable code:

| Discovery | Status |
| --- | --- |
| Matches a §12.4 Known Limitation (still open) | `BLOCKED — known limitation LIM-xxx` · name the upstream owner |
| Matches §2 Scope NOT Implemented | `BLOCKED — out of scope` · quote the exclusion |
| Root cause is an upstream contract gap (GAP-xxx) | `BLOCKED — contract gap GAP-xxx` · name the owner |
| Structural change required | `BLOCKED — structural` · route to Analysis Agent |
| Behaviour is correct per plan §10 / §4 | `NOT A DEFECT — behaves as specified` · quote the spec |

⚠️ If §12.4 shows a limitation marked `✅ Resolved [DEF-xxx]`, the gap is **closed** — do not block against it. The issue is something else.

⚠️ **A blocked issue does NOT stop the run.** Record it, carry it to the §13 entry, and continue.

---

## Output — RCA_RESULT (Per Issue)

```text
ROOT CAUSE ANALYSIS — ISSUE-00N
  Category:      [from intake]
  Status:        DIAGNOSED | BLOCKED (reason) | NOT A DEFECT

  ── Prior Fix Check (§13) ───────────────────────────────────
  Prior fixes touching this code: [DEF-xxx, or: None]
  Regression candidate:           YES → [which fix, what it changed] | NO

  ── Refetch Evidence (if applicable) ────────────────────────
  Artefact:      Figma | Sitecore | BFF | none refetched
  Diff result:   RELEVANT CHANGE FOUND | NO RELEVANT CHANGE
  Implication:   [e.g. "gap token changed 16→24px, explains the report"
                  or "reported property unchanged — source did NOT change,
                      code was always wrong → agent miss"]

  ── Location ────────────────────────────────────────────────
  File:          Portals/Sme/Features/Motor/PolicyList/Mappers/PolicyMapper.ts
  Line:          41
  Symbol:        mapPolicyResponse()
  Located via:   Summary §7 Data Flow Trace | §13 | diff | fallback discovery
  Confidence:    HIGH | REDUCED (fallback — no prior summary)

  ── Mechanism ───────────────────────────────────────────────
  [Precise description of what the code does vs what it should do]

  ── Expected vs Actual ──────────────────────────────────────
  Expected:      [from plan §10 / §4 / summary §7 / the diff]
  Actual:        [observed]

  ── Fault Origin ────────────────────────────────────────────
  Origin:        Agent miss | Regression | Upstream gap |
                 Contract change | Design change | Ambiguous
  Reasoning:     [answer to the classification test]
  Learning:      YES → [candidate rule + namespace]  |  NO → [why not]
  Recurrence:    NEW | EXISTING RULE NOT APPLIED (⚠️ flag for Phase 6)

  ── Blast Radius ────────────────────────────────────────────
  Changing:      [file]
  Consumed by:   [list from catalogue / §3]
  Risk:          LOW | MEDIUM | HIGH
  Must verify:   [existing tests that must still pass]

  ── Applicable Dev Notes ────────────────────────────────────
  DDN-xxx:       [if a defect note dictates the fix approach]
  DN-xxx:        [if a story note constrains it]
  Supersession:  [if DDN contradicts DN — record it]

  ── Fix Direction (NOT the fix itself) ──────────────────────
  [One or two lines on the minimal change required — enough for Phase 4
   to write a failing test. No code here.]

  ── Summary Sections To Update (for Phase 6) ────────────────
  [e.g. §3 file row · §7 policyNumber trace · §8 empty-state row · §10 test row]

  ── Scope Boundary (if artefact refetched) ──────────────────
  In scope:      [the reported delta only]
  Out of scope:  [other diff changes → observations for separate tickets]
```

⚠️ The **Summary Sections To Update** block feeds Phase 6 directly — identify it here while the diagnosis is fresh.

---

### Gate: Phase 3 Complete (Per Issue) When

```text
- [ ] Summary used as the index first; actual file opened and confirmed
- [ ] §13 Change Log checked for prior fixes on the same code
- [ ] Regression candidate identified or ruled out
- [ ] Refetch diff consulted FIRST where an artefact was refetched
- [ ] A "no relevant change" diff correctly reclassified as agent miss
- [ ] Root cause named to FILE + LINE + MECHANISM — not just a file
- [ ] Expected vs actual stated, sourced from plan/summary/diff
- [ ] Fault origin classified into ONE of the six origins
- [ ] Design change vs agent miss distinguished using diff evidence
- [ ] Learning candidate drafted as a RULE (agent miss / regression only)
- [ ] Existing learnings checked — recurrence flagged if the rule existed
- [ ] Blast radius determined; catalogue consulted for design-system changes
- [ ] Structural change detected and escalated, not diagnosed as fixable
- [ ] Applicable DDN / DN identified; any supersession recorded
- [ ] Confidence flagged REDUCED if fallback discovery was used
- [ ] Summary sections to update identified for Phase 6
- [ ] Scope boundary recorded where an artefact was refetched
- [ ] Blocked / not-a-defect issues recorded with justification — run continues
- [ ] NO source file modified; NO test written
```

### Never Do

- **Never name a file as the root cause without the line and mechanism.**
- **Never assert a cause from the summary alone** — open and confirm the file.
- **Never skip the §13 check** — regressions are indistinguishable from agent misses without it.
- **Never ignore a refetch diff** — it is the primary evidence when present.
- **Never treat a "no relevant change" diff as inconclusive** — it proves agent miss.
- **Never skip fault origin classification** — it gates the learning loop.
- **Never classify an agent miss as a design or contract change** to avoid writing a learning.
- **Never classify an external change as an agent miss** — it pollutes the learnings file.
- **Never write a learning as a war story** — write a generalisable rule.
- **Never propose a fix without determining blast radius.**
- **Never diagnose a structural change as fixable** — escalate to the Analysis Agent.
- **Never block against a limitation already marked Resolved.**
- **Never modify source or write tests in this phase.**
- **Never stop the run because an issue is blocked** — record and continue.
- **Never close or transition the defect ticket** — lifecycle belongs to the developer.
- Never re-read the parent story ticket or re-run analysis.
