# Frontend Test Generation

Generates co-located Vitest + React Testing Library tests based on the actual generated source files, targeting 90–100% branch/function coverage, and applies the runtime-file classification policy so every runtime file gets a co-located test unless explicitly excluded.

## Use This For

- Writing behavioural tests from the real generated source (Phase 10).
- Applying classification-aware strategies per file type.
- Building branch-mapped coverage toward 90–100%.

## Expected Flow

```text
For each runtime source file (not excluded):
  → Classify file type
  → Build coverage map (branches/callbacks/states/exports)
  → Generate co-located Vitest + RTL test
  → Use userEvent + accessible queries; mock boundaries; no snapshots
  → Cover all states, callbacks, null/empty/partial paths, RTL/keyboard
```

## Key Rules

- Co-location policy: every runtime file gets a test unless excluded.
- Coverage target 90–100%; state intended coverage if execution is out of scope.
- Test behaviour, not implementation details; no snapshot tests.
- Mock external boundaries; keep tests deterministic (fake timers).
- Load only the TEST LEARNINGS namespace .

See [SKILL.md](./SKILL.md) for the full instructions.
