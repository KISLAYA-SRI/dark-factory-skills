---
name: implementation-contract-loader
description: Use at the start of the FE Code Generation workflow to read the approved ANALYSIS_PLAN.md and CODING_AGENT_CHECKLIST.md once and convert them into a single normalized in-memory implementation manifest for the whole run. Does NOT rebuild any checklist. Triggers include contract loading, analysis plan ingestion, coding manifest, or "load the plan for <TICKET_ID>".
disable-model-invocation: true
---

## Implementation Contract Loader

### Purpose

Read the upstream analysis artefacts **exactly once** and produce a single normalized `IMPLEMENTATION_MANIFEST` that every downstream coding skill consumes. This eliminates the repeated "re-read the plan, re-extract files, re-derive the checklist" work that the four legacy agents each performed.

⚠️ **Do NOT rebuild a checklist.** The Analysis Agent already produced `CODING_AGENT_CHECKLIST.md`. This skill **loads** it and holds it as the validation contract for Phase 11. Regenerating it would duplicate work and risk drift from the analysis decisions.

### Inputs

<table>
<tr><th>Input</th><th>Source</th><th>Required?</th></tr>
<tr><td>Analysis Plan</td><td>.SS_WF/Agent/Analysis/{{ticket_id}}_ANALYSIS_PLAN.md</td><td>**Mandatory**</td></tr>
<tr><td>Coding Agent Checklist</td><td>.SS_WF/Agent/Analysis/{{ticket_id}}_CODING_AGENT_CHECKLIST.md</td><td>**Mandatory**</td></tr>
<tr><td>Responsive Reconciliation</td><td>.SS_WF/figma-output/responsive_design_intent.json</td><td>If Figma-driven UI</td></tr>
<tr><td>Figma Context (Desktop/Mobile)</td><td>.SS_WF/figma-output/**/**-context.json</td><td>If visual detail needed</td></tr>
<tr><td>Component Catalogue</td><td>component-catalogue.json at repo root</td><td>**Mandatory** for reuse</td></tr>
</table>

If `ANALYSIS_PLAN.md` is missing → HALT and report. Never re-run analysis to compensate.

### Answer to "Do we need to build a checklist again?"

**No.** Use the two documents the Analysis Agent already generated:
- `ANALYSIS_PLAN.md` — the actionable plan (Section 11 = ordered Code Generation Plan). This drives WHAT to build and in WHAT order.
- `CODING_AGENT_CHECKLIST.md` — the validation contract. This is **reused as-is** by `generated-code-self-validation` in Phase 11.

This skill does **not** produce a new checklist and does **not** produce new planning documents. It only normalizes existing inputs into working memory.

### What to Extract into the Manifest

Parse `ANALYSIS_PLAN.md` into these fields:

```text
IMPLEMENTATION_MANIFEST = {
  ticketId
  classification            # Presentational | Transactional | Hybrid   (Section 3)
  developerNotes[]          # DN-001…  (Section 1 — Developer Notes Applied table)
  filesToCreate[]           # path + ownership marker [design-system|cms|feature|shared]
  filesToUpdate[]           # path + reason
  componentHierarchy        # Section 7 — tree with markers, no file paths
  responsibilityMatrix      # Section 8
  containerViewDecisions    # Section 9
  folderStructure           # Section 10 — target paths + naming
  reuseDecisions[]          # Section 19 — reuse existing / enhance / create new / feature-specific
  sitecoreContracts         # Section 16 — CMS field contracts (or NOT REQUIRED)
  bffContracts              # Section 17 — request/response/error/nullable + data-fetching pattern (or NOT REQUIRED)
  propModels[]              # Section 18 — per-component prop table (name, type, source, source detail)
  states[]                  # Section 14 — default/loading/success/error/empty/partial/disabled
  interactions[]            # Section 13
  acceptanceCriteria[]      # Section 5 — AC-xxx + FE implication + owner component
  nfr                       # Section 20 — RTL / a11y / responsive / overflow
  orderedPlan[]             # Section 11 — ordered code-gen steps + "things NOT to implement"
  storybookTargets[]        # derived: DS + CMS-mapped reusable components eligible for stories
  testTargets[]             # derived: every runtime file that will be created/modified
  executionPath             # derived from classification (lean | full)
}
```

Hold `CODING_AGENT_CHECKLIST.md` verbatim as `VALIDATION_CONTRACT` (do not transform its items).

### Derivation Rules

- **executionPath**: `Presentational → lean`; `Transactional | Hybrid → full`.
- **storybookTargets**: include only new/enhanced Design System components, Sitecore-mapped reusable presentation components, and reusable DS files. Exclude containers, hooks, services, mappers, type-only files, one-off feature components.
- **testTargets**: include every file in `filesToCreate` + `filesToUpdate` that contains runtime behaviour. Exclude barrels, type-only files, stories, configs, and primitive-constant files (they are handled by the runtime-file classification policy in `frontend-test-generation`).
- **NOT-to-implement list**: carry Section 11's "things NOT to implement" forward so later skills never exceed scope.

### Context Reuse Rule

Read each source **once**. After parsing, reuse the manifest from working memory. Do not re-open `ANALYSIS_PLAN.md`, the catalogue, or Figma JSON again in later phases.

### Output

A single in-memory `IMPLEMENTATION_MANIFEST` + `VALIDATION_CONTRACT`. This skill writes **no files**.

### Gate: Complete When

```text
- [ ] ANALYSIS_PLAN.md parsed into all manifest fields.
- [ ] CODING_AGENT_CHECKLIST.md loaded verbatim as VALIDATION_CONTRACT (not rebuilt).
- [ ] classification + executionPath selected.
- [ ] filesToCreate / filesToUpdate / reuseDecisions / orderedPlan captured.
- [ ] storybookTargets and testTargets derived.
- [ ] "things NOT to implement" carried forward.
```

### Never Do

- Never regenerate `CODING_AGENT_CHECKLIST.md` or any planning document.
- Never re-run story analysis to fill gaps — mark missing fields as `Not Provided in Plan`.
- Never re-read a source that is already in the manifest.
