---
name: file-io
description: "Use this skill to read or write files when the caller supplies the content directly. Handles write modes create, append, and write, plus read and status. Triggers include: any request shaped as {\"mode\": \"...\", \"path\": \"...\", \"content\": \"...\"}, asking to create a file, append a section to a file, read a file back, or check whether a file exists and how large it is. Designed for callers that already split long content into chunks and send them one at a time — this skill just performs each requested operation. Do NOT use for binary formats such as .docx, .pptx, .xlsx, or .pdf, which have their own skills."
---

# File read / write

## Overview

Perform a single file operation described by a JSON request. The caller decides what
the content is and how it is split; this skill only executes the operation and
reports the result.

All work is done by `scripts/file_io.py`. Do not write files by other means when this
skill applies — the script handles directory creation, newline hygiene, append
separators, path safety, and rollback on failure.

## Request format

```json
{
  "mode": "append",
  "path": "src/.SS_WF/Agent/Analysis/TAW-232_ANALYSIS_PLAN.md",
  "content": "ABCD"
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `mode` | yes | `create`, `write` (alias of create), `append`, `read`, `status` |
| `path` | yes | Relative to `--root` (default: cwd). Parent directories are created as needed. |
| `content` | writes only | The exact text to write. |
| `overwrite` | no | `true` lets `create` replace an existing non-empty file. Default `false`. |
| `separator` | no | `false` appends with no blank line before the chunk. Default `true`. |
| `start_line` / `end_line` | read only | 1-based inclusive slice. |

## How to run it

Pipe the request on stdin — this is the safest form, since content never touches the
shell:

```bash
python scripts/file_io.py --root . <<'JSON'
{"mode":"append","path":"docs/plan.md","content":"## Section 2\nbody"}
JSON
```

Other forms:

```bash
python scripts/file_io.py --request '{"mode":"read","path":"docs/plan.md"}'
python scripts/file_io.py --request-file request.json
```

## Modes

- **create / write** — writes `content` to a new file. Fails if the file already
  exists with content, unless `"overwrite": true`. Use this for the first chunk.
- **append** — adds `content` to the end, creating the file if absent. Use this for
  every chunk after the first. A single blank line is inserted between blocks so
  sections never run together.
- **read** — returns the file's content plus line/byte counts. Optionally slice with
  `start_line` / `end_line` to avoid pulling a huge file into context.
- **status** — existence, line count, and byte count only. Use it to check progress
  without loading content.

## Response

Success prints JSON on stdout with `"ok": true`, the resolved `path`, and
`lines` / `bytes` after the operation. Writes also return `created` and
`bytes_written`; reads return `content`.

Errors print JSON on stderr with `"ok": false` and an `error` message, and exit 1.
Report the `error` text to the caller rather than retrying blindly.

## Rules

- **One request per invocation.** For a multi-chunk document: `create` the first
  chunk, then `append` each subsequent chunk in order.
- **Never re-run `create` mid-sequence** — it is the only mode that can discard
  existing content, and doing so loses every chunk already written.
- **Always pass content via stdin or `--request-file`** when it contains quotes,
  backticks, `$`, or newlines. Inline `--request` is for short requests only.
- **Check `lines` in the response after each write** to confirm the file is growing
  before sending the next chunk.
- Paths must stay inside `--root`; traversal outside it is rejected. Set the
  environment variable `FILE_IO_ALLOW_OUTSIDE_ROOT=1` only when writing outside the
  project root is genuinely intended.

## Failure handling

| Error | Cause | Fix |
|-------|-------|-----|
| `already exists and is not empty` | `create` on a live file | switch to `append`, or set `"overwrite": true` |
| `file not found` | `read` before anything was written | check the path, or use `status` first |
| `path escapes the working root` | `..` or an outside absolute path | correct the path, or set the env var if intended |
| `content is required` | write request missing `content` | resend with the field |
| `request is not valid JSON` | malformed payload | fix the JSON; content with newlines must be properly escaped or sent via `--request-file` |

## Self-test

`python scripts/test_file_io.py` runs the full suite. Run it after any change to
the script.
