# Dimension 3: Maintainability (Code Smells) — Node/React Fix Patterns & Examples

## Overview

Code smells reduce readability and make future changes risky. Fix by reducing complexity, removing dead code, and improving naming, in both Node.js services and React components.

---

## Cognitive Complexity Reduction

```ts
// BAD - high cognitive complexity (nested ifs, loops, conditions)
function processOrder(order: Order): string {
  if (order) {
    if (order.status === 'PENDING') {
      if (order.items && order.items.length > 0) {
        for (const item of order.items) {
          if (item.quantity > 0) {
            if (item.price > 0) {
              // process
            }
          }
        }
      }
    }
  }
  return 'done';
}

// GOOD - extract functions, use guard clauses, array methods
function processOrder(order: Order): string {
  validateOrder(order);
  processValidItems(order.items);
  return 'done';
}

function validateOrder(order: Order): void {
  if (!order) throw new Error('Order must not be null');
  if (order.status !== 'PENDING') throw new Error('Order is not in PENDING status');
}

function processValidItems(items: OrderItem[] = []): void {
  items
    .filter((item) => item.quantity > 0 && item.price > 0)
    .forEach(processItem);
}
```

---

## Component and Function Size

- Keep functions/hooks focused on a single responsibility; extract helpers for distinct logical steps.
- Keep React components under roughly 150–200 lines; extract subcomponents when a component mixes multiple concerns (data fetching, layout, presentation).
- Extract complex conditional rendering into small named components or helper functions instead of deeply nested JSX ternaries.

```tsx
// BAD - deeply nested ternaries in JSX
return (
  <div>
    {isLoading ? <Spinner /> : error ? <ErrorMessage error={error} /> : data ? <ResultList data={data} /> : <EmptyState />}
  </div>
);

// GOOD - extract to a small render function or early returns
function renderContent() {
  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!data) return <EmptyState />;
  return <ResultList data={data} />;
}

return <div>{renderContent()}</div>;
```

---

## Dead Code Removal

```ts
// BAD - unused import
import { debounce } from 'lodash'; // never used

// BAD - unreachable code
function getValue() {
  return result;
  console.log('returned'); // unreachable
}

// BAD - unused variable/parameter
function handler(event, _context) { // _context intentionally unused should be prefixed or removed per lint config
  console.log(event);
}

// FIX - remove all dead code and unused imports/variables
```

---

## Magic Numbers and Strings

```ts
// BAD
if (user.age > 18) { ... }
if (status === 'ACTIVE') { ... }
setTimeout(retry, 5000);

// GOOD - named constants
const MINIMUM_AGE = 18;
const STATUS_ACTIVE = 'ACTIVE';
const RETRY_DELAY_MS = 5_000;

if (user.age > MINIMUM_AGE) { ... }
if (status === STATUS_ACTIVE) { ... }
setTimeout(retry, RETRY_DELAY_MS);

// BETTER - use string literal unions or enums for status
type UserStatus = 'ACTIVE' | 'INACTIVE' | 'SUSPENDED';
if (user.status === 'ACTIVE' satisfies UserStatus) { ... }
```

---

## Naming Conventions

```ts
// BAD
class Mgr { ... }              // abbreviation
let d: number;                 // single letter
function doIt() { ... }        // vague
function getUsrs() { ... }     // typo

// GOOD
class UserManager { ... }
let durationInSeconds: number;
function processUserRegistration() { ... }
function getUsers() { ... }
```

---

## Boolean Expression Simplification

```ts
// BAD
if (isValid === true) { ... }
if (isActive !== false) { ... }
return count > 0 ? true : false;

// GOOD
if (isValid) { ... }
if (isActive) { ... }
return count > 0;
```

---

## Prop Drilling and State Colocation

```tsx
// BAD - passing the same props through many intermediate components
<Parent user={user}>
  <Child user={user}>
    <GrandChild user={user} />
  </Child>
</Parent>

// GOOD - colocate state closer to where it's used, or use context/composition
const UserContext = createContext<User | null>(null);

<UserContext.Provider value={user}>
  <Parent>
    <Child>
      <GrandChild />
    </Child>
  </Parent>
</UserContext.Provider>

// In GrandChild:
const user = useContext(UserContext);
```

---

## ESLint Rules Commonly Backing These Smells

Align fixes with the project's existing ESLint configuration (`.eslintrc`, `eslint.config.js`) rather than introducing a new one. Common rules relevant to Maintainability findings:

- `complexity` / `sonarjs/cognitive-complexity` — cognitive complexity threshold.
- `no-unused-vars`, `no-unreachable` — dead code.
- `no-magic-numbers` — magic numbers.
- `eqeqeq` — strict equality.
- `react-hooks/exhaustive-deps` — hook dependency correctness (also relevant to Reliability).
