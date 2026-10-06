# Posting Review Comments to GitLab (Language-Agnostic)

This reference applies regardless of the detected project family (Maven or Node/React). It covers how to post the synthesized `pr-code-review-doc.md` back to the merge request using the `gitlab-mcp` MCP tool (or its discovered equivalent, if no tool is registered under that exact name) resolved in SKILL.md's STEP 0.

## Idempotency — Avoid Duplicate Comments

Before posting, use the discovered "list existing notes/comments" tool (if available) to check whether a prior automated review comment already exists on this MR/PR from this same skill (look for a comment containing the `# PR Code Review` heading or a recognizable marker such as `<!-- code-review-skill -->`).

- If a prior automated review comment exists and this run is re-reviewing the **same** diff/commit, do not post a duplicate — either skip posting or update/replace the existing note if the tool supports editing.
- If this run reviews a **new** push/commit on the same MR/PR, post a new comment (do not overwrite history) so reviewers can see the review evolve with the PR.

Add a hidden marker to the posted comment so future runs can recognize it:

```markdown
<!-- code-review-skill -->
# PR Code Review — <project/MR reference>
...
```

## Posting the Summary Note

Use the discovered "post a general note/comment" tool (via `gitlab-mcp` or its equivalent) with:
- The target project path and MR/PR IID/number (from the resolved scope in SKILL.md STEP -1, or from the metadata captured during STEP 0.5 if `pr-code-context.md` was generated standalone).
- The full Markdown body of `pr-code-review-doc.md` (or a reference to it, if the tool only accepts a short body — in that case, post the `## Summary` section plus a note that the full report is available as `pr-code-review-doc.md` in the pipeline artifacts).

## Posting Inline/Line-Level Comments (Optional, When Supported)

If the discovered tool supports inline diff discussions and a finding has a known file + line number:

1. Post `[BLOCKER]` and `[ISSUE]` findings as inline comments anchored to the exact changed line, using the finding's one-line description and suggested fix.
2. Do not post `[SUGGESTION]`-level findings inline by default (keep inline threads focused on things that matter for merge decisions); they remain in the summary note only.
3. If the tool requires diff position metadata (old/new line number, SHA) that is not available from the resolved context, fall back to the summary note for that finding rather than failing the whole posting step.

## When Posting Is Not Possible

If no tool in the current execution context supports posting notes or comments on the MR/PR:

- Do not fail the skill.
- Clearly report in the Completion Summary that the review was completed but **not posted**, and state the reason (no matching tool discovered, insufficient permissions, or the MR/PR is closed/merged).
- The `pr-code-review-doc.md` file remains the authoritative output for a human or a downstream step to pick up.

## Formatting Notes

- Keep the posted comment in GitLab-flavored Markdown (headings, bold severity tags, fenced code blocks for suggested fixes).
- Do not include secrets, tokens, or full sensitive payloads in the posted comment even when quoting a `[BLOCKER]` finding about a hardcoded secret — redact the actual secret value (e.g., `glpat-***redacted***`) and describe the issue instead of echoing the real value back into a public MR thread.
