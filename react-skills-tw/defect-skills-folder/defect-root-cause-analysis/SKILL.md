---
name: defect-root-cause-analysis
description: Use as Phase 3 of the FE Defect Fix workflow to read the current code first, detect drift from the Code Generation Summary, locate the exact cause to file and symbol, classify fault origin across seven categories to gate the learning update, determine blast radius with concrete test files, and build the edge-case matrix and test plan that Phase 4 executes. Runs once per issue. Triggers include root cause analysis, RCA, locate defect, diagnose issue, or impact analysis.
disable-model-invocation: true
---

## Defect Root Cause and Impact Analysis

### Purpose — five questions, once per issue

```text
1. What does the code do NOW?        current code first; drift recorded
2. WHERE is the fault?               file + symbol + mechanism
3. WHY did it happen?                fault origin (gates the learning)
4. What else does it touch?          blast radius, with covering test files
5. What must STILL work after a fix? the edge-case matrix
```

⚠️ **A file name is not a root cause.** Name the **symbol** and the **mechanism**: *"`PolicyMapper.ts → mapPolicyResponse()` returns `undefined` for null `policyNumber` instead of `'—'`, so `PolicyCard` renders an empty span."*

⚠️ **No fix, no tests in this phase.** The output must be precise enough for Phase 4 to write a test that fails.

---

## STEP 1 — Read the current code first

Developers change generated code. The summary says **where to look**; only the file says **what is there**.

```text
For every file §3 / §5 / §7 / §8 points to:
  1. OPEN it as it is now
  2. FIND the symbol BY NAME — never by the summary's line number
  3. READ the actual branches, defaults and conditions
  4. COMPARE with what the summary records
```

### Drift

```text
DRIFT — ISSUE-002
  Location:    Mappers/PolicyMapper.ts → mapPolicyResponse()
  Summary §7:  null policyNumber → "—"
  Code now:    null → policy.legacyNumber ?? ""
  Explained:   git — 2026-08-21, developer commit, no §13 entry
  → POST-GENERATION MANUAL CHANGE
```

Load git history **only** when drift must be explained:

```bash
git log -L :mapPolicyResponse:path/to/PolicyMapper.ts --format="%h %ad %an %s" --date=short
```

| Evidence | Meaning |
| --- | --- |
| Changed after generation, matches a §13 `[DEF-xxx]` | Prior defect fix → regression candidate |
| Changed after generation, no §13 entry | Developer → post-generation manual change |
| Unchanged since generation | As the agent generated it |
| No git | Record `drift source: unknown` — do not guess |

⚠️ **Drift is information, not a defect.**

```text
❌ Never revert code to match the summary
❌ Never classify drift itself as the defect
✅ Diagnose against the REQUIREMENT · build the fix on the CURRENT code
```

### The two questions

| Question | Answer from |
| --- | --- |
| What **should** happen? | DDN → DN → refetch diff → Analysis Plan §4/§10/§11 *(load only if needed)* |
| What **does** happen? | Current code → git → summary (map only) |

⚠️ If code and summary agree but the ticket still reports a problem, you cannot tell defect from change-request without plan §4/§10. **That is the trigger to load them.**

---

## STEP 2 — Locate

| Symptom | Start at | Then verify in |
| --- | --- | --- |
| Value blank / wrong | §7 Data Flow Trace | The mapper/service/hook as it is now |
| Wrong UI for a state | §8 State Matrix | The container's current guards |
| Authored content missing | §5 field → prop | Current field access and helper |
| Visual differs from design | §9 Design Notes | Current classes and tokens |
| Candidate files | §3 File Inventory | Plus files the developer added since |
| Touched before? | §13 Change Log | The prior fix in the current file |
| Should it work at all? | §12.4 + §2 | — |

⚠️ Files added after generation are **not** in §3. Follow imports the summary never mentions.

**If an artefact was refetched**, the diff is primary evidence. A diff showing **no relevant change** disproves the source-change hypothesis → the code was always wrong → **agent miss**.

---

## STEP 3 — Fault origin (gates the learning)

| Origin | Definition | Learning? |
| --- | --- | --- |
| **Agent miss** | Code as generated; agent had what it needed | ✅ |
| **Regression from prior fix** | A §13 fix changed this and broke it | ✅ |
| Upstream gap | Plan omitted or mis-specified it | ❌ |
| Contract change | Sitecore/BFF changed after generation | ❌ |
| Design change | Figma changed after generation | ❌ |
| **Post-generation manual change** | A developer wrote the faulty line | ❌ |
| Ambiguous requirement | AC open to interpretation | ❌ |

```text
1. Is the faulty code still as generated?
     No, by a §13 fix      → REGRESSION                      ✅
     No, by a developer    → POST-GENERATION MANUAL CHANGE   ❌
     Yes → continue
2. Given the plan, guidelines and contracts available AT GENERATION TIME,
   could the agent have got this right?
     Yes → AGENT MISS      ✅        No → external / upstream / ambiguous  ❌
```

⚠️ **Step 1 comes first.** Otherwise a developer's bug teaches the coding agent a rule for code it never wrote.

⚠️ **Design change vs agent miss:** if a refetch shows the reported property **unchanged**, the design never changed — agent miss, whatever the ticket claimed.

For agent miss / regression, draft the learning **now** as a generalisable rule (not a war story) with its namespace. If an existing learning already covers it → **recurrence**, flag for Phase 6.

---

## STEP 4 — Blast radius, with test files

Phase 4 executes these, so name **files**, not concepts.

| Change location | Consumers | Find their tests via |
| --- | --- | --- |
| Design-system component | ⚠️ every consumer | catalogue + import search; `--related-scope all` |
| Design token | every user | search the token name |
| Shared component | 2+ features | catalogue + import search |
| Mapper / service | every data consumer | §7 + import search |
| Container / feature / Sitecore entry | usually local | co-located tests |

```bash
grep -rl --include=*.ts --include=*.tsx "mapPolicyResponse" Portals/ Packages/
```

⚠️ **A consumer with no test is a gap** — record it; Phase 4 adds a guard test or §13 flags it unverified.

---

## STEP 5 — Edge-case matrix

> **Change narrowly. Verify widely.** The minimal-change contract limits what you edit, never what you check.

Enumerate every case flowing through the lines about to change. Each row becomes a Phase 4 guard test.

| Dimension | Always check |
| --- | --- |
| **Data** | null · undefined · `""` · whitespace · `0`/`false` · empty array · one item · many · overlong · wrong type |
| **Branches** | **Both sides** — especially the path that was already correct |
| **Locale** | `en` **and** `ar` — an RTL fix must not break LTR |
| **RTL numerics** | LTR content inside RTL text needs `<bdi>` |
| **Responsive** | 390 · 1024 · 1700 when layout is involved |
| **State** | Transitions **into and out of** the changed state |
| **Interaction** | Rapid repeat · keyboard as well as pointer · disabled path |
| **Persona** | Every role variant |
| **Consumers** | Each blast-radius consumer's use of the changed behaviour |
| **Prior fixes** | Behaviour a §13 fix established here |
| **Developer changes** | Behaviour a manual change introduced — **must be preserved** unless the requirement says otherwise |

```text
FIX IMPACT — ISSUE-002   (PolicyMapper.ts → mapPolicyResponse, policyNumber fallback)
| # | Case                        | Input                  | Expected   | Type       |
| 1 | Reported defect             | null                   | "—"        | REGRESSION |
| 2 | Undefined / "" / whitespace | absent · "" · "   "    | "—"        | GUARD      |
| 3 | Valid value (untouched)     | "POL-001"              | unchanged  | GUARD      |
| 4 | Developer legacy fallback   | null + legacy "L-9"    | "L-9"      | GUARD      |
| 5 | Arabic locale               | dir="rtl"              | <bdi>      | GUARD      |
| 6 | Consumer PolicySummary      | null                   | "—", no crash | BLAST   |
```

⚠️ **Only REGRESSION rows must fail first.** GUARD and BLAST rows protect behaviour that is already correct.

| Finding while building the matrix | Action |
| --- | --- |
| The planned fix handles a case wrongly | Adjust the fix — still within RCA-named lines |
| The fix newly exposes a case | **In scope** — handle it, add a guard row |
| A pre-existing unrelated bug | **Observation** for a separate ticket |

---

## STEP 6 — Test plan + escalation

```text
TEST PLAN — ISSUE-002
  Regression (must FAIL first):  Mappers/PolicyMapper.test.ts
                                 "handles null policyNumber [DEF-486 / ISSUE-002]"
  Guards (must PASS):            rows 2–5
  Blast radius (must PASS):      --files PolicyMapper.test.ts PolicyListContainer.test.tsx
                                 --related Mappers/PolicyMapper.ts
  Untested consumers:            [list, or None]
```

**Structural change → escalate, do not fix.** New/removed components or endpoints, changed hierarchy, changed response shape, altered responsive strategy:

```text
BLOCKED — structural. Requires re-analysis via the Analysis Agent.
```

⚠️ A renamed field is surgical; a restructured response shape is not.

**Other non-defects:** open §12.4 limitation → `BLOCKED — known limitation LIM-xxx` · §2 exclusion → `BLOCKED — out of scope` · contract gap → `BLOCKED — GAP-xxx` · matches the requirement → `NOT A DEFECT`. A `✅ Resolved` row is closed — do not block against it. **A blocked issue does not stop the run.**

---

## Output — one block per issue, no narration

```text
RCA — ISSUE-002 · DIAGNOSED
  Drift:      mapPolicyResponse() null → legacyNumber ?? ""  (developer, a1b2c3)
  Location:   Mappers/PolicyMapper.ts → mapPolicyResponse()  :47
  Mechanism:  empty-string fallback renders blank; §7 records "—"
  Expected:   "—"  (summary §7)          Actual: ""
  Origin:     Post-generation manual change → no learning
  Blast:      PolicyListContainer.test.tsx · PolicySummary.test.tsx
  Matrix:     6 rows (1 regression · 4 guard · 1 blast)
  Plan:       [test plan]
  §6 updates: §3 rows · §7 trace (fix + drift)
```

---

### Gate (per issue)

```text
- [ ] Current code read; symbols found by name, not line
- [ ] Drift recorded with its source (or "unknown"); not treated as the defect
- [ ] Root cause = file + symbol + mechanism
- [ ] Expected behaviour from the requirement, never from the code
- [ ] Origin classified; "still as generated?" answered first
- [ ] Learning drafted as a rule (agent miss / regression only)
- [ ] Blast radius lists consumers AND test files; untested consumers flagged
- [ ] Edge-case matrix across every applicable dimension, incl. developer behaviour
- [ ] Test plan written; summary rows for Phase 6 identified
- [ ] Structural change escalated; blocked issues recorded — run continues
- [ ] NO source modified; NO test written
```

### Never

- Never diagnose from the summary without opening the file.
- Never locate code by the summary's line number.
- Never revert, or plan to revert, a developer's change.
- Never take expected behaviour from the code.
- Never classify a developer's change as an agent miss.
- Never skip the edge-case matrix — a fix that passes the reported case can break its neighbours.
- Never leave a consumer's tests out of the plan.
- Never diagnose a structural change as fixable.
- Never modify source or write tests here.
- Never narrate beyond the per-issue output block.
