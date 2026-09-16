---
name: story-analysis-end-to-end
description: Use this skill to perform end-to-end analysis of a frontend user story from the story text alone — story understanding, component classification, scope derivation, acceptance criteria, interactions, states, ownership separation, provisional prop model, and NFR analysis. Runs before Figma and API analysis; produces the classification that drives context validation. Triggers include story analysis, user story analysis, FE story analysis, acceptance criteria, or component classification.
---

## Story Analysis — End to End

### Purpose

This skill performs the **complete analysis of a frontend user story from the story text alone**. It is self-contained and embeds all rules, guidelines, and decision logic internally.
### Priority Order (Non-Negotiable at Every Decision Point)

```text
Dev Notes  →  Project Guidelines  →  React / Frontend Best Practices
```

⚠️ **Dev Notes are SACRED LAW.** If a Dev Note covers a topic, it IS the answer. Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").
---

### ⚠️ INPUTS — STORY ONLY

| Input | Available? |
| --- | --- |
| JIRA User Story | ✅ **Use this** |
| Developer Notes (DN-xxx) | ✅ **Use this — sacred law** |
| Figma Design Intent JSONs | ❌ Not yet analysed — do NOT read |
| Sitecore API JSON | ❌ Not yet analysed — do NOT read |
| BFF API specs | ❌ Not yet analysed — do NOT read |

The artefacts were fetched in Phase 2, but they are **interpreted in Phases 5 and 6**. This phase derives everything it can from the story and Dev Notes, and explicitly marks what must be resolved later.

⚠️ Do not open, parse, or reason over Figma or API artefacts here. Doing so duplicates work the dedicated skills perform, and produces conclusions that later phases will contradict.

---

### ⚠️ PROVISIONAL vs FINAL OUTPUTS

Because Figma and API context are not yet available, some outputs are **provisional** and are enriched by the phases that follow.

| Step | Status After This Phase | Enriched By |
| --- | --- | --- |
| 1 — Story Understanding | **Final** | — |
| 2 — Classification | **Final** — drives Context Validation | — |
| 3 — Scope Derivation | **Final** | — |
| 4 — Acceptance Criteria | **Final** | — |
| 5 — Interaction Analysis | **Provisional** — story-declared only | Phase 5 adds design-only interactions |
| 6 — State & Edge Cases | **Provisional** — story + UI states only | Phase 6 adds API-driven states |
| 7.1 — Ownership Separation | **Provisional** — ownership category per item | Phases 5–6 confirm exact sources |
| 7.2 — Prop-Driven Model | **Provisional** — props + `Source` known; `Source Detail` pending | Phase 6 fills field/endpoint; Phase 5 confirms labels |
| 8 — NFR Analysis | **Provisional** — story-derived requirements | Phase 5 adds design-driven RTL/responsive exceptions |

For every provisional item that cannot yet be resolved, write `To be resolved in Figma/API analysis` rather than guessing. Never invent a field name, endpoint, node name, or token to complete a provisional structure.

---

### ⚠️ ANALYSIS DEPTH vs OUTPUT WIDTH

**Every step is mandatory and must be performed in full.** What is trimmed is only what gets emitted into ANALYSIS_PLAN.md.

| Step | Analysis Performed | Emitted To |
| --- | --- | --- |
| 1 — Story Understanding | All 11 items extracted in full | **§2 (4 fields only)**; remainder → internal + DEV_REVIEW context |
| 2 — Classification | Full decision tree | **§3** + **Context Validation gate** |
| 3 — Scope Derivation | In-scope **and** out-of-scope derived | **§8 Things NOT to Implement**; in-scope → internal |
| 4 — Acceptance Criteria | All ACs incl. agent decision + basis | **§4 (5 cols)**; decision/basis → **DEV_REVIEW §1/§4** |
| 5 — Interaction Analysis | All story-declared interactions | **§9 (5 cols)**; `Confirmed In`/`Notes` → **DEV_REVIEW §4** |
| 6 — State & Edge Cases | All story + UI states | **§10 (4 cols)**; `Source` → **DEV_REVIEW §4** |
| 7.1 — Ownership Separation | Full Sitecore/API/FE separation | **Internal only** — feeds 7.2; no standalone table |
| 7.2 — Prop-Driven Model | Full prop table per component | **§12** — the authoritative ownership record |
| 8 — NFR Analysis | All 4 categories against all rules | **§13.2 exceptions only**; baselines → internal |

⚠️ **Never emit these columns into ANALYSIS_PLAN.md:** `Agent Decision`, `Basis`, `Confirmed In`, `Source`, `Confidence`, `Notes`. Route every one of them into DEV_REVIEW.md.

---

### Step 1 — Story Understanding

Extract all eleven items. They inform classification, scope, and component planning even when not emitted.

| Item | What to Extract | Emitted? |
| --- | --- | --- |
| Story title | Exact title from JIRA | ✅ §2 |
| Page / component name | The page or component this story relates to | ✅ §2 |
| Default view / state | What the user sees on first load | ✅ §2 |
| Persona / role variations | Any persona, role, or session-based differences | ✅ §2 |
| User goal | What the user is trying to achieve | ❌ internal |
| Business intent | Why this feature exists | ❌ internal |
| Journey context | Where this sits in the user journey | ❌ internal |
| Major UI sections | Named visible regions or panels | ❌ internal → drives breakdown |
| Visible interactions | All user-triggered actions mentioned or implied | ❌ internal → feeds Step 5 |
| Dependencies | Other stories, components, or systems | ❌ internal → DEV_REVIEW if risk-bearing |
| Explicit in-scope items | Items the story explicitly includes | ❌ internal → feeds Step 3 |

Produce a concise internal summary covering what the component does, who uses it, the primary user goal, and the key business intent. Only the four emitted fields reach §2.

---

### Step 2 — Component Classification

⚠️ **This is the most consequential output of this phase.** It determines which artefacts the Context Validation gate treats as mandatory. A wrong classification either blocks a valid story or lets an under-specified one through.

Classify using this decision tree:

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

#### Classification Rules

| Classification | When to Use | Typical Examples |
| --- | --- | --- |
| **Presentational** | Renders authored content, media, links, CTAs, variants and visual layout. May own local visual interaction (carousel index, hover, expand). No API call or user-specific data. | Hero Banner, Hero Carousel, Promo Card, Rich Text, FAQ, Feature Grid |
| **Transactional** | Loads data from APIs, handles user interaction, manages loading/error states, applies persona/session rules or triggers business actions. | Account Settings, Dashboard Section, Policy Summary |
| **Hybrid** | Has both a Sitecore-authored shell and dynamic data-driven regions within the same component. | Profile Section with authored header + API-driven data rows |

#### Classification Signals in the Story

Read for these, since the API spec is not yet available:
- Mentions of endpoints, operationIds, or "fetch/load/submit/save" → Transactional
- Mentions of persona, role, entitlement, session → Transactional
- Only authored copy, media, links, CTAs, variants → Presentational
- Authored shell plus a data-driven region → Hybrid

⚠️ If the story mentions backend operationIds, the component is **not** Presentational — regardless of how simple its UI looks. Phase 4 will fail validation on this mismatch, so resolve it here.

If the story is genuinely ambiguous, choose the classification the **acceptance criteria** support, and record the reasoning in DEV_REVIEW.md §1.

#### Classification Output → §3

```text
Classification: Presentational / Transactional / Hybrid
Rationale: [one clear sentence explaining why]
Data-Fetching Required: Yes / No
CMS-Authored Required: Yes / No
FE-Only Logic: [local state, visibility, mapping, layout logic summary]
```

---

### Scope Rules Based on Classification

#### If Classification = Presentational

| Step | Execute? | Scope Note |
| --- | --- | --- |
| Step 3: Scope Derivation | Yes | Full |
| Step 4: Acceptance Criteria | Yes | Full |
| Step 5: Interaction Analysis | Yes | UI-level only — carousel, accordion, hover, focus, scroll; no API triggers |
| Step 6: State & Edge Cases | **Yes — SCOPED** | ⚠️ See below |
| Step 7.1: Ownership Separation | Yes | Sitecore vs FE only — no API column |
| Step 7.2: Prop-Driven Model | Yes | Sitecore props + FE-derived props only; no BFF API props |
| Step 8: NFR Analysis | Yes | Full (RTL, Accessibility, Responsive, Overflow) |

⚠️ **Step 6 is SCOPED, not skipped.** A Presentational component still has real states — default, active/selected slide, hover, focus, disabled, paused, hidden. Skipping Step 6 would leave §10 empty and deprive the Coding Agent of a state contract, and leave Test Generation with no state cases to cover.

**For Presentational, Step 6 must:**
- ✅ Analyse: default/initial, active/selected, disabled, hidden, hover/focus, and any visual-effect state (autoplay, paused, transitioning).
- ❌ Omit: loading, success, empty, partial data, error, unavailable — API-driven with no trigger in a Presentational component.
- ❌ Omit all API-driven edge cases (API failure, missing/partial/invalid data, unauthorised, empty list).
- ✅ Keep media edge cases where relevant (missing image / broken media URL).

#### If Classification = Transactional or Hybrid

Execute ALL steps (Step 3 through Step 8) in full. No step may be skipped or scoped down.

---

### Step 3 — Scope Derivation

Derive out-of-scope items from:
- Explicit story wording ("this story does not cover…")
- AC boundaries (what is not mentioned in any AC)
- Separate story references ("covered in story X")
- Missing detail (no spec, no AC)
- Update/edit actions not covered by any AC

Produce **both** lists internally:

**In Scope** — internal working list. Validates that Step 4 ACs and the later breakdown cover everything. Not emitted as its own section.

**Out of Scope (Derived)** — each item with its reason. **Emitted to §8 — Things NOT to Implement**, the single authoritative out-of-scope guardrail for the Coding Agent.

⚠️ Design elements visible in Figma but not mentioned in the story cannot be assessed yet. Phase 5 adds them to the out-of-scope list if they are genuinely unsupported by any AC.

---

### Step 4 — Acceptance Criteria Analysis

For every AC in the JIRA story:
- Assign a stable ID: AC-001, AC-002, AC-003 …
- Restate the AC clearly in plain language
- Identify the FE implication (what must the frontend do?)
- Identify the owner component
- Identify state / interaction impact
- **Determine the agent decision and its basis** — still required; it disciplines the interpretation

⚠️ **Do NOT skip vague or implied ACs.** If an AC is ambiguous, make the most reasonable interpretation using the priority order, then record the uncertainty in DEV_REVIEW.md.

#### AC Output → §4

| AC ID | AC Statement | FE Implication | Owner Component | State / Interaction Impact |
| --- | --- | --- | --- | --- |
| AC-001 | | | | |

#### Provenance Routing
- Ambiguous or judgement-based AC interpretation → **DEV_REVIEW.md §1**
- Derived vs story-confirmed status → **DEV_REVIEW.md §4**

---

### Step 5 — Interaction Analysis (Provisional)

Identify ALL interactions mentioned or implied **in the story**.

#### Interaction Types to Check

| Interaction Type | Examples |
| --- | --- |
| Tab / segment click | Switching between tabs, segments, views |
| Accordion expand / collapse | Expand a section to reveal content |
| Carousel / slider | Next, previous, pager, autoplay, pause-on-hover |
| Form input | Text, select, checkbox, radio, date picker |
| CTA click | Primary/secondary button actions |
| Navigation | Internal page navigation, back, breadcrumb |
| Modal / drawer trigger | Open/close modal, bottom sheet, side panel |
| Selection | Single or multi-select from a list |
| Filter / search / sort / pagination | List manipulation |
| Disabled / unavailable action | Greyed-out CTA, locked state |
| Scroll / infinite load | Scroll-triggered data loading |
| Hover / focus states | Tooltip reveal, focus ring, hover highlight |

⚠️ **Interactions visible only in the design are added later** by Phase 5. Do not speculate about them here.

#### Interaction Output → §9

| Interaction ID | Description | Trigger | Owner Component | State Impact |
| --- | --- | --- | --- | --- |
| INT-001 | | | | |

`Confirmed In` and any `Notes` → **DEV_REVIEW.md §4**.

Continue the INT-xxx numbering in Phase 5 when Figma-only interactions are added. Do not renumber.

---

### Step 6 — State and Edge Case Analysis (Provisional)

#### States to Analyse

| State | Definition | Presentational? |
| --- | --- | --- |
| Default / initial | What the user sees on first load with no interaction | ✅ |
| Active / selected | A tab, item, slide, or option is selected | ✅ |
| Hover / focus | Pointer or keyboard focus state | ✅ |
| Disabled | A control is present but not interactive | ✅ |
| Hidden | A section is conditionally not rendered | ✅ |
| Transitioning / paused | Animation or autoplay state (carousel, banner) | ✅ |
| Loading | Data is being fetched — show skeleton/spinner | ❌ API-driven |
| Success | Data loaded successfully | ❌ API-driven |
| Empty | API returned no data or an empty list | ❌ API-driven |
| Partial data | Some fields missing or null in the response | ❌ API-driven |
| Error | API call failed or returned an error | ❌ API-driven |
| Unavailable | Feature/action not available for this persona/session | ❌ API-driven |

#### Edge Cases to Analyse

| Edge Case | When to Consider | Presentational? |
| --- | --- | --- |
| Missing image / media | Media URL absent or broken | ✅ |
| Long / overflowing content | Text growth, localisation, narrow viewport | ✅ |
| API failure | Network error, timeout, 5xx | ❌ |
| Missing data | Required field absent from response | ❌ |
| Partial data | Some fields null or absent | ❌ |
| Invalid data | Data present but unexpected format | ❌ |
| Unsupported persona | User lacks access | ❌ |
| Unauthorised access | Session expired, token invalid | ❌ |
| No-access state | Authenticated but not permitted | ❌ |
| Empty list | API returns empty array | ❌ |
| Failed user action | Form submission or CTA action fails | ❌ |

⚠️ **For Transactional/Hybrid stories**, analyse API-driven states from the story's described behaviour. Phase 6 later refines them against the actual contract — for example, mapping specific error codes to specific UI states.

#### Derivation Rule
If a state or edge case is not specified in the story, derive it from project frontend best practices. Emit the behaviour definitively into §10; record `Derived` status in **DEV_REVIEW.md §4**.

#### State Output → §10

| State / Edge Case | Applicable Component | Trigger / Condition | Expected FE Behaviour |
| --- | --- | --- | --- |
| | | | |

Continue STATE-xxx numbering in Phase 6; do not renumber.

---

### Step 7 — Ownership Separation and Provisional Prop Model

#### Ownership Categories

| Owner | Owns |
| --- | --- |
| **Sitecore / CMS** | Labels, copy, media, links, CTAs, variants, authored configuration, error message copy, localisation strings |
| **Backend / API / System** | Runtime values, user-specific data, computed fields, policy data, account data, transaction data |
| **Frontend** | Rendering logic, interaction handling, state management, persona/session conditional logic, API integration wiring, visibility rules |

#### Prop Source Rules

| Item | Expected Source |
| --- | --- |
| Labels | Sitecore / localisation / API-provided config |
| Field values | Backend API / system-derived values |
| CTA text | Sitecore / localisation / API-provided config |
| CTA links | Sitecore / API |
| Variants | Sitecore config or feature-level prop |
| Visibility flags | Derived from parent/container logic |
| Empty / error messages | Sitecore / API — or project-standard fallback config |

#### 7.1 — Ownership Separation (INTERNAL WORKING STEP)

⚠️ **This step produces no standalone section in ANALYSIS_PLAN.md.** Ownership is stated **per prop** in §12, because per-prop ownership is what actually generates code.

Perform the separation in full for every content/data item — page headings, tab labels, field labels, field values, visibility, interaction state, variants, error copy. Carry every conclusion directly into 7.2 as the `Source` value.

Self-check before proceeding: every item classified in 7.1 must appear as a prop row in 7.2. If an item has no prop, either it is not rendered, or a prop is missing.

#### 7.2 — Provisional Prop-Driven Component Model → §12

For **every component** identified, produce the explicit prop shape.

**Rules:**
- Every prop must declare a source: `Sitecore` / `BFF API` / `FE Derived` / `Unknown`.
- No prop may be hardcoded. No label, value, copy, or colour may be inlined.
- **`Source Detail` is provisional at this stage.** The exact Sitecore field name or API field path is not yet known — Phases 5 and 6 resolve it.

**Output format per component:**

```text
Component: [ComponentName]
Type: [Sitecore-mapped / Container / View / Feature Display / Design System]

| Prop Name | Type    | Source     | Source Detail (field/endpoint)        | Required? |
| --------- | ------- | ---------- | ------------------------------------- | --------- |
| [prop]    | string  | Sitecore   | To be resolved in API analysis        | Yes       |
| [prop]    | string  | BFF API    | To be resolved in API analysis        | Yes       |
| [prop]    | boolean | FE Derived | Computed from [condition]             | Yes       |
| [prop]    | string  | Unknown    | Source contract not provided          | Yes       |
```

⚠️ `FE Derived` props can be completed now — their detail is a computation, not an external contract. Sitecore and BFF props carry `To be resolved in API analysis` until the contract is read.

⚠️ **Never invent a field name or endpoint path** to fill `Source Detail`. An invented path silently produces broken generated code.

**Sitecore Helper Usage (where applicable):**

| Helper Function | When to Apply |
| --- | --- |
| `extractFormField` | Extracting form field config from Sitecore data |
| `extractCTA` | Extracting CTA configuration from Sitecore |
| `extractLink` | Extracting link configuration from Sitecore |
| `findErrorMessage` | Mapping API error codes to Sitecore-authored display messages |
| `transformSitecoreDynamicValue` | Replacing placeholders in Sitecore dynamic values |
| `extractApiResponseMessages` | Extracting API response messages from Sitecore data |

---

### Step 8 — NFR Analysis (Provisional)

⚠️ **Scope:** RTL, Accessibility (a11y), Responsive Design, Overflow & Scroll Handling.

**Analyse every rule below in full.** Emit only **story-specific exceptions** to §13.2 — baseline rules are already embedded in the Coding Agent's skills.

#### 8.1 — RTL (Right-to-Left) Support

**Context:** This project does NOT use i18n libraries. RTL is implemented via CSS logical properties, TailwindCSS RTL utilities, and the HTML `dir` attribute.

| Rule | Correct Approach |
| --- | --- |
| Layout direction | Set `dir` at `<html>` root — single source of truth |
| Margins / padding | CSS logical properties: `margin-inline-start`, `padding-inline-end` |
| Text alignment | `text-start` / `text-end` — never `text-left` / `text-right` |
| Directional icons | Mirror arrows/chevrons in RTL: `rtl:rotate-180` |
| Symmetric icons | Do NOT mirror: close ✕, check ✓, warning ⚠ |
| Mixed-language inputs | Use `dir="auto"` on text inputs |
| LTR content in RTL text | Wrap with `<bdi>` (IDs, codes, numbers) |
| Floats | Never `float: left` / `float: right` — use Flexbox or Grid |
| Absolute positioning | Never hardcoded left/right offsets in RTL-sensitive layouts |
| Physical directional classes | Never `ml-`, `mr-`, `pl-`, `pr-` in layout-critical styles |

#### 8.2 — Accessibility (a11y)

| Rule | Implementation |
| --- | --- |
| Semantic HTML | `<header>`, `<main>`, `<nav>`, `<section>`, `<table>`, `<button>` |
| Interactive elements | Every one must have `aria-label` or a visible label |
| Scrollable containers | `role="region"` + `aria-label` |
| Dynamic content | `aria-live="polite"` on loaders and status updates |
| Loading tables/lists | `aria-busy={isLoading}` |
| Form inputs | `<label htmlFor>` — never omit labels |
| Keyboard navigation | All interactive elements keyboard-navigable |
| Table headers | `scope="col"` on `<th>` |
| Non-semantic interactives | Never `div`/`span` for interactive elements — use `<button>`/`<a>` |

#### 8.3 — Responsive Design

- **Design reference widths:** Mobile 390px · Desktop 1700px
- Apply **mobile-first**: base classes for mobile, `lg:` overrides for desktop.
- Use `Grid` / `GridItem` from `@dxp/design-system`: `columns={12}` responsive, `columns={4}` mobile-only.
- Mobile fill `w-full`; desktop fixed `w-full lg:max-w-[1700px]`.

⚠️ Detailed responsive behaviour comes from the design. Phase 5 produces the authoritative responsive contract. Record here only what the **story** explicitly requires.

#### 8.4 — Overflow & Scroll Handling

- `overflow-y-auto` for containers whose content can exceed height.
- `overflow-x-auto` for wide content (tables, carousels).
- `overflow-auto` when content may exceed both dimensions.
- Always add `role="region"` and `aria-label` to scrollable containers.
- Never allow content to overflow and become hidden without scroll.
- Never `overflow: hidden` on containers with dynamic/variable-length content.

#### NFR Output → §13.2 (Exceptions Only)

| NFR Category | Story-Specific Exception / Requirement |
| --- | --- |
| | |

Emit a row **only** when this story needs something beyond the standard rules. If nothing, emit:

```text
No story-specific NFR exceptions. Standard project NFR rules apply.
```

---

### Handoff to Phase 4 (Context Validation)

This phase's **classification** is the input Context Validation depends on:

```text
Presentational        →  Sitecore + Figma required; BFF not checked
Transactional/Hybrid  →  Sitecore + Figma + BFF all required
```

State the classification unambiguously. If the signals surfaced a contradiction — e.g. the story names backend operationIds but the UI looks purely presentational — resolve it **here**, in favour of the stronger signal (API usage ⇒ Transactional). Phase 4 will halt on an unresolved mismatch.

---

### Guardrails

#### Always Do
- Check the active Dev Notes list before every decision; label with DN IDs.
- Apply the priority order at every decision point.
- **Perform every step in full** — analysis depth is never reduced.
- **Produce a definitive classification** — the Context Validation gate depends on it.
- Mark provisional items as `To be resolved in Figma/API analysis`.
- Route every `Basis`, `Confidence`, `Source`, `Confirmed In` and `Agent Decision` into DEV_REVIEW.md.
- Mark every missing input clearly: Not Provided.
- Keep all components prop-driven.
- Carry every Step 7.1 ownership conclusion into a Step 7.2 prop row.
- Analyse all applicable states and edge cases even when not mentioned in the story.

#### Never Do
- **Never read or reason over Figma context, Sitecore JSON, or BFF specs in this phase.**
- **Never invent a field name, endpoint path, node name, or token** to complete a provisional structure.
- Never override a Dev Note — not even as a "suggestion".
- **Never classify a component as Presentational when the story references backend endpoints.**
- Never skip Step 6 for a Presentational component — **scope** it instead.
- **Never emit `Agent Decision`, `Basis`, `Confirmed In`, `Source`, `Confidence` or `Notes` columns into ANALYSIS_PLAN.md.**
- **Never emit a standalone Ownership table** — ownership lives per-prop in §12.
- **Never emit a standalone In-Scope section** — out-of-scope goes to §8 only.
- **Never emit NFR baseline rows** — §13.2 carries exceptions only.
- Never write "needs developer approval", "to be confirmed", or "option A or B" into ANALYSIS_PLAN.md.
- Never place API calls inside feature display components.
- Never place business logic inside design-system components.
- Never generate implementation code.

---

### Output Checklist (Self-Verify Before Phase 4)

**Analysis completeness:**
- [ ] All 11 story-understanding items extracted (even the 7 not emitted)
- [ ] **Component classified with rationale — definitive, no deferral**
- [ ] In-scope **and** out-of-scope both derived
- [ ] All ACs analysed with FE implications, owner components, state/interaction impact
- [ ] All story-declared interactions identified
- [ ] All applicable states analysed (scoped correctly for Presentational)
- [ ] All applicable edge cases analysed
- [ ] Ownership separation completed for every content/data item (Step 7.1)
- [ ] Provisional prop model produced for EVERY component (Step 7.2)
- [ ] Every 7.1 ownership item appears as a 7.2 prop row
- [ ] Unresolved `Source Detail` marked `To be resolved in API analysis` — never invented
- [ ] All 4 NFR categories analysed against all rules

**Emission discipline:**
- [ ] §2 carries only Title, Page/Component, Default View/State, Personas
- [ ] §3 classification stated definitively
- [ ] §4 carries exactly 5 columns — no Agent Decision, no Basis
- [ ] §9 carries exactly 5 columns — no Confirmed In, no Notes
- [ ] §10 carries exactly 4 columns — no Source; **non-empty for every classification**
- [ ] No standalone Ownership or In-Scope section produced
- [ ] §13.2 carries exceptions only — no baseline rows
- [ ] Every Dev Note applied and labelled with its DN ID
- [ ] Every uncertain decision and provenance value routed to DEV_REVIEW.md
- [ ] No Figma context file or API spec file was opened
