---
name: code-review
description: Use when reviewing a GitLab merge request or pull request diff for security vulnerabilities, code quality, and architecture issues, and posting the findings as MR/PR comments. Runs standalone — fetches PR/commit details itself via the gitlab-mcp MCP tool and generates pr-code-context.md when it is not already provided — and optionally grounds the review in jira-context.md when present. Applies to both Java Maven backend microservices/adapter libraries and Node.js/React/TypeScript frontend or backend projects. Triggers include PR review, MR review, code review, merge request review, pull request review, review this diff, security review, code quality review, jira-context.md, pr-code-context.md, pr-code-review-doc.md, post review comments, gitlab-mcp, BLOCKER/ISSUE/SUGGESTION findings, or reviewing new code before merge.
---

# Code Review Skill

Review a merge/pull request's changed code for **security vulnerabilities** and **code quality / architecture issues**, synthesize the findings into a single severity-tagged markdown report, and post that report as comments/notes on the merge request. This skill is **review-only**: it never edits source files or applies fixes. It detects the target project's language/framework family (Java Maven or Node/React) first and loads only the matching review patterns.

This skill is designed to **run standalone**, not only as a chained step after an upstream "Fetch PR Details" agent. When `pr-code-context.md` does not already exist, this skill fetches the PR/MR details, diff, and commit history itself using the `gitlab-mcp` MCP tool and generates `pr-code-context.md` before reviewing.

> **No Human-in-the-Loop:** This skill runs as an autonomous step, whether invoked standalone or inside an agentic PR-review pipeline. It never pauses for approval of a finding, a severity label, or whether to post a comment. Scope resolution, severity classification, and posting are driven by the deterministic rules in this document.

> **Read-only on source code:** This skill only reads the diff/changed files. It never writes to, renames, or edits the files under review. Its only write outputs are `pr-code-context.md` (when it must be generated), the review markdown file (`pr-code-review-doc.md`), and the posted MR/PR comment(s).

---

## STEP -2: Load Implementation Context (Optional — Run First)

Before resolving the diff, check the workspace root for a `jira-context.md` file (or an equivalently named implementation/requirements context file handed off from an upstream step, e.g. a JIRA-fetch agent or the `code-context-retrieval` skill).

```
IF jira-context.md (or equivalent) exists at the workspace root:
  → Read it and extract: the ticket/story intent, acceptance criteria, scope boundaries,
    and any explicitly called-out technical constraints.
  → Use this as additional grounding during the review passes (STEP 2 and STEP 3) to:
    - Flag changes that fall outside the stated scope/acceptance criteria as a [SUGGESTION]
      or [ISSUE] ("scope not covered by the linked requirement") when relevant.
    - Flag missing coverage: an acceptance criterion that the diff does not appear to address
      at all (note this once in the Synthesis step, not as a per-file finding).
    - Prefer the project's own conventions over jira-context.md when they conflict on a
      purely technical/style matter; jira-context.md governs *intent and scope*, not code style.
ELSE:
  → Proceed directly to STEP -1 using only the PR diff itself. Do not block, ask for, or wait
    on a jira-context.md file that was not provided — it is purely optional enrichment.
```

`jira-context.md` is never required. Its absence is normal and must never be treated as a blocker, a missing input, or a reason to skip the review.

---

## STEP -1: Resolve Review Scope

Resolve the diff to review, in this order of precedence:

1. **Pre-generated PR context** — if a `pr-code-context.md` (or an equivalently named PR/diff documentation file) already exists in the workspace or was handed off from an upstream step (e.g., an n8n/agent workflow's `Fetch PR Details` step), use it as the source of truth for changed files and new code. Do not re-fetch the diff or regenerate it if this is present and complete.
2. **Standalone generation via `gitlab-mcp`** — if no pre-generated context exists, this skill operates standalone: discover the GitLab MCP tool (STEP 0 below) and generate `pr-code-context.md` itself (STEP 0.5 below) before reviewing.
3. **Local git diff** — if no GitLab MCP tool is reachable at all (STEP 0 finds nothing usable), fall back to the local repository's diff against the target branch (`git diff <target-branch>...HEAD` or the equivalent for the current checkout) and review that directly, without a generated `pr-code-context.md`.

If none of the three sources yields a usable diff, stop and report the blocker (what was tried) rather than reviewing stale or unrelated code.

### MR/PR Status Guard

Before reviewing, confirm the MR/PR is still open/active (not closed or already merged), when that status is available from context or the MCP tool. If the status is `closed` or `merged`, skip the review and posting steps entirely and report that no review was needed — do not post comments to a closed/merged request.

---

## STEP 0: GitLab Tool Discovery (Run Before Fetching or Posting)

The expected GitLab MCP tool/server name is **`gitlab-mcp`**. Look for it first by that exact name.

1. **Check for a tool/server literally named `gitlab-mcp`** (or namespaced as `gitlab-mcp__<operation>` / `mcp__gitlab-mcp__<operation>`, depending on how the current environment exposes MCP server tools). If found, use its exposed operations directly.
2. **If no tool is registered under the name `gitlab-mcp`**, do not assume GitLab access is unavailable — scan all available tools in the current execution context and find the one actually associated with GitLab (it may be registered under a different label in some environments, for example a workflow-specific name such as `bsd-git-lab-tool`). Match by name/description patterns using the Operation Lookup table below.
3. **Prefer the most specific match** when multiple GitLab-related tool variants exist.
4. **Never fail because the exact name `gitlab-mcp` is missing** — use the closest matching available GitLab tool, or fall back per STEP -1 (local git diff) if truly nothing GitLab-related is available.
5. **Cache the resolved tool/server name** for the remainder of this review run so repeated lookups in later steps do not re-run discovery.

### Operation Lookup (within `gitlab-mcp` or its equivalent)

| Required Operation | Look For in Tool Names/Descriptions |
|---|---|
| Get MR/PR details and status (open/closed/merged) | (`merge_request` or `pull_request` or `mr` or `pr`) + (`get` or `show` or `detail`) |
| Get MR/PR diff / changed files | (`diff` or `changes` or `files`) + (`merge_request` or `pull_request`) |
| **List MR/PR commits** | (`commit`) + (`list` or `get` or `merge_request` or `pull_request`) |
| List/read file content at a given ref | `file` + (`get` or `read` or `raw`) |
| Post a general note/comment on the MR/PR | (`note` or `comment`) + (`create` or `add` or `post`) |
| Post an inline/line-level comment (diff discussion) | (`discussion` or `inline` or `thread`) + (`create` or `add`) |
| List existing notes/comments (for idempotency) | (`note` or `comment` or `discussion`) + (`list` or `search` or `get`) |
| Clone or read repository content | `repo` or `project` + (`clone` or `tree` or `file`) |

### Fallback Strategy

If no tool matches an operation even after discovery:
1. Look for a more general tool that could serve the same purpose (a generic repository/file read tool, or a generic HTTP/API call tool pointed at the GitLab REST API).
2. If fetching is not possible at all, fall back to the local git diff per STEP -1.
3. If posting comments specifically is not possible with any available tool, still produce the review markdown file and clearly report in the Completion Summary that posting was skipped and why — never silently drop the review.

---

## STEP 0.5: Generate `pr-code-context.md` (Standalone Mode Only)

Run this step only when STEP -1 determined that no pre-generated `pr-code-context.md` exists. Skip this step entirely if one was already provided — do not regenerate or overwrite a pre-existing, complete PR context file.

Load [`references/pr-context-generation.md`](references/pr-context-generation.md) for the full procedure. In summary, using the `gitlab-mcp` tool (or its discovered equivalent) resolved in STEP 0:

1. Fetch the **MR/PR details and metadata** (project path, MR/PR IID/number, title, description, author, source/target branch, status) using the project path and PR number supplied in the task/config (e.g., `repo_path`, `pr_no`, `project_key`).
2. Fetch the **MR/PR diff / changed files** (full new/changed code per file).
3. Fetch the **MR/PR commit history** (commit SHAs, messages, and authors for every commit included in the MR/PR) — this is required, not optional, even in standalone mode, since commit messages often carry intent not visible in the diff alone.
4. Assemble all of the above into a single, review-ready `pr-code-context.md` written to the workspace root, containing: PR metadata, the commit list/summary, and the full changed-code content grouped by file name.
5. Proceed to STEP 1 using the freshly generated `pr-code-context.md` as the scope.

If any of steps 1–3 fails (tool unavailable, PR not found, access denied), fall back to the local git diff per STEP -1 rather than producing an incomplete `pr-code-context.md`.

---

## STEP 1: Detect Project Family (Run Before Loading Review References)

Determine which project family the changed files belong to. This selects which `references/<family>/` folder to use in Step 3.

| Signal | Project Family | Reference Folder |
|---|---|---|
| `pom.xml` at the repo/module root, changed files under `src/main/java` (or `src/test/java`) | **Maven (Java)** | `references/maven/` |
| `package.json` at the repo root, changed files as `.js`/`.jsx`/`.ts`/`.tsx` | **Node/React** | `references/node/` |
| Both present (mixed repo) | **Mixed** | Use `references/maven/` for `.java` files and `references/node/` for `.js`/`.jsx`/`.ts`/`.tsx` files, scoped per changed file |

Detection steps:

1. Look for `pom.xml` and `package.json` in the repository root or affected module root.
2. If only one is present, that determines the project family for the whole review.
3. If both are present, classify each changed file independently by its own extension/location — never apply a Java-specific pattern to a `.ts`/`.tsx` file, or vice versa.
4. If detection is ambiguous (e.g., neither marker file is reachable from context), default to a language-neutral review using the generic principles in this file only, and note the detection gap in the Completion Summary.

---

## Reference Files (Lazy Loading)

This skill uses a lazy-loading pattern, split by review dimension and project family. **Load the reference file for a dimension only when there are changed files to review for that dimension and family.** Do not load all reference files upfront.

| Reference | When to Load |
|---|---|
| [`references/pr-context-generation.md`](references/pr-context-generation.md) | Only in standalone mode, when `pr-code-context.md` must be generated (STEP 0.5) |
| [`references/maven/01-security-review.md`](references/maven/01-security-review.md) / [`references/node/01-security-review.md`](references/node/01-security-review.md) | Always, for every changed file in the detected family (Security Review pass) |
| [`references/maven/02-code-quality-architecture.md`](references/maven/02-code-quality-architecture.md) / [`references/node/02-code-quality-architecture.md`](references/node/02-code-quality-architecture.md) | Always, for every changed file in the detected family (Code Quality & Architecture pass) |
| [`references/gitlab-comment-posting.md`](references/gitlab-comment-posting.md) | Whenever the review proceeds to the Posting step (STEP 5) |

For **Mixed** repositories, load both family folders and apply each to only the files matching that family's extensions.

---

## STEP 2: Security Review Pass

For every changed/new file in scope, review it as an **Application Security Engineer** would: look for hardcoded secrets/credentials, injection flaws (SQL/NoSQL/command), XSS, broken authentication/authorization, insecure deserialization, sensitive data exposure (logs, responses, storage), SSRF, insecure randomness/cryptography, and vulnerable new dependencies introduced by the diff.

1. Load the security reference matching the file's detected family (see table above) before judging an unfamiliar pattern.
2. Map each finding to an OWASP Top 10 category where applicable.
3. Classify severity using the Severity Model below.
4. If `jira-context.md` was loaded in STEP -2, note (but do not over-weight) any security-relevant constraint it states (e.g., a requirement to mask a specific field, or a named compliance rule) and check the diff against it.
5. If no security issues are found in the diff, record that explicitly — do not fabricate findings to appear thorough.

---

## STEP 3: Code Quality & Architecture Review Pass

For every changed/new file in scope, review it as a **Senior Software Architect** would: naming conventions, single responsibility, method/class size and complexity, duplication, architectural alignment with the existing layering (e.g., `Controller/Listener -> Service -> ServiceImpl -> adapter/shared-lib client` for Java services, or `component -> hook/service -> API client` for React/Node), performance concerns, error handling, and missing/weak unit test coverage for the changed behavior.

1. Load the code-quality reference matching the file's detected family before judging an unfamiliar pattern.
2. Check only the **changed/added lines and their immediate context** — do not sweep the whole file for unrelated pre-existing issues unless they are directly touched by the diff.
3. Classify severity using the Severity Model below.
4. If `jira-context.md` was loaded in STEP -2, check whether the diff's scope matches the stated acceptance criteria; note any clear mismatch once during synthesis rather than per file.
5. If no quality issues are found, record that explicitly.

---

## Severity Model

Use exactly these three severity tags when writing findings — they match the standard convention expected by downstream automation and reviewers:

| Tag | Meaning | Criteria |
|---|---|---|
| **[BLOCKER]** | Fatal bug or security leak; must not merge as-is | Hardcoded secret/credential, SQL/NoSQL/command injection, XSS via unsanitized rendering, broken authentication/authorization, swallowed exception that hides a failure, blocking call in reactive code, public API/event contract breakage, data loss or correctness bug in the changed logic |
| **[ISSUE]** | Real bug or bad practice that should be fixed before/soon after merge | Missing input validation at a trust boundary, missing error handling for a new failure path, dependency-direction/layering violation, God-class/SRP violation introduced by the diff, missing unit tests for new non-trivial logic, sensitive data logged, duplicated logic (3+ places), performance anti-pattern (N+1 calls, unnecessary blocking I/O, unbounded loops/recursion on request paths), scope diverging from `jira-context.md` acceptance criteria when that file is present |
| **[SUGGESTION]** | Clean-code / style improvement, non-blocking | Naming clarity, minor duplication (same-file), magic values not yet promoted to constants, missing `final`/immutability where locally idiomatic, verbose/awkward conditionals, comment hygiene, test readability |

Use industry-standard static-analysis thresholds as the objective bar when no stricter local/Sonar convention exists in the repo: cyclomatic complexity > 10 is a quality concern worth flagging as `[ISSUE]` (>15 as `[BLOCKER]`-level complexity risk only if it also hides a correctness/security problem), methods > ~40 executable lines, classes > ~500 lines or clearly mixed responsibilities, 4+ parameters, nesting > 3 levels, and 6+ duplicated lines across 2+ locations.

If the repository defines its own thresholds (`sonar-project.properties`, ESLint/ Checkstyle/PMD rulesets already in the repo), those take precedence over the defaults above.

---

## STEP 4: Synthesize the Review

Combine the Security Review and Code Quality & Architecture Review findings into a single, readable Markdown document, written as a **Principal Engineer synthesizing sub-agent review notes** would:

- Group findings by file, then by severity within each file (`[BLOCKER]` first, then `[ISSUE]`, then `[SUGGESTION]`).
- For each finding: file path, line/range (when known), a one-line description of the problem, and a concrete, minimal suggested fix direction (this skill reports the fix; it does not apply it).
- If `jira-context.md` was loaded, include one short note on requirement/scope alignment (covered, partially covered, or diverging) — omit this section entirely if `jira-context.md` was not provided.
- If both review passes found nothing across the whole diff, the entire document is a short, warm approval: **"Looks good to me!"** — do not pad a clean diff with manufactured nitpicks.
- Keep the tone constructive and specific; avoid vague feedback like "improve error handling" without naming the exact gap.

### Output File

- **File name:** `pr-code-review-doc.md` (write to the workspace root, or the location specified by the invoking workflow/handoff context).
- **Format:**

```markdown
# PR Code Review — <project/MR reference if known>

## Summary
<one or two lines: overall verdict, counts per severity, or "Looks good to me!">

## Requirement Alignment
<only included when jira-context.md was present: covered / partially covered / diverging, one or two lines>

## Findings

### <file path>
- [BLOCKER] <description> — <suggested fix>
- [ISSUE] <description> — <suggested fix>
- [SUGGESTION] <description> — <suggested fix>

### <next file path>
...

## Security Review Notes
<short summary from the Security Review pass — or "No security issues found.">

## Code Quality & Architecture Notes
<short summary from the Code Quality & Architecture Review pass>
```

---

## STEP 5: Post Review Comments on the Merge/Pull Request

After writing `pr-code-review-doc.md`, post the review to the MR/PR using the `gitlab-mcp` tool (or its discovered equivalent) resolved in STEP 0. Load [`references/gitlab-comment-posting.md`](references/gitlab-comment-posting.md) for the exact posting conventions (idempotency, note vs. inline discussion, formatting). In summary:

1. Check for an existing review note from a prior run on the same MR/PR (idempotency) before posting, to avoid duplicate comments on re-runs.
2. Post the full `pr-code-review-doc.md` content as a single summary note/comment on the MR/PR when a tool for general notes is available.
3. If the discovered tool also supports inline/line-level discussions and the findings include known line numbers, additionally post `[BLOCKER]`/`[ISSUE]` findings as inline comments on their respective diff lines — `[SUGGESTION]` items can stay in the summary note only.
4. If no posting-capable tool is available, skip posting and clearly state this in the Completion Summary — the review document is still the authoritative output.

Never post partial findings while the synthesis is still in progress — post once, after Step 4 is complete.

---

## Completion Summary

Emit a short, non-blocking summary once scope resolution, both review passes, synthesis, and posting (or the documented reason posting was skipped) are complete:

- **Scope**: MR/PR reference (project path + MR/PR number) and files reviewed, or the fallback source used (local diff) if the GitLab tool was unavailable.
- **Implementation context**: whether `jira-context.md` was found and used, or "not provided — reviewed PR diff only."
- **PR context source**: pre-generated `pr-code-context.md` (reused as-is), newly generated via `gitlab-mcp` (standalone mode), or local git diff fallback.
- **Detected project family**: Maven, Node/React, or Mixed, and which reference folder(s) were used.
- **Findings**: counts by severity (`[BLOCKER]` / `[ISSUE]` / `[SUGGESTION]`), or "Looks good to me!" if none.
- **Review document**: path to `pr-code-review-doc.md`.
- **Posting result**: posted (note/inline), skipped (with reason), or not attempted (MR/PR closed/merged).

This skill always completes and hands control back to the workflow — it never blocks on a human decision.
