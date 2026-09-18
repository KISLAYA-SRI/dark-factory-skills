# Implementation Contract Loader

Reads the approved ANALYSIS_PLAN.md and CODING_AGENT_CHECKLIST.md once and converts them into a single normalized in-memory implementation manifest for the entire code-generation run. Does not rebuild any checklist.

## Use This For

- Loading the analysis contract at the start of the coding workflow (Phase 1).
- Normalizing plan content into one manifest that every downstream skill consumes.
- Reusing the existing CODING_AGENT_CHECKLIST.md as the validation contract (no rebuild).
- Deriving the execution path (lean vs full), Storybook targets, and test targets.

## Expected Flow

```text
Load ANALYSIS_PLAN.md
  → Parse classification, DN table, files, hierarchy, reuse decisions, contracts, states, ACs, ordered plan
  → Load CODING_AGENT_CHECKLIST.md verbatim as VALIDATION_CONTRACT
  → Load responsive_design_intent.json + Figma context (if UI-driven)
  → Derive executionPath, storybookTargets, testTargets
  → Output single IMPLEMENTATION_MANIFEST (no files written)
```

## Key Rules

- ANALYSIS_PLAN.md is authoritative — parse it, never re-analyse.
- Do NOT rebuild CODING_AGENT_CHECKLIST.md — load and reuse it for Phase 11 validation.
- Read each source only once; reuse the manifest from working memory.
- HALT if ANALYSIS_PLAN.md is missing — never fabricate the contract.
- Carry the "things NOT to implement" list forward so later skills never exceed scope.

See [SKILL.md](./SKILL.md) for the full instructions.
