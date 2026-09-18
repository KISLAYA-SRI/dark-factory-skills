---
name: frontend-test-generation
description: Use to generate co-located Vitest + React Testing Library tests based on the actual generated source files, targeting 90–100% branch/function coverage. Applies the runtime-file classification policy so every runtime file gets a co-located test unless explicitly excluded. Triggers include test generation, unit tests, Vitest, React Testing Library, coverage, or write tests for these files.
disable-model-invocation: true
---

## Frontend Test Generation

### Purpose

Generate co-located behavioural tests from the ACTUAL generated source (not the plan). Source files are the ground truth: inspect real branches, callbacks, states, and exports, then test observable behaviour.

### Co-Location Policy (Resolved Conflict 5)

> Every new or modified file containing runtime behaviour must have a co-located test unless explicitly excluded by the runtime-file classification policy.

**Runtime files that REQUIRE a test:**
- Components (presentational + containers), hooks, services, mappers, validation utilities, stores, Sitecore rendering entries.

**Excluded by classification policy (no test):**
- Barrel/index files, type-only files, `*.stories.tsx`, config files, primitive constants files (pure literals with no logic).

Co-locate: `<Source>.test.tsx` / `<Source>.test.ts` beside the source.

### Coverage Target (Resolved Conflict 4)

Design tests to cover **90%–100%** of generated runtime code (branches + functions). Build a coverage map per file and add cases until every branch, callback, and state path is exercised.

⚠️ If test **execution** is outside the current scope, state **intended** coverage (with the branch map) — do not claim measured coverage without a run. A separate runtime quality gate verifies the actual number.

### Classification-Aware Strategies (Applied Additively)

Pick strategies by file type; a file may use several:

```text
UI component        → render; assert prop-driven output; fire interactions via userEvent;
                      assert callback invocations; assert each visual state (loading/empty/error/disabled);
                      assert a11y roles/labels; RTL render assertion.
Container           → mock the hook; assert correct state → props mapping; assert callbacks/navigation.
Hook (TanStack)     → wrap in QueryClientProvider; mock service; assert loading/success/error;
                      assert mapper output shape (ViewModel).
Service             → mock the API client; assert endpoint/params from constants; assert typed result on 2xx/4xx/5xx.
Mapper/util         → pure input→output cases incl. null/empty/partial; boundary values.
Validation util     → valid/invalid/edge inputs; error message correctness.
Store (Zustand)     → initial state; each action; selector behaviour.
Sitecore entry      → mock fields (incl. unauthored/null); assert field→prop mapping; preview-safe render.
```

### Test Quality Rules

- Explicit Vitest imports: `import { describe, it, expect, vi, beforeEach } from 'vitest'`.
- User interactions via `@testing-library/user-event` (`userEvent.setup()`), not raw `fireEvent` where avoidable.
- Query by role/label/text (accessible queries) — test behaviour, not implementation details.
- **No snapshot tests.**
- Mock external boundaries (API client, navigation, services) — never hit the network.
- Deterministic: fake timers for autoplay/carousel/debounce; no real waits.
- One behaviour per `it`; descriptive names.

### Branch Coverage Checklist (per file)

```text
- [ ] Every conditional/ternary branch has a test.
- [ ] Every callback prop is asserted as called with expected args.
- [ ] Every state (default/loading/success/error/empty/partial/disabled) rendered.
- [ ] Every exported function/hook has at least one direct test.
- [ ] Null/empty/partial data paths covered (mappers/containers).
- [ ] RTL and keyboard interaction covered for interactive UI.
```

### Learnings Namespace (Resolved Conflict 6)

Load only the `# TEST LEARNINGS` namespace.

### Output (per runtime source file)

```text
<Source>.test.tsx  (co-located)  — Vitest + RTL, branch-mapped cases
```

### Gate: Complete When

```text
- [ ] Every runtime file has a co-located test (or is explicitly excluded).
- [ ] Branch/coverage map shows 90–100% intended coverage per file.
- [ ] Interactions via userEvent; accessible queries used; no snapshots.
- [ ] External boundaries mocked; tests deterministic (fake timers where needed).
- [ ] All visual states and callbacks asserted.
```

### Never Do

- Never test implementation details (internal state names, private functions) instead of behaviour.
- Never use snapshot tests.
- Never hit the real network or leave timing non-deterministic.
- Never claim measured coverage without an actual test run.
- Never skip a runtime file that is not on the exclusion list.
