# Generating `pr-code-context.md` Standalone (via `gitlab-mcp`)

This reference applies when `code-review` is invoked **standalone** (no upstream "Fetch PR Details" step has already produced `pr-code-context.md`). It covers how to fetch everything needed directly from GitLab using the `gitlab-mcp` MCP tool (or its discovered equivalent, resolved in `SKILL.md` STEP 0) and assemble it into a review-ready `pr-code-context.md`.

Only run this procedure when `SKILL.md` STEP -1 has determined that no usable `pr-code-context.md` already exists. Never regenerate or overwrite a pre-existing, complete one.

## Required Inputs

Resolve these from the task/config context before calling any tool (for example, from a `config_json`-style input: `repo_path`, `pr_no`, `project_key`):

| Input | Description |
|---|---|
| `project_path` | GitLab project path or ID (e.g., `ksa-backend/engagement/cat-3/ciam-engagement`) |
| `mr_iid` / `pr_no` | The merge/pull request IID or number |
| `project_key` (optional) | Jira/project key, if supplied — not used for the GitLab fetch itself, but worth carrying into the generated context header for traceability |

If `project_path` or the MR/PR number is missing from context entirely, stop and report the blocker rather than guessing a target.

## Fetch Sequence

Using the `gitlab-mcp` tool (or its discovered equivalent):

### 1. MR/PR Details and Status

Call the operation matching "get MR/PR details" (see the Operation Lookup table in `SKILL.md` STEP 0) with `project_path` + `mr_iid`. Capture:

- Title, description
- Author
- Source branch, target branch
- State (`opened`, `closed`, `merged`)
- Web URL (for traceability in the generated doc)

Apply the **MR/PR Status Guard** from `SKILL.md` STEP -1 here: if state is `closed` or `merged`, stop this generation step and report that no review is needed — do not continue to fetch the diff/commits for a closed/merged request.

### 2. MR/PR Diff / Changed Files

Call the operation matching "get MR/PR diff / changed files" with `project_path` + `mr_iid`. Capture, per changed file:

- File path
- Change type (added / modified / deleted / renamed)
- The full diff hunk(s) or, when the tool supports it, the complete new file content for added/modified files

If the tool returns only unified diff hunks (not full file content) and the review needs broader context around a hunk, use the "read file content at a given ref" operation to pull additional surrounding lines from the MR's head SHA — but do not pull entire unrelated files beyond what's needed to understand the changed hunk's context.

### 3. MR/PR Commit History (Required)

Call the operation matching "list MR/PR commits" with `project_path` + `mr_iid`. Capture, per commit:

- Short SHA
- Commit message (first line / summary at minimum; full message if concise)
- Author and timestamp

Commit history is required even in standalone mode — commit messages frequently state intent, scope, or known trade-offs ("WIP: temporary hardcoded flag for testing", "fix: revert previous validation change") that the diff alone does not convey, and that materially affects severity judgment in STEP 2/STEP 3 of `SKILL.md`.

## Assembling `pr-code-context.md`

Write a single Markdown file to the workspace root with this structure:

```markdown
# PR Code Context — <project_path> !<mr_iid>

## Metadata
- Project: <project_path>
- MR/PR: !<mr_iid>
- Title: <title>
- Author: <author>
- Source branch -> Target branch: <source> -> <target>
- Status: <opened|closed|merged>
- Project Key: <project_key, if supplied>
- URL: <web_url, if available>

## Commits
- `<short_sha>` <commit message summary> (<author>, <date>)
- `<short_sha>` <commit message summary> (<author>, <date>)
...

## Changed Files

### <file path 1> (<added|modified|deleted|renamed>)
```<language>
<new/changed code content for this file>
```

### <file path 2> (<added|modified|deleted|renamed>)
```<language>
<new/changed code content for this file>
```
...
```

Notes on assembly:

- Order changed files in a stable, predictable order (e.g., as returned by the diff tool, or alphabetically if the tool does not guarantee order).
- For deleted files, list the path and change type but omit a content block (there is nothing new to review).
- For renamed files with no content change, note the rename and skip a content block; if a rename also changed content, include the new content.
- Keep the file self-contained — this document is the sole input to `SKILL.md` STEP 1 onward, so it must include everything needed to detect the project family (file extensions/paths) and perform both review passes (actual changed code, not just file names).

## Error Handling

- If the "get MR/PR details" call fails (PR not found, access denied, tool error), do not proceed to diff/commit fetching — fall back to the local git diff per `SKILL.md` STEP -1 and note the failure reason in the Completion Summary.
- If MR/PR details succeed but the diff fetch fails, still generate `pr-code-context.md` with the Metadata and Commits sections populated, and note in the Changed Files section that the diff could not be retrieved — then fall back to the local git diff for the actual review content if one is reachable.
- If the commit list fetch fails but details and diff succeed, proceed without the Commits section rather than blocking the whole review — note the gap in the Completion Summary.
