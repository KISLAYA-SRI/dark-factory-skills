# Storybook and Component Catalogue

Generates or updates Storybook stories and the root component-catalogue.json for eligible reusable components — Design System components, Sitecore-mapped reusable presentation components, and any reusable file created in the Design System.

## Use This For

- Writing co-located stories for eligible reusable components (Phase 9).
- Covering props, variants, visual states, RTL, and responsive contexts.
- Upserting the root component-catalogue.json without corrupting existing entries.

## Expected Flow

```text
For each eligible component:
  → Read generated Props/variants/states from actual source
  → Generate <Component>.stories.tsx (default + variants + states + RTL + responsive)
  → Wire callbacks to Storybook actions; mock props only
  → Upsert entry in root component-catalogue.json (match by name)
  → Validate catalogue JSON
```

## Key Rules

- Eligibility: DS components, Sitecore-mapped reusable presentation components, reusable DS files only (Resolved Conflict 7).
- Never write stories for containers, hooks, services, mappers, or one-off feature components.
- component-catalogue.json lives at the repository root (Resolved Conflict 2).
- Upsert by name — never blind-append or delete unrelated entries.
- Load only the STORYBOOK LEARNINGS namespace.

See [SKILL.md](./SKILL.md) for the full instructions.
