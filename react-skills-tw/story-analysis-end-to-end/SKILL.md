---
name: story-analysis-end-to-end
description: Use when performing complete end-to-end analysis of a frontend user story. Covers story understanding, component classification, scope derivation, acceptance criteria analysis, interaction analysis, state and edge case analysis, ownership separation, prop-driven model definition, and NFR analysis. Triggers include story analysis, user story analysis, FE story analysis, acceptance criteria, component classification, ownership separation, or prop-driven model.
---

# Story Analysis — End to End

## Purpose

This skill performs the **complete analysis of a frontend user story** — from understanding the story through to a fully actionable code generation plan. It is self-contained and embeds all rules, guidelines, and decision logic internally.

---

## Priority Order (Non-Negotiable at Every Decision Point)

```
Dev Notes  →  Project Guidelines  →  Figma  →  React / Frontend Best Practices
```

When two sources conflict, the higher-priority source wins. The conflict and resolution MUST be recorded in DEV_REVIEW.md.

> ⚠️ **Dev Notes are SACRED LAW.** If a Dev Note covers a topic, it IS the answer. Do not produce an alternative, suggestion, or recommendation. Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").

---

## Step 1 — Story Understanding

Extract the following from the JIRA user story:

| Item                      | What to Extract                                       |
| ------------------------- | ----------------------------------------------------- |
| Story title               | Exact title from JIRA                                 |
| Page / component name     | The page or component this story relates to           |
| User goal                 | What the user is trying to achieve                    |
| Business intent           | Why this feature exists from a business perspective   |
| Journey context           | Where this sits in the user journey                   |
| Default view / state      | What the user sees on first load                      |
| Major UI sections         | Named visible regions or panels                       |
| Visible interactions      | All user-triggered actions mentioned or implied       |
| Persona / role variations | Any persona, role, or session-based differences       |
| Dependencies              | Other stories, components, or systems this depends on |
| Explicit in-scope items   | Items the story explicitly includes                   |

### Story Summary Output

Produce a concise story summary covering:

- What the component does
- Who uses it and in what context
- What the primary user goal is
- What the key business intent is

---

## Step 2 — Component Classification

Before any breakdown, classify the primary component using this decision tree:

```text
Component to Analyse
│
├── Is it only rendering Sitecore-authored content (fields, media, links, variants)?
│   No API, no session, no user-specific data?
│   └── PRESENTATIONAL
│
├── Does it fetch data, use session/persona, manage state, or trigger actions?
│   └── TRANSACTIONAL
│
└── Does it have a Sitecore shell AND dynamic data-driven areas?
    └── HYBRID
```

### Classification Rules

| Classification     | When to Use                                                                                                                               | Typical Examples                                            |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Presentational** | Renders authored content, media, links, CTAs, variants and visual layout. No API call or user-specific data.                              | Hero Banner, Promo Card, Rich Text, FAQ, Feature Grid       |
| **Transactional**  | Loads data from APIs, handles user interaction, manages loading/error states, applies persona/session rules or triggers business actions. | Account Settings, Dashboard Section, Policy Summary         |
| **Hybrid**         | Has both a Sitecore-authored shell and dynamic data-driven regions within the same component.                                             | Profile Section with authored header + API-driven data rows |

### Classification Output

Record:

```
Classification: Presentational / Transactional / Hybrid
Rationale: [one clear sentence explaining why]
```

---

## Step 3 — Scope Derivation

Derive out-of-scope items from:

- Explicit story wording ("this story does not cover...")
- AC boundaries (what is not mentioned in any AC)
- Separate story references ("covered in story X")
- Missing detail (no spec, no Figma, no AC)
- Figma elements visible in design but not mentioned in story
- Update/edit actions not covered by any AC

### Scope Output

Produce two lists:

**In Scope:**

- [item 1]
- [item 2]

**Out of Scope (Derived):**

- [item 1] — Reason: [why derived as out of scope]
- [item 2] — Reason: [why derived as out of scope]

---

## Step 4 — Acceptance Criteria Analysis

For every AC in the JIRA story:

1. Assign a stable ID: `AC-001`, `AC-002`, `AC-003` …
2. Restate the AC clearly in plain language
3. Identify the FE implication (what must the frontend do to satisfy this AC?)
4. Identify the owner component (which component is responsible?)
5. Identify state / interaction impact (does this AC trigger a state change, interaction, or conditional render?)
6. Record the agent decision and its basis

> ⚠️ **Do NOT skip vague or implied ACs.** If an AC is ambiguous, make the most reasonable interpretation based on the priority order and record the uncertainty in DEV_REVIEW.md.

### AC Analysis Output Table

| AC ID  | AC Statement | FE Implication | Owner Component | State / Interaction Impact | Agent Decision | Basis |
| ------ | ------------ | -------------- | --------------- | -------------------------- | -------------- | ----- |
| AC-001 |              |                |                 |                            |                |       |

---

## Step 5 — Interaction Analysis

Identify ALL interactions mentioned or implied in the story or Figma context.

### Interaction Types to Check

| Interaction Type                    | Examples                                         |
| ----------------------------------- | ------------------------------------------------ |
| Tab / segment click                 | Switching between tabs, segments, or views       |
| Accordion expand / collapse         | Expand a section to reveal content               |
| Form input                          | Text input, select, checkbox, radio, date picker |
| CTA click                           | Primary/secondary button actions                 |
| Navigation                          | Internal page navigation, back, breadcrumb       |
| Modal / drawer trigger              | Open/close modal, bottom sheet, side panel       |
| Selection                           | Single or multi-select from a list               |
| Filter / search / sort / pagination | List manipulation interactions                   |
| Disabled / unavailable action       | Greyed-out CTA, locked state, restricted action  |
| Scroll / infinite load              | Scroll-triggered data loading                    |
| Hover / focus states                | Tooltip reveal, focus ring, hover highlight      |

### Figma Interaction Rule

If an interaction is **visible in Figma but NOT confirmed in the story or ACs** → mark as:

> `Visible in design but not confirmed in story. Included in analysis based on Figma. Needs developer confirmation if out of scope.`

### Interaction Output Table

| Interaction ID | Interaction Description | Trigger | Owner Component | State Impact | Confirmed In            | Notes |
| -------------- | ----------------------- | ------- | --------------- | ------------ | ----------------------- | ----- |
| INT-001        |                         |         |                 |              | Story / Figma / Derived |       |

---

## Step 6 — State and Edge Case Analysis

### States to Analyse

For every applicable component, analyse all of the following states:

| State             | Definition                                                 |
| ----------------- | ---------------------------------------------------------- |
| Default / initial | What the user sees on first load with no interaction       |
| Active / selected | A tab, item, or option is selected                         |
| Loading           | Data is being fetched — show skeleton/spinner              |
| Success           | Data loaded successfully                                   |
| Empty             | API returned no data or an empty list                      |
| Partial data      | Some fields are missing or null in the response            |
| Error             | API call failed or returned an error                       |
| Disabled          | A control is present but not interactive                   |
| Unavailable       | A feature/action is not available for this persona/session |
| Hidden            | A section is conditionally not rendered                    |

### Edge Cases to Analyse

| Edge Case             | When to Consider                          |
| --------------------- | ----------------------------------------- |
| API failure           | Network error, timeout, 5xx response      |
| Missing data          | Required field absent from API response   |
| Partial data          | Some fields null or absent                |
| Invalid data          | Data present but in unexpected format     |
| Unsupported persona   | User does not have access to this feature |
| Unauthorised access   | Session expired, token invalid            |
| No-access state       | User authenticated but not permitted      |
| Empty list            | API returns empty array                   |
| Failed user action    | Form submission fails, CTA action fails   |
| Missing image / media | Media URL absent or broken                |

### Derivation Rule

If a state or edge case is **not specified in the story** → derive it from project frontend best practices and mark clearly:

> `Derived from project frontend best practices.`

### State and Edge Case Output Table

| State / Edge Case | Applicable Component | Trigger / Condition  | Expected FE Behaviour | Source (Story / Figma / Derived) |
| ----------------- | -------------------- | -------------------- | --------------------- | -------------------------------- |
| Loading           |                      | API call in progress | Show skeleton         | Derived                          |
| Error             |                      | API returns 5xx      | Show error message    | Derived                          |

---

## Step 7 — Ownership Separation and Prop-Driven Model

Clearly separate what is owned by Sitecore/CMS, Backend/API, and Frontend. Then produce the explicit prop-driven model for every component.

### Ownership Categories

| Owner                      | Owns                                                                                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sitecore / CMS**         | Labels, copy, media, links, CTAs, variants, authored configuration, error message copy, localisation strings                                |
| **Backend / API / System** | Runtime values, user-specific data, computed fields, policy data, account data, transaction data                                            |
| **Frontend**               | Rendering logic, interaction handling, state management, persona/session-driven conditional logic, API integration wiring, visibility rules |

### Prop Source Rules

| Item                   | Expected Source                                                |
| ---------------------- | -------------------------------------------------------------- |
| Labels                 | Sitecore / localisation / API-provided config                  |
| Field values           | Backend API / system-derived values                            |
| CTA text               | Sitecore / localisation / API-provided config                  |
| CTA links              | Sitecore / API                                                 |
| Variants               | Sitecore config or feature-level prop                          |
| Visibility flags       | Derived from parent/container logic                            |
| Empty / error messages | Sitecore / API — but props or project-standard fallback config |

If the final source is unknown:

> `Source contract not provided. Keep as prop-driven and map later once Sitecore/API contract is available.`

### 7.1 — Ownership Output Table

| Area              | Expected Source                  | Owner            | Notes |
| ----------------- | -------------------------------- | ---------------- | ----- |
| Page heading      | Sitecore/content prop            | Sitecore         |       |
| Tab labels        | Sitecore/content prop            | Sitecore         |       |
| Field labels      | Sitecore/localisation/API config | Content/config   |       |
| Field values      | Backend/API/system               | Backend/API      |       |
| Visibility        | FE derived state                 | Frontend         |       |
| Interaction state | FE state                         | Frontend         |       |
| Variants          | Sitecore config or FE prop       | Depends on story |       |
| Error copy        | Project fallback/config prop     | Content/config   |       |

### 7.2 — Prop-Driven Component Model (Per Component)

For **every component** identified in the story analysis, produce the explicit prop shape:

> ⚠️ **Rules:**
>
> - Every prop must have a declared source: `Sitecore` / `BFF API` / `FE Derived` / `Unknown — keep as prop`.
> - No prop may be hardcoded. No label, value, copy, or colour may be inlined.
> - If source is unknown → represent as a prop and mark: `Source contract not provided. Keep as prop-driven and map later.`
> - Correlated with Phase 4 API contracts — every API field used as a prop must reference its source endpoint and field name.
> - Apply Sitecore Helper functions where applicable: `extractFormField`, `extractCTA`, `extractLink`, `findErrorMessage`, `extractApiResponseMessages`.

**Output format per component:**

```
Component: [ComponentName]
Type: [Sitecore-mapped / Container / View / Feature Display / Design System]

| Prop Name        | Type       | Source         | Source Detail (field/endpoint)     | Required? | Notes |
| ---------------- | ---------- | -------------- | ---------------------------------- | --------- | ----- |
| [propName]       | string     | Sitecore       | [Sitecore field name]              | Yes       |       |
| [propName]       | string     | BFF API        | [endpoint + field path]            | Yes       |       |
| [propName]       | boolean    | FE Derived     | Computed from [condition]          | Yes       |       |
| [propName]       | string     | Unknown        | Source contract not provided       | Yes       |       |
```

**Sitecore Helper Usage (where applicable):**

| Helper Function                 | When to Apply                                                      |
| ------------------------------- | ------------------------------------------------------------------ |
| `extractFormField`              | When extracting form field config from Sitecore data               |
| `extractCTA`                    | When extracting CTA configuration from Sitecore                    |
| `extractLink`                   | When extracting link configuration from Sitecore                   |
| `findErrorMessage`              | When mapping API error codes to Sitecore-authored display messages |
| `transformSitecoreDynamicValue` | When replacing placeholders in Sitecore dynamic values             |
| `extractApiResponseMessages`    | When extracting API response messages from Sitecore data           |

---

## Step 8 — NFR Analysis

> ⚠️ **Scope:** This step covers ONLY the following NFR categories:
>
> - **Section 6** — RTL (Right-to-Left) Layout Support
> - **Section 7** — Accessibility (a11y)
> - **Section 9** — Responsive Design
> - **Section 10** — Overflow & Scroll Handling
>
> Other NFR categories (Localisation, Performance, Security/PII, Maintainability, Testability) are covered by other phases and skills. Do NOT analyse them here.

All derived NFR recommendations must be marked:

> `Derived from project frontend standards and best practices.`

### 8.1 — RTL (Right-to-Left) Support

> **Context:** This project does NOT use i18n libraries. RTL is implemented via CSS logical properties, TailwindCSS RTL utilities, and the HTML `dir` attribute.

| Rule                         | Correct Approach                                                        |
| ---------------------------- | ----------------------------------------------------------------------- |
| Layout direction             | Set `dir` at `<html>` root — single source of truth                     |
| Margins / padding            | Use CSS logical properties: `margin-inline-start`, `padding-inline-end` |
| Text alignment               | Use `text-start` / `text-end` — never `text-left` / `text-right`        |
| Directional icons            | Mirror arrows/chevrons in RTL: `rtl:rotate-180`                         |
| Symmetric icons              | Do NOT mirror: close ✕, check ✓, warning ⚠                              |
| Mixed-language inputs        | Use `dir="auto"` on text inputs                                         |
| LTR content in RTL text      | Wrap with `<bdi>` (IDs, codes, numbers)                                 |
| Floats                       | Never use `float: left` / `float: right` — use Flexbox or Grid          |
| Absolute positioning         | Never use hardcoded `left`/`right` offsets in RTL-sensitive layouts     |
| Physical directional classes | Never use `ml-`, `mr-`, `pl-`, `pr-` in layout-critical styles          |

### 8.2 — Accessibility (a11y)

| Rule                      | Implementation                                                               |
| ------------------------- | ---------------------------------------------------------------------------- |
| Semantic HTML             | Use `<header>`, `<main>`, `<nav>`, `<section>`, `<table>`, `<button>`        |
| Interactive elements      | Every interactive element must have `aria-label` or visible label            |
| Scrollable containers     | Use `role="region"` + `aria-label`                                           |
| Dynamic content           | Use `aria-live="polite"` on infinite scroll loaders and status updates       |
| Loading tables/lists      | Use `aria-busy={isLoading}`                                                  |
| Form inputs               | Use `<label htmlFor>` — never omit labels                                    |
| Keyboard navigation       | All interactive elements must be keyboard-navigable                          |
| Table headers             | Use `scope="col"` on `<th>` elements                                         |
| Non-semantic interactives | Never use `div` or `span` for interactive elements — use `<button>` or `<a>` |

### 8.3 — Responsive Design

- **Design reference widths:** Mobile: `390px` | Desktop: `1700px`
- Use the **Responsive Reconciliation JSON** (`responsive_design_intent.json`) as the authoritative source for responsive behaviour when both viewports are provided.
- If only one viewport is available, use that context file directly.
- Apply **mobile-first** implementation: base classes apply to mobile, `lg:` overrides apply to desktop.
- Use the `Grid` / `GridItem` components from `@dxp/design-system` for responsive layouts:
  - `columns={12}` for responsive layouts (mobile → desktop)
  - `columns={4}` for mobile-only layouts
- Mobile fill: `w-full` | Desktop fixed: `w-full lg:max-w-[1700px]`

### 8.4 — Overflow & Scroll Handling

- Apply `overflow-y-auto` to any container whose content can exceed its height.
- Apply `overflow-x-auto` to containers with wide content (tables, carousels).
- Use `overflow-auto` when content may exceed both width and height.
- Always add `role="region"` and `aria-label` to scrollable containers.
- Never allow content to overflow and become hidden or inaccessible without scroll.
- Never use `overflow: hidden` on containers with dynamic/variable-length content.

### NFR Analysis Output

| NFR Category      | Applies? | Agent Decision / Recommendation | Source                  |
| ----------------- | -------- | ------------------------------- | ----------------------- |
| RTL               | Yes/No   |                                 | Story / Figma / Derived |
| Accessibility     | Yes/No   |                                 | Story / Figma / Derived |
| Responsive        | Yes/No   |                                 | Story / Figma / Derived |
| Overflow & Scroll | Yes/No   |                                 | Story / Figma / Derived |

---

## Guardrails

### Always Do

- Check active Dev Notes list before every decision in this skill. If a Dev Note covers the topic, it IS the answer.
- Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").
- Apply the priority order at every decision point: Dev Notes → Guidelines → Figma → Best Practices.
- Mark every derived recommendation clearly: `Derived from project frontend best practices.`
- Mark every missing input clearly: `Not Provided.`
- Record every uncertain decision in DEV_REVIEW.md — never in ANALYSIS_PLAN.md.
- Keep all components prop-driven — no hardcoded labels, values, or copy.
- Separate Sitecore, API, and FE ownership clearly.
- Analyse all states and edge cases even if not mentioned in the story.
- Analyse the 4 in-scope NFR categories (RTL, Accessibility, Responsive Design, Overflow & Scroll Handling) even if not mentioned in the story.
- Use Figma Responsive Reconciliation JSON as authoritative source for responsive behaviour.

### Never Do

- Never override a Dev Note — not even as a "suggestion" or "recommendation".
- Never hardcode labels, values, copy, or colours inside feature components.
- Never write "needs developer approval", "to be confirmed", "option A or B" in ANALYSIS_PLAN.md.
- Never write "Check if supported in DEV REVIEW" or any equivalent phrase.
- Never skip any step in this skill — all steps are mandatory.
- Never invent API fields or Sitecore props that are not in the spec.
- Never use raw mobile/desktop context JSONs to override the Responsive Reconciliation JSON.
- Never place API calls inside feature display components.
- Never place business logic inside design-system components.
- Never generate implementation code — that is the Coding Agent's job.

---

## Output Checklist (Self-Verify Before Proceeding to Next Skill)

Before passing output to the next phase, verify:

- [ ] Story fully understood — title, goal, intent, journey context, major sections recorded
- [ ] Component classified as Presentational / Transactional / Hybrid with rationale
- [ ] In-scope and out-of-scope items clearly listed
- [ ] All ACs analysed with FE implications, owner components, and state/interaction impact
- [ ] All interactions identified — story-confirmed and Figma-visible ones labelled separately
- [ ] All states analysed: default, loading, success, empty, error, disabled, unavailable, hidden
- [ ] All edge cases analysed: API failure, missing data, partial data, invalid data, persona, auth, empty list
- [ ] Ownership table produced — Sitecore, API, and FE ownership clearly separated (Step 7.1)
- [ ] Prop-driven model produced for EVERY component — all props have declared source, type, and detail (Step 7.2)
- [ ] Every prop correlated with API contracts where applicable
- [ ] Sitecore Helper functions identified where applicable (extractFormField, extractCTA, extractLink, etc.)
- [ ] NFR analysis completed for the 4 in-scope categories: RTL, Accessibility, Responsive Design, Overflow & Scroll Handling
- [ ] Every Dev Note applied and labelled with DN ID
- [ ] Every uncertain decision recorded in DEV_REVIEW.md, not in ANALYSIS_PLAN.md
