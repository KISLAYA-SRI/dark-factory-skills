# Dimension 1: Reliability (Bugs) — Node/React Fix Patterns & Examples

## Overview

Reliability issues are defects that represent incorrect behavior at runtime in JavaScript/TypeScript, Node.js, and React codebases. SonarQube flags these as **Bugs**. Fix all BLOCKER and CRITICAL bugs before proceeding to lower severities.

---

## Null / Undefined Dereference

```ts
// BAD - potential runtime TypeError
const value = response.data.user.name;

// GOOD - optional chaining + nullish coalescing
const value = response.data?.user?.name ?? '';

// GOOD - explicit guard
if (response.data?.user) {
  const value = response.data.user.name;
}
```

---

## Unhandled Promise Rejections

```ts
// BAD - rejection is never caught
async function loadUser(id: string) {
  const user = await userService.getUser(id);
  return user;
}
loadUser(id); // fire-and-forget, unhandled rejection on failure

// GOOD - caller awaits and handles the error
try {
  const user = await loadUser(id);
} catch (error) {
  logger.error('Failed to load user', error);
}

// BAD - dangling promise in a non-async context
function handleClick() {
  saveDraft(); // returns a promise, ignored
}

// GOOD - explicitly handle or mark intent
function handleClick() {
  void saveDraft().catch((error) => logger.error('Save draft failed', error));
}
```

---

## Missing Error Handling in Async/Await

```ts
// BAD - no try/catch around await, error propagates uncontrolled
export async function fetchOrder(orderId: string) {
  const response = await httpClient.get(`/orders/${orderId}`);
  return response.data;
}

// GOOD - handle and translate errors at the boundary
export async function fetchOrder(orderId: string): Promise<Order> {
  try {
    const response = await httpClient.get(`/orders/${orderId}`);
    return response.data;
  } catch (error) {
    throw new OrderServiceError(`Failed to fetch order ${orderId}`, { cause: error });
  }
}
```

---

## React Hook Dependency and State Bugs

```tsx
// BAD - missing dependency causes stale closure bug
useEffect(() => {
  fetchResults(query);
}, []); // query changes are ignored

// GOOD - include all dependencies used inside the effect
useEffect(() => {
  fetchResults(query);
}, [query]);

// BAD - state update based on stale state value
setCount(count + 1);
setCount(count + 1); // both use the same stale `count`

// GOOD - use the functional updater form
setCount((prev) => prev + 1);
setCount((prev) => prev + 1);

// BAD - setting state after unmount
useEffect(() => {
  fetchData().then((data) => setData(data)); // may run after unmount
}, []);

// GOOD - guard with a cleanup flag or AbortController
useEffect(() => {
  let isMounted = true;
  fetchData().then((data) => {
    if (isMounted) setData(data);
  });
  return () => {
    isMounted = false;
  };
}, []);
```

---

## Strict Equality and Type Coercion Bugs

```ts
// BAD - loose equality causes unexpected coercion
if (value == null) { ... }      // matches both null and undefined implicitly, may be unintended
if (id == '123') { ... }        // string/number coercion bug

// GOOD - explicit strict comparisons
if (value === null || value === undefined) { ... }
if (String(id) === '123') { ... }
```

---

## Array/Object Mutation Bugs

```ts
// BAD - mutating props or state directly (breaks React re-render detection)
function addItem(item: Item) {
  this.state.items.push(item); // mutates state directly
  this.setState({ items: this.state.items });
}

// GOOD - create new references
function addItem(item: Item) {
  setItems((prev) => [...prev, item]);
}

// BAD - mutating a function argument
function normalize(items: Item[]) {
  items.sort(); // mutates caller's array
  return items;
}

// GOOD - copy before mutating
function normalize(items: Item[]) {
  return [...items].sort();
}
```

---

## TypeScript Strict Null Safety

Enable and respect strict null checks instead of suppressing them:

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true
  }
}
```

```ts
// BAD - non-null assertion hides a real bug
const user = users.find((u) => u.id === id)!;

// GOOD - handle the not-found case explicitly
const user = users.find((u) => u.id === id);
if (!user) {
  throw new NotFoundError(`User not found: ${id}`);
}
```
