# App Router Edge Cases
- Client components cannot directly use server-only APIs.
- Static routes with dynamic user data can leak stale or wrong data.
- Hydration mismatches often come from non-deterministic client/server rendering.

## System-Level Risk Patterns
- Prefer typed contracts, explicit boundaries, and realistic failure states.