#!/usr/bin/env python3
"""
verify-evidence.py - evidence gate for one defect issue (defect-fix v7).

GATE=PASS requires:
  1. reproduction run: EXPECTED_FAIL or FAIL
  2. baseline run exists (related tests before any change)
  3. after-fix run newer than reproduction: PASS, includes reproduction test file(s)
  4. related run newer than reproduction: no failing test that was not failing in baseline
  5. reproduction test file exists and is added/changed in git
  6. at least one non-test source file changed
  7. impact map exists, has rows in groups A..E, and no row is unknown/unverified/empty evidence
Always exits 0. First stdout line: GATE=PASS | GATE=FAIL.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

TEST_RE = re.compile(r"\.(test|spec)\.[jt]sx?$")
IGNORE = (".SS_WF/", ".project/learnings/", "figma-output/", ".python/", "bin/")
EVIDENCE = ("new assertion:", "existing test:", "related run:", "found, not fixed:", "outside fe:", "ac conflict:")


def repo_root(arg):
    for c in [arg, "src", "."]:
        if not c:
            continue
        try:
            return Path(subprocess.run(["git", "-C", c, "rev-parse", "--show-toplevel"],
                                       capture_output=True, text=True, check=True).stdout.strip())
        except Exception:
            pass
    return None


def latest(runs, prefix, kind):
    pat = re.compile(rf"^{re.escape(prefix)}-{kind}-(\d{{8}}-\d{{6}})$")
    hits = [(m.group(1), d) for d in (runs.iterdir() if runs.exists() else [])
            if (m := pat.match(d.name)) and (d / "summary.json").exists()]
    if not hits:
        return None, None, None
    s, d = sorted(hits)[-1]
    return s, d, json.loads((d / "summary.json").read_text(encoding="utf-8"))


def files_of(data):
    return {f["file"] for p in (data or {}).get("packages", []) for f in p.get("files", []) if f.get("file")}


def failing(data):
    out = set()
    for t in (data or {}).get("failed_tests", []):
        out.add(json.dumps(t, sort_keys=True) if not isinstance(t, str) else t)
    for p in (data or {}).get("packages", []):
        for f in p.get("files", []):
            if f.get("failed"):
                out.add(f"{f.get('file')}::failed")
    return out


def changed(repo):
    out = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "-uall"],
                         capture_output=True, text=True).stdout
    return [l[3:].split(" -> ")[-1].strip().strip('"') for l in out.splitlines() if l[3:].strip()]


def check_impact(path):
    issues = []
    if not path.exists():
        return [f"impact map missing: {path.name} (Stage 4)"]
    rows = [r for r in path.read_text(encoding="utf-8").splitlines()
            if r.strip().startswith("|") and not re.match(r"^\|\s*-", r.strip()) and "| ID |" not in r]
    if not rows:
        return ["impact map has no rows"]
    groups = set()
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) < 6:
            issues.append(f"impact row malformed: {r.strip()[:80]}")
            continue
        rid, status, ev = cells[0], cells[4].lower(), cells[5].lower()
        if rid[:1].upper() in "ABCDE":
            groups.add(rid[:1].upper())
        if "unknown" in status or "unverified" in ev or not ev.startswith(EVIDENCE):
            issues.append(f"impact row {rid} not verified (status '{cells[4]}', evidence '{cells[5][:40]}')")
    for g, name in [("A", "reported"), ("B", "same behaviour"), ("D", "consumers"), ("E", "introduced by fix")]:
        if g not in groups:
            issues.append(f"impact map has no {g}-rows ({name})")
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticket", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--repo", default="")
    a = ap.parse_args()
    repo = repo_root(a.repo)
    if not repo:
        print("GATE=FAIL\n  - repo root not found (expected ./src)")
        return 0
    prefix = f"{a.ticket}-{a.issue}"
    runs = repo / ".SS_WF/Agent/TEST_RUNS"
    R = []

    rs, rd, r = latest(runs, prefix, "reproduction")
    bs, bd, b = latest(runs, prefix, "baseline")
    fs, fd, f = latest(runs, prefix, "after-fix")
    ls_, ld, l = latest(runs, prefix, "related")

    if not r:
        R.append(f"no {prefix}-reproduction run")
    elif r.get("verdict") not in ("EXPECTED_FAIL", "FAIL"):
        R.append(f"reproduction verdict {r.get('verdict')} (needs EXPECTED_FAIL/FAIL) -> Stage 3")
    tests = files_of(r)
    if r and not tests:
        R.append("reproduction run recorded no test files")

    if not b:
        R.append(f"no {prefix}-baseline run (related tests before the change) -> Stage 4")

    if not f:
        R.append(f"no {prefix}-after-fix run")
    else:
        if rs and fs <= rs:
            R.append("after-fix run not newer than reproduction")
        if f.get("verdict") != "PASS":
            R.append(f"after-fix verdict {f.get('verdict')} (needs PASS)")
        miss = tests - files_of(f)
        if tests and miss:
            R.append(f"after-fix run missing reproduction file(s): {sorted(miss)}")

    new_fail = []
    if not l:
        R.append(f"no {prefix}-related run")
    else:
        if rs and ls_ <= rs:
            R.append("related run not newer than reproduction")
        if l.get("verdict") not in ("PASS", "FAIL"):
            R.append(f"related verdict {l.get('verdict')} (needs PASS, or FAIL only with baseline failures)")
        new_fail = sorted(failing(l) - failing(b))
        if new_fail:
            R.append(f"new failures vs baseline (regression from the fix): {new_fail[:5]}")

    ch = changed(repo)
    for t in sorted(tests):
        if not (repo / t).exists():
            R.append(f"reproduction test deleted: {t}")
        elif t not in ch:
            R.append(f"reproduction test not added/changed in git: {t}")
    src = [p for p in ch if not TEST_RE.search(p) and not p.startswith(IGNORE)]
    if not src:
        R.append("no non-test source file changed")

    R += check_impact(runs / f"{prefix}-impact.md")

    info = {"ticket": a.ticket, "issue": a.issue, "gate": "FAIL" if R else "PASS", "reasons": R,
            "runs": {k: (d.name if d else None, x.get("verdict") if x else None)
                     for k, d, x in [("reproduction", rd, r), ("baseline", bd, b), ("after_fix", fd, f), ("related", ld, l)]},
            "test_files": sorted(tests), "source_files": src, "new_failures": new_fail}
    runs.mkdir(parents=True, exist_ok=True)
    out = runs / f"{prefix}-gate.json"
    out.write_text(json.dumps(info, indent=2), encoding="utf-8")

    print(f"GATE={info['gate']}")
    for k, (n, v) in info["runs"].items():
        print(f"  {k:<13}{n} -> {v}")
    print(f"  tests:       {', '.join(info['test_files']) or 'none'}")
    print(f"  source:      {', '.join(src) or 'none'}")
    for x in R:
        print(f"  - {x}")
    print(f"  output:      {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
