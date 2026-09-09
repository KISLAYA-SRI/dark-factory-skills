# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact, including the `references/` subfolder, and make sure `SKILL.md` remains at the root of the skill folder.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/fix-sonar-issues/SKILL.md
<repo>/.agent/skills/fix-sonar-issues/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/fix-sonar-issues/SKILL.md
~/.agent/skills/fix-sonar-issues/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt:

```text
Use the fix-sonar-issues skill in Agent mode to fetch the current SonarQube quality gate results and fix the failing dimensions.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompt:

```text
Use the fix-sonar-issues skill to fetch and fix the open Reliability and Security issues for this project.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use fix-sonar-issues for this remediation.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/fix-sonar-issues/SKILL.md
.claude/skills/fix-sonar-issues/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/fix-sonar-issues fix the current SonarQube quality gate failures for this microservice.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/fix-sonar-issues/SKILL.md
.claude/skills/fix-sonar-issues/SKILL.md
.agents/skills/fix-sonar-issues/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/fix-sonar-issues/SKILL.md
~/.agents/skills/fix-sonar-issues/SKILL.md
```

Example prompt:

```text
Use the fix-sonar-issues skill to resolve the BLOCKER and CRITICAL issues from the latest SonarQube analysis, then report a fix summary.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- SonarQube project key, or confirmation that the agent should discover it.
- Repository path of the Java Maven project to be fixed.
- Branch, PR, or analysis context for the SonarQube results being remediated.
- Any pre-loaded issue list/context, if analysis results were already fetched.
- Confirmation that a SonarQube MCP tool or equivalent tooling is configured and accessible.

Expected result: a structured fix report grouped by file and rule, covering issues fixed, suppressed, and skipped, plus the build/test validation command and outcome.
