# Component Breakdown and Hierarchy

Skill for producing the complete component hierarchy, responsibility matrix, and folder/file structure for a frontend user story. Applies Presentational, Transactional, or Hybrid breakdown rules based on the classification from Phase 3.

## Use This For

- Building the full component hierarchy tree for a frontend user story.
- Applying the correct breakdown logic (Presentational, Transactional, or Hybrid).
- Defining the responsibility matrix for every component in the hierarchy.
- Proposing the folder and file structure with correct naming conventions.
- Producing the component list that feeds into Phase 6 (Component Reuse Validation).

## Expected Flow

```text
Phase 3 output (component classification + story analysis)
  → Apply breakdown logic based on classification:
    Presentational → Presentational breakdown rules
    Transactional  → Transactional breakdown rules
    Hybrid         → Hybrid breakdown rules
  → Build component hierarchy tree
  → Define component responsibility matrix
  → Propose folder/file structure with naming conventions
  → Output: complete component list for Phase 6
```

This skill must complete before Phase 6 (Component Reuse Validation) begins.

## Key Rules

- Phase 3 (Story Analysis End to End) must be complete before this skill runs.
- The component classification from Phase 3 is the mandatory input — do not re-derive it here.
- Follow the priority order at every decision: Dev Notes → Project Guidelines → Figma → React/Frontend Best Practices.
- Apply only the relevant breakdown rules for the classification — do not mix rules.
- Folder and file naming must follow the project's established conventions.
- Every component in the hierarchy must have a defined responsibility in the matrix.
- All conflicts between sources must be recorded in DEV_REVIEW.md with the resolution.

See [SKILL.md](./SKILL.md) for the full instructions.
