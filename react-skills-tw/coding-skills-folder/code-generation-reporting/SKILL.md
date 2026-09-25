---
name: code-generation-reporting
description: Use to produce the SINGLE consolidated code-generation summary document covering file inventory, UI, Sitecore, logic, data flow, state behaviour, tests, AC evidence, deviations, and an append-only change log in one file. Written to serve both the reviewing developer and the defect fix workflow. Replaces the four legacy per-agent documents. Triggers include code generation summary, consolidated report, final document, or write the summary.
disable-model-invocation: true
---

## Code Generation Reporting

### Purpose

Generate **ONE** consolidated summary of everything the Coding Agent produced. This replaces the legacy `CODE_GENERATION.md` + `TEST_GENERATION.md` + Storybook handoff with a single file.

**File path:** `.SS_WF/Agent/CODE/{{ticket_id}}_CODE_GENERATION_SUMMARY.md`

⚠️ This is the **only** document the Coding Agent produces. Source files, stories and tests are implementation artefacts, not reports.

---

## ⚠️ THIS DOCUMENT IS A LIVING RECORD

The summary does not stop being true when code generation ends. **Every later defect fix updates it in place**, so sections 1–12 keep describing the code as it currently is.

```text
Generation          → §1–§12 written · §13 seeded empty
Defect fix DEF-123  → state sections updated + tagged [DEF-123] · §13 entry appended
Defect fix DEF-456  → state sections updated + tagged [DEF-456] · §13 entry appended
```

That is why this skill **seeds §13 on the first run**. Without it, a summary that has never had a defect is structurally different from one that has, and the defect agent must create the section rather than append to it.

⚠️ **There is no separate `DEFECT_FIX_SUMMARY.md`.** The §13 Change Log replaced it.

⚠️ **The code may also change without a defect.** Developers often edit generated code. The defect workflow therefore treats this document as a **map** and verifies it against the current code — write paths, symbols and traces precisely so they can be verified.

### State vs Historical Sections

| Nature | Sections | Later behaviour |
| --- | --- | --- |
| **State** — what the code IS | §3 §4 §5 §6 §7 §8 §9 §10 §12.4 | Updated in place by every defect fix |
| **Historical** — what happened at build | §1 §2 §11 §12.1 §12.2 §12.5 | Never changed after generation (§11 status only) |
| **Append-only** | §13 | One entry per defect fix or enhancement |

---

## ⚠️ THE TWO CONSUMERS — WRITE FOR BOTH

| Consumer | What they need | The question they ask |
| --- | --- | --- |
| **Reviewing Developer** | What was built and **why** a decision was made | *"Why was it done this way?"* |
| **Defect Fix Workflow** | The file, layer and symbol responsible for a behaviour | *"Where do I look when X breaks?"* |

### The Governing Principle

> **Document decisions and locations — not compliance.**
>
> If a rule is enforced by a coding skill and verified by the self-validation gate, restating it adds length without diagnostic value.
>
> If something was **decided** — a token created, a gap worked around, a conflict resolved, a fallback chosen — that reasoning exists **nowhere else** and must be captured.

```text
❌ "Mobile-first approach applied"              → compliance, already enforced
❌ "Logical properties used for RTL"            → compliance, already enforced
❌ 40-row table where every row says "Covered"  → noise

✅ "Created --gap-18 (18px); no existing token matched Figma"
✅ "Figma showed 3-col; plan said 2-col → implemented Figma (visual source of truth)"
✅ "policyNumber null → mapPolicyResponse() returns '—' (PolicyMapper.ts:34)"
✅ "Expiry badge hidden — GAP-003, no expiry field in contract"
```

### ⚠️ Locations Must Survive Edits

Line numbers drift with every edit. **Always give the symbol with the line**, so the location stays findable after the file changes:

```text
✅ PolicyMapper.ts → mapPolicyResponse()  :34
❌ PolicyMapper.ts:34
```

### ⚠️ Paths Use Exact On-Disk Casing

Write every path exactly as it exists on disk. The SME portal's feature root is lowercase `features/`; the design system's source root is `Src/`.

```text
✅ Portals/Sme/features/Motor/PolicyList/Hooks/usePolicyList.ts
✅ Packages/DesignSystem/Foundation/Src/Organisms/HeroCarousel/HeroCarousel.tsx
❌ Portals/Sme/Features/Motor/PolicyList/Hooks/usePolicyList.ts
```

A path with the wrong casing cannot be found on Linux/CI — the defect workflow would fail to locate the file.

---

## ⚠️ HOW TO WRITE IT

**This skill defines WHAT the summary must contain. You decide HOW to write it using your file-writing tool.**

Write the summary **completely, in a single write operation**.

### If a single write fails or is rejected for size

1. Write the leading sections first, creating the file.
2. To add the remaining sections: **read the file's current content, concatenate the new sections, and write the complete combined content back.** Repeat until all 13 sections are present.
3. Keep sections whole — never split mid-section or mid-table.
4. Write sections in ascending order, 1 → 13.

⚠️ **Do not assume an append mode exists.** Read → concatenate → write back.

### Non-negotiable outcomes

| Outcome | Requirement |
| --- | --- |
| **Single file** | Exactly one document |
| **Completeness** | All 13 sections present, story-specific |
| **Order** | Ascending, 1 → 13 |
| **Integrity** | No duplicated, truncated or orphaned sections; no partial tables |
| **No loss** | Rewriting preserves prior content verbatim |
| **§13 seeded** | Change Log present, even on the first run |

### Efficiency rules

- **Reuse computed content.** If a write fails, reuse what you generated — never re-run the build.
- **Do not re-read a file you just wrote** to confirm success.
- **Never restart the build** because of a write failure.
- **Do not use shell commands** (`cat`, `cp`, `sed`, temp-file merges) to assemble the document.
- **If content must be reduced**, condense §9 and §10 rows first. **Never condense §3, §7, §8, §12 or §13.** Note any reduction as `[Condensed: Section X]`.

---

## Consolidated Summary Template (13 Sections)

```markdown
# Code Generation Summary — {{ticket_id}}

**Story:** {{story title}}
**Classification:** Presentational | Transactional | Hybrid
**Generated:** {{YYYY-MM-DD}}

> Sections 1–12 describe the CURRENT state of the code.
> Section 13 records every change made after original generation.

---

## 1. Developer Notes Applied

| DN ID  | Instruction | Files Affected | How Applied | Status                                 |
| ------ | ----------- | -------------- | ----------- | -------------------------------------- |
| DN-001 |             |                |             | Implemented / Not Applicable / Blocked |

> Every DN resolves to Implemented (with file evidence), Not Applicable (with reason),
> or Blocked (by a named unavailable dependency). "Considered" is not evidence.
> If none: "No Developer Notes. Normal priority order applied."

---

## 2. Story & Classification Summary

- **Classification:** Presentational | Transactional | Hybrid
- **Rationale:** [one line — why this classification]
- **Execution path:** lean (0–5, 8–11) | full (all phases)
- **Component(s) built:** [names]
- **Entry point:** [Sitecore rendering name, or route]

### Scope Explicitly NOT Implemented

> From plan §8 Things NOT to Implement. **Defect workflow: check here first.**

| Item | Reason |
| ---- | ------ |
|      |        |

---

## 3. File Inventory

> ⚠️ **Complete, flat, greppable list of every file touched.** Defect work starts here.
> Every file created or modified in this run appears exactly once, with exact on-disk casing.

| #   | File Path | Type | Action | Purpose |
| --- | --------- | ---- | ------ | ------- |
| 1   | Packages/DesignSystem/Foundation/Src/Organisms/HeroCarousel/HeroCarousel.tsx | Component | Created | Carousel organism — slides, autoplay |
| 2   | Portals/Sme/features/Motor/PolicyList/Hooks/usePolicyList.ts | Hook | Created | TanStack infinite query for policy list |
| 3   | src/component-catalogue.json | Catalogue | Modified | Added HeroCarousel entry |

**Type values:** Component · Container · Hook · Service · Mapper · Types · Constants · Store · Validator · CMS Entry · Story · Test · Barrel · Catalogue · Config

**Action values:** Created · Modified

**Totals:** N created · N modified · N total

> Later defect fixes add rows and tag changed rows with `[DEF-xxx]`.

---

## 4. UI Components Generated

| Component | Owner | Reuse Decision | Exported Symbol | File Path |
| --------- | ----- | -------------- | --------------- | --------- |
|           | DS / CMS / Feature / Shared | reuse / enhance / new | `HeroCarousel` | |

> `Exported Symbol` lets a defect triager grep the codebase for consumers.

### Component Composition

> Only where a component composes others — the render tree for tracing a visual defect.

```text
HeroBanner (CMS entry)
└── HeroCarousel [design-system]
    ├── CarouselSlide [design-system]
    └── CarouselPager [design-system]
```

---

## 5. Sitecore Integration

> If not applicable: "Not Applicable — no CMS-mapped components."

- **Rendering name / registry key:** [exact, case-sensitive]
- **Entry component:** [file path]
- **Placeholder(s):** [keys, or: None]
- **Registry commands run:** `pnpm run build:cms-component-registry` · `pnpm run build:component-registry`

### Sitecore Field → Prop Mapping

| Sitecore Field | Type | Helper Used | Maps To Prop | Fallback if Missing |
| -------------- | ---- | ----------- | ------------ | ------------------- |
| `Title` | Single-Line Text | — | `title` | empty string |
| `CtaLink` | General Link | `extractCTA` | `ctaHref`, `ctaLabel` | CTA hidden |

> **Defect workflow:** if authored content is not appearing, check this table first —
> field name mismatch and missing helper are the two most common causes.

---

## 6. Logic & API Integration

> If not applicable: "Not Applicable — Presentational component."

| Layer | File | Responsibility |
| ----- | ---- | -------------- |
| Types | `PolicyTypes.ts` | API contract + ViewModel |
| Constants | `POLICY_CONSTANTS.ts` | Query keys + endpoints |
| Mapper | `PolicyMapper.ts` | Response → ViewModel |
| Service | `PolicyListService.ts` | fetch to BFF |
| Hook | `usePolicyList.ts` | useInfiniteQuery |
| Container | `PolicyListContainer.tsx` | State orchestration |

### Endpoint Configuration

| Endpoint | Method | Query Key | Hook | staleTime | gcTime | retry |
| -------- | ------ | --------- | ---- | --------- | ------ | ----- |
| `/api/policies` | GET | `POLICY_QUERY_KEYS.list(params)` | `usePolicyList` | 0 | 5min | 1 |

### Error Code → UI Mapping

| Error Code | UI State | Message Source | Component |
| ---------- | -------- | -------------- | --------- |
| 404 | Empty state | Sitecore `NoPoliciesFound` | PolicyListContainer |
| 5xx (all) | Error banner | Sitecore `GenericError` | PolicyListContainer |

---

## 7. Data Flow Trace

> ⚠️ **Transactional / Hybrid only.** Presentational: "Not Applicable — all data is CMS-authored, see §5."
>
> **One trace per rendered data field** — the defect workflow's primary lookup for
> *"where does this value come from and where could it break?"*

```text
FIELD: policyNumber
  BFF getPolicyList → response.items[].policyNumber (string, nullable)
    → PolicyListService.fetchPolicies()    features/Motor/PolicyList/Services/PolicyListService.ts
    → usePolicyList()                      features/Motor/PolicyList/Hooks/usePolicyList.ts
        queryKey: POLICY_QUERY_KEYS.list(params)
    → PolicyMapper.mapPolicyResponse()     features/Motor/PolicyList/Mappers/PolicyMapper.ts :34
        null / undefined → "—"
    → PolicyListContainer                  features/Motor/PolicyList/Components/PolicyListContainer.tsx
    → PolicyCard (prop: policyNumber)      features/Motor/PolicyList/Components/PolicyCard.tsx

FIELD: expiryDate
  ⚠️ NOT AVAILABLE — see GAP-003 (§12). Badge hidden.
```

**Trace every rendered field.** Include the transformation point (symbol + line) and the null/missing default — that is where display defects originate.

> Later defect fixes update these entries, tagged `[DEF-xxx]`.

---

## 8. State → UI Behaviour Matrix

> ⚠️ **Every state from plan §10.** When a defect reports *"wrong thing shows when X"*,
> this names the owning file immediately.

| State | Trigger Condition | What Renders | Owning File |
| ----- | ----------------- | ------------ | ----------- |
| default | data loaded, length > 0 | `PolicyCard` list | `PolicyListContainer.tsx` |
| loading | `isLoading === true` | `PolicyCardSkeleton` ×3 | `PolicyListContainer.tsx` |
| error | `isError === true` | `ErrorBanner` + retry CTA | `PolicyListContainer.tsx` |
| empty | `data.length === 0` | `EmptyState` | `PolicyListContainer.tsx` |
| partial | some fields null | card renders, section hidden | `PolicyCard.tsx` |
| hover | pointer over card | elevation token applied | `PolicyCard.tsx` |
| disabled | `isDisabled` prop | reduced opacity, `aria-disabled` | `PolicyCard.tsx` |

> Presentational components list UI interaction states only (default, active/selected,
> hover/focus, transitioning/paused, disabled, hidden).

---

## 9. Design & NFR Notes

> ⚠️ **Non-obvious decisions ONLY.** Do NOT restate compliance.

### New Design Tokens Created

| Token | Value | Why No Existing Token Matched | Where Used |
| ----- | ----- | ----------------------------- | ---------- |
|       |       |                               |            |

> ⚠️ **Mandatory if any primitive or semantic token was added.** Run `pnpm build:css`.
> If none: "No new tokens created."

### Token / Design Discrepancies

| Component | Figma Value | Token Used | Delta | Reason |
| --------- | ----------- | ---------- | ----- | ------ |
| ClaimCard | 18px gap | `gap-m` (16px) | −2px | No 18px token exists |

### NFR Exceptions Applied

> From plan §13.2 — story-specific exceptions only.

| Category | Exception | Implementation |
| -------- | --------- | -------------- |
| RTL | Carousel pager arrows mirrored | `rtl:rotate-180` on `CarouselPager` |

### Media Handling

> If none: "Not Applicable — no media in this story."

| Asset | Source | Optimisation | Loading |
| ----- | ------ | ------------ | ------- |
| Hero image | Sitecore Media Library → CDN | `next/image`, responsive `sizes` | eager (LCP) |

### Storybook & Catalogue

| Component | Story File | JSDoc | Catalogue |
| --------- | ---------- | ----- | --------- |
| HeroCarousel | `HeroCarousel.stories.tsx` | ✅ 14 tags | Added |

> Catalogue path: `./src/component-catalogue.json`

---

## 10. Tests & Coverage

| Source File | Classification | Test File | Cases | Branch Coverage |
| ----------- | -------------- | --------- | ----- | --------------- |
| `PolicyCard.tsx` | Presentational | `PolicyCard.test.tsx` | 12 | 94% (targeted) |
| `PolicyListContainer.tsx` | Transactional | `PolicyListContainer.test.tsx` | 9 | 91% (targeted) |

- **Overall coverage:** NN% — **targeted** | **measured**
- ⚠️ "measured" **only** if a coverage run was actually executed (`run-test-cases --coverage`). Otherwise "targeted".
- **Excluded from testing:** barrels, type-only files, stories, configs, primitive constants
- **Test file locations** use exact on-disk paths — SME portal tests sit under `Portals/Sme/features/`, the portal's Vitest scan directory

### AC → Test Mapping

> **Defect workflow:** names the test that should have caught a defect mapped to an AC.

| AC ID | Covering Test(s) |
| ----- | ---------------- |
| AC-001 | `PolicyCard.test.tsx` → "renders policy number from props" |
| AC-003 | `PolicyListContainer.test.tsx` → "shows empty state when no policies" |

### Untested Behaviours

> Anything deliberately not covered, with the reason. If none: "None."

| Behaviour | Reason |
| --------- | ------ |
|           |        |

---

## 11. Acceptance Criteria Evidence

> ⚠️ **Every AC needs ✅ with a specific file path AND code reference.**
> **Vague or assumed coverage is NOT acceptable.** Any ❌ must also appear in §12.

| AC ID | Status | Implemented In (file + symbol/line) | Verified By (test) |
| ----- | ------ | ----------------------------------- | ------------------ |
| AC-001 | ✅ | `PolicyCard.tsx` → `policyNumber` prop render | `PolicyCard.test.tsx:24` |
| AC-002 | ✅ | `PolicyListContainer.tsx` → error branch :41 | `PolicyListContainer.test.tsx:56` |
| AC-003 | ❌ | Not implemented — see LIM-001 | — |

**Coverage:** N of M acceptance criteria fully implemented.

---

## 12. Deviations, Gaps & Limitations

> ⚠️ **The most valuable section for both consumers** — the ONLY place recording *why*.
> Never condense or omit.

### 12.1 Decisions & Conflict Resolutions

| ID | Area | Conflict | Decision | Priority Rule Applied |
| -- | ---- | -------- | -------- | --------------------- |
| DEC-001 | Layout | Figma 3-col vs plan 2-col | Implemented Figma | Figma = visual source of truth |
| DEC-002 | Placement | Plan path `Features/` vs disk `features/` | Used `features/` | On-disk casing wins |

> Record every **casing deviation** — a path written to match the on-disk casing rather than the plan.

### 12.2 Assumptions Made

| ID | Assumption | Because | Impact if Wrong |
| -- | ---------- | ------- | --------------- |
| ASS-001 | Empty list shows CMS message | Plan did not specify copy source | Wrong copy displayed |

### 12.3 Upstream Contract Gaps Encountered

> Gaps from the Analysis Plan (`Unknown — source contract not provided`). These props
> remain **prop-driven** — never hardcoded.

| Gap ID | What Was Missing | How Implementation Handled It |
| ------ | ---------------- | ----------------------------- |
| GAP-003 | No `expiryDate` in BFF response | Prop modelled as Unknown; badge hidden |

### 12.4 Known Limitations

> ⚠️ **Defect workflow: check this table BEFORE raising a defect.**
> A known limitation is a tracked gap awaiting an upstream fix, not a defect.

| ID | Limitation | Root Cause | User-Visible Impact | Resolution Owner | Status |
| -- | ---------- | ---------- | ------------------- | ---------------- | ------ |
| LIM-001 | Expiry badge never renders | GAP-003 — field absent from contract | Users cannot see expiry | Backend team | Open |

> A later defect fix that closes a limitation marks it `✅ Resolved [DEF-xxx]` — the row is never deleted.

### 12.5 Validation Exceptions

> ONLY items marked Not Applicable, or checks that initially failed and were fixed.
> Do NOT list passing checks.

| Check | Status | Reason / Fix Applied |
| ----- | ------ | -------------------- |
| API-001 | Not Applicable | Presentational component — no API integration |
| FILE-002 | Failed → Fixed | Barrel export missing; added named re-export |

> If everything passed: "All validation checks passed. No exceptions."

---

## 13. Change Log

> Append-only record of every defect fix and enhancement that modified this component
> after original generation.
>
> ⚠️ **Sections 1–12 always describe the CURRENT state of the code.** This log records
> how it got there. When a defect fix updates a state section, it tags the changed row
> with the defect ID and appends an entry here.

_No changes since original generation._
```

---

## Content Rules

### Always

- Populate every section with **story-specific** detail — real paths, symbols and line references. No boilerplate.
- **Use exact on-disk casing** for every path — `Portals/Sme/features/`, `Foundation/Src/`.
- **Give symbol + line**, never a bare line number.
- **§3 File Inventory complete** — every created/modified file exactly once, from the actual write operations.
- **§7 Data Flow Trace: one trace per rendered field**, with the transformation point and the null/missing default.
- **§8 State Matrix: every state from plan §10**, with the owning file.
- **§11: every AC has a specific file path and code reference.**
- **§12.1: record every casing deviation** from the plan.
- **§12.4: include the `Status` column** (Open / Resolved).
- **§13: seed with the placeholder line.**
- Record every new design token in **both** §9 and §12.
- Confirm gapped props remained prop-driven with no hardcoded substitute.
- Preserve DN, AC, GAP and STATE IDs exactly as numbered upstream.
- Pull content from the in-memory manifest and skill outputs — do **not** re-open source files.

### Never

- Never restate compliance that the skills enforce and validation verifies.
- Never list passing validation checks.
- Never paste full source code.
- Never leave a section empty — use "Not Applicable" or "None".
- Never claim measured coverage without an executed coverage run.
- Never write a path with casing that differs from the disk.
- Never omit §13.

### Presentational Runs

| Section | Treatment |
| --- | --- |
| §5 Sitecore | Populate if CMS-mapped, else "Not Applicable" |
| §6 Logic & API | "Not Applicable — Presentational component" |
| §7 Data Flow Trace | "Not Applicable — all data is CMS-authored, see §5" |
| §8 State Matrix | **Still required** — UI interaction states only |
| §13 Change Log | **Still required** — seeded with the placeholder |

⚠️ §8 and §13 are **never** omitted. A Presentational component has real states and can receive defect fixes.

---

### Gate: Complete When

```text
- [ ] Exactly one summary at .SS_WF/Agent/CODE/{{ticket_id}}_CODE_GENERATION_SUMMARY.md
- [ ] All 13 sections present, ascending, no duplication or truncation
- [ ] Header note: "Sections 1–12 describe the CURRENT state… §13 records changes"
- [ ] Every path uses exact on-disk casing; every location gives symbol + line
- [ ] §3 complete — every written file exactly once, with totals
- [ ] §7 trace for every rendered field (Transactional/Hybrid)
- [ ] §8 covers every plan §10 state, with owning file — never empty
- [ ] §11 every AC has a file path + code reference; ❌ items appear in §12
- [ ] §12 populated across all five subsections (or "None"); casing deviations in §12.1
- [ ] §12.4 has a Status column, defaulting to Open
- [ ] §13 seeded with "No changes since original generation."
- [ ] Every DN resolved with evidence
- [ ] New tokens in §9 and §12
- [ ] Validation exceptions only
- [ ] Coverage labelled "targeted" or "measured" (measured only after an executed run)
- [ ] Presentational: §6 and §7 Not Applicable; §8 and §13 populated
```

### Never Do

- Never produce more than one document.
- Never emit `CODE_GENERATION.md`, `TEST_GENERATION.md`, or a separate Storybook doc.
- **Never omit or rename §13** — the defect workflow appends to it by name.
- **Never assume an append mode exists** — read, concatenate, write back.
- **Never lose previously written content** when rewriting.
- **Never split a section or table across two writes.**
- **Never write sections out of ascending order.**
- **Never condense §3, §7, §8, §12, or §13.**
- **Never restart the build** to regenerate the summary.
- **Never use shell commands** to assemble or repair the document.
- Never re-read a file you just wrote merely to confirm the write.
- Never paste full source code.
- Never leave a section empty.
- Never claim measured coverage without an executed run.
- Never renumber DN, AC, INT, STATE or GAP IDs.
