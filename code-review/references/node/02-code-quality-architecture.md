# Code Quality & Architecture Review — Node.js / React / TypeScript

## Role

Review changed JS/TS code as a Senior Software Architect would: naming, structure, architectural alignment, performance, and test coverage for the **changed/added lines**, not a full-file sweep.

## Expected Layering (Baseline to Check Against)

**Node/Express/NestJS/Fastify backend:**

```text
Route/Controller -> Service -> Repository/Client (DB or adapter/API client)
```

**React/Next.js frontend:**

```text
Page/Route component -> Container/Feature component (data loading, state) -> Presentational component -> Design-system atom/molecule
```

- Route handlers/controllers validate and delegate; they should not embed raw downstream/DB calls when a service layer already exists.
- Presentational components should not directly call APIs; data loading belongs in containers/hooks/services.
- Shared logic lives in hooks, services, or utility modules — not duplicated across components/routes.

## Checklist

1. **Naming & readability** — components/functions/variables state intent without a comment; no generic names (`data`, `helper`, `Manager`) unless already the local convention.
2. **Single Responsibility** — flag a changed component/module that now mixes data fetching, business logic, and rendering/response-building together.
3. **Function/component size & complexity** — flag new/changed functions over ~40 executable lines, cyclomatic complexity over 10, or JSX nesting/conditional branching deeper than 3 levels.
4. **Function arguments / prop count** — flag new functions with more than 3-4 parameters, or components receiving more than ~7-8 unrelated props (consider a config object or composition).
5. **Duplication (DRY)** — flag 6+ duplicated lines introduced by the diff that duplicate an existing hook, utility, or component instead of reusing it.
6. **Architecture/dependency direction** — flag presentational components making direct API calls, or route handlers embedding business logic that belongs in a service.
7. **Error handling** — flag new `async`/`await` code paths with no `try`/`catch` or `.catch()`, unhandled promise rejections, and new API routes with no error-forwarding (`next(error)` in Express-style apps).
8. **React-specific correctness** — flag missing/incorrect `useEffect`/`useMemo`/`useCallback` dependency arrays introduced by the diff, direct state/array/object mutation instead of immutable updates, and new prop-drilling chains of 3+ levels where context/composition would be clearer.
9. **Constants over magic values** — flag new repeated literals (numeric, string, duration/threshold) that should be named constants or config.
10. **Dead code & redundancy** — flag unused imports/variables introduced by the diff, unreachable branches, and commented-out code left in.
11. **Type safety (TypeScript)** — flag new `any` usage where a concrete type/interface is available, missing return types on exported functions, and unchecked type assertions (`as`) that bypass real validation.
12. **Testability** — flag new business logic embedded directly in a component/route handler with no extracted, independently testable function/hook.
13. **Test coverage** — flag non-trivial new logic, new branches, or new error paths introduced by the diff with no corresponding new/updated test (Jest/Vitest + React Testing Library, or equivalent).

## Examples

### Architecture Violation (Presentational Component Fetching Data)

```tsx
// FLAG — [ISSUE] presentational component directly calling an API
function UserCard({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch(`/api/users/${userId}`).then(r => r.json()).then(setUser); // should be in a container/hook
  }, [userId]);
  return <div>{user?.name}</div>;
}

// ACCEPTABLE — data loading lives in a hook/container, component stays presentational
function UserCard({ user }: { user: User }) {
  return <div>{user.name}</div>;
}
```

### Unhandled Promise Rejection

```ts
// FLAG — [BLOCKER] no error handling; an unhandled rejection crashes the process
async function syncUsers() {
  const users = await userService.fetchAll();
  await db.save(users);
}
syncUsers(); // fire-and-forget, no .catch()

// ACCEPTABLE
syncUsers().catch(err => logger.error('syncUsers failed', err));
```

### Missing `useEffect` Dependency

```tsx
// FLAG — [ISSUE] stale closure risk from missing dependency
useEffect(() => {
  fetchData(filter);
}, []); // `filter` used inside but omitted from deps

// ACCEPTABLE
useEffect(() => {
  fetchData(filter);
}, [filter]);
```

### State Mutation

```ts
// FLAG — [ISSUE] direct mutation of state array
function addItem(item: Item) {
  items.push(item); // mutates state directly
  setItems(items);
}

// ACCEPTABLE
function addItem(item: Item) {
  setItems(prev => [...prev, item]);
}
```

### Magic Values

```ts
// FLAG — [SUGGESTION]
if (retryCount > 3) { ... }

// ACCEPTABLE
const MAX_RETRY_ATTEMPTS = 3;
if (retryCount > MAX_RETRY_ATTEMPTS) { ... }
```

### Missing Test Coverage

```ts
// New branch added in the diff:
if (amount <= 0) {
  throw new ValidationError('Amount must be positive');
}
// FLAG — [ISSUE] no corresponding test asserting ValidationError for a zero/negative amount
```

## Severity Guidance for This Dimension

- **[BLOCKER]**: unhandled promise rejection on a critical path, swallowed error that hides a failure, public contract/response-shape breakage.
- **[ISSUE]**: architecture/layering violation (presentational component fetching data, business logic in a route handler), missing error handling for a new path, missing tests for new non-trivial logic, state mutation bugs, duplicated logic (3+ places).
- **[SUGGESTION]**: naming, magic values, minor same-file duplication, `any` usage where a type is easily inferable, comment hygiene, verbose conditionals.

## When Nothing Is Found

If the diff introduces no quality/architecture concern from the checklist above, state plainly that the code quality and architecture of the change are sound. Do not invent findings to pad the review.
