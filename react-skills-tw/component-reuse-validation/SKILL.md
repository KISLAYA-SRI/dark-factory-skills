---
name: component-reuse-validation
description: Use this Skill to validate every applicable component against component-catalogue.json using the mandatory 4-step reuse decision workflow. Assigns a definitive reuse category to every display component. Triggers include component reuse, catalogue validation, reuse decision, component catalogue, enhance existing component, or create new component.
---

## Component Reuse Validation

### Purpose

This skill validates every applicable component against `component-catalogue.json` and assigns a definitive reuse decision.

This skill covers:

- Running the mandatory 4-step reuse decision workflow for every applicable component from Phase 7.
- Assigning a definitive reuse category to every component.
- Excluding non-applicable component types.
- Producing the Component Inventory & Reuse Validation table for **ANALYSIS_PLAN.md §13.1**.

⚠️ **There is no separate Component Reuse Agent.** All reuse analysis is performed here. Do NOT defer, skip, or delegate any step.

### Priority Order (Non-Negotiable at Every Decision Point)

```text
Dev Notes  →  Project Guidelines  →  Figma  →  React / Frontend Best Practices
```

⚠️ **Dev Notes are SACRED LAW.** Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").

---

### ⚠️ ANALYSIS DEPTH vs OUTPUT WIDTH

Run all four steps in full for every applicable component. The per-component output block below is an **internal working record** that disciplines the decision; only the summary table reaches the plan.

| Work Performed (always, in full)                 | Emitted To                              |
| ------------------------------------------------ | --------------------------------------- |
| Atomic level classification + reason             | **§13.1** (level only; reason internal) |
| Step 2 exact-match check                         | Internal → determines category          |
| Step 3 partial-match + mandatory code check      | Internal → determines category          |
| Step 4 reuse-potential evaluation                | Internal → determines category          |
| Per-component output block                       | Internal working record                 |
| Final reuse category + gap + catalogue flag      | **§13.1**                               |
| Uncertainty about catalogue data or Figma intent | **DEV_REVIEW.md §1**                    |
| Backward-compatibility impact of an enhancement  | **DEV_REVIEW.md §1**                    |

---

### Exclusions — Do NOT Validate for Reuse

The following are **excluded** from the 4-step workflow:

- Containers / controllers
- Mapper files
- Hook files
- Type files
- Visibility utilities
- API service files

Only **display components** (atoms, molecules, organisms, feature display components) go through the workflow.

### Scope Rules Based on Classification

#### If Classification = Presentational

- Execute the 4-Step Workflow for **display/UI components only**.
- Skip reuse validation for containers, hooks, mappers, type files, and any direct Sitecore-mapped wrapper with no reusable UI pattern.

#### If Classification = Transactional or Hybrid

- Execute the 4-Step Workflow for all applicable display components per the Exclusions above.

---

### Step 1 — Classify the Atomic Level (ALWAYS First)

| Level        | Definition                                                                                                                | Examples                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Atom**     | Smallest indivisible UI unit. No meaningful sub-components. Single visual or interactive primitive.                       | Button, Icon, Label, Input, Badge, Avatar, Spinner   |
| **Molecule** | Meaningful combination of atoms forming a single functional unit with a clear, self-contained purpose.                    | InputField (Label + Input + Error), Card, Tag, Toast |
| **Organism** | Complex, self-contained UI section composed of molecules and/or atoms. Represents a distinct region of a page or feature. | Header, Form, DataTable, HeroCarousel, TabsPanel     |

Record internally: `Component: [Name] | Atomic Level: Atom / Molecule / Organism | Reason: [one-line justification]`

### Step 2 — Exact Match Check Against component-catalogue.json

- Check whether the component exists with an exact match (name/purpose, visual pattern, required variant/state/config).
- **`component-catalogue.json` is the ONLY source of truth for existence validation.**
- **If exact match found:** Assign `Reuse existing variant`. Specify component name, variant/config, props. **STOP.**
- **If no exact match:** Proceed to Step 3.

### Step 3 — Partial Match Check (Catalogue + Code Verification)

- Check whether a related component covers the same pattern but is missing a specific variant, state, prop, or configuration.
- **If partial match found in catalogue:**

  ⚠️ **MANDATORY CODE CHECK**: Before assigning `Enhance existing component`, you MUST check the component's actual source code to verify the required variant/state does NOT already exist.
  - If variant/state **IS found in code** → treat as exact match. Assign `Reuse existing variant`. **STOP.**
  - If variant/state **IS NOT found in code** → Assign `Enhance existing component`. Specify: existing component name, current gap, proposed new prop/variant/slot/state. Record backward-compatibility impact in **DEV_REVIEW.md §1**. **STOP.**

- **If no partial match:** Proceed to Step 4.

### Step 4 — No Match: Evaluate Reuse Potential

| Evaluation Question                                               | If YES                                       | If NO                                       |
| ----------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------- |
| Is the pattern generic and business-neutral?                      | Propose as reusable design-system component  | Propose as feature-specific component       |
| Could it be used in more than one feature or page?                | Propose as reusable (atom/molecule/organism) | Propose as feature-specific component       |
| Does it represent a named UI concept (not a business concept)?    | Propose as reusable design-system component  | Propose as feature display component        |
| Is it tightly coupled to a specific business domain or API shape? | Propose as feature-specific component        | Propose as reusable design-system component |

- **If reusable:** Assign `Create new reusable component`. Specify proposed name, atomic level, expected props, variants, states. Storybook required: Yes. Catalogue update required: Yes.
- **If feature-specific:** Assign `Create feature-specific component`. Specify name, reason, which existing catalogue/design-system components it reuses internally, expected props.

---

### Reuse Decision Categories

| Category                                        | When Assigned                                                                         |
| ----------------------------------------------- | ------------------------------------------------------------------------------------- |
| Reuse existing variant                          | Step 2 exact match, OR Step 3 variant found in code                                   |
| Enhance existing component                      | Step 3 partial match AND variant NOT found in code                                    |
| Compose from existing components                | No single component fits, but lower-level existing components can compose the UI      |
| Extract reusable pattern from feature component | Existing feature component contains a reusable visual pattern that should be promoted |
| Create new reusable component                   | Step 4: no match AND pattern is generic/reusable                                      |
| Create feature-specific component               | Step 4: no match AND pattern is business-specific/feature-coupled                     |

⚠️ **The `Needs clarification` category is prohibited.** ANALYSIS_PLAN.md must contain no deferred decisions — the output contract's prohibition check blocks them. When catalogue data or Figma intent is genuinely unclear:

1. Make the **most defensible definitive decision** using the priority order.
2. Emit that definitive category into §13.1.
3. Record the uncertainty, the options considered, and your confidence in **DEV_REVIEW.md §1 (Decisions Made Under Uncertainty)**.

Likewise, never emit `approval required: Yes` into the plan. An enhancement decision is final for code generation; its backward-compatibility risk is a DEV_REVIEW concern.

---

### Per-Component Working Record (Internal)

Produce this for every component that goes through the workflow. It is **not** emitted into ANALYSIS_PLAN.md — it exists to prove no step was skipped.

```text
Component: [Name]
Atomic Level: Atom / Molecule / Organism / Feature Display / CMS Component
Step 2 — Exact Match: [Yes — use ComponentX with variant=Y] / [No]
Step 3 — Partial Match: [Yes — ComponentX is close, missing variant Z] / [No]
           Code Check: [Variant Z not found in source] / [Variant Z found — treat as exact match]
Step 4 — No Match Decision: [Create new reusable ...] / [Create feature-specific ...]
Final Reuse Category: [category]
Decision: [one clear sentence]
Catalogue Update Required: Yes / No
Storybook Required: Yes / No
```

### Output → §13.1

| Component | Atomic Level | Reuse Decision | Existing Component | Gap / Enhancement | New Component Name | Catalogue Update? |
| --------- | ------------ | -------------- | ------------------ | ----------------- | ------------------ | ----------------- |
|           |              |                |                    |                   |                    |                   |

This table feeds two downstream consumers:

- **Coding Phase 4** — `presentational-ui-generation` honours each reuse decision before creating anything.
- **Coding Phase 9** — `storybook-and-component-catalogue` uses `Catalogue Update?` and the new/enhanced flags to determine story eligibility.

---

### Guardrails

#### Always Do

- Check the active Dev Notes list before every decision; label items with their DN ID.
- Apply the priority order at every decision point.
- Run all 4 steps in order for every applicable component — no skipping.
- Assign a **definitive** reuse category to every applicable component.
- Use `component-catalogue.json` as the ONLY source of truth for existence validation.
- Perform the mandatory code check for every partial match.
- Exclude containers, hooks, mappers, types, utilities, and service files.
- Route uncertainty and backward-compatibility impact to DEV_REVIEW.md §1.
- Produce the internal working record for every component.
- Set the `Catalogue Update?` flag correctly — it drives Storybook eligibility downstream.

#### Never Do

- Never skip a step in the 4-step workflow.
- Never assign a reuse category without completing all applicable prior steps.
- Never skip the mandatory code check when a partial match is found.
- Never validate containers, controllers, hooks, mappers, or service files for reuse.
- Never use any source other than `component-catalogue.json` to determine existence.
- **Never emit `Needs clarification` into ANALYSIS_PLAN.md** — decide definitively, log the uncertainty in DEV_REVIEW.md §1.
- **Never emit `approval required` or any deferred-decision phrasing into ANALYSIS_PLAN.md.**
- **Never emit the per-component working record into ANALYSIS_PLAN.md** — only the §13.1 summary table.
- Never override a Dev Note.
- Never generate implementation code.
- Never defer reuse decisions to a later phase — all are finalised here.

---

### Gate: Phase 8 Complete When

**Analysis completeness:**

- [ ] Every applicable display component went through all 4 steps in order
- [ ] No step skipped for any applicable component
- [ ] Mandatory code check performed for every partial match
- [ ] Containers, controllers, hooks, mappers, types, utilities, service files excluded
- [ ] `component-catalogue.json` used as the ONLY existence source
- [ ] Internal working record produced for every component

**Emission discipline:**

- [ ] Every component has a **definitive** reuse category — no `Needs clarification`
- [ ] No `approval required` or deferred phrasing in the emitted table
- [ ] §13.1 table complete and ready for ANALYSIS_PLAN.md
- [ ] `Catalogue Update?` flag set correctly for Storybook eligibility downstream
- [ ] Working records kept internal — not emitted
- [ ] Every Dev Note applied and labelled with its DN ID
- [ ] Every uncertainty routed to DEV_REVIEW.md §1
