#!/usr/bin/env python3
"""Tests for file_io.py. Run: python scripts/test_file_io.py"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "file_io.py")
PASSED, FAILED = [], []


def call(req, root, raw=None):
    payload = raw if raw is not None else json.dumps(req)
    r = subprocess.run([sys.executable, SCRIPT, "--root", root],
                       input=payload, capture_output=True, text=True)
    body = r.stdout or r.stderr
    try:
        js = json.loads(body)
    except json.JSONDecodeError:
        js = {"ok": False, "error": f"non-json output: {body[:200]}"}
    return r.returncode, js


def check(name, cond, detail=""):
    (PASSED if cond else FAILED).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" +
          (f"  -- {detail}" if not cond and detail else ""))


def main():
    root = tempfile.mkdtemp(prefix="fileio-")
    rel = "src/.SS_WF/Agent/Analysis/TAW-232_ANALYSIS_PLAN.md"
    full = os.path.join(root, rel)

    print("== write: create ==")
    rc, js = call({"mode": "create", "path": rel, "content": "# Analysis Plan\n"}, root)
    check("create writes file", rc == 0 and js["ok"] and os.path.exists(full), js)
    check("nested dirs auto-created", os.path.isdir(os.path.dirname(full)))
    check("create reports created=True", js.get("created") is True)

    print("== write: append ==")
    rc, js = call({"mode": "append", "path": rel, "content": "## Scope\nABCD"}, root)
    body = open(full, encoding="utf-8").read()
    check("append adds content", rc == 0 and "ABCD" in body, js)
    check("separator inserted", "# Analysis Plan\n\n## Scope" in body, repr(body))
    check("no triple newline", "\n\n\n" not in body, repr(body))
    check("line count reported", js["lines"] == len(body.splitlines()), js)

    rc, js = call({"mode": "append", "path": rel, "content": "X",
                   "separator": False}, root)
    check("separator:false suppresses blank line",
          "ABCD\nX" in open(full, encoding="utf-8").read())

    print("== write: overwrite protection ==")
    rc, js = call({"mode": "create", "path": rel, "content": "WIPED"}, root)
    check("create refuses existing file",
          rc == 1 and not js["ok"] and "WIPED" not in open(full, encoding="utf-8").read())
    check("error suggests append", "append" in js["error"].lower(), js["error"])
    rc, js = call({"mode": "create", "path": rel, "content": "NEW",
                   "overwrite": True}, root)
    check("overwrite:true replaces file",
          rc == 0 and open(full, encoding="utf-8").read().strip() == "NEW")

    print("== read ==")
    call({"mode": "create", "path": "r.md", "content": "l1\nl2\nl3\nl4\nl5",
          "overwrite": True}, root)
    rc, js = call({"mode": "read", "path": "r.md"}, root)
    check("read returns content", rc == 0 and js["content"] == "l1\nl2\nl3\nl4\nl5\n", js)
    check("read returns line count", js["lines"] == 5, js)
    rc, js = call({"mode": "read", "path": "r.md", "start_line": 2, "end_line": 4}, root)
    check("read slices lines", js["content"] == "l2\nl3\nl4\n" and js["sliced"], js)
    rc, js = call({"mode": "read", "path": "missing.md"}, root)
    check("read on missing file errors", rc == 1 and "not found" in js["error"])
    rc, js = call({"mode": "read", "path": "."}, root)
    check("read on directory errors", rc == 1)

    print("== status ==")
    rc, js = call({"mode": "status", "path": "r.md"}, root)
    check("status reports metadata", rc == 0 and js["exists"] and js["lines"] == 5, js)
    rc, js = call({"mode": "status", "path": "ghost.md"}, root)
    check("status on missing file is graceful", rc == 0 and js["exists"] is False, js)

    print("== append creates when missing ==")
    rc, js = call({"mode": "append", "path": "new/deep.md", "content": "first"}, root)
    check("append creates missing file",
          rc == 0 and open(os.path.join(root, "new/deep.md"), encoding="utf-8").read()
          == "first\n", js)

    print("== content integrity ==")
    nasty = "`tick` $VAR \"q\" 's' \\ | & ; <> \u00e9\u4e2d\u6587 \U0001f600"
    call({"mode": "create", "path": "n.md", "content": nasty, "overwrite": True}, root)
    check("shell metachars + unicode preserved",
          nasty in open(os.path.join(root, "n.md"), encoding="utf-8").read())
    call({"mode": "create", "path": "c.md", "content": "a\r\nb\rc",
          "overwrite": True}, root)
    check("CRLF/CR normalised",
          open(os.path.join(root, "c.md"), "rb").read() == b"a\nb\nc\n")
    call({"mode": "create", "path": "b.md", "content": "\ufeffhdr",
          "overwrite": True}, root)
    check("BOM stripped",
          not open(os.path.join(root, "b.md"), encoding="utf-8").read().startswith("\ufeff"))
    call({"mode": "create", "path": "e.md", "content": "", "overwrite": True}, root)
    rc, js = call({"mode": "read", "path": "e.md"}, root)
    check("empty content allowed", rc == 0, js)

    print("== validation ==")
    rc, js = call({"mode": "bogus", "path": "x.md", "content": "y"}, root)
    check("unknown mode rejected", rc == 1 and "valid_modes" in js)
    rc, js = call({"path": "x.md", "content": "y"}, root)
    check("missing mode rejected", rc == 1 and "mode" in js["error"])
    rc, js = call({"mode": "append", "content": "y"}, root)
    check("missing path rejected", rc == 1 and "path" in js["error"])
    rc, js = call({"mode": "append", "path": "x.md"}, root)
    check("missing content rejected", rc == 1 and "content" in js["error"])
    rc, js = call({"mode": "append", "path": "x.md", "content": 42}, root)
    check("non-string content rejected", rc == 1)
    rc, js = call(None, root, raw="{not json")
    check("invalid JSON rejected", rc == 1 and "JSON" in js["error"])
    rc, js = call(None, root, raw="   ")
    check("empty request rejected", rc == 1)
    rc, js = call(None, root, raw='["a"]')
    check("non-object request rejected", rc == 1)

    print("== path safety ==")
    rc, js = call({"mode": "create", "path": "../escape.md", "content": "x"}, root)
    check("path traversal blocked", rc == 1 and "escapes" in js["error"], js)
    check("no file written outside root",
          not os.path.exists(os.path.join(os.path.dirname(root), "escape.md")))
    rc, js = call({"mode": "create", "path": "/etc/passwd", "content": "x"}, root)
    check("absolute path outside root blocked", rc == 1)
    rc, js = call({"mode": "create", "path": os.path.join(root, "abs.md"),
                   "content": "x"}, root)
    check("absolute path inside root allowed", rc == 0 and js["ok"], js)

    print("== invocation styles ==")
    r = subprocess.run([sys.executable, SCRIPT, "--root", root, "--request",
                        json.dumps({"mode": "status", "path": "r.md"})],
                       capture_output=True, text=True)
    check("--request flag works", r.returncode == 0 and json.loads(r.stdout)["ok"])
    reqf = os.path.join(root, "req.json")
    with open(reqf, "w", encoding="utf-8") as fh:
        json.dump({"mode": "append", "path": "rf.md", "content": "via file"}, fh)
    r = subprocess.run([sys.executable, SCRIPT, "--root", root,
                        "--request-file", reqf], capture_output=True, text=True)
    check("--request-file works",
          r.returncode == 0 and "via file" in
          open(os.path.join(root, "rf.md"), encoding="utf-8").read())

    print("== multi-chunk assembly ==")
    doc = "plan.md"
    call({"mode": "create", "path": doc, "content": "# Plan", "overwrite": True}, root)
    for i in range(1, 26):
        rc, js = call({"mode": "append", "path": doc,
                       "content": f"## Section {i}\n" + ("line\n" * 40)}, root)
        if rc != 0:
            check(f"chunk {i}", False, js)
            break
    rc, js = call({"mode": "read", "path": doc}, root)
    check("25-chunk document assembled", js["lines"] > 1000, js.get("lines"))
    check("all sections present",
          all(f"## Section {i}" in js["content"] for i in range(1, 26)))

    shutil.rmtree(root, ignore_errors=True)
    total = len(PASSED) + len(FAILED)
    print(f"\n{len(PASSED)}/{total} passed")
    if FAILED:
        print("FAILED: " + ", ".join(FAILED))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
