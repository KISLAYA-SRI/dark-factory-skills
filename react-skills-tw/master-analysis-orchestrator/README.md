# Master Analysis Orchestrator

Master orchestration skill that drives the complete end-to-end FE Story Analysis workflow — defining the mandatory phase sequence, skill invocation map, decision gates, and quality standards the final output must meet before being passed to the Coding Agent.

## Use This For

- Running the full FE Story Analysis workflow from start to finish.
- Defining the mandatory execution sequence across all sub-skills and phases.
- Enforcing decision gates between phases before the next phase begins.
- Ensuring all three output documents are produced at the end of the workflow.
- Applying the correct priority order: Dev Notes → Project Guidelines → Figma → React/Frontend Best Practices.

## Expected Flow

```text
Phase 1: Developer Notes Protocol
  → Phase 2: Figma Fetch, Reconcile, and Analyse
  → Phase 3: API Analysis (Sitecore and BFF)
  → Phase 4: Story Analysis End to End
  → Phase 5: Component Breakdown and Hierarchy
  → Phase 6: Component Reuse Validation
  → Phase 7: Prop-Driven Model and Code Generation Plan
  → Phase 8: Output Contract Framework (Self-Validation + 3 Documents)
```

Each phase feeds its output into the next. No phase may be skipped. Decision gates between phases must pass before proceeding.

## Key Rules

- Follow this master skill as the primary execution blueprint — all other skills are invoked from here.
- Every decision must be made by the agent — no open questions, no deferred approvals, no options.
- Dev Notes are sacred law and override all other sources at every decision point.
- All three output documents (ANALYSIS_PLAN.md, DEV_REVIEW.md, CODING_AGENT_CHECKLIST.md) must be produced at the end.
- Quality gates must pass before the final output is produced.
- The output goes directly to the Code Generation Agent — no developer review beforehand.

See [SKILL.md](./SKILL.md) for the full instructions.
