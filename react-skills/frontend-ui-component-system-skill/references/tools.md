# UI Component Tool Contract
- Inspect existing component folders, design tokens, Storybook config, styling conventions, and accessibility patterns before adding components.
- Prefer existing primitives and design-system APIs over bespoke controls.
- storybook_runner: use the project Storybook command to verify component stories and documentation when configured.
- testing_library_react: use Testing Library React/Vitest/Jest to verify component behavior and interaction states.
- typecheck: run `tsc --noemit` or the project-native typecheck script before claiming typed component readiness.
- lint: run ESLint or the project-native lint script for component and hook changes.