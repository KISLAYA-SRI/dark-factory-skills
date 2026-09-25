---
name: frontend-test-generation
description: Use to generate co-located Vitest + React Testing Library tests based on the actual generated source files, targeting 90–100% branch/function coverage. Applies classification-aware strategies (Presentational, Transactional, Hybrid two-level) additively with file-type strategies. Embeds package-level vitest configs and project testing standards. Triggers include test generation, unit tests, Vitest, React Testing Library, coverage, or write tests for these files.
disable-model-invocation: true
---

## Frontend Test Generation

### Purpose

Generate co-located behavioural tests from the **ACTUAL generated source** (not the plan). Source files are the ground truth: inspect real branches, callbacks, states, and exports, then test observable behaviour.

⚠️ **This skill embeds the project's testing standards and package-level configs.** No external lookup required.

---

## ⚠️ WRITE TEST FILES, NOT DESCRIPTIONS

Every `.test.ts` / `.test.tsx` file must be **written to disk** at the co-located path. Files described in the summary but not written **do not count**.

---

## 1. Read the Source Before Writing Any Test

```text
ABSOLUTE — NO EXCEPTIONS:
- Read EVERY source file before writing its test — never from memory or assumptions
- Extract the complete prop interface, all exported functions, all visual states, all callbacks
- Identify every branch (if/else, ternary, optional chaining, nullish coalescing)
- Map every branch to at least one test case
- If the source file does not exist on disk, record it as a gap and skip it
```

Build a **coverage map** per file before writing any test:
- Every exported function/component
- Every prop and its type
- Every visual state (`isLoading`, `isEmpty`, `hasError`, `isDisabled`, …)
- Every callback prop
- Every conditional branch (`if/else`, ternary, `&&`, `??`, optional chaining)
- Every error path
- Every edge case (empty array, null, undefined, boundary values)

---

## 2. Project Test Environment

| Setting | Value |
| --- | --- |
| Framework | **Vitest + React Testing Library** |
| Environment | jsdom (configured per-package) |
| **Globals** | **`false`** — all Vitest APIs must be **explicitly imported** |
| DOM matchers | `@testing-library/jest-dom/vitest` — extended via `setup.ts` |
| Cleanup | Automatic via `afterEach(() => cleanup())` in `setup.ts` — **do NOT add manual cleanup** |
| Coverage target | **≥ 90%** branch and function coverage per file |
| Co-location | Test file lives in the **SAME folder** as its source |
| Naming | `<ComponentName>.test.tsx` · `<hookName>.test.ts` |

### ⚠️ Package-Level Vitest Configs

| Package / Portal | Config Location | Test Include Pattern | Setup File |
| --- | --- | --- | --- |
| `@dxp/foundation` | `Packages/DesignSystem/Foundation/vitest.config.ts` | `Src/{Atoms,Molecules,Organisms,Templates}/**/*.{test,spec}.{ts,tsx}` | `Packages/DesignSystem/Foundation/Src/setup.ts` |
| `@dxp/theme` | `Packages/DesignSystem/Themes/vitest.config.ts` | `Src/**/*.{test,spec}.{ts,tsx}` | `Packages/DesignSystem/Themes/Src/setup.ts` |
| `@dxp/cms-components` | `Packages/Cms/CmsComponents/vitest.config.ts` | `**/*.{test,spec}.{ts,tsx}` | `Packages/Cms/CmsComponents/Src/setup.ts` |
| `portals/sme` | `Portals/Sme/vitest.config.ts` | `features/**/*.{test,spec}.{ts,tsx}` | `Portals/Sme/features/setup.ts` |

⚠️ Test files must be placed **inside the include pattern** of their package's config, or they will never run.

### Pre-Configured Global Mocks

- **`next/router`** — mocked globally in `@dxp/foundation` setup; `useRouter` returns a stable mock object
- **`next/navigation`** — mock if needed for SME portal tests using App Router utilities
- **`@dxp/theme`** — mock `cn()` if needed; prefer the real implementation for class composition tests

⚠️ No test file may import from paths outside its package boundary — use mocks for cross-package dependencies.

---

## 3. Co-Location Policy

Every new or modified file containing runtime behaviour must have a co-located test.

**Runtime files that REQUIRE a test:**
Components (presentational + containers) · hooks · services · mappers · validation utilities · stores · Sitecore rendering entries

**Excluded by classification policy (no test):**

```text
❌ index.ts / barrel export files (no logic)
❌ *.stories.tsx / *.stories.ts
❌ *.types.ts / *.d.ts (type-only, no runtime logic)
❌ setup.ts
❌ vitest.config.ts
❌ *.config.ts / *.config.mjs
❌ constants files with only exported primitives and no logic
```

⚠️ If a file contains **ANY** runtime logic (functions, conditionals, transformations), it MUST have a test — even if it is primarily a types file.

```text
Source: Packages/DesignSystem/Foundation/Src/Atoms/Button.tsx
Test:   Packages/DesignSystem/Foundation/Src/Atoms/Button.test.tsx

Source: Portals/Sme/Features/Motor/Claims/Hooks/useClaimData.ts
Test:   Portals/Sme/Features/Motor/Claims/Hooks/useClaimData.test.ts
```

❌ Never place test files in a separate `__tests__` folder (unless the source is already there).

---

## 4. Coverage Target

Design tests to cover **90%–100%** of generated runtime code (branches + functions). Build a coverage map per file and add cases until every branch, callback, and state path is exercised.

⚠️ If test **execution** is outside the current scope, state **intended** coverage (with the branch map) — **do not claim measured coverage without a run.**

---

## 5. Test Structure — AAA Pattern

Every test follows **Arrange → Act → Assert** with JSDoc documentation:

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { Button } from "./Button";

describe("Button", () => {
  describe("User Interactions", () => {
    /**
     * Verifies that onClick callback is called when button is clicked
     * Scenario: Button with click handler receives a user click
     * Expected: onClick is called exactly once
     */
    it("calls onClick when clicked", async () => {
      // Arrange
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Click me</Button>);

      // Act
      await userEvent.click(screen.getByRole("button"));

      // Assert
      expect(handleClick).toHaveBeenCalledOnce();
    });
  });
});
```

---

## 6. ⚠️ CLASSIFICATION-AWARE STRATEGIES

Every source file has a classification. **Section 7 (file type) and this section (classification) are ADDITIVE — not alternatives.** Both sets of scenarios are mandatory.

### Quick Classification Test

```text
Does the file contain useQuery / useMutation / fetch / session / persona logic?
  YES → Transactional
  NO  → Does it compose both a static CMS shell AND a Container?
          YES → Hybrid
          NO  → Presentational
```

### 6.1 Presentational — Required Scenarios

```text
✅ REQUIRED:
1. RENDERING — renders with required props only; with all optional props;
   correct text/labels from props; children/slot content; correct ARIA roles + semantic HTML
2. VISUAL VARIANTS — each variant value renders; each size value renders;
   each visual state prop (isActive, isSelected) renders correct treatment
   (assert observable behaviour or role — do NOT assert specific CSS class names)
3. SITECORE FIELD RENDERING — CMS labels render from props; links render with correct
   href/target; images render with correct src/alt; missing/empty fields produce safe
   fallback (no crash); null/undefined optional props render without errors
4. REPEATABLE CONTENT — list renders correct item count; empty array renders empty
   state or nothing; single-item array renders correctly
5. EDGE CASES — very long strings do not throw; empty strings render;
   null/undefined optional props render
6. ACCESSIBILITY — aria-label applied to correct element; data-testid present;
   semantic HTML used

❌ NOT REQUIRED:
   Loading state tests · error state tests from API failures · hook mocking ·
   mutation/form submission tests (unless the component has an interactive form)
```

### 6.2 Transactional — Required Scenarios

```text
✅ REQUIRED:
1. LOADING — skeleton/spinner shown while isLoading=true; content NOT rendered;
   isLoading transitions to false after data resolves
2. ERROR — error UI shown when isError=true; error message passed correctly;
   component does not crash — graceful degradation
3. EMPTY — empty state UI shown when data is empty array or null/undefined;
   presentational component NOT rendered
4. HAPPY PATH — presentational component receives correctly mapped props;
   all required props passed; data transformed and displayed correctly
5. INTERACTIONS & MUTATIONS — callback props trigger correct hook mutations;
   mutation called with correct arguments; navigation triggered with correct path;
   optimistic updates / cache invalidation where applicable
6. SITECORE PROPS — CMS labels passed to presentational component;
   missing Sitecore fields produce safe fallback
7. HOOK-SPECIFIC (renderHook + waitFor) — correct initial state (isLoading=true,
   data=undefined); correct data after success; isError=true on failure;
   correct endpoint called with correct params; raw API → ViewModel mapping;
   null/undefined API fields → safe defaults; cache invalidation after mutation
8. MAPPER-SPECIFIC — correct output for complete valid input; null fields → safe
   defaults; undefined fields → safe defaults; empty object does not throw;
   boundary values handled; zero-item arrays → empty array (not null/undefined)
9. EDGE CASES — network timeout / rejected promise handled; concurrent calls
   deduplicated; retry behaviour if applicable

❌ NOT REQUIRED:
   Visual variant tests · Sitecore field rendering tests · snapshot tests
```

### 6.3 ⚠️ Hybrid — TWO-LEVEL Testing

A hybrid component is tested at **two separate levels, in two separate test files**.

```text
LEVEL 1 — Outer Sitecore shell (presentational layer):
   - Renders without errors with required Sitecore props
   - CMS labels/links/media render from props
   - Missing Sitecore fields produce safe fallback
   - The inner Container IS RENDERED (verify present in the DOM)

LEVEL 2 — Inner Container (transactional layer, its OWN test file):
   - Apply ALL Transactional scenarios (6.2) to the Container
   - Mock the hook used by the Container
   - Test loading, error, empty, happy path
   - Test user interactions and mutations
```

⚠️ **Critical separation rules:**
- Do **NOT** test the Container's data logic inside the outer shell's test file
- The outer shell test only verifies the Container is mounted and receives correct Sitecore props
- The Container's own test file covers all data/state/interaction scenarios
- At the shell level, **do NOT** test loading, error, or mutation — those are owned by the Container

### 6.4 Classification → Scenario Matrix

| Scenario | Presentational | Transactional | Hybrid (Shell) | Hybrid (Container) |
| --- | --- | --- | --- | --- |
| Renders with required props | ✅ | ✅ | ✅ | ✅ |
| Renders with all optional props | ✅ | ✅ | ✅ | ✅ |
| Visual variants per prop value | ✅ | ❌ | ✅ | ❌ |
| Sitecore field rendering | ✅ | ⚠️ labels only | ✅ | ⚠️ labels only |
| Missing Sitecore fields (fallback) | ✅ | ✅ | ✅ | ✅ |
| Repeatable content list | ✅ | ❌ | ✅ | ❌ |
| Loading state | ❌ | ✅ | ❌ | ✅ |
| Error state | ❌ | ✅ | ❌ | ✅ |
| Empty state | ❌ | ✅ | ❌ | ✅ |
| Happy path data rendering | ❌ | ✅ | ❌ | ✅ |
| User interactions / callbacks | ✅ UI events | ✅ mutations | ✅ UI events | ✅ mutations |
| Disabled / non-interactivity | ✅ | ✅ | ✅ | ✅ |
| Hook mocking (`vi.mock`) | ❌ | ✅ | ❌ | ✅ |
| API endpoint called with args | ❌ | ✅ | ❌ | ✅ |
| Data mapping / transformation | ❌ | ✅ | ❌ | ✅ |
| Null/undefined API → defaults | ❌ | ✅ | ❌ | ✅ |
| Accessibility (aria, testid) | ✅ | ✅ | ✅ | ✅ |
| Edge cases (null, empty string) | ✅ | ✅ | ✅ | ✅ |

---

## 7. File-Type Strategies (Applied ADDITIVELY with Section 6)

```text
UI component   → render; assert prop-driven output; fire interactions via userEvent;
                 assert callback invocations; assert each visual state;
                 assert a11y roles/labels; RTL render assertion
Container      → mock the hook; assert state → props mapping; assert callbacks/navigation
Hook (TanStack)→ wrap in QueryClientProvider; mock service; assert loading/success/error;
                 assert mapper output shape (ViewModel)
Service        → mock the API client; assert endpoint/params from constants;
                 assert typed result on 2xx/4xx/5xx
Mapper/util    → pure input→output incl. null/empty/partial; boundary values
Validation util→ valid/invalid/edge inputs; error message correctness
Store (Zustand)→ initial state; each action; selector behaviour
Sitecore entry → mock fields (incl. unauthored/null); assert field→prop mapping;
                 preview-safe render
```

---

## 8. Test Quality Rules

- ✅ **Explicit Vitest imports**: `import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'`
- ✅ Import `render`, `screen`, `waitFor`, `within`, `renderHook`, `act` from `@testing-library/react`
- ✅ Import `userEvent` from `@testing-library/user-event`
- ✅ **Use `userEvent` over `fireEvent`** — more realistic simulation
- ✅ Query preference order: `getByRole` > `getByLabelText` > `getByText` > `getByTestId`
- ✅ Use `vi.fn()` for all mock callbacks; `vi.mock()` for module-level mocks
- ✅ Use `renderHook()` for hooks; `waitFor()` for async state; `within()` to scope queries
- ✅ Follow AAA; descriptive names: "[does something] when [condition]"
- ✅ Group with nested `describe()` blocks; add JSDoc above each test
- ✅ Deterministic: fake timers for autoplay/carousel/debounce — no real waits
- ✅ Mock external boundaries (API client, navigation, services) — never hit the network
- ✅ One behaviour per `it`
- ❌ **Never** rely on global Vitest APIs — `globals: false` is enforced
- ❌ **Never** use snapshot tests — brittle, don't verify behaviour
- ❌ **Never** test implementation details (internal state, private methods, CSS class names)
- ❌ **Never** write tautological tests (always pass regardless of implementation)
- ❌ **Never** write tests that test the mock instead of the component
- ❌ **Never** leave TODO comments or empty test bodies
- ❌ **Never** import from barrel index files when a direct import is available (avoids circular deps)

### Mocking Patterns

```ts
// Module mock
vi.mock("next/router", () => ({
  useRouter: vi.fn(() => ({ push: vi.fn(), pathname: "/", query: {} })),
}));

// Hook mock inside a container test
vi.mock("../Hooks/useMyHook", () => ({ useMyHook: vi.fn() }));
import { useMyHook } from "../Hooks/useMyHook";

vi.mocked(useMyHook).mockReturnValue({
  data: { id: "1", name: "Test" },
  isLoading: false,
  isError: false,
});
```

---

## 9. Branch Coverage Checklist (Per File)

```text
- [ ] Every conditional/ternary branch has a test
- [ ] Both truthy AND falsy sides of every conditional covered
- [ ] Every callback prop asserted as called with expected args
- [ ] Every callback asserted as NOT called when disabled
- [ ] Every state rendered (default/loading/success/error/empty/partial/disabled)
- [ ] Every exported function/hook has at least one direct test
- [ ] Null/empty/partial data paths covered (mappers/containers)
- [ ] RTL and keyboard interaction covered for interactive UI
- [ ] Every prop variant tested
- [ ] Accessibility attributes verified (aria-label, data-testid)
```

---

### Learnings Namespace

Load only the `# TEST LEARNINGS` namespace.

### Output

```text
<Source>.test.tsx  (co-located) — Vitest + RTL, branch-mapped cases
```

---

### Gate: Complete When

```text
SOURCE READING
- [ ] Every source file READ FROM DISK before its test was written
- [ ] Complete prop interface extracted for every component
- [ ] Every conditional branch identified and mapped to a test case

CLASSIFICATION
- [ ] Every file classified Presentational / Transactional / Hybrid
- [ ] Classification-specific scenarios (Section 6) applied
- [ ] File-type scenarios (Section 7) applied ADDITIVELY
- [ ] Hybrid components tested at BOTH levels in SEPARATE files

COVERAGE
- [ ] Every runtime file has a co-located test (or is on the exclusion list)
- [ ] Branch/coverage map shows 90–100% intended coverage per file
- [ ] All visual states and callbacks asserted
- [ ] Edge cases (null, undefined, empty string, empty array) tested

QUALITY
- [ ] Explicit Vitest imports — no globals
- [ ] userEvent used for interactions; accessible queries used
- [ ] No snapshots, no tautological tests, no placeholder bodies
- [ ] External boundaries mocked; tests deterministic (fake timers where needed)
- [ ] Test files placed inside the package's vitest include pattern
- [ ] No imports from outside the package boundary
```

### Never Do

- **Never describe a test without writing the file to disk.**
- Never modify any existing source component, hook, mapper, or integration file.
- Never add business logic, API calls, or Sitecore wiring to test files.
- Never use global Vitest APIs without importing them.
- Never use `fireEvent` when `userEvent` is available.
- Never test implementation details instead of behaviour.
- Never use snapshot tests.
- Never hit the real network or leave timing non-deterministic.
- Never claim measured coverage without an actual test run.
- Never skip a runtime file that is not on the exclusion list.
- Never create test files in a separate `__tests__` folder.
- Never use `.spec.*` — only `.test.*`.
- Never create Storybook `.stories` files.
- Never run lint, type-check, or coverage commands.
- Never re-analyse the story or change approved architecture.
