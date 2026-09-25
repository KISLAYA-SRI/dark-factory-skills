# Code Generation Reporting

Produces the SINGLE consolidated code-generation summary document covering UI, Storybook, Logic, and Tests in one file — written with the Chunked Write Protocol (write first chunk, append the rest) to conserve tokens. Replaces the four legacy per-agent documents.

## Use This For

- Producing the one final summary at the end of the coding workflow (Phase 12).
- Consolidating UI, Sitecore, logic, state, Storybook, and test outputs into one file.
- Writing large documents efficiently via chunked write/append.

## Expected Flow

```text
Chunk 1 (write) : Sections 1–3
Chunk 2 (append): Sections 4–6
Chunk 3 (append): Sections 7–9
Chunk 4 (append): Sections 10–13
  → Save to .SS_WF/Agent/Coding/{{ticket_id}}_CODE_GENERATION_SUMMARY.md
```

## Key Rules

- Only ONE document is produced — no separate CODE_GENERATION / TEST_GENERATION / Storybook docs.
- Never write the summary in a single call — chunk 1 write, rest append; 2-retry guard per chunk.
- Presentational runs mark logic/state/Sitecore sections as Not Applicable.
- Populate every section with story-specific detail; link file paths, don't paste source.
- Never restart the build to regenerate the summary — re-attempt only the failed chunk.

See [SKILL.md](./SKILL.md) for the full instructions.
