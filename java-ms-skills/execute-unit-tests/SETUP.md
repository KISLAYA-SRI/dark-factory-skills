# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact and make sure `SKILL.md` remains at the root of the skill folder.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/execute-unit-tests/SKILL.md
<repo>/.agent/skills/execute-unit-tests/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/execute-unit-tests/SKILL.md
~/.agent/skills/execute-unit-tests/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt:

```text
Use the execute-unit-tests skill in Agent mode to run and stabilize the tests for the changed service class.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompt:

```text
Use the execute-unit-tests skill to run and fix the failing OrderServiceTest class.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use execute-unit-tests for this test run.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/execute-unit-tests/SKILL.md
.claude/skills/execute-unit-tests/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/execute-unit-tests run and stabilize the tests for the changed controller class.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/execute-unit-tests/SKILL.md
.claude/skills/execute-unit-tests/SKILL.md
.agents/skills/execute-unit-tests/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/execute-unit-tests/SKILL.md
~/.agents/skills/execute-unit-tests/SKILL.md
```

Example prompt:

```text
Use the execute-unit-tests skill to run the class-level test for PaymentClientImplTest and fix any failures until it passes.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- The changed or failing test class name(s).
- Target repository or module.
- Any known environment constraints (credentials, network access, external services).
- Coverage or integration gate requirements, if applicable.

Expected result: the exact Maven command that passed, or a concise report of the failing test class/method, root cause, and whether the failure is code, test, or environment related.
