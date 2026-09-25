# Generated Code Self-Validation

Final gate before the summary — runs deterministic structural checks on the generated code and walks the existing CODING_AGENT_CHECKLIST.md item by item with file evidence.

## Use This For

- Validating generated code before producing the consolidated summary (Phase 11).
- Confirming structure, ownership, prop-driven discipline, and classification compliance.
- Resolving every CODING_AGENT_CHECKLIST.md item with evidence.

## Expected Flow

```text
Part A: Structural gate (files, casing, boundaries, data discipline, classification, tests, scope)
  → Part B: Walk CODING_AGENT_CHECKLIST.md (Covered / Not Applicable + evidence)
  → Record deviations for the summary
```

## Key Rules

- No summary is produced until all checks pass.
- Reuse CODING_AGENT_CHECKLIST.md — never rebuild it.
- Every DN-xxx must be confirmed applied with no contradictions.
- Presentational: confirm NO container/hook/service/mapper/store exists.
- Fix and re-run the gate on failure — never restart the whole build.

See [SKILL.md](./SKILL.md) for the full instructions.
