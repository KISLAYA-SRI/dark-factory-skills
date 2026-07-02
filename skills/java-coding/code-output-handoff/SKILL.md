---
name: code-output-handoff
description: Use when creating or updating the concise implementation handoff file after Java backend API or adapter-lib code changes. Triggers include ss_code_gen.md, implementation summary, code generation handoff, downstream test agent handoff, files changed summary, build result summary, or output file instructions.
---

# Code Output Handoff

Create or replace `ss_code_gen.md` after implementation work when a downstream test/review agent needs a factual handoff.

## Location

Create the file in the workspace root, not inside the Java code repository.

If the agent is running from inside the Java repo, place `ss_code_gen.md` in the parent/workspace path specified by the orchestration context. If the workspace root is ambiguous, use the directory that contains the checked-out target repo and any sibling handoff artifacts.

## Required Structure

Use exactly these sections:

```text
## Functionality Implemented
- Brief bullets describing behavior added or changed.

## Files Changed
- Relative paths to production files changed.

## Key Technical Notes
- Factual notes needed by test/review agents: contracts followed, mapper/client/error behavior, assumptions from provided context.

## Build Result
- <command> : SUCCESS
```

## Rules

- Keep it concise and factual.
- Do not include code snippets, diffs, future work, recommendations, or test plans.
- Do not describe implementation line by line.
- Include only what was actually implemented.
- If no code changes were required, state that the existing implementation already satisfied the requirement and list the existing files that cover it.
- If build was blocked, write the exact command and concise blocker instead of claiming success.
