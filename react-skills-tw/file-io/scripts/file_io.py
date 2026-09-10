#!/usr/bin/env python3
"""file_io.py - read and write files from a simple JSON request.

The caller sends one JSON object; the script performs it and prints a JSON result.

Write:  {"mode": "append", "path": "docs/plan.md", "content": "..."}
Read:   {"mode": "read",   "path": "docs/plan.md"}

Modes
-----
  create  create the file (or truncate it) and write content
  append  append content to the end, creating the file if needed
  write   alias for create
  read    return the file's content
  status  return metadata only (exists, lines, bytes) - no content

Invocation
----------
  echo '{"mode":"append","path":"a.md","content":"hi"}' | python file_io.py
  python file_io.py --request '{"mode":"read","path":"a.md"}'
  python file_io.py --request-file req.json

Exit codes: 0 ok, 1 error (details in the JSON "error" field on stderr).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

VALID_MODES = {"create", "write", "append", "read", "status"}
MAX_BYTES = 32 * 1024 * 1024  # sanity cap for a single content payload


def out(payload: dict, code: int = 0):
    stream = sys.stdout if code == 0 else sys.stderr
    json.dump(payload, stream, indent=2)
    stream.write("\n")
    sys.exit(code)


def fail(msg: str, **extra):
    out({"ok": False, "error": msg, **extra}, 1)


def load_request(args) -> dict:
    if args.request_file:
        try:
            with open(args.request_file, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except OSError as exc:
            fail(f"cannot read request file: {exc}")
    elif args.request:
        raw = args.request
    else:
        raw = sys.stdin.read()
    if not raw.strip():
        fail("empty request; send a JSON object on stdin or via --request")
    try:
        req = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"request is not valid JSON: {exc}")
    if not isinstance(req, dict):
        fail("request must be a JSON object")
    return req


def resolve(path_value, base: str) -> str:
    if not isinstance(path_value, str) or not path_value.strip():
        fail("'path' is required and must be a non-empty string")
    path = os.path.expanduser(path_value)
    if not os.path.isabs(path):
        path = os.path.join(base, path)
    path = os.path.abspath(path)
    base_abs = os.path.abspath(base)
    # keep writes inside the working root unless the caller opts out
    if os.environ.get("FILE_IO_ALLOW_OUTSIDE_ROOT") != "1":
        if os.path.commonpath([path, base_abs]) != base_abs:
            fail(f"path escapes the working root: {path_value}",
                 root=base_abs)
    return path


def stats(path: str) -> dict:
    if not os.path.exists(path):
        return {"exists": False, "lines": 0, "bytes": 0}
    size = os.path.getsize(path)
    with open(path, "rb") as fh:
        blob = fh.read()
    lines = blob.count(b"\n") + (0 if not blob or blob.endswith(b"\n") else 1)
    return {"exists": True, "lines": lines, "bytes": size}


def do_read(req: dict, path: str):
    if not os.path.exists(path):
        fail("file not found", path=path)
    if os.path.isdir(path):
        fail("path is a directory", path=path)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
    except OSError as exc:
        fail(f"read failed: {exc}", path=path)

    start = req.get("start_line")
    end = req.get("end_line")
    sliced = False
    if start is not None or end is not None:
        lines = content.splitlines(keepends=True)
        s = max(1, int(start or 1)) - 1
        e = int(end) if end is not None else len(lines)
        content = "".join(lines[s:e])
        sliced = True

    info = stats(path)
    out({"ok": True, "mode": "read", "path": path, "content": content,
         "sliced": sliced, **info})


def do_write(req: dict, path: str, mode: str):
    content = req.get("content")
    if content is None:
        fail("'content' is required for write modes", path=path)
    if not isinstance(content, str):
        fail("'content' must be a string", path=path)
    if len(content.encode("utf-8")) > MAX_BYTES:
        fail("content exceeds the size cap; send it as multiple chunks")

    if os.path.isdir(path):
        fail("path is a directory", path=path)

    content = content.replace("\r\n", "\n").replace("\r", "\n")
    if content.startswith("\ufeff"):
        content = content[1:]

    existed = os.path.exists(path)
    before = os.path.getsize(path) if existed else 0

    if mode in ("create", "write"):
        if existed and before > 0 and not req.get("overwrite", False):
            fail("file already exists and is not empty; use mode 'append' to add "
                 "to it, or pass \"overwrite\": true to replace it",
                 path=path, bytes=before)
        open_mode = "w"
    else:  # append
        open_mode = "a"

    payload = content
    # keep exactly one blank line between appended blocks
    if open_mode == "a" and before > 0 and req.get("separator", True):
        with open(path, "rb") as fh:
            fh.seek(max(0, before - 2))
            tail = fh.read().decode("utf-8", errors="ignore")
        if tail.endswith("\n\n"):
            pass
        elif tail.endswith("\n"):
            payload = "\n" + payload
        else:
            payload = "\n\n" + payload
    if not payload.endswith("\n"):
        payload += "\n"

    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, open_mode, encoding="utf-8", newline="") as fh:
            fh.write(payload)
            fh.flush()
            os.fsync(fh.fileno())
    except OSError as exc:
        # roll the file back so a failed write never leaves a partial chunk
        try:
            if open_mode == "a" and existed:
                with open(path, "r+b") as fh:
                    fh.truncate(before)
            elif not existed and os.path.exists(path):
                os.remove(path)
        except OSError:
            pass
        fail(f"write failed and was rolled back: {exc}", path=path)

    info = stats(path)
    out({"ok": True, "mode": mode, "path": path, "created": not existed,
         "bytes_written": len(payload.encode("utf-8")), **info})


def main(argv=None):
    p = argparse.ArgumentParser(description="Read/write files from a JSON request.")
    p.add_argument("--request", help="the JSON request as a string")
    p.add_argument("--request-file", help="file containing the JSON request")
    p.add_argument("--root", default=os.getcwd(),
                   help="base directory for relative paths (default: cwd)")
    args = p.parse_args(argv)

    req = load_request(args)
    mode = req.get("mode")
    if mode is None:
        fail("'mode' is required", valid_modes=sorted(VALID_MODES))
    if not isinstance(mode, str) or mode.lower() not in VALID_MODES:
        fail(f"unknown mode: {mode!r}", valid_modes=sorted(VALID_MODES))
    mode = mode.lower()

    path = resolve(req.get("path"), args.root)

    if mode == "read":
        do_read(req, path)
    elif mode == "status":
        out({"ok": True, "mode": "status", "path": path, **stats(path)})
    else:
        do_write(req, path, mode)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        fail("interrupted")
    except BrokenPipeError:
        sys.exit(0)
