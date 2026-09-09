# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact and make sure `SKILL.md` remains at the root of the skill folder.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/validate-project-compile/SKILL.md
<repo>/.agent/skills/validate-project-compile/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/validate-project-compile/SKILL.md
~/.agent/skills/validate-project-compile/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt:

```text
Use the validate-project-compile skill in Agent mode to confirm the project compiles after this change.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompt:

```text
Use the validate-project-compile skill to build the project and fix any compile errors from the recent change.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use validate-project-compile for this build check.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/validate-project-compile/SKILL.md
.claude/skills/validate-project-compile/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/validate-project-compile confirm the module compiles after the adapter client change.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/validate-project-compile/SKILL.md
.claude/skills/validate-project-compile/SKILL.md
.agents/skills/validate-project-compile/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/validate-project-compile/SKILL.md
~/.agents/skills/validate-project-compile/SKILL.md
```

Example prompt:

```text
Use the validate-project-compile skill to build the service module and resolve any Lombok/MapStruct annotation processing errors.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- The changed module or repository.
- Any known dependency/repository access constraints.
- Whether a targeted module build or a full multi-module build is expected.

Expected result: the exact Maven command that succeeded, or a concise report of the failing module, goal, exception, and first actionable compiler error if blocked.
