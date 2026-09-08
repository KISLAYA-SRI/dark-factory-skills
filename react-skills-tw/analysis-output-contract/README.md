# Analysis Output Contract

Final-phase skill for running the complete self-validation checklist and producing all three output documents (ANALYSIS_PLAN.md, DEV_REVIEW.md, CODING_AGENT_CHECKLIST.md) for the FE Story Analysis Agent.

## Use This For

- Running the mandatory 13-section self-validation checklist before any document is produced.
- Verifying that all analysis areas from Phases 17 are complete and correct.
- Producing ANALYSIS_PLAN.md the primary input for the Code Generation Agent.
- Producing DEV_REVIEW.md capturing all doubts, conflicts, and confidence-rated decisions.
- Producing CODING_AGENT_CHECKLIST.md the self-validation checklist for the Coding Agent.
- Enforcing the prohibition check to ensure no disallowed content appears in the output.

## Expected Flow

```text
Phases 17 complete
   PART A  Self-Validation:
    Run 13-section checklist
     All checks pass?  Proceed to output production
     Any check fails?  Complete missing analysis first
   PART B  Output Production:
    Generate ANALYSIS_PLAN.md (decisive, no open questions)
    Generate DEV_REVIEW.md (doubts with confidence levels)
    Generate CODING_AGENT_CHECKLIST.md (self-validation for Coding Agent)
```

No output document may be produced until ALL self-validation checks pass.

## Key Rules

- Self-validation is mandatory not optional. All 13 sections must be checked.
- If any check fails, complete the missing analysis before producing any document.
- Mark unavailable information as `Not Provided` never invent or assume.
- Mark best-practice-derived decisions as `Derived` never present them as specified.
- ANALYSIS_PLAN.md must be fully decisive no open questions, no options, no deferred decisions.
- DEV_REVIEW.md captures all uncertainty with confidence levels not decisions for the developer to make.
- The output goes directly to the Code Generation Agent no developer review beforehand.

See [SKILL.md](./SKILL.md) for the full instructions.
