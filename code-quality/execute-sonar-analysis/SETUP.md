# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact — including the `references/` subfolder and the `scripts/execute-sonar.sh` script — and make sure `SKILL.md` remains at the root of the skill folder.

After installing the skill in any of the locations below, ensure `scripts/execute-sonar.sh` keeps its executable bit (`chmod +x scripts/execute-sonar.sh`) if your install/copy mechanism does not preserve file permissions.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/execute-sonar-analysis/SKILL.md
<repo>/.agent/skills/execute-sonar-analysis/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/execute-sonar-analysis/SKILL.md
~/.agent/skills/execute-sonar-analysis/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompts:

```text
Use the execute-sonar-analysis skill in Agent mode to run the SonarQube analysis for this Maven project and report the quality gate result.
```

```text
Use the execute-sonar-analysis skill in Agent mode to run the SonarQube scan for this React app and report the quality gate result.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompts:

```text
Use the execute-sonar-analysis skill to run mvn verify sonar:sonar for this repository against project key SONAR_PROJECT_ID and report the quality gate status.
```

```text
Use the execute-sonar-analysis skill to run the sonar-scanner for this Node/React project against project key SONAR_PROJECT_ID and report the quality gate status.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use execute-sonar-analysis for this run.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/execute-sonar-analysis/SKILL.md
.claude/skills/execute-sonar-analysis/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/execute-sonar-analysis run the SonarQube analysis for this microservice and report pass/fail.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/execute-sonar-analysis/SKILL.md
.claude/skills/execute-sonar-analysis/SKILL.md
.agents/skills/execute-sonar-analysis/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/execute-sonar-analysis/SKILL.md
~/.agents/skills/execute-sonar-analysis/SKILL.md
```

Example prompt:

```text
Use the execute-sonar-analysis skill to trigger a SonarQube scan for this project using the provided SONAR_PROJECT_ID, SONAR_URL, and SONAR_TOKEN, and tell me if the quality gate passed.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- `SONAR_PROJECT_ID` — the SonarQube project key.
- `SONAR_URL` — the SonarQube server base URL.
- `SONAR_TOKEN` — the authentication token used to publish analysis results.
- Target repository or module (Maven root POM path or module path, or the npm/yarn/pnpm workspace/package root for Node/React projects).
- Confirmation that the project currently builds/compiles, since the analysis command runs a full build/verify (Maven) or relies on the project's existing lint/build/test setup (Node/React) before publishing.
- For Mixed repositories, which module(s) to analyze.

Expected result: the detected project family, which Node/React scanner resolution path was used (if applicable), the exact analysis command run (token masked), the build/scan outcome, and the SonarQube quality gate status, with a handoff recommendation to `fix-sonar-issues` if the quality gate failed.
