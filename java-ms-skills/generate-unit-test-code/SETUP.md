# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact and make sure `SKILL.md` remains at the root of the skill folder.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/generate-unit-test-code/SKILL.md
<repo>/.agent/skills/generate-unit-test-code/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/generate-unit-test-code/SKILL.md
~/.agent/skills/generate-unit-test-code/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt:

```text
Use the generate-unit-test-code skill in Agent mode to add unit tests for the newly changed ServiceImpl behavior.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompt:

```text
Use the generate-unit-test-code skill to add tests for the newly changed controller and service behavior.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use generate-unit-test-code for this test coverage change.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/generate-unit-test-code/SKILL.md
.claude/skills/generate-unit-test-code/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/generate-unit-test-code add unit tests for the changed adapter client behavior.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/generate-unit-test-code/SKILL.md
.claude/skills/generate-unit-test-code/SKILL.md
.agents/skills/generate-unit-test-code/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/generate-unit-test-code/SKILL.md
~/.agents/skills/generate-unit-test-code/SKILL.md
```

Example prompt:

```text
Use the generate-unit-test-code skill to add focused tests for the changed order lookup service method, covering success, validation, and error propagation.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- The changed production class(es) or code-generation handoff from a prior implementation skill.
- Any updated contract details relevant to expected test behavior.
- Target repository or module.
- Existing test fixtures, builders, or object mappers to reuse.

Expected result: focused unit tests for the changed behavior only, following existing test conventions, plus a concise handoff of created/modified test files and a recommendation to run `execute-unit-tests` next.
