# API Integration Edge Cases
- Retrying non-idempotent writes can duplicate side effects.
- BFF routes must not become unaudited backend business logic.
- Generated type drift must be caught by contract/typegen checks.

## System-Level Risk Patterns
- Prefer typed contracts, explicit boundaries, and realistic failure states.