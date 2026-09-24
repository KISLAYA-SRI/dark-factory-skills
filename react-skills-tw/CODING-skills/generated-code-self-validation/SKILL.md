---
name: generated-code-self-validation
description: Use as the final gate before producing the summary — runs deterministic structural checks on generated code AND walks the existing CODING_AGENT_CHECKLIST.md item by item with file evidence. Triggers include self-validation, code validation gate, pre-completion check, or validate the generated code.
disable-model-invocation: true
---

## Generated Code Self-Validation

### Purpose

Verify the generated code is structurally correct, scope-compliant, and satisfies the validation contract **BEFORE** the consolidated summary is produced. Two parts run in sequence: **(A)** deterministic structural gate, **(B)** `CODING_AGENT_CHECKLIST.md` walk.

⚠️ No summary may be produced until all checks pass. On failure, fix the **specific** code and re-run this gate — **never restart the whole build**.

---

## Part A — Structural Gate (Deterministic)

### Files on Disk

```text
- [ ] Every file in the manifest's filesToCreate/filesToUpdate EXISTS ON DISK.
- [ ] No file was only described in documentation without being written.
- [ ] No forbidden roots created (new src/Src, duplicate .storybook, new .SS_WF).
- [ ] Existing filesystem casing reused; no case-insensitive duplicate paths.
- [ ] Nearest barrels updated with explicit named re-exports (default export for CMS entries).
- [ ] No `export *` used in any barrel.
```

### Folder & Naming

```text
- [ ] All folders PascalCase at every level — no kebab-case anywhere.
- [ ] No folder created directly under Features/ without a domain subfolder.
- [ ] Standard feature subfolders used (Components/Hooks/Services/Types/Constants).
- [ ] File naming matches convention per type (PascalCase component, camelCase use* hook,
      *Service, *Types, *Mapper, *_CONSTANTS).
- [ ] Test files use .test.* — never .spec.*
- [ ] No interface prefixed with I; no empty interfaces.
- [ ] Interface suffix correct (Props / none / Params / Response / State / Context / Config).
```

### Ownership & Boundaries

```text
- [ ] No feature-to-feature imports.
- [ ] Design System imports no feature/CMS/API code.
- [ ] CMS components may import Design System — not the reverse.
- [ ] Components placed under the correct owner (DS / CMS / Feature / Shared).
- [ ] No business logic or API calls inside Packages/DesignSystem.
- [ ] No feature-specific code inside Features/Shared.
```

### Prop-Driven & Data Discipline

```text
- [ ] No hardcoded labels, copy, CTA text, messages, routes, URLs, or icon names.
- [ ] No hardcoded colour, spacing, typography, radius, or shadow where tokens exist.
- [ ] No raw API DTO reaches a display component (mapper present).
- [ ] No API call / data fetching inside design-system or feature display components.
- [ ] Services are framework-agnostic — zero Next.js imports, zero React hooks.
- [ ] Endpoints and query keys sourced from Constants/, never inline.
- [ ] Query keys use `as const`.
- [ ] No new QueryClientProvider created.
- [ ] useInfiniteQuery used for lists/tables — no numbered pagination.
- [ ] Props linked to a gap remain prop-driven — no hardcoded substitute.
```

### Styling, RTL & Accessibility

```text
- [ ] cn() used for all conditional/merged classes — no string concatenation.
- [ ] No style={{ ... }} inline styles, CSS modules, or styled-components.
- [ ] Semantic tokens used — no primitive tokens, no raw hex/px values.
- [ ] Text component used for all text; semantic heading hierarchy preserved.
- [ ] Logical properties only (ms-, me-, ps-, pe-, text-start, text-end).
- [ ] No physical directional classes in layout-critical styles.
- [ ] Directional icons mirrored; neutral (eye/help/search/calendar), symmetric
      (✕ ✓ ⚠) and brand logos NOT mirrored.
- [ ] Semantic HTML used; interactive elements are <button>/<a>, never div/span.
- [ ] Every interactive element has aria-label or a visible label.
- [ ] data-testid on interactive and key structural elements.
- [ ] Scrollable containers have role="region" + aria-label.
- [ ] No overflow: hidden on dynamic/variable-length content.
```

### Classification Compliance

```text
- [ ] Presentational: NO container/hook/service/mapper/store generated.
- [ ] Transactional: types + constants + mapper + service + hook + container present.
- [ ] Transactional: all applicable states handled (loading/error/empty/partial/success).
- [ ] Hybrid: CMS shell and container both present, clearly separated.
```

### Sitecore (If Applicable)

```text
- [ ] CMS field contracts typed; Sitecore helpers used for extraction.
- [ ] Rendering entry default-exported and registered.
- [ ] CMS folder name PascalCase, matching the Sitecore rendering name exactly.
- [ ] Registry build commands recorded for the summary.
- [ ] Placeholder keys match the rendering definition — none invented.
- [ ] CMS labels separate from API values; preview-safe on null fields.
- [ ] No CMS copy used as a fallback prop value.
```

### Storybook & Catalogue (If Applicable)

```text
- [ ] Stories exist for every eligible reusable component (and only those).
- [ ] JSDoc block with all 14 tags present on every reusable component.
- [ ] ./src/component-catalogue.json valid JSON; unrelated entries intact.
- [ ] Catalogue NOT placed at repository root or duplicated elsewhere.
- [ ] No new .storybook/ folder created.
```

### Tests

```text
- [ ] Every runtime file has a co-located test (or is on the exclusion list).
- [ ] Hybrid components tested at BOTH levels in separate files.
- [ ] Test files sit inside their package's vitest include pattern.
- [ ] Explicit Vitest imports — no globals.
- [ ] Branch map shows 90–100% intended coverage; no snapshots.
```

### Scope

```text
- [ ] Nothing on the plan's "things NOT to implement" list was implemented.
- [ ] No update/edit flows generated when only read was in scope.
- [ ] No invented API or Sitecore fields.
- [ ] No unrelated files modified.
```

---

## Part B — Coding Agent Checklist Walk

Use the `CODING_AGENT_CHECKLIST.md` loaded at contract-load time (**do NOT rebuild it**). For every item, mark status + evidence:

```text
For each checklist item (DN / AC / INT / STATE / SCOPE / PROP / CMS / API / COMP / DS /
                         RESP / A11Y / RTL / NFR / FILE / TEST):
  → Covered          (with file path / test evidence)
  → Not Applicable   (with reason — e.g. Presentational)

No item may be left unresolved.
```

### Developer Notes Evidence Requirement

Every `DN-xxx` must resolve to one of:

- **Implemented** — with concrete evidence: generated/updated file, symbol, or configuration
- **Not Applicable** — with a stated reason
- **Blocked** — by a genuinely unavailable dependency, explicitly named

⚠️ "Considered" or "reviewed" is **not** evidence. No generated file may contradict a Dev Note.

### Lint / Typecheck / Test Execution

If execution is within scope, run and record results. If out of scope, mark as **"static validation only"** and defer execution proof to the runtime quality gate.

---

### Gate: Complete When

```text
- [ ] All Part A structural checks pass (or failures fixed and re-run).
- [ ] Every CODING_AGENT_CHECKLIST.md item marked Covered / Not Applicable with evidence.
- [ ] Every DN-xxx confirmed applied with file-level evidence; no contradictions.
- [ ] Deviations recorded for the summary's Deviations section.
```

### Never Do

- Never produce the summary while any check is failing.
- Never rebuild the checklist — reuse the one from the analysis output.
- Never restart the whole build on a single failure — fix and re-run the gate.
- Never mark an item Covered without concrete file/test evidence.
- Never accept "considered" as Dev Note evidence.
- Never pass a file that was documented but not written to disk.
