# Master React Coding Orchestrator

Master orchestration skill that drives the complete end-to-end FE Code Generation workflow — turning an approved ANALYSIS_PLAN.md into production React/Next.js code across UI, Sitecore, logic, state, Storybook, and tests, then producing a single consolidated summary document.

## Use This For

- Running the full FE Code Generation workflow from an approved analysis plan to production code.
- Defining the mandatory execution sequence across all coding sub-skills and phases.
- Selecting the correct path: Presentational (lean) vs Transactional (full).
- Enforcing decision gates between phases before the next phase begins.
- Producing ONE consolidated summary (UI + Storybook + Logic + Tests) at the end.
- Applying the correct priority order: Dev Notes → Figma Reconciliation → Analysis Plan → Project Guidelines → React/Frontend Best Practices.

## Expected Flow

```text
Phase 0: Pre-Coding Setup
  → Phase 1: Load Implementation Contract (implementation-contract-loader)
  → Phase 2: Developer Notes Enforcement (developer-notes-protocol, reused)
  → Phase 3: Repository Structure Governance
  → Phase 4: Presentational UI Generation (+ responsive-figma, + media)
      ↳ Presentational path stops here → jump to Phase 9
  → Phase 5: Sitecore Rendering Integration (if CMS-mapped)
  → Phase 6: Frontend Logic Integration (Transactional)
  → Phase 7: State and Form Management (if forms/shared state)
  → Phase 9: Storybook and Component Catalogue (eligible components only)
  → Phase 10: Frontend Test Generation (90–100% coverage target)
  → Phase 11: Generated Code Self-Validation
  → Phase 12: Consolidated Summary Document (ONE file, chunked write/append)
```

Each phase feeds its output into the next. Presentational components take the lean path and skip logic phases. Decision gates between phases must pass before proceeding.

## Key Rules

- Follow this master skill as the primary execution blueprint — all other skills are invoked from here.
- ANALYSIS_PLAN.md is finalised — build it, never re-analyse the story.
- Dev Notes are sacred law and override all other sources at every decision point.
- Never over-engineer a Presentational component (no containers, hooks, services, mappers, or stores).
- Only ONE consolidated summary document is produced — not four.
- CODING_AGENT_CHECKLIST.md is reused for validation — it is not rebuilt.
- Quality gates must pass before the final summary is produced.

See [SKILL.md](./SKILL.md) for the full instructions.
