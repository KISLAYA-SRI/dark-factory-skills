# Developer Notes Protocol

Skill for extracting and enforcing Developer Notes from a Jira user story before any analysis begins. Developer Notes are sacred law and override every other source in the pipeline.

## Use This For

- Extracting all Developer Notes / Dev Notes from a Jira user story before any other analysis step.
- Numbering and cataloguing each Dev Note as DN-001, DN-002, DN-003, etc.
- Enforcing Dev Note instructions at every analysis decision point throughout the entire workflow.
- Overriding Figma, API specs, guidelines, or best practices wherever a Dev Note applies.
- Flagging and recording every decision influenced by a Dev Note with its DN ID.

## Expected Flow

```text
Jira Story
  → Scan for Developer Notes section
  → Extract and number every instruction (DN-001, DN-002, ...)
  → Maintain active working list throughout analysis
  → At every decision: check if a Dev Note covers the topic
    → YES: Dev Note IS the answer — no alternative produced
    → NO: Proceed with normal source priority order
```

This step runs first — before Figma, before API specs, before any other source is consulted.

## Key Rules

- Developer Notes are the single highest-priority input in the entire analysis pipeline.
- Extract Dev Notes before reading any other source — Figma, Sitecore API, BFF API, or guidelines.
- Every Dev Note instruction must be followed exactly — no interpretation, override, or exception.
- If a Dev Note covers a topic, it IS the answer. Do not produce an alternative or recommendation.
- Label every decision influenced by a Dev Note with its DN ID (e.g., "Per DN-002").
- If no Developer Notes section exists in the story, record that explicitly and proceed.

See [SKILL.md](./SKILL.md) for the full instructions.
