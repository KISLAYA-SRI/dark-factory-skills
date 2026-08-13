# UI Component Edge Cases
- Loading, error, empty, disabled, and pending states must be explicit for data-backed screens and components.
- Reusable components should not own feature-specific data fetching.
- Dark mode and responsive variants often fail when tokens are hard-coded.
- Headless primitives still require correct labels and controlled state.

## System-Level Risk Patterns
- Prefer typed contracts, explicit boundaries, and realistic failure states.