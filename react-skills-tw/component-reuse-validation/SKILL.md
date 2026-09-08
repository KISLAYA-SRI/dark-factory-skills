---
name: component-reuse-validation
description: Use when validating every applicable component against component-catalogue.json using the mandatory 4-step reuse decision workflow. Assigns a definitive reuse category (reuse existing, enhance existing, create new reusable, or create feature-specific) to every display component. Triggers include component reuse, catalogue validation, reuse decision, component catalogue, enhance existing component, or create new component.
---

# Component Reuse Validation

## Purpose

This skill validates every applicable component against `component-catalogue.json` and assigns a definitive reuse decision. It is invoked as Phase 6 of the master analysis orchestrator and must complete before Phase 7 (Prop-Driven Model and Code Generation Plan) begins.

This skill covers:

1. Running the mandatory 4-step reuse decision workflow for every applicable component from Phase 5.
2. Assigning a definitive reuse category to every component.
3. Excluding non-applicable component types (containers, hooks, types, etc.).
4. Producing a complete Component Inventory & Reuse Validation table for inclusion in ANALYSIS_PLAN.md.

> ⚠️ **Prerequisite**: Phase 5 (Component Breakdown and Hierarchy) MUST be complete. The full component hierarchy and responsibility matrix produced in Phase 5 are the mandatory inputs to this skill.

> ⚠️ **There is no separate Component Reuse Agent.** All reuse analysis is performed directly within this phase. Do NOT defer, skip, or delegate any step.

---

## Priority Order (Non-Negotiable at Every Decision Point)

```
Dev Notes  →  Project Guidelines  →  Figma  →  React / Frontend Best Practices
```

When two sources conflict, the higher-priority source wins. The conflict and resolution MUST be recorded in DEV_REVIEW.md.

> ⚠️ **Dev Notes are SACRED LAW.** If a Dev Note covers a topic, it IS the answer. Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").

---

## Exclusions — Do NOT Validate for Reuse

The following component types are **excluded** from the 4-step reuse workflow. Do not run any reuse check on them:

- Containers / controllers
- Mapper files
- Hook files
- Type files
- Visibility utilities
- API service files

Only **display components** (atoms, molecules, organisms, feature display components) go through the 4-step workflow.

---

## Step 1 — Classify the Atomic Level (ALWAYS First)

For every applicable component, classify its atomic level before any catalogue check.

| Level        | Definition                                                                                                                | Examples                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Atom**     | Smallest indivisible UI unit. No meaningful sub-components. Single visual or interactive primitive.                       | Button, Icon, Label, Input, Badge, Avatar, Spinner   |
| **Molecule** | Meaningful combination of atoms forming a single functional unit with a clear, self-contained purpose.                    | InputField (Label + Input + Error), Card, Tag, Toast |
| **Organism** | Complex, self-contained UI section composed of molecules and/or atoms. Represents a distinct region of a page or feature. | Header, Form, DataTable, IdentityOrganism, TabsPanel |

Record: `Component: [Name] | Atomic Level: Atom / Molecule / Organism | Reason: [one-line justification]`

---

## Step 2 — Exact Match Check Against `component-catalogue.json`

- Check whether the component exists with an exact match (name/purpose, visual pattern, required variant/state/config).
- **`component-catalogue.json` is the ONLY source of truth for existence validation.**
- **If exact match found:** Assign `Reuse existing variant`. Specify component name, variant/config, props. **STOP — do not proceed to Step 3.**
- **If no exact match:** Proceed to Step 3.

---

## Step 3 — Partial Match Check (Catalogue + Code Verification)

- Check whether a related component covers the same pattern but is missing a specific variant, state, prop, or configuration.
- **If partial match found in catalogue:**
  > ⚠️ **MANDATORY CODE CHECK**: Before assigning `Enhance existing component`, you MUST check the component's actual source code to verify the required variant/state does NOT already exist in code.
  - If variant/state **IS found in code** → treat as exact match. Assign `Reuse existing variant`. **STOP.**
  - If variant/state **IS NOT found in code** → Assign `Enhance existing component`. Specify: existing component name, current gap, proposed new prop/variant/slot/state, backward compatibility impact, approval required: Yes. **STOP.**
- **If no partial match:** Proceed to Step 4.

---

## Step 4 — No Match: Evaluate Reuse Potential

When no exact or partial match is found, evaluate whether the component should be reusable or feature-specific:

| Evaluation Question                                               | If YES                                       | If NO                                       |
| ----------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------- |
| Is the pattern generic and business-neutral?                      | Propose as reusable design-system component  | Propose as feature-specific component       |
| Could it be used in more than one feature or page?                | Propose as reusable (atom/molecule/organism) | Propose as feature-specific component       |
| Does it represent a named UI concept (not a business concept)?    | Propose as reusable design-system component  | Propose as feature display component        |
| Is it tightly coupled to a specific business domain or API shape? | Propose as feature-specific component        | Propose as reusable design-system component |

- **If reusable:** Assign `Create new reusable component`. Specify: proposed name, atomic level, expected props, expected variants, expected states, why reusable, Storybook required: Yes, catalogue update required: Yes.
- **If feature-specific:** Assign `Create feature-specific component`. Specify: feature component name, reason it is feature-specific, which existing catalogue/design-system components it reuses internally, expected props.

---

## Reuse Decision Categories

| Category                                          | When Assigned                                                                                 |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `Reuse existing variant`                          | Step 2: Exact match found in catalogue, OR Step 3: variant found in code                      |
| `Enhance existing component`                      | Step 3: Partial match in catalogue AND variant NOT found in code                              |
| `Compose from existing components`                | No single component fits, but lower-level existing components can compose the UI              |
| `Extract reusable pattern from feature component` | Existing feature component contains reusable visual pattern that should be promoted/extracted |
| `Create new reusable component`                   | Step 4: No match AND pattern is generic/reusable                                              |
| `Create feature-specific component`               | Step 4: No match AND pattern is business-specific/feature-coupled                             |
| `Needs clarification`                             | Requirement, Figma intent, or catalogue data is unclear                                       |

---

## Output Format Per Component

For every component that goes through the workflow, produce the following output block:

```
Component: [Name]
Atomic Level: Atom / Molecule / Organism / Feature Display / CMS Component
Step 2 — Exact Match: [Yes — use ComponentX with variant=Y] / [No]
Step 3 — Partial Match: [Yes — ComponentX is close, missing variant Z] / [No]
         Code Check: [Variant Z not found in source code] / [Variant Z found — treat as exact match]
Step 4 — No Match Decision: [Create new reusable atom/molecule/organism] / [Create feature-specific component]
Final Reuse Category: [category]
Decision: [one clear sentence]
Catalogue Update Required: Yes / No
Storybook Required: Yes / No
```

---

## Guardrails

### Always Do

- Check active Dev Notes list before every decision. If a Dev Note covers the topic, it IS the answer.
- Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").
- Apply the priority order at every decision point: Dev Notes → Guidelines → Figma → Best Practices.
- Run all 4 steps in order for every applicable component — no skipping.
- Assign a definitive reuse category to every applicable component before proceeding to Phase 7.
- Use `component-catalogue.json` as the ONLY source of truth for existence validation.
- Perform the mandatory code check for every partial match before assigning `Enhance existing component`.
- Exclude containers, hooks, mappers, types, utilities, and service files from the reuse workflow.
- Record every uncertain decision in DEV_REVIEW.md — never in ANALYSIS_PLAN.md.
- Mark every derived recommendation clearly: `Derived from project frontend best practices.`

### Never Do

- Never skip a step in the 4-step workflow for any applicable component.
- Never assign a reuse category without completing all applicable prior steps.
- Never skip the mandatory code check when a partial match is found in the catalogue.
- Never validate containers, controllers, hooks, mappers, or service files for reuse.
- Never use any source other than `component-catalogue.json` to determine component existence.
- Never leave any component without a definitive reuse category — `Needs clarification` is only valid when the requirement or Figma intent is genuinely unclear.
- Never override a Dev Note — not even as a "suggestion" or "recommendation".
- Never generate implementation code — that is the Coding Agent's job.
- Never defer reuse decisions to Phase 7 — all reuse decisions must be finalised in this phase.

---

## Output Checklist (Self-Verify Before Proceeding to Phase 7)

Before passing output to Phase 7 (Prop-Driven Model and Code Generation Plan), verify:

- [ ] Every applicable display component has gone through all 4 steps in order
- [ ] No step skipped for any applicable component
- [ ] Every applicable component has a definitive reuse category assigned
- [ ] Mandatory code check performed for every partial match (Step 3)
- [ ] Containers, controllers, hooks, mappers, types, utilities, and service files excluded from reuse check
- [ ] `component-catalogue.json` used as the ONLY source of truth for existence validation
- [ ] Output block produced for every component that went through the workflow
- [ ] Component Inventory & Reuse Validation table ready for inclusion in ANALYSIS_PLAN.md (Section 19)
- [ ] Every Dev Note applied and labelled with DN ID
- [ ] Every uncertain decision recorded in DEV_REVIEW.md, not in ANALYSIS_PLAN.md
