---
name: defect-fix-and-regression-test
description: Use as Phase 4 of the FE Defect Fix workflow to write a failing regression test, apply the minimal fix, and prove the test now passes. Enforces the minimal-change contract, scope-to-diff for refetched artefacts, and delegates to coding skills by issue category for standards. Runs once per issue. Triggers include apply fix, fix defect, regression test, or failing-first test.
disable-model-invocation: true
---

## Defect Fix and Regression Test

### Purpose

This skill is **Phase 4** of the FE Defect Fix Agent, run **once per issue**. Fix and test are a **single atomic unit** — never separate phases — because the failing-first protocol is what proves the root cause was correct.

```text
write failing test → apply minimal fix → prove it passes → verify no regressions
```

---

## ⚠️ THE FAILING-FIRST PROTOCOL (MANDATORY)

```text
STEP 1  Write a regression test expressing the EXPECTED behaviour
STEP 2  Run it → it MUST FAIL against current code       ← proves the RCA
STEP 3  Apply the minimal fix
STEP 4  Run it → it MUST PASS
STEP 5  Run existing tests for every touched file → no regressions
```

### ⚠️ If the test does NOT fail at Step 2

**Stop. The root cause is wrong.** Return to Phase 3.

A test that passes before the fix proves nothing. Common causes:

```text
- The test asserts the wrong thing
- The test exercises a different code path than the defect
- The root cause was located in the wrong file or branch
- The defect only reproduces under a condition the test does not set up
  (locale, persona, viewport, specific data shape)
```

⚠️ Do **not** proceed on an unproven root cause. Do **not** adjust the test until it fails — that inverts the logic and produces a test shaped around an assumption.

---

## ⚠️ THE MINIMAL-CHANGE CONTRACT (NON-NEGOTIABLE)

```text
CHANGE ONLY what Root Cause Analysis explicitly named.

❌ No refactoring of surrounding code
❌ No "while I'm here" improvements
❌ No renaming, reordering, or reformatting
❌ No extracting helpers or tidying imports
❌ No dependency changes
❌ No unrelated file touches
❌ No adding features the defect did not ask for
❌ No "fixing" other problems you notice
```

### The Test

```text
For every line you are about to change, ask:

  "Did RCA name this line as part of the root cause?"

  YES → change it
  NO  → do not touch it. Record as an observation for a separate ticket.
```

⚠️ A defect fix that also refactors is **not a defect fix** — it is an untested change set masquerading as one. Every extra changed line is regression surface the developer did not ask for and will not review carefully.

### Unrelated Problems

```text
OBSERVATION (not fixed — separate ticket recommended)
  File:     Portals/Sme/Features/Motor/PolicyList/Hooks/usePolicyList.ts:22
  Issue:    staleTime hardcoded rather than sourced from constants
  Why not fixed: outside ISSUE-002 root cause; would expand regression surface
```

Record it in the FIX_RESULT. **Do not fix it.** Phase 6 carries it into the §13 Change Log entry.

---

## ⚠️ SCOPE-TO-DIFF — REFETCHED ARTEFACTS

When Phase 2 refetched an artefact, the diff may contain **many** changes — only one of which the defect reports.

```text
Figma diff shows:
  ✅ gap 16px → 24px         ← defect reports this  → FIX
  ⛔ new CTA button added     ← not reported → OBSERVATION, separate ticket
  ⛔ heading token changed    ← not reported → OBSERVATION, separate ticket
  ⛔ divider removed          ← not reported → OBSERVATION, separate ticket
```

⚠️ **A refreshed artefact is NOT licence to re-implement the component against the latest version.** The minimal-change contract still governs.

```text
❌ "The design was updated, so I brought the component fully up to date"
✅ "The design changed the gap token; the defect reported spacing;
    I changed the gap token only. Three other design changes recorded
    as observations."
```

### Structural Change — Escalate, Do Not Attempt

If Phase 3 flagged the issue as `BLOCKED — structural`:

```text
Do NOT attempt the fix.
Record: "EXCEEDS DEFECT SCOPE — requires re-analysis via the Analysis Agent."
Continue with the remaining issues.
```

---

## Skill Delegation by Category

Load coding skills for their **standards, guidelines and conventions** — tokens, RTL rules, layering, naming, test conventions.

| Category | Skills loaded |
| --- | --- |
| UI / Visual | `presentational-ui-generation` |
| RTL | `presentational-ui-generation` |
| Responsive | `presentational-ui-generation` |
| Accessibility | `presentational-ui-generation` |
| Media | `presentational-ui-generation` + `frontend-media-integration` |
| Sitecore | `sitecore-rendering-integration` |
| BFF / API / mapper | `frontend-logic-integration` |
| State / forms | `frontend-logic-integration` + `frontend-state-and-form-management` |
| Any file move or rename | `+ repository-structure-governance` |
| DS component public API changed | `+ storybook-and-component-catalogue` |
| **Always** | `developer-notes-protocol` · `frontend-test-generation` |

⚠️ **Load per issue; discard before the next.** An RTL issue followed by a BFF issue should not carry `presentational-ui-generation` into the second — dead context increases the chance of drift.

### ⚠️ Coding Skills Are NOT Licence to Regenerate

Those skills are written for *generation* and carry completeness instincts — "generate all states", "cover every variant", "implement every §10 state". **In defect mode the minimal-change contract overrides all of it.**

```text
Use coding skills for:   HOW to write the fix correctly
                         (which token, which property, which layer, which convention)

Never use them for:      Regenerating the file
                         Adding states/variants the defect did not mention
                         Restructuring to match the ideal shape
                         "Completing" what looks partially implemented
```

### If a DS Component Changed

If the fix modifies a design-system component's public API — a new prop, a new variant — `storybook-and-component-catalogue` is loaded to update the story and the catalogue entry.

⚠️ Update **only** the entry for the changed component, reflecting **only** the change made. Do not regenerate the story file or rewrite unrelated catalogue entries.

---

## Applying the Fix

### Order of Operations

```text
1. Confirm the RCA finding by opening the file at the named line
2. Confirm which DDN / DN apply to this issue
3. Confirm the scope boundary if an artefact was refetched
4. Write the failing test → verify it fails
5. Apply the minimal change
6. Verify the test passes
7. Run existing tests for all touched files
8. Record what changed — including which summary sections Phase 6 must update
```

### Dev Notes Precedence

```text
DDN-xxx  Defect Dev Notes   ← TOP priority; if it dictates the approach, follow it exactly
DN-xxx   Story Dev Notes    ← still binding unless a DDN supersedes
```

⚠️ If a **DDN specifies how to fix**, that instruction overrides your own judgement — even if you would have chosen differently. Apply it literally. If it contradicts a DN, follow the DDN and record the supersession.

### Fix Quality Standards

The fix must conform to the same standards as generated code:

```text
✅ Design tokens — never hardcoded colour/spacing/typography values
✅ Logical properties for RTL (ms-/me-/ps-/pe-/text-start/text-end)
✅ cn() for class composition
✅ Typed — no `any`, no @ts-ignore without explanation
✅ Prop-driven — no hardcoded labels, copy, routes, or URLs
✅ Constants for endpoints, query keys, magic values
✅ Service layer stays framework-agnostic
✅ Correct layer — mapper defaults in the mapper, not the component
```

⚠️ A fix that introduces a hardcoded value to resolve a defect creates a new defect. If the correct value has no source, that is a **contract gap** — record it rather than hardcoding.

⚠️ If a design-change fix requires a token that does not exist, **create the primitive and record it** — same rule as generation. Never hardcode the raw value.

---

## Writing the Regression Test

### ⚠️ This Is a Different Mode From Test Generation

| | `frontend-test-generation` | Here |
| --- | --- | --- |
| Written from | Generated source (ground truth) | **Expected behaviour** |
| Source state | Correct | **Broken** |
| First run | Passes | **MUST FAIL** |
| Purpose | Coverage | **Prove the root cause + prevent recurrence** |

Delegate to `frontend-test-generation` for **conventions** — co-location, explicit Vitest imports, `userEvent`, accessible queries, package include patterns. The **failing-first protocol is owned here**.

### Test Placement

```text
✅ Co-located with the source file being fixed
✅ Added to the EXISTING test file where one exists
✅ New test file only if none exists for that source
❌ Never a separate __tests__ folder
❌ Never .spec.* — only .test.*
```

### Test Naming — Reference the Defect

```text
it("renders em-dash when policyNumber is null [DEF-4521 / ISSUE-002]", async () => {
```

The defect reference makes the test's origin obvious when it fails in future — and signals it must not be casually deleted.

### Test Must Reproduce the Exact Condition

```text
⚠️ The test must set up the SAME condition that triggers the defect:

  RTL issue        → render with dir="rtl"
  Locale issue     → set the locale the defect reports
  State issue      → mock the hook into that exact state
  Null-data issue  → mock the response with that field null/absent
  Persona issue    → set the persona from the defect evidence
  Viewport issue   → set the viewport from the defect evidence
  Design change    → assert the NEW expected token/value
```

A test that does not reproduce the reported condition cannot fail first — and cannot prevent recurrence.

---

## ⚠️ Never Weaken an Existing Test

```text
❌ Never delete an existing test to make a fix pass
❌ Never skip (.skip) or comment out an existing test
❌ Never loosen an assertion to accommodate the fix
❌ Never change expected values to match new (wrong) behaviour
```

If an existing test now fails, **one of two things is true**:

| Situation | Action |
| --- | --- |
| The fix is wrong | Return to Phase 3 — the RCA or the fix approach is incorrect |
| The test encoded the old design/contract | Update it, and **record the change and reasoning** |

⚠️ The second case is common after a **design change** or **contract change** — an existing test may assert the old token or field name. Updating it is legitimate, but it must be **explicit in the §13 Change Log entry**. A silently-updated test is how defects get re-introduced.

---

## Output — FIX_RESULT (Per Issue)

```text
FIX APPLIED — ISSUE-00N
  Status:          FIXED | BLOCKED (not fixed — see RCA) | NOT A DEFECT

  ── Regression Test ─────────────────────────────────────────
  Test file:       [path]
  Test name:       [name with defect reference]
  Condition set:   [locale / state / data shape reproduced]
  Failed first:    ✅ YES — [assertion that failed and why]
  Passes now:      ✅ YES

  ── Fix ─────────────────────────────────────────────────────
  File:            [path]
  Lines changed:   [line numbers / range]
  Change:          [precise description of the minimal edit]
  Skills used:     [which coding skills provided the standards]
  DDN applied:     [DDN-xxx, or: None]
  New token:       [if created — name, value, why — else: None]

  ── Summary Sections To Update (Phase 6) ────────────────────
  §3   → [file rows to update/add]
  §7   → [field trace — new line number / changed default]
  §8   → [state row — changed renderer or owning file]
  §10  → [test row — case count increase]
  §5   → [field mapping, if changed]
  §9   → [token/exception, if changed]
  §12.4 → [limitation to mark Resolved, if applicable]

  ── Scope Boundary (if artefact refetched) ──────────────────
  Diff changes in scope:     [the reported delta]
  Diff changes NOT applied:  [list → observations]

  ── Regression Check ────────────────────────────────────────
  Existing tests for touched files: PASS | [failures + resolution]
  Blast-radius consumers verified:  [list, or: N/A]
  Existing test modified:           NO | YES → [which + why]

  ── Scope Discipline ────────────────────────────────────────
  Files touched:   [count] — matches RCA finding: ✅
  Observations recorded (not fixed): [list, or: None]
```

⚠️ The **Summary Sections To Update** block is what keeps the parent summary accurate. Capture it here, while the change is fresh — Phase 6 applies it.

---

### Gate: Phase 4 Complete (Per Issue) When

```text
- [ ] Regression test written and PROVEN TO FAIL against current code
- [ ] Test reproduces the exact reported condition (locale/state/data/persona/viewport)
- [ ] Test references the defect ID in its name
- [ ] Test co-located; added to existing file where one exists; .test.* naming
- [ ] Minimal fix applied to disk at the RCA-named location
- [ ] ONLY RCA-named code changed — no refactoring, renaming, or tidying
- [ ] Scope-to-diff honoured where an artefact was refetched
- [ ] Unapplied diff changes recorded as observations
- [ ] Structural-change issues escalated, NOT attempted
- [ ] Test now passes
- [ ] Existing tests for all touched files still pass
- [ ] Blast-radius consumers verified for design-system changes
- [ ] Storybook/catalogue updated ONLY if a DS public API changed
- [ ] No existing test weakened, skipped, or deleted
- [ ] Any existing-test modification recorded with reasoning
- [ ] Fix conforms to token / RTL / typing / prop-driven standards
- [ ] New tokens recorded, never hardcoded values
- [ ] Applicable DDN applied literally; supersession recorded
- [ ] Summary sections to update captured for Phase 6
- [ ] Unrelated problems recorded as observations, NOT fixed
```

### Never Do

- **Never apply a fix without a test that failed first.**
- **Never adjust the test until it fails** — that inverts the logic.
- **Never proceed on an unproven root cause** — return to Phase 3.
- **Never change code RCA did not name.**
- **Never refactor, rename, reformat, or tidy while fixing.**
- **Never fix an unrelated problem you notice** — record it as an observation.
- **Never re-implement a component against a refreshed design** — fix the reported delta only.
- **Never attempt a structural change** — escalate to the Analysis Agent.
- **Never regenerate a component** because a coding skill was loaded.
- **Never add states, variants, or features the defect did not mention.**
- **Never weaken, skip, or delete an existing test** to make a fix pass.
- **Never silently update an existing test** — record the change and reasoning.
- **Never hardcode a value** to resolve a defect — create a token or record a contract gap.
- **Never introduce `any`, physical RTL properties, or raw hex/px values.**
- **Never override a DDN** with your own preferred approach.
- **Never regenerate a story file or rewrite unrelated catalogue entries.**
- Never close or transition the defect ticket.
