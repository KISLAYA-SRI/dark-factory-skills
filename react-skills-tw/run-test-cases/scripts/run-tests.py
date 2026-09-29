#!/usr/bin/env python3
"""
run-tests.py — run the monorepo's tests and return a machine-readable verdict.

ROBUST BY DESIGN
  You do not need to know where the repo root is, or how a path should be
  written. Run the script from anywhere, pass any path form, and it resolves
  the rest — or tells you exactly what it tried and why it failed.

    # All of these work, from any working directory:
    python3 run-tests.py --files Portals/Sme/Features/.../X.test.tsx
    python3 run-tests.py --files src/Portals/Sme/Features/.../X.test.tsx
    python3 run-tests.py --files ./Features/Shared/.../X.test.tsx
    python3 run-tests.py --files /abs/path/.../X.test.tsx

TWO ENGINES
  SUITE     --all       Runs a root package.json script as developers do
                        (default: test:parallel = turbo run test --parallel).
                        → static code quality workflow
  TARGETED  --files     Direct Vitest in the owning package, JSON reporter, so
            --related   every test has a precise status and a load error is told
            --package   apart from an assertion failure.
                        → defect fix workflow

EXIT CODES
  0  Expectation met      PASS · EXPECTED_FAIL
  1  Expectation NOT met  FAIL · PASSED_UNEXPECTEDLY · FAILED_FOR_WRONG_REASON
  2  Usage error          (message lists what was tried)
  3  Nothing ran          NOT_COLLECTED · NO_TASKS
  4  Environment error    pnpm missing, repo root / package / script not found
  5  Runner error         turbo/Vitest crashed, timed out, or produced no result
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

EXIT_OK, EXIT_EXPECTATION_NOT_MET, EXIT_USAGE = 0, 1, 2
EXIT_NOTHING_RAN, EXIT_ENV, EXIT_RUNNER = 3, 4, 5

PACKAGE_ALIASES = {
    "foundation": "@dxp/foundation",
    "theme": "@dxp/theme",
    "cms-utils": "@dxp/cms-utils",
    "cms-components": "@dxp/cms-components",
    "sme": "@dxp/sme-portal",
}
DEV_SCRIPT = {
    "@dxp/foundation": "pnpm run test:foundation",
    "@dxp/theme": "pnpm run test:theme",
    "@dxp/cms-utils": "pnpm run test:cms-utils",
    "@dxp/cms-components": "pnpm run test:cms-components",
    "@dxp/sme-portal": "pnpm run test:sme",
}
DEFAULT_SUITE_SCRIPT = "test:parallel"
DEFAULT_COVERAGE_SCRIPT = "test:coverage"

# Sub-folders commonly holding the workspace when the script is run from above it.
NESTED_ROOT_CANDIDATES = ("src", "Src", "repo", "app")
ROOT_MARKERS = ("pnpm-workspace.yaml", "turbo.json")

CONFIG_NAMES = [f"{b}.{e}" for b in ("vitest.config", "vite.config")
                for e in ("ts", "mts", "cts", "js", "mjs", "cjs")]
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".turbo", "coverage", ".SS_WF"}
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
MAX_MESSAGE = 800


# ═══════════════════════════════════════════════════════════ helpers

def fail(code: int, message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def clean(text: str, limit: int = MAX_MESSAGE) -> str:
    text = ANSI.sub("", text or "").strip()
    return text if len(text) <= limit else text[:limit] + " …[truncated]"


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def is_root(path: Path) -> bool:
    return any((path / marker).exists() for marker in ROOT_MARKERS)


def find_repo_root(start: Path, script_dir: Path) -> tuple[Path | None, list[str]]:
    """
    Locate the workspace root without being told.

      1. `start` and its parents          — the usual case
      2. known sub-folders of those       — script run one level above the repo
      3. `start`/its parents relative to the script's own location
    Returns (root, tried) so a failure can explain itself.
    """
    tried: list[str] = []

    def probe(candidate: Path) -> Path | None:
        tried.append(str(candidate))
        return candidate if is_root(candidate) else None

    for base in [start, *start.parents]:
        if (found := probe(base)):
            return found, tried
        for nested in NESTED_ROOT_CANDIDATES:
            if (found := probe(base / nested)):
                return found, tried

    for base in [script_dir, *script_dir.parents]:
        if (found := probe(base)):
            return found, tried
        for nested in NESTED_ROOT_CANDIDATES:
            if (found := probe(base / nested)):
                return found, tried

    return None, tried


def resolve_input_path(value: str, repo_root: Path, cwd: Path) -> tuple[Path | None, list[str]]:
    """
    Resolve a user-supplied path without caring which form it is in.

    Tries, in order: absolute · relative to cwd · relative to repo root ·
    repo root with a leading duplicate segment stripped (e.g. `src/...` passed
    when the repo root already IS `.../src`).
    """
    candidate = Path(value)
    attempts: list[Path] = []
    if candidate.is_absolute():
        attempts.append(candidate)
    else:
        attempts += [cwd / candidate, repo_root / candidate]
        parts = candidate.parts
        if parts and parts[0] == repo_root.name:
            attempts.append(repo_root / Path(*parts[1:]))
        attempts.append(repo_root.parent / candidate)

    tried = []
    for attempt in attempts:
        resolved = attempt.resolve()
        text = str(resolved)
        if text not in tried:
            tried.append(text)
        if resolved.exists():
            return resolved, tried
    return None, tried


def suggest_similar(value: str, repo_root: Path, limit: int = 5) -> list[str]:
    """Find files sharing the basename — catches casing and prefix mistakes."""
    name = Path(value).name
    if not name:
        return []
    matches = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for filename in filenames:
            if filename.lower() == name.lower():
                matches.append(rel(Path(dirpath) / filename, repo_root))
                if len(matches) >= limit:
                    return matches
    return matches


def owning_package(path: Path, repo_root: Path) -> tuple[str, Path] | None:
    current = path if path.is_dir() else path.parent
    while current != repo_root and repo_root in current.parents:
        manifest = read_json(current / "package.json")
        if manifest and manifest.get("name"):
            return manifest["name"], current
        current = current.parent
    return None


def discover_packages(repo_root: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        if len(Path(dirpath).relative_to(repo_root).parts) > 5:
            dirnames[:] = []
            continue
        if "package.json" in filenames and Path(dirpath) != repo_root:
            manifest = read_json(Path(dirpath) / "package.json")
            if manifest and manifest.get("name"):
                found[manifest["name"]] = Path(dirpath)
    return found


def rel(path: Path | str, base: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(base))
    except ValueError:
        return str(path)


def execute(repo_root: Path, cmd: list[str], log_path: Path, timeout: int,
            extra_env: dict | None = None) -> tuple[int, str, bool]:
    env = {**os.environ, "CI": "true", "FORCE_COLOR": "0", "NO_COLOR": "1",
           "TURBO_UI": "false", **(extra_env or {})}
    timed_out = False
    try:
        proc = subprocess.run(cmd, cwd=repo_root, env=env, capture_output=True,
                              text=True, timeout=timeout)
        output, code = (proc.stdout or "") + (proc.stderr or ""), proc.returncode
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout or ""
        if isinstance(partial, bytes):
            partial = partial.decode(errors="replace")
        output, code, timed_out = f"{partial}\nTIMEOUT after {timeout}s", 124, True
    except FileNotFoundError as exc:
        output, code = f"Command not found: {exc}", 127
    output = ANSI.sub("", output)
    log_path.write_text(output, encoding="utf-8")
    return code, output, timed_out


# ═══════════════════════════════════════════════════════════ vitest config

def _strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(?<![:'\"`])//[^\n]*", "", text)


def _read_expression(text: str, start: int) -> str:
    depth, quote, i = 0, "", start
    while i < len(text) and i - start < 400:
        ch = text[i]
        if quote:
            if ch == quote and text[i - 1] != "\\":
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
    return text[start:i]


def _config_value(text: str, key: str) -> tuple[str, str] | None:
    match = re.search(rf"(?<![\w.$]){re.escape(key)}\s*:\s*", text)
    if not match:
        return None
    expression = _read_expression(text, match.end())
    literals = re.findall(r"""['"`]([^'"`]+)['"`]""", expression)
    return (literals[-1], expression.strip()) if literals else None


def package_test_script(pkg_dir: Path) -> tuple[list[str], Path | None, str]:
    manifest = read_json(pkg_dir / "package.json") or {}
    script = (manifest.get("scripts") or {}).get("test", "") or ""
    flags, config = [], None
    for opt in ("--config", "-c", "--root", "-r", "--dir"):
        match = re.search(rf"(?:^|\s){re.escape(opt)}(?:=|\s+)(?!-)(\S+)", script)
        if match:
            flags += [opt, match.group(1)]
            if opt in ("--config", "-c"):
                config = (pkg_dir / match.group(1)).resolve()
    return flags, config, script


def detect_scan_dir(pkg_dir: Path, flags: list[str], explicit_config: Path | None) -> tuple[Path, str]:
    def resolve_literal(base: Path, literal: str, expression: str) -> Path:
        anchored = "__dirname" in expression or "import.meta" in expression
        return ((pkg_dir if anchored else base) / literal).resolve()

    root, scan_dir, notes = pkg_dir, None, []
    config = explicit_config if explicit_config and explicit_config.exists() else \
        next((pkg_dir / n for n in CONFIG_NAMES if (pkg_dir / n).exists()), None)

    if config:
        try:
            text = _strip_comments(config.read_text(encoding="utf-8"))
        except OSError:
            text = ""
        if (found := _config_value(text, "root")):
            candidate = resolve_literal(pkg_dir, *found)
            if candidate.is_dir():
                root, _ = candidate, notes.append(f"root: {found[1]}")
        if (found := _config_value(text, "dir")):
            candidate = resolve_literal(root, *found)
            if candidate.is_dir():
                scan_dir, _ = candidate, notes.append(f"dir: {found[1]}")
        notes.insert(0, config.name)
    else:
        notes.append("no vitest config found")

    for i in range(0, len(flags), 2):
        opt, value = flags[i], flags[i + 1]
        if opt in ("--root", "-r") and (pkg_dir / value).resolve().is_dir():
            root = (pkg_dir / value).resolve()
            notes.append(f"test script {opt} {value}")
        elif opt == "--dir" and (root / value).resolve().is_dir():
            scan_dir = (root / value).resolve()
            notes.append(f"test script --dir {value}")

    return scan_dir or root, " · ".join(notes)


def path_forms(files: list[Path], scan_dir: Path, pkg_dir: Path) -> list[tuple[str, list[str]]]:
    forms: list[tuple[str, list[str]]] = []
    try:
        forms.append(("scan-dir-relative", ["./" + str(f.relative_to(scan_dir)) for f in files]))
    except ValueError:
        pass
    forms.append(("absolute", [str(f) for f in files]))
    try:
        forms.append(("package-relative", [str(f.relative_to(pkg_dir)) for f in files]))
    except ValueError:
        pass
    seen, unique = set(), []
    for label, targets in forms:
        if tuple(targets) not in seen:
            seen.add(tuple(targets))
            unique.append((label, targets))
    return unique


# ═══════════════════════════════════════════════════════════ targeted engine

def build_vitest_command(mode: str, package: str, targets: list[str], forwarded: list[str],
                         json_path: Path, name: str | None, coverage: bool) -> list[str]:
    cmd = ["pnpm", "--filter", package, "exec", "vitest"]
    cmd += ["related", "--run", *targets] if mode == "related" else ["run", *targets]
    cmd += forwarded
    if name:
        cmd += ["-t", name]
    if coverage:
        cmd += ["--coverage"]
    cmd += ["--reporter=default", "--reporter=json", f"--outputFile.json={json_path}"]
    return cmd


def parse_json_report(json_path: Path, repo_root: Path) -> dict | None:
    data = read_json(json_path)
    if data is None:
        return None
    files, failed, suite_errors = [], [], []
    passed = failed_count = skipped = 0
    for suite_result in data.get("testResults", []):
        file_rel = rel(suite_result.get("name", ""), repo_root)
        counts = {"passed": 0, "failed": 0, "skipped": 0}
        for test in suite_result.get("assertionResults", []) or []:
            status = test.get("status", "")
            if status == "passed":
                counts["passed"] += 1
            elif status == "failed":
                counts["failed"] += 1
                failed.append({"file": file_rel,
                               "test": test.get("fullName") or test.get("title", ""),
                               "message": clean("\n".join(test.get("failureMessages", []) or []))})
            else:
                counts["skipped"] += 1
        if suite_result.get("status") == "failed" and counts["failed"] == 0:
            suite_errors.append({"file": file_rel, "message": clean(suite_result.get("message", ""))})
        passed += counts["passed"]
        failed_count += counts["failed"]
        skipped += counts["skipped"]
        files.append({"file": file_rel, **counts, "suite_status": suite_result.get("status", "")})
    return {"files": files, "failed": failed, "suite_errors": suite_errors,
            "passed": passed, "failed_count": failed_count, "skipped": skipped}


def run_targeted_package(repo_root: Path, pkg_name: str, pkg_dir: Path, mode: str,
                         files: list[Path], targets: list[str], out_dir: Path, safe: str,
                         name: str | None, coverage: bool, timeout: int) -> dict:
    forwarded, explicit_config, test_script = package_test_script(pkg_dir)
    scan_dir, scan_source = detect_scan_dir(pkg_dir, forwarded, explicit_config)
    requested = [rel(f, repo_root) for f in files]
    candidates = path_forms(files, scan_dir, pkg_dir) if files else [("targets", targets)]

    attempts, chosen = [], None
    for index, (form, form_targets) in enumerate(candidates):
        json_path = out_dir / f"{safe}.{index}.json"
        log_path = out_dir / f"{safe}.{index}.log"
        cmd = build_vitest_command(mode, pkg_name, form_targets, forwarded, json_path, name, coverage)
        started = time.time()
        code, output, timed_out = execute(repo_root, cmd, log_path, timeout)
        report = parse_json_report(json_path, repo_root)
        collected = {f["file"] for f in report["files"]} if report else set()
        attempt = {"form": form, "targets": form_targets, "command": " ".join(cmd),
                   "exit_code": code, "timed_out": timed_out,
                   "duration_s": round(time.time() - started, 1),
                   "log": rel(log_path, repo_root), "report": report, "output": output,
                   "missing": [r for r in requested if r not in collected],
                   "extra": sorted(collected - set(requested)) if requested else []}
        attempts.append(attempt)
        if timed_out or not files or (report is not None and not attempt["missing"]):
            chosen = attempt
            break
    if chosen is None:
        chosen = min(attempts, key=lambda a: (len(a["missing"]), a["report"] is None))

    return {"pkg_name": pkg_name, "scan_dir": scan_dir, "scan_source": scan_source,
            "test_script": test_script, "requested": requested,
            "chosen": chosen, "attempts": attempts}


def dev_reproduce(pkg_name: str, targets: list[str], name: str | None) -> str:
    script = DEV_SCRIPT.get(pkg_name)
    if not script:
        return ""
    parts = [script, "--", "--run", *targets]
    if name:
        parts += ["-t", f'"{name}"']
    return " ".join(parts) if targets else script


def decide_targeted(expect: str, name: str | None, totals: dict, not_collected: list,
                    runner_errors: list) -> tuple[str, int, str]:
    if runner_errors:
        return "RUNNER_ERROR", EXIT_RUNNER, "Vitest crashed, timed out or produced no report — see logs."
    if not_collected:
        return ("NOT_COLLECTED", EXIT_NOTHING_RAN,
                "Requested test files were never run under any path form. NEVER a pass — check "
                "the file sits inside the package's vitest include pattern.")
    ran = totals["passed"] + totals["failed_count"]
    suite_errors = totals["suite_errors"]
    if expect == "pass":
        if ran == 0 and not suite_errors:
            return "NOT_COLLECTED", EXIT_NOTHING_RAN, "No tests executed."
        if totals["failed_count"] == 0 and not suite_errors:
            return "PASS", EXIT_OK, "All executed tests passed."
        return "FAIL", EXIT_EXPECTATION_NOT_MET, "One or more tests failed or a suite errored."
    if suite_errors and totals["failed_count"] == 0:
        return ("FAILED_FOR_WRONG_REASON", EXIT_EXPECTATION_NOT_MET,
                "The suite failed to load (import/compile/setup error), not on an assertion. "
                "This does NOT prove the root cause. Fix the test setup, not the assertion.")
    if totals["failed_count"] == 0:
        return ("PASSED_UNEXPECTEDLY", EXIT_EXPECTATION_NOT_MET,
                "The test passed against current code. The root cause is wrong — return to RCA.")
    if name and not any(name.lower() in f["test"].lower() for f in totals["failed"]):
        return ("FAILED_FOR_WRONG_REASON", EXIT_EXPECTATION_NOT_MET,
                f"Tests failed, but none matching '{name}'. A different test failed.")
    if suite_errors:
        return ("FAILED_FOR_WRONG_REASON", EXIT_EXPECTATION_NOT_MET,
                "The target failed, but other suites also errored — the failure is not isolated.")
    return "EXPECTED_FAIL", EXIT_OK, "Target test failed on an assertion, as required."


def targeted(args, repo_root: Path, cwd: Path, packages: dict[str, Path],
             out_dir: Path) -> tuple[dict, int]:
    plan: dict[str, dict] = {}

    def resolve_or_fail(value: str, kind: str) -> Path:
        path, tried = resolve_input_path(value, repo_root, cwd)
        if path:
            return path
        lines = [f"{kind} not found: {value}",
                 f"  repo root: {repo_root}",
                 "  tried:"] + [f"    {t}" for t in tried]
        if (similar := suggest_similar(value, repo_root)):
            lines += ["  files with the same name in the repo:"] + [f"    {s}" for s in similar]
            lines.append("  → check the folder casing and the leading path segments")
        fail(EXIT_USAGE, "\n".join(lines))

    if args.files:
        for value in args.files:
            path = resolve_or_fail(value, "Test file")
            owner = owning_package(path, repo_root)
            if not owner:
                fail(EXIT_ENV, f"No owning package.json between {repo_root} and {path}")
            plan.setdefault(owner[0], {"mode": "run", "dir": owner[1], "files": [], "targets": []})
            plan[owner[0]]["files"].append(path)
    elif args.related:
        sources = [resolve_or_fail(v, "Source file") for v in args.related]
        if args.related_scope == "all":
            names = list(packages)
        else:
            names = []
            for src in sources:
                owner = owning_package(src, repo_root)
                if not owner:
                    fail(EXIT_ENV, f"No owning package.json for: {src}")
                if owner[0] not in names:
                    names.append(owner[0])
        for pkg in names:
            plan[pkg] = {"mode": "related", "dir": packages[pkg], "files": [],
                         "targets": [str(s) for s in sources]}
    else:
        for value in args.package:
            pkg = PACKAGE_ALIASES.get(value, value)
            if pkg not in packages:
                known = ", ".join(sorted(packages)) or "none discovered"
                fail(EXIT_ENV, f"Package not found: {pkg}\n  known packages: {known}")
            plan[pkg] = {"mode": "run", "dir": packages[pkg], "files": [], "targets": []}

    if args.dry_run:
        for pkg, entry in plan.items():
            forwarded, config, _ = package_test_script(entry["dir"])
            scan_dir, source = detect_scan_dir(entry["dir"], forwarded, config)
            forms = path_forms(entry["files"], scan_dir, entry["dir"]) if entry["files"] \
                else [("targets", entry["targets"])]
            form, form_targets = forms[0]
            print(f"# repo root: {repo_root}")
            print(f"# {pkg} · scan dir: {rel(scan_dir, repo_root)} ({source}) · form: {form}")
            print(" ".join(build_vitest_command(entry["mode"], pkg, form_targets, forwarded,
                                                out_dir / "report.json", args.name, args.coverage)))
        sys.exit(EXIT_OK)

    results, not_collected, runner_errors = [], [], []
    totals = {"passed": 0, "failed_count": 0, "skipped": 0, "failed": [], "suite_errors": []}

    for pkg, entry in plan.items():
        safe = pkg.replace("@", "").replace("/", "_")
        run = run_targeted_package(repo_root, pkg, entry["dir"], entry["mode"], entry["files"],
                                   entry["targets"], out_dir, safe, args.name, args.coverage,
                                   args.timeout or 600)
        chosen = run["chosen"]
        record = {
            "package": pkg, "mode": entry["mode"],
            "scan_dir": rel(run["scan_dir"], repo_root), "scan_dir_source": run["scan_source"],
            "path_form": chosen["form"], "command": chosen["command"],
            "developer_equivalent": dev_reproduce(pkg, chosen["targets"] if entry["files"] else [],
                                                  args.name),
            "exit_code": chosen["exit_code"], "duration_s": chosen["duration_s"],
            "log": chosen["log"],
            "attempts": [{"form": a["form"], "exit_code": a["exit_code"],
                          "collected_all": not a["missing"] and a["report"] is not None}
                         for a in run["attempts"]],
        }
        report = chosen["report"]
        if report is None:
            if chosen["timed_out"]:
                record["status"] = "TIMEOUT"
                runner_errors.append(pkg)
            elif "No test files found" in chosen["output"] or run["requested"]:
                record["status"] = "NOT_COLLECTED"
                not_collected.extend(run["requested"] or [f"{pkg} (no test files matched)"])
            elif entry["mode"] == "related" and chosen["exit_code"] == 0:
                record["status"] = "NO_RELATED_TESTS"
            else:
                record["status"] = "RUNNER_ERROR"
                record["tail"] = clean(chosen["output"][-1500:], 1500)
                runner_errors.append(pkg)
            results.append(record)
            continue

        not_collected.extend(chosen["missing"])
        record.update({"status": "RAN", "files": report["files"], "passed": report["passed"],
                       "failed": report["failed_count"], "skipped": report["skipped"],
                       "not_collected": chosen["missing"], "also_ran": chosen["extra"]})
        results.append(record)
        totals["passed"] += report["passed"]
        totals["failed_count"] += report["failed_count"]
        totals["skipped"] += report["skipped"]
        totals["failed"].extend(report["failed"])
        totals["suite_errors"].extend(report["suite_errors"])

    verdict, exit_code, reason = decide_targeted(args.expect, args.name, totals,
                                                 not_collected, runner_errors)
    summary = {
        "engine": "targeted", "label": args.label, "expect": args.expect, "name_filter": args.name,
        "verdict": verdict, "expectation_met": exit_code == EXIT_OK, "reason": reason,
        "repo_root": str(repo_root),
        "totals": {"passed": totals["passed"], "failed": totals["failed_count"],
                   "skipped": totals["skipped"], "suite_errors": len(totals["suite_errors"]),
                   "not_collected": len(not_collected)},
        "failed_tests": totals["failed"], "suite_errors": totals["suite_errors"],
        "not_collected": not_collected, "packages": results,
    }

    t = summary["totals"]
    print(f"TEST RUN — {args.label}")
    print(f"  Verdict:   {verdict}   (expected: {args.expect})")
    print(f"  Reason:    {reason}")
    print(f"  Totals:    {t['passed']} passed · {t['failed']} failed · {t['skipped']} skipped · "
          f"{t['suite_errors']} suite errors · {t['not_collected']} not collected")
    for r in results:
        tried = " → ".join(f"{a['form']}{'✓' if a['collected_all'] else '✗'}" for a in r["attempts"])
        print(f"  Package:   {r['package']:<22} {r['status']:<16} exit={r['exit_code']}  {r['duration_s']}s")
        print(f"             scan dir: {r['scan_dir']}  ·  form: {r['path_form']}  ·  tried: {tried}")
        if r["developer_equivalent"]:
            print(f"             reproduce: {r['developer_equivalent']}")
        for extra in r.get("also_ran", []):
            print(f"  ℹ ALSO RAN  {extra}   (filter matched an unrequested file)")
    for f in totals["failed"]:
        print(f"  ✗ FAILED  {f['file']} › {f['test']}")
        if f["message"]:
            print("      " + f["message"].replace("\n", "\n      ")[:400])
    for e in totals["suite_errors"]:
        print(f"  ⚠ SUITE ERROR  {e['file']}")
    for n in not_collected:
        print(f"  ⚠ NOT COLLECTED  {n}")
    return summary, exit_code


# ═══════════════════════════════════════════════════════════ suite engine

def turbo_task(script_command: str) -> str | None:
    match = re.search(r"\bturbo\s+(?:run\s+)?(?!-)([\w:.-]+)", script_command)
    return match.group(1) if match else None


def parse_counts(text: str) -> dict:
    counts = {}
    for key in ("failed", "passed", "skipped", "todo"):
        match = re.search(rf"(\d+)\s+{key}", text)
        counts[key] = int(match.group(1)) if match else 0
    total = re.search(r"\((\d+)\)", text)
    counts["total"] = int(total.group(1)) if total else sum(counts.values())
    return counts


def summarise_package_log(lines: list[str]) -> dict:
    cache = None
    for line in lines:
        low = line.lower()
        if "cache hit" in low:
            cache = "hit"
        elif "cache miss" in low:
            cache = "miss"
        elif "cache bypass" in low:
            cache = "bypass"
    test_files = tests = None
    failures, seen = [], set()
    for line in lines:
        if (m := re.match(r"^\s*Test Files\s+(.*)$", line)):
            test_files = parse_counts(m.group(1))
        elif (m := re.match(r"^\s*Tests\s{2,}(\d.*)$", line)):
            tests = parse_counts(m.group(1))
        elif (m := re.match(r"^\s*FAIL\s+(\S.*?)\s*$", line)):
            parts = [p.strip() for p in m.group(1).split(" > ")]
            key = (parts[0], " > ".join(parts[1:]))
            if key not in seen:
                seen.add(key)
                failures.append({"file": key[0], "test": key[1]})
    return {"cache": cache, "test_files": test_files, "tests": tests,
            "failures_from_log": failures,
            "no_test_files": any("No test files found" in l for l in lines),
            "errored": any(re.search(r"ELIFECYCLE|ERR_PNPM|exited \(\d+\)", l) for l in lines)}


def suite(args, repo_root: Path, cwd: Path, packages: dict[str, Path],
          out_dir: Path) -> tuple[dict, int]:
    scripts = (read_json(repo_root / "package.json") or {}).get("scripts", {}) or {}
    script = args.script or (DEFAULT_COVERAGE_SCRIPT if args.coverage else DEFAULT_SUITE_SCRIPT)
    if script not in scripts:
        available = ", ".join(sorted(s for s in scripts if s.startswith("test"))) or "none"
        fail(EXIT_ENV, f"Root package.json ({repo_root}) has no '{script}' script.\n"
                       f"  test scripts available: {available}")

    script_command = scripts[script]
    task = turbo_task(script_command)
    cmd = ["pnpm", "run", script]
    extra_env = {"TURBO_FORCE": "true"} if args.force else {}
    timeout = args.timeout or 1800

    if args.dry_run:
        print(f"# repo root: {repo_root}")
        print(f"# {script} = {script_command} · turbo task: {task or 'n/a'}"
              + (" (TURBO_FORCE=true)" if args.force else ""))
        print(" ".join(cmd))
        sys.exit(EXIT_OK)

    started = time.time()
    code, output, timed_out = execute(repo_root, cmd, out_dir / "suite.log", timeout, extra_env)
    duration = round(time.time() - started, 1)

    per_package: dict[str, list[str]] = {}
    unprefixed: list[str] = []
    prefix = re.compile(rf"^(?P<pkg>\S+?):{re.escape(task)}: ?(?P<line>.*)$") if task else None
    for raw in output.splitlines():
        match = prefix.match(raw) if prefix else None
        if match:
            per_package.setdefault(match.group("pkg"), []).append(match.group("line"))
        else:
            unprefixed.append(raw)
    if not prefix:
        per_package = {"(root)": output.splitlines()}

    turbo = {"successful": None, "total": None, "cached": None, "time": None, "failed": []}
    for line in unprefixed:
        if (m := re.search(r"Tasks:\s+(\d+)\s+successful,\s+(\d+)\s+total", line)):
            turbo["successful"], turbo["total"] = int(m.group(1)), int(m.group(2))
        if (m := re.search(r"Cached:\s+(\d+)\s+cached,\s+(\d+)\s+total", line)):
            turbo["cached"] = int(m.group(1))
        if (m := re.search(r"^\s*Time:\s+(.+?)\s*$", line)):
            turbo["time"] = m.group(1)
        if "Failed:" in line:
            turbo["failed"] += [p for p in re.findall(r"([@\w./-]+)#", line)
                                if p not in turbo["failed"]]
    for pkg in turbo["failed"]:
        per_package.setdefault(pkg, [])

    results = []
    totals = {"tests_passed": 0, "tests_failed": 0, "tests_skipped": 0,
              "files_passed": 0, "files_failed": 0}
    for pkg, lines in sorted(per_package.items()):
        info = summarise_package_log(lines)
        counts_failed = (info["tests"] or {}).get("failed", 0) or \
                        (info["test_files"] or {}).get("failed", 0)
        if pkg in turbo["failed"] or info["errored"] or counts_failed:
            status = "NO_TEST_FILES" if info["no_test_files"] else "FAILED"
        elif info["tests"] or info["test_files"]:
            status = "PASSED"
        else:
            status = "PASSED" if code == 0 else "UNKNOWN"
        if info["tests"]:
            totals["tests_passed"] += info["tests"]["passed"]
            totals["tests_failed"] += info["tests"]["failed"]
            totals["tests_skipped"] += info["tests"]["skipped"] + info["tests"]["todo"]
        if info["test_files"]:
            totals["files_passed"] += info["test_files"]["passed"]
            totals["files_failed"] += info["test_files"]["failed"]
        results.append({"package": pkg, "status": status, "cache": info["cache"],
                        "tests": info["tests"], "test_files": info["test_files"],
                        "failures_from_log": info["failures_from_log"]})

    failed_packages = [r for r in results if r["status"] in ("FAILED", "NO_TEST_FILES")]

    drill = []
    if failed_packages and not args.no_drill_down and not timed_out:
        drill_dir = out_dir / "drill-down"
        drill_dir.mkdir(exist_ok=True)
        for r in failed_packages:
            if r["status"] != "FAILED" or r["package"] not in packages:
                continue
            safe = r["package"].replace("@", "").replace("/", "_")
            run = run_targeted_package(repo_root, r["package"], packages[r["package"]], "run",
                                       [], [], drill_dir, safe, None, False, args.timeout or 600)
            report = run["chosen"]["report"]
            entry = {"package": r["package"], "log": run["chosen"]["log"]}
            if report is None:
                entry["status"] = "NO_REPORT"
            elif report["failed_count"] == 0 and not report["suite_errors"]:
                entry["status"] = "PASSED_ON_RERUN"
                entry["note"] = ("Failed under turbo but passed alone — possible flaky, "
                                 "order-dependent or parallelism-sensitive test.")
            else:
                entry["status"] = "FAILED"
            if report:
                entry.update({"failed_tests": report["failed"],
                              "suite_errors": report["suite_errors"]})
            drill.append(entry)

    if timed_out:
        verdict, exit_code, reason = "RUNNER_ERROR", EXIT_RUNNER, f"Suite timed out after {timeout}s."
    elif code == 0:
        if turbo["total"] == 0:
            verdict, exit_code, reason = "NO_TASKS", EXIT_NOTHING_RAN, "Turbo executed no test tasks."
        elif failed_packages:
            verdict, exit_code, reason = ("FAIL", EXIT_EXPECTATION_NOT_MET,
                                          "Command exited 0 but the log reports failing tests.")
        else:
            verdict, exit_code, reason = "PASS", EXIT_OK, "All test tasks passed."
    elif failed_packages:
        names = ", ".join(r["package"] for r in failed_packages)
        verdict, exit_code, reason = ("FAIL", EXIT_EXPECTATION_NOT_MET,
                                      f"{len(failed_packages)} package(s) failed: {names}.")
    else:
        verdict, exit_code, reason = ("RUNNER_ERROR", EXIT_RUNNER,
                                      f"Command exited {code} with no failing package identified — "
                                      "see suite.log.")

    failed_tests = [dict(t, package=d["package"]) for d in drill for t in d.get("failed_tests", [])]
    if not failed_tests:
        failed_tests = [dict(f, package=r["package"], message="")
                        for r in failed_packages for f in r["failures_from_log"]]

    summary = {
        "engine": "suite", "label": args.label, "script": script, "script_command": script_command,
        "command": " ".join(cmd), "force": bool(args.force), "repo_root": str(repo_root),
        "verdict": verdict, "expectation_met": exit_code == EXIT_OK, "reason": reason,
        "exit_code": code, "duration_s": duration, "turbo": turbo, "totals": totals,
        "packages": results, "failed_tests": failed_tests, "drill_down": drill,
        "log": rel(out_dir / "suite.log", repo_root),
        "developer_equivalent": " ".join(cmd) + ("   (TURBO_FORCE=true)" if args.force else ""),
    }

    print(f"TEST SUITE — {args.label}")
    print(f"  Command:   {' '.join(cmd)}   →  {script_command}"
          + ("   [TURBO_FORCE]" if args.force else ""))
    print(f"  Verdict:   {verdict}")
    print(f"  Reason:    {reason}")
    if turbo["total"] is not None:
        print(f"  Turbo:     {turbo['successful']} successful · {turbo['total']} total · "
              f"{turbo['cached'] if turbo['cached'] is not None else '?'} cached · "
              f"{turbo['time'] or f'{duration}s'}")
    print(f"  Tests:     {totals['tests_passed']} passed · {totals['tests_failed']} failed · "
          f"{totals['tests_skipped']} skipped   ·   files {totals['files_passed']} passed · "
          f"{totals['files_failed']} failed")
    print(f"  {'Package':<24}{'Status':<16}{'Tests p/f/s':<16}{'Files p/f':<12}Cache")
    for r in results:
        t, f = r["tests"], r["test_files"]
        tests_col = f"{t['passed']}/{t['failed']}/{t['skipped'] + t['todo']}" if t else "—"
        files_col = f"{f['passed']}/{f['failed']}" if f else "—"
        print(f"  {r['package']:<24}{r['status']:<16}{tests_col:<16}{files_col:<12}{r['cache'] or '—'}")
    for t in failed_tests:
        print(f"  ✗ FAILED  [{t['package']}] {t['file']} › {t.get('test', '')}")
    for d in drill:
        if d["status"] == "PASSED_ON_RERUN":
            print(f"  ⚠ PASSED ON RE-RUN  {d['package']} — {d['note']}")
    return summary, exit_code


# ═══════════════════════════════════════════════════════════ main

def main() -> None:
    parser = argparse.ArgumentParser(description="Run monorepo tests and return a verdict.")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true")
    scope.add_argument("--files", nargs="+")
    scope.add_argument("--related", nargs="+")
    scope.add_argument("--package", nargs="+")
    scope.add_argument("--where", action="store_true",
                       help="Print the detected repo root and packages, then exit")
    parser.add_argument("--script")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-drill-down", action="store_true")
    parser.add_argument("--related-scope", choices=["owner", "all"], default="owner")
    parser.add_argument("--name")
    parser.add_argument("--expect", choices=["pass", "fail"], default="pass")
    parser.add_argument("--coverage", action="store_true")
    parser.add_argument("--label", default="run")
    parser.add_argument("--out-dir")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--repo-root")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.expect == "fail" and not args.files:
        fail(EXIT_USAGE, "--expect fail is only valid with --files (a specific regression test).")
    if args.all and args.name:
        fail(EXIT_USAGE, "--name is not supported with --all. Use --files or --package.")

    cwd = Path.cwd().resolve()
    script_dir = Path(__file__).resolve().parent

    if args.repo_root:
        given = Path(args.repo_root)
        repo_root = (given if given.is_absolute() else cwd / given).resolve()
        if not repo_root.is_dir():
            fail(EXIT_ENV, f"--repo-root does not exist: {repo_root}")
        if not is_root(repo_root):
            fail(EXIT_ENV, f"--repo-root has no {' or '.join(ROOT_MARKERS)}: {repo_root}")
    else:
        repo_root, tried = find_repo_root(cwd, script_dir)
        if not repo_root:
            fail(EXIT_ENV, "Repository root not found (no pnpm-workspace.yaml or turbo.json).\n"
                           f"  cwd: {cwd}\n  tried:\n" + "\n".join(f"    {t}" for t in tried[:12])
                           + "\n  → pass --repo-root <path>")

    packages = discover_packages(repo_root)

    if args.where:
        print(f"repo root:  {repo_root}")
        print(f"script:     {Path(__file__).resolve()}")
        print(f"cwd:        {cwd}")
        print("packages:")
        for name, directory in sorted(packages.items()):
            forwarded, config, _ = package_test_script(directory)
            scan_dir, source = detect_scan_dir(directory, forwarded, config)
            print(f"  {name:<24} dir={rel(directory, repo_root):<38} "
                  f"scan={rel(scan_dir, repo_root)}  ({source})")
        sys.exit(EXIT_OK)

    if not args.dry_run and not shutil.which("pnpm"):
        fail(EXIT_ENV, "pnpm is not available on PATH.")

    stamp = time.strftime("%Y%m%d-%H%M%S")
    if args.out_dir:
        out_dir = Path(args.out_dir).resolve()
    elif (repo_root / ".SS_WF").is_dir():
        out_dir = repo_root / ".SS_WF" / "Agent" / "TEST_RUNS" / f"{args.label}-{stamp}"
    else:
        out_dir = Path(tempfile.mkdtemp(prefix=f"test-run-{args.label}-"))
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    engine = suite if args.all else targeted
    summary, exit_code = engine(args, repo_root, cwd, packages, out_dir)

    summary.update({"timestamp": stamp, "output_dir": rel(out_dir, repo_root)})
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"  Output:    {summary['output_dir']}/summary.json")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
