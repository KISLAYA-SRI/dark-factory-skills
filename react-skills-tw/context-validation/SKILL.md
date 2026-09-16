---
name: context-validation
description: Use this skill to verify that every required external artefact — Sitecore API JSON, BFF API specs, and Figma Design Intent JSONs — was found and written to disk. Classification-aware hard gate. Halts the entire agent when required context is missing. Triggers include context validation, artefact validation, verify context, required context check, or context gate.
---

## Context Validation

### Purpose

This skill verifies that every external artefact the story depends on was both **found in the story** and **successfully written to disk** by Context Gathering.

The required set depends on the component classification produced in Phase 3:

```text
Pure Presentational  →  Sitecore + Figma required.  BFF NOT checked.
Transactional        →  Sitecore + Figma + BFF ALL required.
Hybrid               →  Sitecore + Figma + BFF ALL required.
```

There are exactly two outcomes: **SUCCESS** (continue) or **REQUIRED CONTEXT NOT FOUND** (halt everything).

⚠️ **Prerequisites:** Phase 2 must have produced the `CONTEXT_MANIFEST`, and Phase 3 must have produced the classification.

---

### ⚠️ THIS GATE IS DIFFERENT FROM THE CONTEXT GATHERING FAIL-STOP

Do not confuse the two. They operate at different levels and have opposite consequences.

|            | Phase 2 — Context Gathering                   | Phase 4 — Context Validation        |
| ---------- | --------------------------------------------- | ----------------------------------- |
| Scope      | Per task                                      | Whole agent                         |
| On failure | Stop **that task only**; other tasks continue | **Halt everything**                 |
| Records    | Failure noted in CONTEXT_MANIFEST             | Error report; no documents produced |
| Downstream | Later phases still run                        | **No later phase runs**             |

Context Gathering is permissive so that one broken fetch does not block the others. Context Validation is strict: once we know the classification, we know exactly what is mandatory, and missing mandatory context makes the analysis unsound.

---

### Inputs

| Input             | Source                                                             | Required?                                       |
| ----------------- | ------------------------------------------------------------------ | ----------------------------------------------- |
| CONTEXT_MANIFEST  | Phase 2 — Context Gathering                                        | **Mandatory**                                   |
| Classification    | Phase 3 — Story Analysis (Presentational / Transactional / Hybrid) | **Mandatory**                                   |
| Sitecore artefact | `./.SC_API_SPEC/sitecore-api.json`                                 | Existence checked                               |
| BFF artefacts     | `./.BFF_API_SPEC/{operationId}.json`                               | Existence checked (not for Pure Presentational) |
| Figma artefacts   | `./figma-output/figma_design_{Node_id}_-context.json`              | Existence checked                               |

If either the CONTEXT_MANIFEST or the classification is unavailable, **halt** — this gate cannot make a sound decision without both.

---

### The Two-Part Check

Every artefact must pass **both** parts. Passing only one is a failure.

```text
PART 1 — DECLARED?      Was the endpoint / URL found in the JIRA story?
PART 2 — MATERIALISED?  Was the artefact actually written to disk,
                        and is it non-empty and readable?
```

A Figma URL named in the story but never extracted is a **failure**. A Sitecore endpoint that produced an empty file is a **failure**. Silence is never treated as success.

---

### Validation Matrix

| Artefact                                                                        | Pure Presentational | Transactional | Hybrid      |
| ------------------------------------------------------------------------------- | ------------------- | ------------- | ----------- |
| **Sitecore** — at least one endpoint declared AND `sitecore-api.json` written   | ✅ Required         | ✅ Required   | ✅ Required |
| **Figma** — at least one URL declared AND every declared URL has a context file | ✅ Required         | ✅ Required   | ✅ Required |
| **BFF** — every operationId declared has a `{operationId}.json` written         | ⛔ **Not checked**  | ✅ Required   | ✅ Required |

⚠️ **Pure Presentational skips the BFF check entirely.** A presentational component has no API integration, so an absent BFF spec is correct, not a failure. Do not report it, do not warn about it, and do not treat `BFF API NOT FOUND / NOT REQUIRED` as an error.

⚠️ **Hybrid is validated as Transactional.** A Hybrid component contains transactional regions, so all three artefact types are mandatory.

---

### ⚠️ Classification Mismatch Check

Before applying the rules above, cross-check the classification against what Context Gathering actually found:

| Situation                                                                             | Action                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Classification = **Presentational**, but BFF operationIds **were** found in the story | ⚠️ **Classification mismatch.** A component consuming a backend API is not Presentational. Report this as a validation failure and halt — the classification must be corrected before analysis continues. |
| Classification = **Transactional**, and no BFF operationIds were found                | Standard failure — BFF is required and was not discovered. Report `required context not found`.                                                                                                           |

This check prevents a mis-classified story from silently skipping the BFF requirement.

---

### Validation Procedure

**Step 1 — Read the classification.** Presentational → presentational rules. Transactional or Hybrid → transactional rules.

**Step 2 — Run the classification mismatch check.**

**Step 3 — Validate Sitecore.**

- At least one Sitecore endpoint declared in the story? If none → FAIL.
- `./.SC_API_SPEC/sitecore-api.json` exists, non-empty, readable? If not → FAIL.
- CONTEXT_MANIFEST records a Sitecore fetch failure? → FAIL.

**Step 4 — Validate Figma.**

- At least one Figma URL declared in the story? If none → FAIL.
- Every declared URL has a corresponding `figma-output/figma_design_{Node_id}_-context.json`, non-empty and readable? Any missing → FAIL.
- CONTEXT_MANIFEST records a Figma fetch failure for any URL? → FAIL.

**Step 5 — Validate BFF.** _(Transactional and Hybrid only — skip entirely for Pure Presentational.)_

- Every operationId declared in the story has a `./.BFF_API_SPEC/{operationId}.json`, non-empty and readable? Any missing → FAIL.
- CONTEXT_MANIFEST records a BFF fetch failure for any operationId? → FAIL.
- No operationIds declared at all, for a Transactional/Hybrid story? → FAIL. A transactional component requires backend integration by definition.

**Step 6 — Decide.** Any FAIL in the applicable checks → emit the failure report and **HALT**. All applicable checks pass → emit SUCCESS and continue.

⚠️ Check **every** applicable artefact before reporting, even after the first failure. A single report listing all missing context is far more useful to the developer than halting on the first problem.

---

### Output — SUCCESS

```text
CONTEXT VALIDATION: SUCCESS

Classification: [Presentational | Transactional | Hybrid]

Sitecore  ✅  [n] endpoint(s) declared · ./.SC_API_SPEC/sitecore-api.json present
Figma     ✅  [n] URL(s) declared · [n] context file(s) present
BFF       ✅  [n] operationId(s) declared · [n] spec file(s) present
             (or: Not applicable — Pure Presentational component)

All required context is available. Proceeding to Figma Analysis.
```

### Output — FAILURE

```text
CONTEXT VALIDATION: REQUIRED CONTEXT NOT FOUND

Classification: [Presentational | Transactional | Hybrid]
Required for this classification: [Sitecore + Figma | Sitecore + Figma + BFF]

MISSING CONTEXT
  [✗] Sitecore — [no endpoint declared in story | artefact not created | fetch failed: reason]
  [✗] Figma    — [no URL declared | missing context file for: <url/node> | fetch failed: reason]
  [✗] BFF      — [missing spec for operationId: <id> | fetch failed: reason]

PRESENT CONTEXT
  [✓] [artefact] — [detail]

ANALYSIS HALTED.
No further phases will run. No output documents have been produced.

REQUIRED ACTION
  [specific, actionable step per missing item — e.g. "Add the Figma URL for the
   mobile viewport to the story", "Confirm the Sitecore endpoint path",
   "Verify operationId <id> exists in the API catalogue"]
```

⚠️ On failure, produce **no** `ANALYSIS_PLAN.md`, **no** `DEV_REVIEW.md`, and **no** `CODING_AGENT_CHECKLIST.md`. A partial analysis built on missing context is worse than no analysis — the Coding Agent would treat it as complete.

---

### Halt Behaviour

On failure:

- **Do NOT** run Figma Analysis, API Analysis, Component Breakdown, Reuse Validation, or Output Production.
- **Do NOT** produce any output document.
- **Do NOT** invent, infer, or substitute any missing endpoint, field, node, token, or component.
- **Do NOT** attempt to re-fetch — acquisition already ran and recorded its result.
- **Do NOT** downgrade the classification to make a check pass.
- Report the failure in the format above and stop.

---

### Guardrails

#### Always Do

- Read the classification before deciding which artefacts are mandatory.
- Run the classification mismatch check before the main rules.
- Apply **both** parts of the check — declared in story **and** materialised on disk.
- Skip the BFF check entirely for Pure Presentational.
- Validate Hybrid with the Transactional rule set.
- Check every applicable artefact before reporting, so the failure report is complete.
- List both missing and present context in the failure report.
- Give a specific, actionable required-action line for every missing item.
- Halt immediately and completely on any failure.

#### Never Do

- **Never continue to a later phase after a failure** — not even "partially".
- **Never produce any output document on failure.**
- **Never invent, infer, or substitute missing context** to get past this gate.
- **Never treat a missing BFF spec as a failure for a Pure Presentational component.**
- **Never treat an empty or unreadable artefact as present.**
- Never pass a story that declared a Figma URL which was never extracted.
- Never pass a Transactional story with zero declared backend operationIds.
- Never halt on the first failure without checking the remaining artefacts.
- Never downgrade this gate to a warning.

---

### Gate: Phase 4 Complete When

- [ ] Classification read and the applicable rule set selected.
- [ ] Classification mismatch check performed.
- [ ] Sitecore validated — declared in story AND artefact present.
- [ ] Figma validated — declared in story AND every declared URL has a context file.
- [ ] BFF validated (Transactional/Hybrid only) — every declared operationId has a spec file.
- [ ] BFF check correctly skipped for Pure Presentational.
- [ ] All applicable artefacts checked before reporting.
- [ ] SUCCESS or REQUIRED CONTEXT NOT FOUND emitted in the prescribed format.
- [ ] On failure: agent halted, zero documents produced, actionable remediation listed.
