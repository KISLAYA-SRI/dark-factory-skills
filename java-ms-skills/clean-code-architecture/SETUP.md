# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact and make sure `SKILL.md` remains at the root of the skill folder.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/clean-code-architecture/SKILL.md
<repo>/.agent/skills/clean-code-architecture/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/clean-code-architecture/SKILL.md
~/.agent/skills/clean-code-architecture/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt:

```text
Use the clean-code-architecture skill in Agent mode to review and refactor the changed ServiceImpl class for clean-code and architecture issues.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompt:

```text
Use the clean-code-architecture skill to review the changed adapter client for coupling and God-class issues.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use clean-code-architecture for this design review.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/clean-code-architecture/SKILL.md
.claude/skills/clean-code-architecture/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/clean-code-architecture review the changed controller and service classes for clean-code violations.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/clean-code-architecture/SKILL.md
.claude/skills/clean-code-architecture/SKILL.md
.agents/skills/clean-code-architecture/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/clean-code-architecture/SKILL.md
~/.agents/skills/clean-code-architecture/SKILL.md
```

Example prompt:

```text
Use the clean-code-architecture skill to run the standard review checklist against the files changed in this branch and apply safe fixes automatically.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- The changed/target files or classes, or let the skill resolve scope from the current diff.
- The reason for review (new code review, pre-existing smell, architecture question), if known.
- Any project-specific static-analysis thresholds (`sonar-project.properties`, Checkstyle/PMD rulesets) that should take precedence over the default thresholds.

Expected result: a lean, non-blocking completion summary listing scope reviewed/refactored, changes or findings by severity, and any follow-up skill (`execute-unit-tests`, `generate-unit-test-code`) worth queuing next. This skill runs autonomously with no human-in-the-loop gate and never blocks the workflow.
