# Code Quality Skills

This folder groups agent skills for running and remediating SonarQube-based code quality analysis on **Java Maven backend microservices/adapter libraries** and **Node.js/React/TypeScript frontend or backend projects**. The skills are split so that **running** an analysis and **fixing** its findings are handled by separate, focused skills that can be invoked independently or chained together. Both skills detect the target project's family (Maven, Node/React, or Mixed) before acting, and load only the reference material relevant to that family.

## Skills in This Folder

| Skill | Purpose |
|---|---|
| [`execute-sonar-analysis`](./execute-sonar-analysis/SKILL.md) | Detects the project family and triggers a SonarQube analysis (`mvn verify sonar:sonar` for Maven, `sonar-scanner` for Node/React) and reports the build/quality gate outcome. |
| [`fix-sonar-issues`](./fix-sonar-issues/SKILL.md) | Detects the project family, fetches, triages, and fixes SonarQube quality gate findings across all 6 quality dimensions (Reliability, Security, Maintainability, Coverage, Duplications, Security Hotspots) using language-appropriate patterns. |

## Typical Workflow

1. **Run the analysis** — use `execute-sonar-analysis` to trigger the appropriate scan command for the detected project family against the configured SonarQube server and get a pass/fail quality gate result.
2. **Remediate findings** — if the quality gate fails, hand off to `fix-sonar-issues`, which discovers SonarQube MCP tools at runtime, fetches open issues/hotspots, and applies minimal, behavior-preserving fixes grouped by dimension using patterns matched to the project's language/framework.
3. **Re-run the analysis** — after fixes are applied and validated locally, use `execute-sonar-analysis` again to confirm the quality gate now passes.

These two skills are intentionally decoupled: `execute-sonar-analysis` never inspects or fixes findings, and `fix-sonar-issues` never triggers a fresh build/scan on its own (it works from existing analysis results or pre-loaded issue context, and only runs build/test commands for validation of its own fixes).

## Applies To

- Java Maven backend microservices and adapter libraries with a SonarQube project configured, where `sonar:sonar` (or an equivalent Sonar Maven plugin goal) is resolvable from the project's `pom.xml`/parent POM or Maven configuration.
- Node.js/React/TypeScript frontend or backend projects with a SonarQube project configured, where the SonarScanner CLI (`sonar-scanner`) is resolvable via `npx` or an existing npm/yarn/pnpm script.
- Mixed repositories containing both a Maven module and a Node/React module, analyzed and remediated per module.
- CI/CD pipelines or local workflows that already publish to a SonarQube server and need agent-driven triggering and/or remediation.

## Reference Structure for Multi-Project Support

Both skills use a `references/` folder split by project family so that only the relevant patterns/commands are loaded into context:

```text
execute-sonar-analysis/scripts/
  execute-sonar.sh — deterministic runner: detects Maven vs Node/React and resolves the scanner tool

execute-sonar-analysis/references/
  maven.md   — documents the Maven command/flags the script runs
  node.md    — documents the Node/React scanner resolution order and command/flags the script runs

fix-sonar-issues/references/
  maven/     — Java/Maven fix patterns, one file per quality dimension
  node/      — Node.js/React fix patterns, one file per quality dimension
```

`execute-sonar-analysis` prefers running `scripts/execute-sonar.sh` over hand-assembling a command: the script detects the project family (presence of `pom.xml` vs `package.json`), and for Node/React resolves a `sonar-scanner` binary deterministically (`PATH` -> `node_modules/.bin` -> `npx` as a last resort) instead of always shelling out to `npx`, which would otherwise re-download the package on every run. The `references/` files document that logic and serve as a manual fallback. `fix-sonar-issues` detects the project family the same way and loads only the matching reference file(s) for the failing dimensions.

## When Not To Use

- Generic unit test execution without a Sonar analysis — use the relevant `execute-unit-tests` skill instead.
- General code review or architecture review unrelated to SonarQube quality gates — use the relevant clean-code or code-review skill instead.

See each skill's `SKILL.md` for full execution rules, and `SETUP.md` for tool-specific installation instructions.
