# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact, including the `references/` subfolder (`references/pr-context-generation.md`, `references/gitlab-comment-posting.md`, `references/maven/`, `references/node/`), and make sure `SKILL.md` remains at the root of the skill folder.

This skill is designed to run **standalone**: it fetches MR/PR details, diff, and commit history itself via the `gitlab-mcp` MCP tool when `pr-code-context.md` is not already present, so no upstream "Fetch PR Details" step is required. Ensure a `gitlab-mcp` MCP server (or an equivalent GitLab MCP tool) is configured and reachable in the environment for standalone fetching and comment posting to work.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/code-review/SKILL.md
<repo>/.agent/skills/code-review/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/code-review/SKILL.md
~/.agent/skills/code-review/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt:

```text
Use the code-review skill in Agent mode to fetch MR !73 in ksa-backend/engagement/cat-3/ciam-engagement via gitlab-mcp, review it for security and code quality issues, then post the review as comments.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompt:

```text
Use the code-review skill to review MR !73 in ksa-backend/engagement/cat-3/ciam-engagement. No pr-code-context.md exists yet, so fetch it via gitlab-mcp first, then post a severity-tagged review to the merge request.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use code-review for this merge request.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/code-review/SKILL.md
.claude/skills/code-review/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/code-review review the changed controller, service, and adapter classes in this diff for security and architecture issues.
```

```text
/code-review use jira-context.md for requirement context and gitlab-mcp to fetch MR !73, then post the review.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/code-review/SKILL.md
.claude/skills/code-review/SKILL.md
.agents/skills/code-review/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/code-review/SKILL.md
~/.agents/skills/code-review/SKILL.md
```

Example prompt:

```text
Use the code-review skill to run the standard security and code-quality review against the files changed in this pull request and post the findings as PR comments.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- The repository path and MR/PR number (or project key) — required if `pr-code-context.md` does not already exist, so the skill can fetch and generate it itself via `gitlab-mcp`.
- A pre-generated `pr-code-context.md` (or equivalent diff-documentation handoff), if an upstream step already produced one — this lets the skill skip fetching/generating it.
- A `jira-context.md` file at the workspace root, if implementation intent/acceptance criteria should ground the review — this is optional and the skill proceeds normally without it.
- Confirmation that a `gitlab-mcp` MCP server (or an equivalent GitLab MCP tool, discoverable at runtime) is configured and accessible, both for standalone fetching of PR details/diff/commits and for posting comments back to the MR/PR.
- Any project-specific static-analysis thresholds (`sonar-project.properties`, ESLint/Checkstyle/PMD rulesets) that should take precedence over the default severity thresholds.

Expected result: when run standalone, a generated `pr-code-context.md` (MR/PR metadata, commits, changed code) plus a `pr-code-review-doc.md` file with findings grouped by file and severity (`[BLOCKER]`/`[ISSUE]`/`[SUGGESTION]`, or "Looks good to me!"), posted as a comment on the merge request when `gitlab-mcp` (or its discovered equivalent) supports posting, plus a short completion summary covering scope, whether `jira-context.md` was used, PR context source, detected project family, finding counts, and posting result. This skill runs autonomously with no human-in-the-loop gate and never edits source files.
