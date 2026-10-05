#!/usr/bin/env python3
"""
run-tests.py — run the monorepo's tests and return a verdict the agent can always read.

OUTPUT CONTRACT (agent-safe)
  • The FIRST line of stdout is always:   VERDICT=<value>
  • Every run writes  <repo>/.SS_WF/Agent/TEST_RUNS/LATEST.json  (copy of summary.json)
  • Exit code is 0 whenever the script itself worked — including FAIL, EXPECTED_FAIL,
    PASSED_UNEXPECTEDLY, NOT_COLLECTED. Agent tools often hide stdout on a non-zero
    exit; a zero exit guarantees the verdict is visible.
  • Errors (usage / environment) also print VERDICT=USAGE_ERROR or VERDICT=ENV_ERROR
    on stdout and exit 0.
  • Pass --strict-exit for CI: verdict-specific exit codes (see below).

ENGINES
  --all                 Root package.json script, default test:parallel  (quality gate)
  --files / --related / --package   Direct Vitest per owning package, JSON reporter

PATHS
  The repo root is found automatically (upward, and one level into src/ etc.).
  Any path form works: repo-relative, workspace-prefixed (src/...), scan-dir-relative,
  absolute. Vitest filters are written relative to each package's scan dir.

STRICT EXIT CODES (--strict-exit only)
  0 PASS · EXPECTED_FAIL       1 FAIL · PASSED_UNEXPECTEDLY · FAILED_FOR_WRONG_REASON
  2 USAGE_ERROR                3 NOT_COLLECTED · NO_TASKS
  4 ENV_ERROR                  5 RUNNER_ERROR
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

STRICT_CODES = {
    "PASS": 0, "EXPECTED_FAIL": 0,
    "FAIL": 1, "PASSED_UNEXPECTEDLY": 1, "FAILED_FOR_WRONG_REASON": 1,
    "USAGE_ERROR": 2, "NOT_COLLECTED": 3, "NO_TASKS": 3,
    "ENV_ERROR": 4, "RUNNER_ERROR": 5,
}
PACKAGE_ALIASES = {
    "foundation": "@dxp/foundation", "theme": "@dxp/theme", "cms-utils": "@dxp/cms-utils",
    "cms-components": "@dxp/cms-components", "sme": "@dxp/sme-portal",
}
DEV_SCRIPT = {
    "@dxp/foundation": "pnpm run test:foundation", "@dxp/theme": "pnpm run test:theme",
    "@dxp/cms-utils": "pnpm run test:cms-utils",
    "@dxp/cms-components": "pnpm run test:cms-components", "@dxp/sme-portal": "pnpm run test:sme",
}
ROOT_MARKERS = ("pnpm-workspace.yaml", "turbo.json")
NESTED_ROOTS = ("src", "Src", "repo", "app")
CONFIG_NAMES = [f"{b}.{e}" for b in ("vitest.config", "vite.config")
                for e in ("ts", "mts", "cts", "js", "mjs", "cjs")]
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".turbo", "coverage", ".SS_WF"}
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")

STRICT = "--strict-exit" in sys.argv


# ═══════════════════════════════════════════════════════════ output

def finish(verdict: str, lines: list[str] | None = None, summary: dict | None = None,
           out_dir: Path | None = None, repo_root: Path | None = None) -> None:
    """Single exit point. VERDICT line first, then detail. Exit 0 unless --strict-exit."""
    print(f"VERDICT={verdict}")
    for line in lines or []:
        print(line)
    if summary is not None and out_dir is not None:
        text = json.dumps(summary, indent=2)
        (out_dir / "summary.json").write_text(text, encoding="utf-8")
        if repo_root and (repo_root / ".SS_WF").is_dir():
            latest = repo_root / ".SS_WF" / "Agent" / "TEST_RUNS" / "LATEST.json"
            latest.parent.mkdir(parents=True, exist_ok=True)
            latest.write_text(text, encoding="utf-8")
        print(f"  Output:    {rel(out_dir, repo_root) if repo_root else out_dir}/summary.json")
    sys.stdout.flush()
    sys.exit(STRICT_CODES.get(verdict, 1) if STRICT else 0)


def error(verdict: str, message: str) -> None:
    finish(verdict, [f"  Reason:    {line}" if i == 0 else f"             {line}"
                     for i, line in enumerate(message.splitlines())])


def clean(text: str, limit: int = 800) -> str:
    text = ANSI.sub("", text or "").strip()
    return text if len(text) <= limit else text[:limit] + " …[truncated]"


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def rel(path, base) -> str:
    try:
        return str(Path(path).resolve().relative_to(base))
    except (ValueError, TypeError):
        return str(path)


# ═══════════════════════════════════════════════════════════ repo + paths

def is_root(path: Path) -> bool:
    return any((path / m).exists() for m in ROOT_MARKERS)


def find_repo_root(*starts: Path) -> tuple[Path | None, list[str]]:
    tried: list[str] = []
    for start in starts:
        for base in [start, *start.parents]:
            for cand in [base, *(base / n for n in NESTED_ROOTS)]:
                tried.append(str(cand))
                if cand.is_dir() and is_root(cand):
                    return cand, tried
    return None, tried


def resolve_input(value: str, repo_root: Path, cwd: Path) -> tuple[Path | None, list[str]]:
    p = Path(value)
    attempts = [p] if p.is_absolute() else [cwd / p, repo_root / p, repo_root.parent / p]
    if not p.is_absolute() and p.parts and p.parts[0] == repo_root.name:
        attempts.append(repo_root / Path(*p.parts[1:]))
    tried = []
    for a in attempts:
        r = a.resolve()
        if str(r) not in tried:
            tried.append(str(r))
        if r.exists():
            return r, tried
    return None, tried


def similar_files(value: str, repo_root: Path, limit: int = 5) -> list[str]:
    name, hits = Path(value).name.lower(), []
    for dp, dns, fns in os.walk(repo_root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        hits += [rel(Path(dp) / f, repo_root) for f in fns if f.lower() == name]
        if len(hits) >= limit:
            break
    return hits[:limit]


def owning_package(path: Path, repo_root: Path) -> tuple[str, Path] | None:
    cur = path if path.is_dir() else path.parent
    while cur != repo_root and repo_root in cur.parents:
        m = read_json(cur / "package.json")
        if m and m.get("name"):
            return m["name"], cur
        cur = cur.parent
    return None


def discover_packages(repo_root: Path) -> dict[str, Path]:
    found = {}
    for dp, dns, fns in os.walk(repo_root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        if len(Path(dp).relative_to(repo_root).parts) > 5:
            dns[:] = []
            continue
        if "package.json" in fns and Path(dp) != repo_root:
            m = read_json(Path(dp) / "package.json")
            if m and m.get("name"):
                found[m["name"]] = Path(dp)
    return found


# ═══════════════════════════════════════════════════════════ vitest config

def _strip_comments(t: str) -> str:
    return re.sub(r"(?<![:'\"`])//[^\n]*", "", re.sub(r"/\*.*?\*/", "", t, flags=re.S))


def _read_expr(t: str, start: int) -> str:
    depth, quote, i = 0, "", start
    while i < len(t) and i - start < 400:
        ch = t[i]
        if quote:
            if ch == quote and t[i - 1] != "\\":
                quote = ""
        elif ch in "'\"`":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            if depth == 0:
                break
            depth -= 1
        elif ch in ",\n" and depth == 0:
            break
        i += 1
    return t[start:i]


def _config_value(t: str, key: str):
    m = re.search(rf"(?<![\w.$]){re.escape(key)}\s*:\s*", t)
    if not m:
        return None
    expr = _read_expr(t, m.end())
    lits = re.findall(r"""['"`]([^'"`]+)['"`]""", expr)
    return (lits[-1], expr.strip()) if lits else None


def package_test_flags(pkg_dir: Path) -> tuple[list[str], Path | None]:
    script = ((read_json(pkg_dir / "package.json") or {}).get("scripts") or {}).get("test", "") or ""
    flags, config = [], None
    for opt in ("--config", "-c", "--root", "-r", "--dir"):
        m = re.search(rf"(?:^|\s){re.escape(opt)}(?:=|\s+)(?!-)(\S+)", script)
        if m:
            flags += [opt, m.group(1)]
            if opt in ("--config", "-c"):
                config = (pkg_dir / m.group(1)).resolve()
    return flags, config


def scan_dir_of(pkg_dir: Path, flags: list[str], cfg: Path | None) -> tuple[Path, str]:
    def lit(base, value, expr):
        return ((pkg_dir if ("__dirname" in expr or "import.meta" in expr) else base) / value).resolve()

    root, scan, notes = pkg_dir, None, []
    cfg = cfg if cfg and cfg.exists() else next((pkg_dir / n for n in CONFIG_NAMES
                                                  if (pkg_dir / n).exists()), None)
    if cfg:
        try:
            t = _strip_comments(cfg.read_text(encoding="utf-8"))
        except OSError:
            t = ""
        if (v := _config_value(t, "root")) and lit(pkg_dir, *v).is_dir():
            root = lit(pkg_dir, *v)
            notes.append(f"root: {v[1]}")
        if (v := _config_value(t, "dir")) and lit(root, *v).is_dir():
            scan = lit(root, *v)
            notes.append(f"dir: {v[1]}")
        notes.insert(0, cfg.name)
    for i in range(0, len(flags), 2):
        opt, val = flags[i], flags[i + 1]
        if opt in ("--root", "-r") and (pkg_dir / val).resolve().is_dir():
            root = (pkg_dir / val).resolve()
        elif opt == "--dir" and (root / val).resolve().is_dir():
            scan = (root / val).resolve()
    return scan or root, " · ".join(notes) or "no vitest config"


def path_forms(files: list[Path], scan: Path, pkg: Path):
    forms = []
    try:
        forms.append(("scan-dir-relative", ["./" + str(f.relative_to(scan)) for f in files]))
    except ValueError:
        pass
    forms.append(("absolute", [str(f) for f in files]))
    try:
        forms.append(("package-relative", [str(f.relative_to(pkg)) for f in files]))
    except ValueError:
        pass
    seen, out = set(), []
    for label, t in forms:
        if tuple(t) not in seen:
            seen.add(tuple(t))
            out.append((label, t))
    return out


# ═══════════════════════════════════════════════════════════ execution

def execute(root: Path, cmd: list[str], log: Path, timeout: int, env_extra=None):
    env = {**os.environ, "CI": "true", "FORCE_COLOR": "0", "NO_COLOR": "1",
           "TURBO_UI": "false", **(env_extra or {})}
    timed_out = False
    try:
        p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=timeout)
        out, code = (p.stdout or "") + (p.stderr or ""), p.returncode
    except subprocess.TimeoutExpired as exc:
        part = exc.stdout or ""
        out = (part.decode(errors="replace") if isinstance(part, bytes) else part) + \
            f"\nTIMEOUT after {timeout}s"
        code, timed_out = 124, True
    except FileNotFoundError as exc:
        out, code = f"Command not found: {exc}", 127
    out = ANSI.sub("", out)
    log.write_text(out, encoding="utf-8")
    return code, out, timed_out


def vitest_cmd(mode, pkg, targets, flags, json_path, name, coverage):
    cmd = ["pnpm", "--filter", pkg, "exec", "vitest"]
    cmd += ["related", "--run", *targets] if mode == "related" else ["run", *targets]
    cmd += flags
    if name:
        cmd += ["-t", name]
    if coverage:
        cmd += ["--coverage"]
    return cmd + ["--reporter=default", "--reporter=json", f"--outputFile.json={json_path}"]


def parse_report(json_path: Path, root: Path):
    data = read_json(json_path)
    if data is None:
        return None
    files, failed, suite_errors = [], [], []
    passed = fcount = skipped = 0
    for s in data.get("testResults", []):
        f = rel(s.get("name", ""), root)
        c = {"passed": 0, "failed": 0, "skipped": 0}
        for t in s.get("assertionResults", []) or []:
            st = t.get("status", "")
            if st == "passed":
                c["passed"] += 1
            elif st == "failed":
                c["failed"] += 1
                failed.append({"file": f, "test": t.get("fullName") or t.get("title", ""),
                               "message": clean("\n".join(t.get("failureMessages") or []))})
            else:
                c["skipped"] += 1
        if s.get("status") == "failed" and c["failed"] == 0:
            suite_errors.append({"file": f, "message": clean(s.get("message", ""))})
        passed, fcount, skipped = passed + c["passed"], fcount + c["failed"], skipped + c["skipped"]
        files.append({"file": f, **c})
    return {"files": files, "failed": failed, "suite_errors": suite_errors,
            "passed": passed, "failed_count": fcount, "skipped": skipped}


def run_package(root, pkg, pkg_dir, mode, files, targets, out_dir, name, coverage, timeout):
    flags, cfg = package_test_flags(pkg_dir)
    scan, scan_src = scan_dir_of(pkg_dir, flags, cfg)
    requested = [rel(f, root) for f in files]
    candidates = path_forms(files, scan, pkg_dir) if files else [("targets", targets)]
    safe = pkg.replace("@", "").replace("/", "_")
    attempts, chosen = [], None
    for i, (form, tg) in enumerate(candidates):
        jp, lp = out_dir / f"{safe}.{i}.json", out_dir / f"{safe}.{i}.log"
        cmd = vitest_cmd(mode, pkg, tg, flags, jp, name, coverage)
        t0 = time.time()
        code, out, to = execute(root, cmd, lp, timeout)
        rep = parse_report(jp, root)
        got = {f["file"] for f in rep["files"]} if rep else set()
        a = {"form": form, "targets": tg, "command": " ".join(cmd), "exit_code": code,
             "timed_out": to, "duration_s": round(time.time() - t0, 1), "log": rel(lp, root),
             "report": rep, "output": out, "missing": [r for r in requested if r not in got],
             "extra": sorted(got - set(requested)) if requested else []}
        attempts.append(a)
        if to or not files or (rep is not None and not a["missing"]):
            chosen = a
            break
    chosen = chosen or min(attempts, key=lambda a: (len(a["missing"]), a["report"] is None))
    return {"scan": scan, "scan_src": scan_src, "requested": requested,
            "chosen": chosen, "attempts": attempts}


# ═══════════════════════════════════════════════════════════ targeted engine

def targeted(args, root, cwd, packages, out_dir):
    plan: dict[str, dict] = {}

    def need(value, kind):
        p, tried = resolve_input(value, root, cwd)
        if p:
            return p
        msg = [f"{kind} not found: {value}", f"repo root: {root}", "tried:"] + [f"  {t}" for t in tried]
        if (sim := similar_files(value, root)):
            msg += ["files with the same name:"] + [f"  {s}" for s in sim]
            msg.append("→ use one of these paths (check folder casing / leading segment)")
        error("USAGE_ERROR", "\n".join(msg))

    if args.files:
        for v in args.files:
            p = need(v, "Test file")
            o = owning_package(p, root) or error("ENV_ERROR", f"No owning package.json for {p}")
            plan.setdefault(o[0], {"mode": "run", "dir": o[1], "files": [], "targets": []})["files"].append(p)
    elif args.related:
        srcs = [need(v, "Source file") for v in args.related]
        names = list(packages) if args.related_scope == "all" else []
        if not names:
            for s in srcs:
                o = owning_package(s, root) or error("ENV_ERROR", f"No owning package.json for {s}")
                if o[0] not in names:
                    names.append(o[0])
        for n in names:
            plan[n] = {"mode": "related", "dir": packages[n], "files": [], "targets": [str(s) for s in srcs]}
    else:
        for v in args.package:
            n = PACKAGE_ALIASES.get(v, v)
            if n not in packages:
                error("ENV_ERROR", f"Package not found: {n}\nknown: {', '.join(sorted(packages))}")
            plan[n] = {"mode": "run", "dir": packages[n], "files": [], "targets": []}

    if args.dry_run:
        lines = [f"  repo root: {root}"]
        for n, e in plan.items():
            flags, cfg = package_test_flags(e["dir"])
            scan, src = scan_dir_of(e["dir"], flags, cfg)
            form, tg = (path_forms(e["files"], scan, e["dir"]) if e["files"] else [("targets", e["targets"])])[0]
            lines += [f"  {n} · scan {rel(scan, root)} ({src}) · form {form}",
                      "  " + " ".join(vitest_cmd(e["mode"], n, tg, flags, out_dir / "r.json",
                                                 args.name, args.coverage))]
        finish("DRY_RUN", lines)

    results, not_collected, runner_err = [], [], []
    tot = {"passed": 0, "failed_count": 0, "skipped": 0, "failed": [], "suite_errors": []}
    for n, e in plan.items():
        r = run_package(root, n, e["dir"], e["mode"], e["files"], e["targets"], out_dir,
                        args.name, args.coverage, args.timeout or 600)
        c = r["chosen"]
        rec = {"package": n, "scan_dir": rel(r["scan"], root), "path_form": c["form"],
               "command": c["command"], "exit_code": c["exit_code"], "duration_s": c["duration_s"],
               "log": c["log"],
               "reproduce": (f'{DEV_SCRIPT[n]} -- --run {" ".join(c["targets"])}'
                             + (f' -t "{args.name}"' if args.name else "")) if e["files"] and n in DEV_SCRIPT else "",
               "tried": [f'{a["form"]}{"✓" if not a["missing"] and a["report"] else "✗"}' for a in r["attempts"]]}
        rep = c["report"]
        if rep is None:
            if c["timed_out"]:
                rec["status"] = "TIMEOUT"
                runner_err.append(n)
            elif "No test files found" in c["output"] or r["requested"]:
                rec["status"] = "NOT_COLLECTED"
                not_collected += r["requested"] or [f"{n} (no test files matched)"]
            elif e["mode"] == "related" and c["exit_code"] == 0:
                rec["status"] = "NO_RELATED_TESTS"
            else:
                rec["status"] = "RUNNER_ERROR"
                rec["tail"] = clean(c["output"][-1500:], 1500)
                runner_err.append(n)
        else:
            not_collected += c["missing"]
            rec.update({"status": "RAN", "passed": rep["passed"], "failed": rep["failed_count"],
                        "also_ran": c["extra"], "files": rep["files"]})
            tot["passed"] += rep["passed"]
            tot["failed_count"] += rep["failed_count"]
            tot["skipped"] += rep["skipped"]
            tot["failed"] += rep["failed"]
            tot["suite_errors"] += rep["suite_errors"]
        results.append(rec)

    # verdict
    ran = tot["passed"] + tot["failed_count"]
    se = tot["suite_errors"]
    if runner_err:
        v, why = "RUNNER_ERROR", "Vitest crashed, timed out or produced no report — see log tail."
    elif not_collected:
        v, why = "NOT_COLLECTED", "Requested file(s) never ran. NEVER a pass — check include pattern / path."
    elif args.expect == "pass":
        if ran == 0 and not se:
            v, why = "NOT_COLLECTED", "No tests executed (check --name pattern)."
        elif tot["failed_count"] == 0 and not se:
            v, why = "PASS", "All executed tests passed."
        else:
            v, why = "FAIL", "One or more tests failed or a suite errored."
    elif se and tot["failed_count"] == 0:
        v, why = "FAILED_FOR_WRONG_REASON", "Suite failed to load (import/compile/setup) — not an assertion. Not proof."
    elif tot["failed_count"] == 0:
        v, why = "PASSED_UNEXPECTEDLY", "Test passed against current code — the root cause is wrong. Return to RCA."
    elif args.name and not any(args.name.lower() in f["test"].lower() for f in tot["failed"]):
        v, why = "FAILED_FOR_WRONG_REASON", f"Tests failed, but none matching '{args.name}'."
    elif se:
        v, why = "FAILED_FOR_WRONG_REASON", "Target failed, but other suites errored — not isolated."
    else:
        v, why = "EXPECTED_FAIL", "Target test failed on an assertion, as required."

    summary = {"engine": "targeted", "label": args.label, "expect": args.expect, "name": args.name,
               "verdict": v, "reason": why, "repo_root": str(root),
               "totals": {"passed": tot["passed"], "failed": tot["failed_count"], "skipped": tot["skipped"],
                          "suite_errors": len(se), "not_collected": len(not_collected)},
               "failed_tests": tot["failed"], "suite_errors": se, "not_collected": not_collected,
               "packages": results}
    t = summary["totals"]
    lines = [f"  Run:       {args.label}   (expected: {args.expect})", f"  Reason:    {why}",
             f"  Totals:    {t['passed']} passed · {t['failed']} failed · {t['skipped']} skipped · "
             f"{t['suite_errors']} suite errors · {t['not_collected']} not collected"]
    for r in results:
        lines.append(f"  Package:   {r['package']}  {r['status']}  scan={r['scan_dir']}  form={r['path_form']}  "
                     f"tried={' → '.join(r['tried'])}")
        if r["reproduce"]:
            lines.append(f"  Reproduce: {r['reproduce']}")
        lines += [f"  ℹ ALSO RAN {x}" for x in r.get("also_ran", [])]
        if r.get("tail"):
            lines.append("  Log tail:  " + r["tail"].replace("\n", "\n             ")[:600])
    for f in tot["failed"]:
        lines.append(f"  ✗ FAILED  {f['file']} › {f['test']}")
        if f["message"]:
            lines.append("      " + f["message"].replace("\n", "\n      ")[:400])
    lines += [f"  ⚠ SUITE ERROR {e['file']}: {e['message'][:300]}" for e in se]
    lines += [f"  ⚠ NOT COLLECTED {n}" for n in not_collected]
    finish(v, lines, summary, out_dir, root)


# ═══════════════════════════════════════════════════════════ suite engine

def _counts(text):
    c = {k: int(m.group(1)) if (m := re.search(rf"(\d+)\s+{k}", text)) else 0
         for k in ("failed", "passed", "skipped", "todo")}
    return c


def suite(args, root, cwd, packages, out_dir):
    scripts = (read_json(root / "package.json") or {}).get("scripts", {}) or {}
    script = args.script or ("test:coverage" if args.coverage else "test:parallel")
    if script not in scripts:
        error("ENV_ERROR", f"Root package.json has no '{script}' script.\n"
                           f"test scripts: {', '.join(s for s in sorted(scripts) if s.startswith('test'))}")
    cmd_text = scripts[script]
    task = (m.group(1) if (m := re.search(r"\bturbo\s+(?:run\s+)?(?!-)([\w:.-]+)", cmd_text)) else None)
    cmd = ["pnpm", "run", script]
    if args.dry_run:
        finish("DRY_RUN", [f"  repo root: {root}", f"  {script} = {cmd_text}", "  " + " ".join(cmd)])

    t0 = time.time()
    code, out, to = execute(root, cmd, out_dir / "suite.log", args.timeout or 1800,
                            {"TURBO_FORCE": "true"} if args.force else None)
    per: dict[str, list[str]] = {}
    rest: list[str] = []
    rx = re.compile(rf"^(?P<p>\S+?):{re.escape(task)}: ?(?P<l>.*)$") if task else None
    for line in out.splitlines():
        m = rx.match(line) if rx else None
        (per.setdefault(m.group("p"), []).append(m.group("l")) if m else rest.append(line))
    if not rx:
        per = {"(root)": out.splitlines()}
    turbo_failed = []
    for line in rest:
        if "Failed:" in line:
            turbo_failed += re.findall(r"([@\w./-]+)#", line)
    for p in turbo_failed:
        per.setdefault(p, [])

    results, tot = [], {"passed": 0, "failed": 0}
    for p, lines in sorted(per.items()):
        tests = next((_counts(m.group(1)) for l in lines if (m := re.match(r"^\s*Tests\s{2,}(\d.*)$", l))), None)
        no_files = any("No test files found" in l for l in lines)
        errored = any(re.search(r"ELIFECYCLE|ERR_PNPM|exited \(\d+\)", l) for l in lines)
        fails = [l.strip()[5:].strip() for l in lines if re.match(r"^\s*FAIL\s", l)]
        if p in turbo_failed or errored or (tests and tests["failed"]):
            st = "NO_TEST_FILES" if no_files else "FAILED"
        else:
            st = "PASSED" if (tests or code == 0) else "UNKNOWN"
        if tests:
            tot["passed"] += tests["passed"]
            tot["failed"] += tests["failed"]
        results.append({"package": p, "status": st, "tests": tests, "fail_lines": sorted(set(fails))[:20]})

    bad = [r for r in results if r["status"] in ("FAILED", "NO_TEST_FILES")]
    drill = []
    if bad and not args.no_drill_down and not to:
        dd = out_dir / "drill-down"
        dd.mkdir(exist_ok=True)
        for r in bad:
            if r["status"] == "FAILED" and r["package"] in packages:
                run = run_package(root, r["package"], packages[r["package"]], "run", [], [], dd,
                                  None, False, args.timeout or 600)
                rep = run["chosen"]["report"]
                drill.append({"package": r["package"],
                              "status": "NO_REPORT" if rep is None else
                              ("PASSED_ON_RERUN" if rep["failed_count"] == 0 and not rep["suite_errors"] else "FAILED"),
                              "failed_tests": rep["failed"] if rep else [],
                              "suite_errors": rep["suite_errors"] if rep else []})

    if to:
        v, why = "RUNNER_ERROR", "Suite timed out."
    elif bad:
        v, why = "FAIL", f"{len(bad)} package(s) failed: {', '.join(r['package'] for r in bad)}."
    elif code != 0:
        v, why = "RUNNER_ERROR", f"Command exited {code} with no failing package identified — see suite.log."
    elif rx and not results:
        v, why = "NO_TASKS", "Turbo ran no test tasks."
    else:
        v, why = "PASS", "All test tasks passed."

    summary = {"engine": "suite", "label": args.label, "script": script, "command": " ".join(cmd),
               "force": bool(args.force), "verdict": v, "reason": why, "exit_code": code,
               "duration_s": round(time.time() - t0, 1), "totals": tot, "packages": results,
               "drill_down": drill, "log": rel(out_dir / "suite.log", root)}
    lines = [f"  Command:   pnpm run {script} → {cmd_text}" + ("  [TURBO_FORCE]" if args.force else ""),
             f"  Reason:    {why}", f"  Tests:     {tot['passed']} passed · {tot['failed']} failed"]
    for r in results:
        t = r["tests"]
        lines.append(f"  {r['package']:<24}{r['status']:<15}"
                     + (f"{t['passed']}p/{t['failed']}f/{t['skipped'] + t['todo']}s" if t else "—"))
    for d in drill:
        if d["status"] == "PASSED_ON_RERUN":
            lines.append(f"  ⚠ PASSED ON RE-RUN {d['package']} — possible flaky test; not a pass")
        lines += [f"  ✗ FAILED [{d['package']}] {f['file']} › {f['test']}" for f in d["failed_tests"]]
        lines += [f"  ⚠ SUITE ERROR [{d['package']}] {e['file']}" for e in d["suite_errors"]]
    finish(v, lines, summary, out_dir, root)


# ═══════════════════════════════════════════════════════════ main

class Parser(argparse.ArgumentParser):
    def error(self, message):
        error("USAGE_ERROR", message)


def main():
    ap = Parser(description="Run monorepo tests; VERDICT= on first stdout line.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--files", nargs="+")
    g.add_argument("--related", nargs="+")
    g.add_argument("--package", nargs="+")
    g.add_argument("--where", action="store_true")
    ap.add_argument("--script")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-drill-down", action="store_true")
    ap.add_argument("--related-scope", choices=["owner", "all"], default="owner")
    ap.add_argument("--name")
    ap.add_argument("--expect", choices=["pass", "fail"], default="pass")
    ap.add_argument("--coverage", action="store_true")
    ap.add_argument("--label", default="run")
    ap.add_argument("--timeout", type=int)
    ap.add_argument("--repo-root")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict-exit", action="store_true")
    args = ap.parse_args()

    if args.expect == "fail" and not args.files:
        error("USAGE_ERROR", "--expect fail is only valid with --files.")
    if args.all and args.name:
        error("USAGE_ERROR", "--name is not supported with --all.")

    cwd = Path.cwd().resolve()
    if args.repo_root:
        root = Path(args.repo_root)
        root = (root if root.is_absolute() else cwd / root).resolve()
        if not (root.is_dir() and is_root(root)):
            error("ENV_ERROR", f"--repo-root is not a workspace root: {root}")
    else:
        root, tried = find_repo_root(cwd, Path(__file__).resolve().parent)
        if not root:
            error("ENV_ERROR", "Repository root not found (no pnpm-workspace.yaml / turbo.json).\n"
                               f"cwd: {cwd}\ntried: " + ", ".join(tried[:8]))
    packages = discover_packages(root)

    if args.where:
        lines = [f"  repo root: {root}", f"  script:    {Path(__file__).resolve()}", f"  cwd:       {cwd}"]
        for n, d in sorted(packages.items()):
            flags, cfg = package_test_flags(d)
            scan, src = scan_dir_of(d, flags, cfg)
            lines.append(f"  {n:<24} dir={rel(d, root):<36} scan={rel(scan, root)}  ({src})")
        finish("WHERE", lines)

    if not args.dry_run and not shutil.which("pnpm"):
        error("ENV_ERROR", "pnpm is not available on PATH.")

    stamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = (root / ".SS_WF" / "Agent" / "TEST_RUNS" / f"{args.label}-{stamp}"
               if (root / ".SS_WF").is_dir() else Path(tempfile.mkdtemp(prefix=f"test-run-{args.label}-")))
    out_dir.mkdir(parents=True, exist_ok=True)
    (suite if args.all else targeted)(args, root, cwd, packages, out_dir)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # never die silently
        finish("RUNNER_ERROR", [f"  Reason:    script crashed: {type(exc).__name__}: {exc}"])
