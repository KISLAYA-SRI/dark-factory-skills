# API Analysis — Sitecore and BFF

Skill for performing strict Sitecore API and BFF API analysis for a frontend user story. Enforces endpoint-only lookup, deep YAML analysis for all request/response scenarios, and produces the Data Fetching Pattern per endpoint.

## Use This For

- Identifying and analysing Sitecore REST endpoints referenced in a Jira story.
- Identifying and analysing BFF API endpoints from YAML spec files.
- Extracting all request/response scenarios from YAML specs — not just the happy path.
- Determining the correct Data Fetching Pattern (TanStack Query, SSR, or static) per endpoint.
- Producing the API contract summary for use in the Story Analysis and Output Contract phases.

## Expected Flow

```text
Jira Story
  → Identify Sitecore endpoints
    → Strict endpoint-only lookup in SC API spec repo
    → Extract all request/response scenarios from YAML
    → Determine Data Fetching Pattern
  → Identify BFF endpoints
    → Strict endpoint-only lookup in BFF YAML spec
    → Extract all request/response scenarios
    → Determine Data Fetching Pattern
  → Produce API contract summary
```

Both Sitecore and BFF analysis are performed here in a single pass — there is no separate API analysis agent.

## Key Rules

- Never browse folders or list files — look up only the exact endpoint path from the story.
- Never fall back to similar JSON files or approximate endpoint matches.
- Read ALL request/response scenarios from the YAML spec, not just the primary scenario.
- If no Sitecore API details are found, mark as `SITECORE API NOT FOUND / NOT REQUIRED`.
- If no BFF API details are found, mark as `BFF API NOT FOUND / NOT REQUIRED`.
- Do not invent API fields, endpoints, or response shapes.
- The Data Fetching Pattern must be determined per endpoint based on the project's established patterns.

See [SKILL.md](./SKILL.md) for the full instructions.
