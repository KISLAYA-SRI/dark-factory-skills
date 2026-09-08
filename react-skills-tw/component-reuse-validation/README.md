# Component Reuse Validation

Skill for validating every applicable component against `component-catalogue.json` using the mandatory 4-step reuse decision workflow. Assigns a definitive reuse category to every display component before the code generation plan is produced.

## Use This For

- Running the 4-step reuse decision workflow for every component from Phase 5.
- Checking each component against the project's `component-catalogue.json`.
- Assigning a definitive reuse category: reuse existing, enhance existing, create new reusable, or create feature-specific.
- Excluding non-applicable component types (containers, hooks, types, services, etc.) from reuse validation.
- Producing the Component Inventory and Reuse Validation table for inclusion in ANALYSIS_PLAN.md.

## Expected Flow

```text
Phase 5 output (component hierarchy + responsibility matrix)
  → For each applicable display component:
    Step 1: Check component-catalogue.json for exact name match
    Step 2: Exact match found? → Assign "Reuse Existing"
    Step 3: No exact match? → Check for partial/similar match
      Partial match? → Assign "Enhance Existing"
    Step 4: No match? → Assign "Create New Reusable" or "Create Feature-Specific"
  → Produce Component Inventory and Reuse Validation table
```

This skill must complete before Phase 7 (Prop-Driven Model and Code Generation Plan) begins.

## Key Rules

- Phase 5 (Component Breakdown and Hierarchy) must be complete before this skill runs.
- All reuse analysis is performed directly within this phase — do not defer, skip, or delegate any step.
- There is no separate Component Reuse Agent — this skill owns the entire reuse validation.
- Containers, hooks, types, services, and utilities are excluded from reuse validation.
- Every applicable display component must receive a definitive reuse category — no ambiguous or deferred decisions.
- The reuse decision must be based on the catalogue — do not invent matches or assume similarity.
- All reuse decisions must appear in the Component Inventory table in ANALYSIS_PLAN.md.

See [SKILL.md](./SKILL.md) for the full instructions.
