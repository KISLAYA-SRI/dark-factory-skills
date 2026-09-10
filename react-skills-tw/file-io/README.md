# file-io

A minimal Claude skill for reading and writing files from a JSON request. Built for
agents that already chunk their own content and just need each chunk written.

```
file-io/
├── SKILL.md                  # the skill: frontmatter + agent instructions
├── README.md                 # this file
└── scripts/
    ├── file_io.py            # the worker (stdlib only, no dependencies)
    └── test_file_io.py       # 39-case self-test suite
```

## Install

Copy the `file-io/` folder into your skills directory (e.g. `~/.claude/skills/`).
No dependencies — Python 3.8+ standard library only.

```bash
python file-io/scripts/test_file_io.py   # verify
```

## Request shape

```json
{
  "mode": "append",
  "path": "src/.SS_WF/Agent/Analysis/TAW-232_ANALYSIS_PLAN.md",
  "content": "ABCD"
}
```

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `mode` | yes | — | `create` \| `write` \| `append` \| `read` \| `status` |
| `path` | yes | — | relative to `--root`; parent dirs auto-created |
| `content` | writes | — | exact text to write |
| `overwrite` | no | `false` | allow `create` to replace a non-empty file |
| `separator` | no | `true` | insert one blank line before an appended block |
| `start_line`, `end_line` | read | — | 1-based inclusive slice |

## Usage

```bash
S=scripts/file_io.py

# first chunk
python $S --root . <<'JSON'
{"mode":"create","path":"docs/plan.md","content":"# Plan\n"}
JSON

# subsequent chunks
python $S --root . <<'JSON'
{"mode":"append","path":"docs/plan.md","content":"## Scope\nABCD"}
JSON

# read back (optionally sliced)
python $S --request '{"mode":"read","path":"docs/plan.md","start_line":1,"end_line":40}'

# cheap progress check, no content
python $S --request '{"mode":"status","path":"docs/plan.md"}'
```

Three invocation styles: stdin (safest for content with quotes/newlines),
`--request '<json>'`, and `--request-file req.json`.

## Response

```json
{ "ok": true, "mode": "append", "path": "/abs/docs/plan.md",
  "created": false, "bytes_written": 15, "exists": true, "lines": 4, "bytes": 32 }
```

Errors go to stderr as `{"ok": false, "error": "..."}` with exit code 1.

## Behaviour worth knowing

- **`create` won't clobber.** A `create` against an existing non-empty file fails
  with a message pointing at `append`; `"overwrite": true` is the explicit opt-in.
  This is what stops a retried first chunk from wiping a half-built document.
- **`append` creates the file if missing**, so an interrupted sequence can resume.
- **Clean joins.** Exactly one blank line between appended blocks — never merged
  sections, never runaway blank lines. Disable with `"separator": false`.
- **Content is written verbatim.** Backticks, `$`, quotes, and emoji survive because
  content arrives as JSON, not as shell arguments. CRLF/CR are normalised to LF and
  a stray BOM is stripped.
- **Atomic-ish writes.** Content is fsynced, and a failed write truncates back to the
  pre-write byte offset so no partial chunk is left behind.
- **Path safety.** Paths resolve inside `--root`; `../` traversal and outside
  absolute paths are rejected. Override with `FILE_IO_ALLOW_OUTSIDE_ROOT=1`.
- **Validation.** Unknown/missing mode, missing path, missing or non-string content,
  malformed JSON, non-object requests, directory targets, and payloads over 32 MB all
  fail with a clear message rather than a stack trace.

## Testing

```bash
python scripts/test_file_io.py
```

39 cases covering create/append/read/status, overwrite protection, separators,
encoding integrity, request validation, path traversal, all three invocation styles,
and a 25-chunk / 1,000-line document assembly. Runs in a temp directory, cleans up
after itself, exits non-zero on any failure.
