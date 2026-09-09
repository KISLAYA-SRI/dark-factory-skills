# Fix SonarQube Issues

`fix-sonar-issues` is an agent skill for remediating SonarQube quality gate failures across all 6 quality dimensions in **Java Maven backend microservices/adapter libraries** and **Node.js/React/TypeScript frontend or backend projects**. It guides the agent through detecting the project family, fetching, triaging, and fixing issues with minimal, behavior-preserving changes.

Use this skill when the task involves fixing SonarQube quality gate failures, resolving Bugs, Vulnerabilities, Code Smells, Coverage gaps, Duplications, or Security Hotspots reported by a SonarQube analysis — regardless of whether the target project is a Maven service or a Node/React application.

## Applies To

- Fixing **Reliability** issues: Bugs — null/undefined dereferences, resource leaks, unhandled promise rejections, reactive stream error handling, React hook/state bugs, concurrency defects.
- Fixing **Security** issues: Vulnerabilities mapped to OWASP Top 10 — SQL/NoSQL injection, XSS, input validation gaps, dependency CVEs (Maven or npm/yarn/pnpm), hardcoded credentials, sensitive data exposure, SSRF.
- Fixing **Maintainability** issues: Code Smells — high cognitive complexity, dead code, magic numbers, poor naming conventions, oversized components, prop drilling.
- Improving **Coverage**: Writing or extending JUnit 5 + Mockito unit tests (Maven) or Jest/Vitest + React Testing Library tests (Node/React), configuring JaCoCo or LCOV reporting, covering uncovered branches and exception/error paths.
- Reducing **Duplications**: Extracting shared methods/utilities, custom hooks, wrapper components, Template Method patterns, and custom constraint annotations/schemas.
- Reviewing **Security Hotspots**: Assessing each hotspot as Safe (with justification) or Fixed, covering CSRF, XSS, ReDoS, weak cryptography, path traversal, JWT handling, CORS misconfiguration.

## Purpose

This skill applies a **lazy-loading pattern**, split by both **quality dimension** and **project family**. When a SonarQube analysis is fetched, the skill first detects whether the target repository is Maven (Java), Node/React, or Mixed, then identifies which quality dimensions are failing and loads **only the relevant reference file for that dimension and project family**. This keeps the agent context lean and focused on the actual failing areas and the correct language/framework patterns, rather than loading all fix patterns for every language upfront.

All fixes are:
- **Minimal** — scoped to the reported component/line.
- **Behavior-preserving** — public APIs, runtime behavior, and test behavior are not changed.
- **Root-cause first** — suppression is a last resort, not a shortcut.
- **Language-correct** — Java/Maven patterns are never applied to JS/TS files, and vice versa.

## Project Type Detection

Before fetching or fixing anything, the agent detects the project family:

| Signal | Project Family | Reference Folder |
|---|---|---|
| `pom.xml` present, Java sources under `src/main/java` | Maven (Java) | `references/maven/` |
| `package.json` present, `.js`/`.jsx`/`.ts`/`.tsx` sources | Node/React | `references/node/` |
| Both present | Mixed | Both, matched per file's own language |

## Generic Tool Discovery Approach

This skill uses a **generic tool discovery approach** rather than hardcoded MCP tool names. Before executing any SonarQube operation, the agent:

1. **Scans all available tools** in the current execution context.
2. **Matches each required operation** to the best available tool by comparing operation intent with tool name patterns and descriptions.
3. **Prefers the most specific matching tool** when multiple variants exist.
4. **Never fails due to a missing exact tool name** — always finds the closest matching available tool.

This tool discovery step is identical regardless of project family, since it operates purely against the SonarQube server API surface (Maven and Node/React projects both publish standard SonarQube issues, hotspots, and measures).

### Tool Categories Used

The skill discovers and uses tools in the following categories at runtime:

| Category | Operation |
|---|---|
| **Project Discovery** | Discover available SonarQube projects and retrieve project keys |
| **Issue Search** | Search for bugs, vulnerabilities, and code smells |
| **Hotspot Search** | Search for security hotspots pending review |
| **Hotspot Detail** | Get full details of a specific security hotspot |
| **Hotspot Status Update** | Change the review status of a security hotspot |
| **Issue Status Update** | Change issue status (resolve, won't fix, false positive) |
| **Quality Gate Status** | Get overall quality gate status and per-condition details |
| **Quality Gate List** | List all available quality gate definitions |
| **Rule Detail** | Get full details of a specific Sonar rule |
| **Component Measures** | Get quality metrics/measures for a project component |
| **Coverage by File** | Search files by coverage metrics |
| **File Coverage Detail** | Get line-by-line and branch coverage for a specific file |
| **Metrics Search** | Search and list available SonarQube metrics |
| **Duplication Detail** | Get duplication details for a component |
| **Duplicated Files Search** | Search for files with duplicated code blocks |
| **Pull Request List** | List pull requests associated with a project |
| **Branch List** | List branches for a project |
| **Dependency Risk Search** | Search for dependency/library security risks (Maven or npm/yarn/pnpm) |
| **Code Snippet Analysis** | Analyze a code snippet to verify a fix before applying it |

## Prerequisites

Before invoking this skill, ensure the following are available:

- **SonarQube project key** and access to the SonarQube instance (via MCP tool or direct API).
- **Repository path** of the Maven or Node/React project to be fixed.
- **Branch or analysis context** (e.g., branch name, PR number, or analysis ID).
- The project builds/compiles successfully before fixes are applied.
- A SonarQube MCP tool or equivalent tooling is configured and accessible (the skill will discover the exact tool names at runtime).

## Input

The skill expects **one of the following** input modes:

### Mode A — SonarQube Project Key (Full Fetch)

Provide the SonarQube project key and repository path. The agent will:
1. Detect the project family (Maven, Node/React, or Mixed).
2. Discover available SonarQube tools at runtime.
3. Fetch all unresolved issues for the current analysis using the discovered tools.
4. Group issues by dimension and severity.
5. Load the relevant dimension reference files for the detected project family.
6. Apply fixes dimension by dimension, prioritizing BLOCKER and CRITICAL.

### Mode B — Pre-loaded Issue Context

Provide the issue details directly as code-context in the agent invocation (e.g., from a prior handoff or analysis summary). The agent will:
1. Detect the project family from the repository contents.
2. Skip the SonarQube fetch step.
3. Use the provided issue list directly.
4. Load only the reference files for the dimensions with reported issues, from the matching project-family folder.
5. Apply fixes.

> **Tip:** Use the `code-context-retrieval` skill to pre-load SonarQube analysis results as code-context before invoking this skill. This avoids redundant API calls and speeds up execution.

## How to Invoke

### With SonarQube Project Key

```
Fix SonarQube issues for project [PROJECT_KEY] on branch [BRANCH_NAME].
The repository is at [REPO_PATH].
```

### With Pre-loaded Issue Context

```
Fix the following SonarQube issues:
- [List of issues with file, line, rule, and severity]
The repository is at [REPO_PATH].
```

## References Folder

The `references/` folder is split into two project-family subfolders, each containing dimension-specific fix patterns and code examples. The skill uses a **lazy-loading pattern** — only the reference files matching the detected project family and the failing dimensions are loaded during a given remediation session.

| File | Dimension | Maven Contents | Node/React Contents |
|---|---|---|---|
| `01-reliability.md` | Reliability (Bugs) | Null pointer safety, resource leak fixes, reactive error handling, concurrency patterns | Null/undefined safety, unhandled promise rejections, async/await error handling, React hook/state bugs |
| `02-security.md` | Security (Vulnerabilities) | OWASP Top 10 mapping, SQL injection prevention, input validation, dependency CVE remediation | XSS prevention, SQL/NoSQL injection, zod/yup/joi validation, npm dependency CVE remediation, SSRF |
| `03-maintainability.md` | Maintainability (Code Smells) | Cognitive complexity reduction, dead code removal, naming conventions, boolean simplification | Cognitive complexity reduction, component sizing, dead code/unused imports, prop drilling, ESLint rule alignment |
| `04-coverage.md` | Coverage (Unit Tests) | JaCoCo configuration, JUnit 5 + Mockito patterns, reactive test patterns, coverage strategy | LCOV/Jest/Vitest configuration, React Testing Library patterns, HTTP mocking, coverage strategy |
| `05-duplications.md` | Duplications | Extract method/class patterns, Template Method, shared validators, near-duplicate handling | Extract function/hook/component patterns, shared schemas, near-duplicate handling |
| `06-security-hotspots.md` | Security Hotspots | Hotspot review workflow, CSRF/XSS/ReDoS/JWT patterns, justification templates | Hotspot review workflow, eval/XSS/ReDoS/JWT/CORS patterns, justification templates |

Paths: [`references/maven/`](./references/maven/) and [`references/node/`](./references/node/).

### When Each Reference File Is Loaded

The agent loads a reference file **only when the corresponding dimension has failing issues** in the current SonarQube analysis, and only from the folder matching the detected project family (or per-file language, for Mixed repositories):

- `01-reliability.md` — loaded when **Reliability** gate fails or Bug issues are present.
- `02-security.md` — loaded when **Security** gate fails or Vulnerability issues are present.
- `03-maintainability.md` — loaded when **Maintainability** gate fails or Code Smell issues are present.
- `04-coverage.md` — loaded when **Coverage** gate fails or coverage drops below threshold.
- `05-duplications.md` — loaded when **Duplications** gate fails or duplication density exceeds threshold.
- `06-security-hotspots.md` — loaded when **Security Hotspots** are unresolved or require review.

## Expected Output

After remediation, the skill produces a structured report:

### Fix Report

| Category | Details |
|---|---|
| Detected Project Family | Maven, Node/React, or Mixed |
| Issues Fixed | Grouped by file and SonarQube rule |
| Issues Suppressed | Rule, suppression style, and reason |
| Issues Skipped | Rule and reason (ambiguous, risky, or out of scope) |
| Files Changed | Brief behavior-preserving summary per file |
| Validation Result | Build/test command used and outcome |

### Validation

- **Maven/Java**: `mvn compile`/`mvn verify` for build validation, `mvn test` or a targeted test class for test validation.
- **Node/React**: the project's existing build/lint/type-check script (e.g., `npm run build`, `tsc --noEmit`) for build validation, and its existing test script (e.g., `npm test`, `npm run test:coverage`) for test validation.
- Validation is run after all fixes in a dimension are applied, not after each individual fix.
- For Mixed repositories, validation runs per affected module using that module's own toolchain.

## Fix Principles

| Principle | Rule |
|---|---|
| Minimal scope | Fix only the reported component/line; do not refactor unrelated code |
| Behavior-preserving | Public APIs, runtime behavior, and test behavior must not change |
| Root-cause first | Prefer fixing the root cause over suppression |
| Suppression as last resort | Use the language's established suppression convention (`// NOSONAR` with a reason, or the repo's existing ESLint disable pattern) only for genuine false positives |
| Severity priority | Fix BLOCKER → CRITICAL → MAJOR → MINOR → INFO |
| Skip ambiguous findings | If a fix is risky or unclear, skip with a documented reason |
| Language-correct fixes | Never apply a Java/Maven pattern to a JS/TS file, or vice versa |

## Notes on Generic Usage

This skill is **completely project-agnostic** within its two supported families (Java Maven, and Node.js/React/TypeScript):

- All project keys, branch names, and repository paths are sourced from the invocation context — no hardcoded values.
- Package names, test file locations, and build tool configurations are derived from the existing project structure.
- The Maven fix patterns apply to standard Spring Boot, Spring WebFlux, and plain Java Maven projects.
- The Node/React fix patterns apply to standard Express/NestJS/Fastify Node backends and React/Next.js/Vite frontends written in JavaScript or TypeScript.
- No project-specific identifiers, team names, or environment URLs are embedded in the skill.
- **SonarQube tool names are discovered at runtime** — the skill does not depend on any specific MCP tool name being present.

See [SKILL.md](./SKILL.md) for the full execution rules and dimension-by-dimension workflow.
