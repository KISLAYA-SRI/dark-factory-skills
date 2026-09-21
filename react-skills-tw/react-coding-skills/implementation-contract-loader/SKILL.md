---
name: implementation-contract-loader
description: Use at the start of the FE Code Generation workflow to read the approved ANALYSIS_PLAN.md and CODING_AGENT_CHECKLIST.md once and convert them into a single normalized in-memory implementation manifest for the whole run. Does NOT rebuild any checklist. Triggers include contract loading, analysis plan ingestion, coding manifest, or load the plan for a ticket.
disable-model-invocation: true
---

## Implementation Contract Loader

### Purpose

Read the upstream analysis artefacts **exactly once** and produce a single normalized `IMPLEMENTATION_MANIFEST` that every downstream coding skill consumes. This eliminates the repeated "re-read the plan, re-extract files, re-derive the checklist" work the four legacy agents each performed.

⚠️ **Do NOT rebuild a checklist.** The Analysis Agent already produced `CODING_AGENT_CHECKLIST.md`. This skill **loads** it and holds it as the validation contract for the self-validation phase. Regenerating it would duplicate work and risk drift from the analysis decisions.

---

### Inputs

| Input | Source | Required? |
| --- | --- | --- |
| Analysis Plan | `.SS_WF/Agent/Analysis/{{ticket_id}}_ANALYSIS_PLAN.md` | **Mandatory** |
| Coding Agent Checklist | `.SS_WF/Agent/Analysis/{{ticket_id}}_CODING_AGENT_CHECKLIST.md` | **Mandatory** |
| Responsive Reconciliation | `figma-output/responsive_design_intent.json` | If Figma-driven UI |
| Figma Context (Desktop/Mobile) | `figma-output/**/*-context.json` | If visual detail needed |
| Component Catalogue | `./src/component-catalogue.json` | **Mandatory** for reuse |

If `ANALYSIS_PLAN.md` is missing → **HALT** and report. Never re-run analysis to compensate.

⚠️ **`DEV_REVIEW.md` is NOT an input.** It holds provenance and gap detail for human reviewers only.

---

### Answer to "Do we need to build a checklist again?"

**No.** Use the two documents the Analysis Agent already generated:

- **`ANALYSIS_PLAN.md`** — the actionable plan. **Section 8** is the ordered Code Generation Plan. This drives WHAT to build and in WHAT order.
- **`CODING_AGENT_CHECKLIST.md`** — the validation contract, **reused as-is** by `generated-code-self-validation`.

This skill produces **no files** and **no new planning documents**. It only normalizes existing inputs into working memory.

---

## ⚠️ ANALYSIS_PLAN.md IS 13 SECTIONS

The plan is a lean handoff contract carrying **only story-specific decisions**. All project rules — folder placement, PascalCase, naming, export style, RTL, accessibility, tokens, prop-driven discipline — are **embedded in the coding sub-skills**, not in the plan.

### What to Extract into the Manifest

```text
IMPLEMENTATION_MANIFEST = {
  ticketId

  classification            ← Section 3      # Presentational | Transactional | Hybrid
  developerNotes[]          ← Section 1      # DN-001… (4 columns; use Files/Components Affected)
  storyContext              ← Section 2      # title, page/component, default view, personas

  acceptanceCriteria[]      ← Section 4      # AC-xxx + FE implication + owner + state impact
  componentHierarchy        ← Section 5      # tree with markers, no file paths
  responsibilityMatrix      ← Section 6      # Component | Type | Owns | Must NOT Own
  containerViewDecisions    ← Section 6      # the Type column IS the decision
  ownershipMarkers[]        ← Section 7      # [design-system] | [cms] | [feature] | [shared]

  filesToCreate[]           ← Section 8      # name + path + purpose
  filesToUpdate[]           ← Section 8      # name + path + reason
  orderedPlan[]             ← Section 8      # ordered implementation steps
  stateHandlingPlacement    ← Section 8      # Transactional/Hybrid only
  visibilityRules[]         ← Section 8
  propWiring[]              ← Section 8
  notToImplement[]          ← Section 8      # the ONLY out-of-scope guardrail

  interactions[]            ← Section 9      # INT-xxx + trigger + owner + state impact
  states[]                  ← Section 10     # STATE rows — must be non-empty

  sitecoreContracts         ← Section 11.1   # or: NOT REQUIRED
  bffContracts              ← Section 11.2   # FE-relevant slice + Data Fetching Pattern
  mapperDefaults[]          ← Section 11.2   # from the Nullable/Conditional column
  errorStateMap[]           ← Section 11.2   # error code → UI state → component

  propModels[]              ← Section 12     # per component
  propOwnership[]           ← Section 12     # Source + Source Detail = ownership record
  gappedProps[]             ← Section 12     # props marked "Unknown — source contract not provided"

  reuseDecisions[]          ← Section 13.1   # + Catalogue Update? flag
  nfrExceptions[]           ← Section 13.2   # story-specific exceptions ONLY

  storybookTargets[]        ← derived from 13.1
  testTargets[]             ← derived from filesToCreate + filesToUpdate
  executionPath             ← derived from classification (lean | full)
}
```

Hold `CODING_AGENT_CHECKLIST.md` **verbatim** as `VALIDATION_CONTRACT` (do not transform its items).

---

### ⚠️ Sections That No Longer Exist

Do **not** look for these — their absence is intentional:

| Not in the plan | Where it is now |
| --- | --- |
| Derived Scope section | `notToImplement[]` ← Section 8 |
| Sitecore/Backend/FE Ownership section | `propOwnership[]` ← Section 12 `Source` / `Source Detail` |
| Container / View Decision section | `containerViewDecisions` ← Section 6 `Type` column |
| Folder structure tree | `ownershipMarkers[]` ← Section 7; paths resolved by `repository-structure-governance` |
| Naming-convention list | Embedded in `repository-structure-governance` |
| NFR baseline rows | Embedded in `presentational-ui-generation`; §13.2 has exceptions only |
| Sitecore-Authored Props table | `propOwnership[]` ← Section 12 |
| Agent Decision Summary / Assumptions | `DEV_REVIEW.md` — **not an input** |
| Full example payloads / unsurfaced scenarios | Never emitted — §11.2 is the FE-relevant slice |

⚠️ If a section appears empty or marked `NOT REQUIRED`, **that is the instruction**. Do not treat it as missing analysis and do not re-derive it.

---

### Derivation Rules

- **`executionPath`**: `Presentational → lean` (skip logic/state phases); `Transactional | Hybrid → full`.
- **`storybookTargets`**: from Section 13.1 — include new/enhanced Design System components, Sitecore-mapped reusable presentation components, and reusable DS files. Use the `Catalogue Update?` flag. Exclude containers, hooks, services, mappers, type-only files, one-off feature components.
- **`testTargets`**: every file in `filesToCreate` + `filesToUpdate` containing runtime behaviour. Exclude barrels, type-only files, stories, configs, primitive-constant files.
- **`gappedProps`**: any Section 12 prop whose `Source` is `Unknown — source contract not provided`. These must stay prop-driven — **never substitute a hardcoded value.**
- **`notToImplement`**: carry Section 8's list forward so no later skill exceeds scope.

---

### ⚠️ Integrity Checks on Load

Record any of these as a **deviation** for the final summary — do not silently proceed:

```text
- states[] is empty                              → no state contract; flag it
- a Section 12 prop still reads "To be resolved"  → unresolved placeholder leaked from analysis
- filesToCreate[] is empty                        → nothing to build; verify the plan
- classification missing from Section 3           → cannot select an execution path; HALT
- CODING_AGENT_CHECKLIST.md missing               → no validation contract; HALT
```

For `states[]` specifically: implement the states evident from `interactions[]` and flag the gap. **Never silently produce a stateless component.**

---

### Context Reuse Rule

Read each source **once**. After parsing, reuse the manifest from working memory. Do not re-open `ANALYSIS_PLAN.md`, the catalogue, or the Figma JSONs again in later phases.

### Output

A single in-memory `IMPLEMENTATION_MANIFEST` + `VALIDATION_CONTRACT`. This skill writes **no files**.

---

### Gate: Complete When

```text
- [ ] ANALYSIS_PLAN.md parsed into all manifest fields using the 13-section map.
- [ ] CODING_AGENT_CHECKLIST.md loaded verbatim as VALIDATION_CONTRACT (not rebuilt).
- [ ] classification (§3) read and executionPath selected.
- [ ] filesToCreate / filesToUpdate / orderedPlan / notToImplement captured from §8.
- [ ] propOwnership and gappedProps captured from §12.
- [ ] states[] captured from §10 — non-empty, or flagged as a deviation.
- [ ] Component catalogue read from ./src/component-catalogue.json.
- [ ] storybookTargets and testTargets derived.
- [ ] Integrity checks run; deviations recorded for the final summary.
```

### Never Do

- Never regenerate `CODING_AGENT_CHECKLIST.md` or any planning document.
- Never read `DEV_REVIEW.md`.
- Never re-run story analysis to fill gaps — mark missing fields as `Not Provided in Plan`.
- Never expect a scope, ownership, container/view, folder-tree, Sitecore-authored-props or assumptions section.
- Never substitute a hardcoded value for a gapped prop.
- Never look for the catalogue at the repository root — it lives at `./src/component-catalogue.json`.
- Never re-read a source already captured in the manifest.
