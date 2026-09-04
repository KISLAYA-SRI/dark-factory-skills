# Story Analysis — End to End

Skill for performing complete end-to-end analysis of a frontend user story — from story understanding through component classification, acceptance criteria, interaction and state analysis, ownership separation, prop-driven model definition, and NFR analysis.

## Use This For

- Understanding the full scope of a frontend user story from the Jira ticket.
- Classifying the story as Presentational, Transactional, or Hybrid.
- Analysing all acceptance criteria and deriving implementation scope.
- Mapping interaction flows, state transitions, and edge cases.
- Defining ownership separation between server and client components.
- Producing the prop-driven model for all components in scope.
- Running NFR analysis scoped to RTL, Accessibility, Responsive, and Overflow.

## Expected Flow

```text
Jira Story + Dev Notes + Figma + API Analysis outputs
  → Step 1: Story Understanding (extract goals, scope, personas)
  → Step 2: Component Classification (Presentational / Transactional / Hybrid)
  → Step 3: Scope Derivation (what is in scope vs. out of scope)
  → Step 4: Acceptance Criteria Analysis (derive implementation rules per AC)
  → Step 5: Interaction and State Analysis (flows, states, edge cases)
  → Step 6: Ownership Separation (server vs. client component boundaries)
  → Step 7: Prop-Driven Model Definition (props, types, defaults per component)
  → Step 8: NFR Analysis (RTL, Accessibility, Responsive, Overflow only)
  → Step 9: Code Generation Plan prerequisites check
```

This skill is self-contained and embeds all rules, guidelines, and decision logic internally.

## Key Rules

- Follow the priority order at every decision: Dev Notes → Project Guidelines → Figma → React/Frontend Best Practices.
- Dev Notes are sacred law — if a Dev Note covers a topic, it IS the answer.
- Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").
- NFR analysis is scoped to four categories only: RTL, Accessibility, Responsive, and Overflow.
- Do not analyse Localisation, Performance, Security, Maintainability, or Testability in this skill.
- All conflicts between sources must be recorded in DEV_REVIEW.md with the resolution.
- Phase 4 (API Analysis) must be complete before Step 9 runs.

See [SKILL.md](./SKILL.md) for the full instructions.
