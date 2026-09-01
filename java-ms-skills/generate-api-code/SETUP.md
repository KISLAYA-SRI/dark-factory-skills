# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact and make sure `SKILL.md` remains at the root of the skill folder.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/generate-api-code/SKILL.md
<repo>/.agent/skills/generate-api-code/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/generate-api-code/SKILL.md
~/.agent/skills/generate-api-code/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt:

```text
Use the generate-api-code skill in Agent mode to implement this Spring Boot REST API from the JIRA and OpenAPI details.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompt:

```text
Use the backend-api-microservice skill to implement the account summary API from the attached OpenAPI contract and JIRA notes.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use backend-api-microservice for this Spring Boot endpoint change.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/generate-api-code/SKILL.md
.claude/skills/generate-api-code/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/generate-api-code implement the customer profile REST endpoint using the provided API contract.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/generate-api-code/SKILL.md
.claude/skills/generate-api-code/SKILL.md
.agents/skills/generate-api-code/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/generate-api-code/SKILL.md
~/.agents/skills/generate-api-code/SKILL.md
```

Example prompt:

```text
Use the generate-api-code skill to add the order lookup API. Follow the OpenAPI contract, preserve the existing response envelope, and reuse the configured adapter client.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- JIRA story or acceptance criteria.
- OpenAPI/spec details for paths, methods, headers, request bodies, responses, and errors.
- Target repository or module.
- Downstream adapter/shared-lib client expectations.
- Any security, validation, logging, or response envelope constraints.

Expected result: code changes that extend the existing Spring Boot microservice layers cleanly, plus a concise handoff of changed files, assumptions, and any tests that were run or still need to be run.
