# Setup

This folder contains two independent Agent Skills-style skill folders: `execute-sonar-analysis` and `fix-sonar-issues`. Each skill is portable across tools that support Agent Skills-style folders and supports both Maven (Java) and Node.js/React project families. Install and enable skills individually — each skill folder must keep its own `SKILL.md` at its root, along with its `references/` subfolder (`references/maven.md` + `references/node.md` for `execute-sonar-analysis`; `references/maven/` + `references/node/` for `fix-sonar-issues`).

See the per-skill `SETUP.md` for tool-specific installation instructions:

- [`execute-sonar-analysis/SETUP.md`](./execute-sonar-analysis/SETUP.md)
- [`fix-sonar-issues/SETUP.md`](./fix-sonar-issues/SETUP.md)

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/execute-sonar-analysis/SKILL.md
<repo>/.slingshot/skills/fix-sonar-issues/SKILL.md
<repo>/.agent/skills/execute-sonar-analysis/SKILL.md
<repo>/.agent/skills/fix-sonar-issues/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/execute-sonar-analysis/SKILL.md
~/.slingshot/skills/fix-sonar-issues/SKILL.md
~/.agent/skills/execute-sonar-analysis/SKILL.md
~/.agent/skills/fix-sonar-issues/SKILL.md
```

After adding user-level skills, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt (chained workflow, works for either project family):

```text
Use the execute-sonar-analysis skill to run the SonarQube analysis for this project. If the quality gate fails, use the fix-sonar-issues skill to remediate the findings, then re-run the analysis.
```

## Codex

Install each skill folder in the Codex skills location used by your environment, or keep them in a workspace skills folder if your Codex setup loads project-local skills.

```text
Use the execute-sonar-analysis skill to trigger the SonarQube scan for this Node/React app, then use fix-sonar-issues to resolve any BLOCKER/CRITICAL findings.
```

## Claude Code

Install each skill as a personal or project skill:

```text
~/.claude/skills/execute-sonar-analysis/SKILL.md
~/.claude/skills/fix-sonar-issues/SKILL.md
.claude/skills/execute-sonar-analysis/SKILL.md
.claude/skills/fix-sonar-issues/SKILL.md
```

Example prompts:

```text
/execute-sonar-analysis run the SonarQube analysis for this service.
/fix-sonar-issues fix the current SonarQube quality gate failures.
```

## GitHub Copilot

Install each skill folder in a supported skills directory.

Project-level examples:

```text
.github/skills/execute-sonar-analysis/SKILL.md
.github/skills/fix-sonar-issues/SKILL.md
.agents/skills/execute-sonar-analysis/SKILL.md
.agents/skills/fix-sonar-issues/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/execute-sonar-analysis/SKILL.md
~/.copilot/skills/fix-sonar-issues/SKILL.md
```

## Usage Context Checklist

Before invoking either skill, provide or attach:

- Target repository or module (Maven project root, or Node/React project/workspace root; for Mixed repos, specify which module(s)).
- `SONAR_PROJECT_ID`, `SONAR_URL`, and `SONAR_TOKEN` when running `execute-sonar-analysis`.
- SonarQube project key, repository path, and branch/analysis context when running `fix-sonar-issues` (or pre-loaded issue context if analysis results are already available).
- Confirmation that a SonarQube MCP tool or equivalent tooling is configured and accessible for `fix-sonar-issues`.

Expected result: a triggered analysis with a clear pass/fail quality gate status for the detected project family, and — when remediation is needed — a structured fix report grouped by file and rule with validation results appropriate to that project's toolchain.
