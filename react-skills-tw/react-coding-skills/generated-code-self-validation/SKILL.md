---
name: generated-code-self-validation
description: Use as the final gate before producing the summary — runs deterministic structural checks on generated code AND walks the existing CODING_AGENT_CHECKLIST.md item by item with file evidence. Triggers include self-validation, code validation gate, pre-completion check, or validate the generated code.
disable-model-invocation: true
---

## Generated Code Self-Validation

### Purpose

Verify the generated code is structurally correct, scope-compliant, and satisfies the validation contract BEFORE the consolidated summary is produced. Two parts run in sequence: (A) deterministic structural gate, (B) `CODING_AGENT_CHECKLIST.md` walk.

⚠️ No summary may be produced until all checks pass. On failure, fix the specific code and re-run this gate — never restart the whole build.

### Part A — Structural Gate (Deterministic)

```text
Files & Structure
- [ ] Every file in the manifest's filesToCreate/filesToUpdate exists.
- [ ] No forbidden roots created (src, duplicate .storybook, new .SS_WF).
- [ ] Existing filesystem casing reused; no case-insensitive duplicate paths.
- [ ] Nearest barrels updated with explicit named re-exports (default export for CMS entries).

Ownership & Boundaries
- [ ] No feature-to-feature imports; DS imports no feature/CMS/API code.
- [ ] Components placed under correct owner (DS / CMS / Feature / Shared).

Prop-Driven & Data Discipline
- [ ] No hardcoded labels/values/colours where props/tokens are required.
- [ ] No raw API DTO reaches a display component (mapper present).
- [ ] No API call / data fetching inside design-system or feature display components.
- [ ] Services are framework-agnostic; endpoints/keys from constants.

Classification Compliance
- [ ] Presentational: NO container/hook/service/mapper/store generated.
- [ ] Transactional: types+mapper+service+hook+container present; all states handled.

Sitecore (if applicable)
- [ ] CMS field contracts typed; rendering entry default-exported + registered.
- [ ] CMS labels separate from API values; preview-safe on null fields.

Storybook & Catalogue (if applicable)
- [ ] Stories exist for every eligible reusable component (and only those).
- [ ] component-catalogue.json valid JSON at repo root; unrelated entries intact.

Tests
- [ ] Every runtime file has a co-located test (or is on the exclusion list).
- [ ] Branch map shows 90–100% intended coverage; no snapshots.

Scope
- [ ] Nothing on the plan's "things NOT to implement" list was implemented.
```

### Part B — Coding Agent Checklist Walk

Use the `CODING_AGENT_CHECKLIST.md` loaded in Phase 1 (do NOT rebuild it). For every item, mark status + evidence:

```text
For each checklist item (DN / AC / INT / STATE / SCOPE / PROP / CMS / API / COMP / DS /
                         RESP / A11Y / RTL / NFR / FILE / TEST):
  → Covered  (with file path / test evidence)
  → Not Applicable (with reason — e.g. Presentational)
No item may be left unresolved.
```

Every `DN-xxx` must appear as Covered with the file(s) where it was applied. No generated file may contradict a Dev Note.

If lint/typecheck/test execution is within scope, run them and record results; if out of scope, mark as "static validation only" and defer execution proof to the runtime quality gate.

### Gate: Complete When

```text
- [ ] All Part A structural checks pass (or failures fixed and re-run).
- [ ] Every CODING_AGENT_CHECKLIST.md item marked Covered / Not Applicable with evidence.
- [ ] Every DN-xxx confirmed applied; no contradictions.
- [ ] Deviations recorded for the summary's Section 13.
```

### Never Do

- Never produce the summary while any check is failing.
- Never rebuild the checklist — reuse the one from the analysis output.
- Never restart the whole build on a single failure — fix and re-run the gate.
- Never mark an item Covered without concrete file/test evidence.
