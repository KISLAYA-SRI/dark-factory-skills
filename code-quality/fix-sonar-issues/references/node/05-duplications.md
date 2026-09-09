# Dimension 5: Duplications (Code Duplication) — Node/React Fix Patterns & Examples

## Overview

SonarQube flags duplicated blocks (default: 10+ identical lines in 3+ files, or 100+ tokens). Target: **< 3% duplication**. This applies equally to Node.js services and React/TypeScript frontends.

---

## Identifying Duplicated Code from SonarQube

1. In SonarQube UI → Project → **Duplications** tab.
2. Click on a file to see highlighted duplicated blocks.
3. SonarQube shows the other files where the same block appears.
4. Use the discovered **Component Measures** tool with `metricKeys=duplicated_lines_density,duplicated_blocks` and the discovered **Duplicated Files Search**/**Duplication Detail** tools for file-level detail.

---

## Refactoring Strategy: Extract Function/Utility

```ts
// BAD - same validation logic duplicated across route handlers
// userController.ts
if (!body.name || body.name.trim() === '') {
  throw new ValidationError('Name is required');
}
if (!body.email || !body.email.includes('@')) {
  throw new ValidationError('Valid email is required');
}

// profileController.ts - SAME block duplicated
if (!body.name || body.name.trim() === '') {
  throw new ValidationError('Name is required');
}
...

// GOOD - extract to a shared validator/schema
import { z } from 'zod';

export const userRequestSchema = z.object({
  name: z.string().trim().min(1, 'Name is required'),
  email: z.string().email('Valid email is required'),
});

// Use in both handlers
const payload = userRequestSchema.parse(req.body);
```

---

## Refactoring Strategy: Extract Custom Hook (React)

```tsx
// BAD - duplicate data-fetching + loading/error state logic in multiple components
function UserList() {
  const [data, setData] = useState<User[]>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    userApi.list().then(setData).catch(setError).finally(() => setLoading(false));
  }, []);
  // ...
}

function ProductList() {
  const [data, setData] = useState<Product[]>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    productApi.list().then(setData).catch(setError).finally(() => setLoading(false));
  }, []);
  // ...
}

// GOOD - extract a shared hook
function useFetch<T>(fetcher: () => Promise<T>) {
  const [data, setData] = useState<T>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetcher()
      .then((result) => !cancelled && setData(result))
      .catch((err) => !cancelled && setError(err))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [fetcher]);

  return { data, loading, error };
}

// Usage
const { data: users, loading, error } = useFetch(userApi.list);
const { data: products } = useFetch(productApi.list);
```

---

## Refactoring Strategy: Shared Higher-Order Component / Wrapper

```tsx
// BAD - duplicated auth-guard logic in multiple page components
function DashboardPage() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  return <Dashboard />;
}

function SettingsPage() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  return <Settings />;
}

// GOOD - extract a reusable guard component
function RequireAuth({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  return <>{children}</>;
}

// Usage
<Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
<Route path="/settings" element={<RequireAuth><Settings /></RequireAuth>} />
```

---

## Consolidating Error Response Construction (Express/Node)

```ts
// BAD - duplicated error response shape in multiple route handlers
// userRoutes.ts
catch (error) {
  res.status(404).json({ error: error.message, timestamp: new Date().toISOString() });
}

// orderRoutes.ts - SAME pattern
catch (error) {
  res.status(404).json({ error: error.message, timestamp: new Date().toISOString() });
}

// GOOD - centralized error-handling middleware
export function errorHandler(err: AppError, req: Request, res: Response, next: NextFunction) {
  const status = err.statusCode ?? 500;
  res.status(status).json({ error: err.message, timestamp: new Date().toISOString() });
}

// Remove per-route try/catch error formatting where the middleware already covers it,
// and forward errors with next(error) instead.
```

---

## Shared Validation Schemas

```ts
// BAD - same email pattern duplicated across multiple schemas
const loginSchema = z.object({
  email: z.string().regex(/^[^\s@]+@[^\s@]+\.[^\s@]+$/),
});
const registerSchema = z.object({
  email: z.string().regex(/^[^\s@]+@[^\s@]+\.[^\s@]+$/), // duplicated
});

// GOOD - extract a shared schema fragment
const emailField = z.string().email('Must be a valid email address');

const loginSchema = z.object({ email: emailField });
const registerSchema = z.object({ email: emailField, password: z.string().min(8) });
```

---

## Near-Duplicates vs Exact Duplicates

- **Exact duplicates** (same tokens): extract to a shared function/hook/component immediately.
- **Near-duplicates** (slight variations): parameterize the varying parts.

```ts
// Near-duplicate: same logic, different entity names
function buildUserAuditMessage(user: User) {
  return `[${user.id}] User ${user.name} action at ${new Date().toISOString()}`;
}
function buildOrderAuditMessage(order: Order) {
  return `[${order.id}] Order ${order.ref} action at ${new Date().toISOString()}`;
}

// GOOD - parameterize
function buildAuditMessage(entityId: string, entityName: string) {
  return `[${entityId}] ${entityName} action at ${new Date().toISOString()}`;
}
```

---

## Utility Module vs Shared Component Decision

- Use **plain utility functions/modules** when: logic is stateless and framework-agnostic (formatting, validation, calculations).
- Use **custom hooks** when: shared logic involves React state, effects, or lifecycle.
- Use **shared/wrapper components** when: shared logic involves rendering/composition (guards, layouts, providers).
- Prefer composition (hooks, wrapper components) over deep inheritance/class hierarchies in React codebases.
