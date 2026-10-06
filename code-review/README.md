# Code Review

`code-review` is an agent skill for reviewing a GitLab merge request (MR) or pull request (PR) diff for **security vulnerabilities** and **code quality / architecture issues**, synthesizing the findings into a single severity-tagged Markdown report, and posting that report as comments on the MR/PR. It supports both **Java Maven backend microservices/adapter libraries** and **Node.js/React/TypeScript frontend or backend projects**, detecting the project family first and loading only the matching review patterns.

This skill is built to **run standalone**: it is not dependent on an upstream "Fetch PR Details" step. If `pr-code-context.md` is not already present, the skill fetches the MR/PR details, diff, and full commit history itself using the **`gitlab-mcp`** MCP tool and generates `pr-code-context.md` before reviewing. It can also optionally ground its review in a `jira-context.md` file (implementation intent, acceptance criteria) when one is present at the workspace root, but never requires it.

Use this skill when the task is to review new/changed code before merge — whether invoked standalone against a bare repo path + MR/PR number, chained after a `Fetch PR Details`-style step that already produced `pr-code-context.md`, or run as the reviewer stage of an automated PR-review pipeline (e.g., an n8n/agent workflow that fetches a GitLab MR, documents the diff, and expects a review back on the MR).

**No human-in-the-loop:** this skill is designed to run unattended, standalone or as a step in an agentic pipeline. It never pauses for approval of a finding, a severity label, or whether to post a comment. Scope resolution, severity classification, and posting are all driven by the deterministic rules in `SKILL.md`.

**Review-only, no fixes:** this skill never edits source files. Its only write outputs are `pr-code-context.md` (when it must generate one itself), the review Markdown file (`pr-code-review-doc.md`), and the posted MR/PR comment(s). Use `fix-sonar-issues` or `clean-code-architecture` for autonomous remediation of findings this skill reports.

## Applies To

- Reviewing a GitLab merge request diff for security vulnerabilities: hardcoded secrets, SQL/NoSQL injection, XSS, broken authentication/authorization, SSRF, insecure crypto, sensitive data exposure, vulnerable new dependencies.
- Reviewing a diff for code quality and architecture issues: naming, SRP, method/class size and complexity, duplication, dependency-direction/layering violations, missing error handling, reactive-correctness issues, React-specific correctness (hooks, state mutation), and missing unit test coverage for new logic.
- Synthesizing security + quality findings into one `[BLOCKER]` / `[ISSUE]` / `[SUGGESTION]` severity-tagged Markdown review.
- Posting the review as a summary note (and optionally inline comments) on the GitLab merge request via the `gitlab-mcp` MCP tool (or its discovered equivalent).
- Running **standalone**: fetching the MR/PR details, diff, and commit history itself via `gitlab-mcp` and generating `pr-code-context.md` when no upstream step has already produced one.
- Running as the reviewer step in an automated PR-review workflow, consuming a pre-generated `pr-code-context.md` diff-documentation file when one is handed off from an upstream step.
- Grounding the review in a `jira-context.md` implementation/requirements file when present, to flag scope mismatches against stated acceptance criteria.

## Project Type Detection

Before reviewing, the agent detects the project family of the changed files:

| Signal | Project Family | Reference Folder |
|---|---|---|
| `pom.xml` present, changed files under `src/main/java` | Maven (Java) | `references/maven/` |
| `package.json` present, changed files as `.js`/`.jsx`/`.ts`/`.tsx` | Node/React | `references/node/` |
| Both present | Mixed | Both, matched per changed file's own language |

## Context & Scope Resolution Order

0. **Optional implementation context** — if `jira-context.md` exists at the workspace root, it is read first and used to ground the review in the original intent/acceptance criteria (scope-mismatch findings, requirement alignment note). This is pure enrichment: its absence never blocks or changes the rest of the flow.
1. **Pre-generated PR context** — an existing `pr-code-context.md` (or equivalent diff-documentation handoff) is used as-is; the skill does not re-fetch or regenerate the diff.
2. **Standalone generation via `gitlab-mcp`** — if no pre-generated context exists, the skill fetches the MR/PR details, diff, and full commit history itself using the `gitlab-mcp` MCP tool (or its discovered equivalent) and generates `pr-code-context.md` before reviewing.
3. **Local git diff** — falls back to `git diff` against the target branch if no GitLab MCP tool is reachable at all.

The agent also checks the MR/PR status: if it is already closed/merged, the review and posting steps (and context generation) are skipped entirely.

## GitLab Tool Resolution (`gitlab-mcp`)

The expected GitLab MCP tool/server name is **`gitlab-mcp`**. The skill looks for a tool/server registered under that exact name first, for every GitLab operation it needs: fetching MR/PR details, diff, and commits, and posting comments.

If no tool is registered under the name `gitlab-mcp` in the current execution context, the skill does not give up on GitLab access — it falls back to a **generic tool discovery approach** (GitLab MCP tools are observed under varying names across environments, e.g. a tool labeled `bsd-git-lab-tool` in one workflow):

1. Scans all available tools in the current execution context.
2. Matches each required operation (get MR/PR details, get diff, list commits, post note, post inline comment, list existing comments) to the best-available tool by name/description pattern.
3. Prefers the most specific matching tool when multiple variants exist.
4. Never fails due to a missing exact tool name — falls back per the Context & Scope Resolution Order, and reports clearly if fetching or posting isn't possible.

## Reference Structure

```text
code-review/references/
  pr-context-generation.md        — standalone pr-code-context.md generation via gitlab-mcp (details, diff, commits)
  gitlab-comment-posting.md       — language-agnostic posting conventions (idempotency, inline vs. summary note, redaction)
  maven/
    01-security-review.md         — Java/Maven/Spring Boot security review patterns (OWASP mapping, examples)
    02-code-quality-architecture.md — Java/Maven/Spring Boot quality & layering review patterns
  node/
    01-security-review.md         — Node.js/React/TypeScript security review patterns (OWASP mapping, examples)
    02-code-quality-architecture.md — Node.js/React/TypeScript quality & architecture review patterns
```

The skill uses a **lazy-loading pattern**: `pr-context-generation.md` is only loaded in standalone mode when `pr-code-context.md` must be generated; the family-specific review references are loaded based on the detected project family; and the GitLab posting reference is only loaded when the review reaches the posting step.

## Severity Model

| Tag | Meaning |
|---|---|
| `[BLOCKER]` | Fatal bug or security leak — must not merge as-is (hardcoded secret, injection, broken auth, swallowed exception, blocking call in reactive code, contract breakage) |
| `[ISSUE]` | Real bug or bad practice to fix before/soon after merge (missing validation, layering violation, missing tests for new logic, sensitive data logged, duplicated logic) |
| `[SUGGESTION]` | Clean-code/style improvement, non-blocking (naming, magic values, comment hygiene) |

If no findings exist in either review pass, the output is a short, warm **"Looks good to me!"** approval rather than a padded report.

## Input

The skill expects **one of the following**, and separately, optionally picks up `jira-context.md` if present regardless of which mode applies:

### Mode A — Standalone (no pre-generated context; the primary, default mode)

Given just a repo path and MR/PR number (and, if available, a project key), the skill:
1. Confirms the MR/PR is open (skips if closed/merged) using `gitlab-mcp`.
2. Fetches MR/PR details, the diff/changed files, and the full commit history via `gitlab-mcp` (or its discovered equivalent).
3. Generates `pr-code-context.md` from that fetched data.
4. Detects project family, runs both review passes (optionally informed by `jira-context.md`), synthesizes, and posts the review via `gitlab-mcp`.

### Mode B — Chained After PR-Context Fetch (typical in automated pipelines)

A `pr-code-context.md` file already exists (produced by an upstream step such as a `Fetch PR Details` agent). The skill:
1. Reads `pr-code-context.md` as the diff source — does not re-fetch or regenerate it.
2. Detects project family from the listed changed files.
3. Runs the security and quality review passes.
4. Synthesizes `pr-code-review-doc.md`.
5. Posts the review to the MR/PR via `gitlab-mcp` (or its discovered equivalent).

### Mode C — Local Diff Fallback

With no GitLab tool reachable and no pre-generated context, the skill reviews the local `git diff` against the target branch and still produces `pr-code-review-doc.md`; posting is skipped and reported as such.

## How to Invoke

```text
Review the merge request at [repo_path], MR !<number>, for security and code quality issues, and post the review as comments.
```

```text
Use gitlab-mcp to fetch MR !<number> in [repo_path], generate pr-code-context.md, review it, and post the findings to the merge request.
```

```text
Use pr-code-context.md to review the new code and post findings to the GitLab merge request.
```

```text
Use jira-context.md and pr-code-context.md together to review this PR for security, quality, and requirement alignment, then post the review.
```

## Expected Output

| Output | Description |
|---|---|
| `pr-code-context.md` | Generated automatically in standalone mode (Mode A) via `gitlab-mcp`: MR/PR metadata, commit history, and full changed-code content. Not produced when an upstream context file was reused (Mode B) or when falling back to a local diff (Mode C). |
| `pr-code-review-doc.md` | Synthesized Markdown review, findings grouped by file then severity, or a "Looks good to me!" approval; includes a Requirement Alignment note when `jira-context.md` was used |
| MR/PR comment(s) | The same review posted as a summary note, with optional inline comments for `[BLOCKER]`/`[ISSUE]` findings on known lines |
| Completion Summary | Scope reviewed, whether `jira-context.md` was used, PR context source (generated / reused / local fallback), detected project family, finding counts by severity, and posting result (posted / skipped with reason / not attempted) |

## Relationship to Other Skills

- **Upstream (optional)**: a `Fetch PR Details`-style agent/skill that pulls the MR/PR diff and produces `pr-code-context.md`, or a JIRA-fetch step that produces `jira-context.md`, may run before this skill — but neither is required. This skill fetches the PR context itself via `gitlab-mcp` when no upstream step has already done so.
- **`fix-sonar-issues`**: use for SonarQube-reported quality-gate remediation specifically; this skill reviews the PR diff directly rather than fetching from a SonarQube server.
- **`clean-code-architecture`**: use for autonomous refactoring of Java clean-code/architecture issues; this skill reports the same class of architecture findings but does not edit code.
- **`code-context-retrieval`**: use if the review needs external codebase context (e.g., an adapter/shared-library contract) not present in the local diff, beyond what `jira-context.md` provides.

## When Not To Use

Do not use this skill to implement fixes (`fix-sonar-issues`, `clean-code-architecture`, or the relevant `generate-*-code` skill), to trigger a SonarQube scan (`execute-sonar-analysis`), or to run/validate tests (`execute-unit-tests`, `validate-project-compile`). Use this skill specifically for reviewing a diff and posting MR/PR feedback.

See [SKILL.md](./SKILL.md) for the full execution rules.
