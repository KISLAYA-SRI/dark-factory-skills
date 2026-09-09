---
name: fix-sonar-issues
description: Use when fetching, triaging, fixing, or summarizing SonarQube quality gate issues for a Java Maven backend microservice/adapter library, or a Node.js/React/TypeScript frontend or backend project. Triggers include SonarQube, Sonar quality gate, projectKey, current analysis issues, blocker/critical/major/minor issues, code smell, vulnerability, security hotspot, unit test coverage, code duplication, or any of the 6 SonarQube quality dimensions i.e. Reliability, Security, Maintainability, Coverage, Duplications, Security Hotspots.
---

# SonarQube Issue Remediation Skill

Use this skill for comprehensive SonarQube quality gate remediation across all 6 quality dimensions, for both **Java Maven** projects and **Node.js/React/TypeScript** projects. Keep fixes minimal, behavior-preserving, and scoped to issues reported for the current analysis.

## STEP -1: Detect Project Type (MANDATORY — Run First)

Before loading any dimension reference, determine which project family the target repository belongs to. This selects which `references/<family>/` folder to use later.

| Signal | Project Family | Reference Folder |
|---|---|---|
| `pom.xml` at the repo/module root, Java sources under `src/main/java` | **Maven (Java)** | `references/maven/` |
| `package.json` at the repo root, sources under `src/` as `.js`/`.jsx`/`.ts`/`.tsx`, and either a Node backend (Express/NestJS/Fastify) or a React frontend (React/Next.js/Vite) | **Node/React** | `references/node/` |
| Both `pom.xml` and `package.json` present (e.g., a Java backend with an embedded frontend module) | **Mixed** | Use `references/maven/` for Java source paths and `references/node/` for JS/TS source paths, scoped per file |

Detection steps:

1. Look for `pom.xml` (root or module-level) and `package.json` (root or module-level) in the target repository.
2. If only one is present, that determines the project family for the whole repo.
3. If both are present, treat each affected file according to its own file extension/location — do not apply Java-specific patterns to `.ts`/`.tsx` files or vice versa.
4. If detection is ambiguous, ask for clarification (module path, monorepo layout) before proceeding rather than guessing the wrong family.

---

## Reference Files (Lazy Loading)

This skill uses a lazy-loading pattern for dimension-specific fix patterns and examples, split by project family. **When a specific dimension fails or requires attention, read the corresponding reference file from the matching `references/<family>/` folder before applying fixes.** Do not load all reference files upfront — only load the ones relevant to the failing dimensions and the detected project family for the current analysis.

| Dimension | Maven Reference | Node/React Reference | When to Load |
|---|---|---|---|
| Reliability (Bugs) | [`references/maven/01-reliability.md`](references/maven/01-reliability.md) | [`references/node/01-reliability.md`](references/node/01-reliability.md) | When Reliability gate fails or Bug issues are reported |
| Security (Vulnerabilities) | [`references/maven/02-security.md`](references/maven/02-security.md) | [`references/node/02-security.md`](references/node/02-security.md) | When Security gate fails or Vulnerability issues are reported |
| Maintainability (Code Smells) | [`references/maven/03-maintainability.md`](references/maven/03-maintainability.md) | [`references/node/03-maintainability.md`](references/node/03-maintainability.md) | When Maintainability gate fails or Code Smell issues are reported |
| Coverage (Unit Tests) | [`references/maven/04-coverage.md`](references/maven/04-coverage.md) | [`references/node/04-coverage.md`](references/node/04-coverage.md) | When Coverage gate fails or coverage drops below threshold |
| Duplications | [`references/maven/05-duplications.md`](references/maven/05-duplications.md) | [`references/node/05-duplications.md`](references/node/05-duplications.md) | When Duplications gate fails or duplication density exceeds threshold |
| Security Hotspots | [`references/maven/06-security-hotspots.md`](references/maven/06-security-hotspots.md) | [`references/node/06-security-hotspots.md`](references/node/06-security-hotspots.md) | When Security Hotspots require review or are unresolved |

For **Mixed** repositories, load the reference from the folder matching the language/extension of the specific file being fixed (e.g., a `.java` file uses `references/maven/...`, a `.tsx` file uses `references/node/...`).

---

## STEP 0: Generic Tool Discovery (MANDATORY — Run Before Any SonarQube Operation)

**Before executing any SonarQube operation, you MUST perform tool discovery.** SonarQube MCP tools may be registered under different names depending on the environment, MCP server version, or configuration. Never assume a specific tool name exists — always discover and match at runtime. This step is identical regardless of project family (Maven or Node/React) since it operates purely on the SonarQube server API surface.

### Tool Discovery Protocol

1. **Scan all available tools** in the current execution context (MCP tools, function tools, etc.).
2. **For each required SonarQube operation**, identify the best-matching available tool by comparing:
   - The operation's intent (e.g., "search for issues", "get quality gate status")
   - The tool's name patterns (look for keywords like `sonar`, `search`, `issues`, `hotspot`, `coverage`, `duplicate`, `measure`, `rule`, `branch`, `dependency`)
   - The tool's description (if available)
3. **If multiple tool variants exist** (e.g., `search_sonar_issues` vs `search_sonar_issues_in_projects`), prefer the most specific one that matches the current context.
4. **Never fail because an exact tool name is missing** — always find the closest matching available tool for the required operation.
5. **Cache the discovered tool mappings** for the duration of the current session to avoid repeated discovery overhead.

### Operation-to-Tool Matching Guide

Use the following table to match each required SonarQube operation to the best available tool. The "Look For" column describes name patterns and keywords to search for in available tools:

| Required Operation | Look For in Tool Names/Descriptions |
|---|---|
| Discover/list SonarQube projects | tools containing `project` + (`search` or `list` or `my`) |
| Search bugs, vulnerabilities, code smells | tools containing (`search` or `list`) + (`issues` or `sonar`) |
| Search security hotspots | tools containing `hotspot` + (`search` or `list`) |
| Get details of a specific hotspot | tools containing `hotspot` + (`show` or `get` or `detail`) |
| Change hotspot review status | tools containing `hotspot` + (`change` or `update` or `status`) |
| Change issue status (resolve/wontfix/false-positive) | tools containing `issue` + (`change` or `update` or `status`) |
| Get quality gate status | tools containing (`quality` or `gate`) + (`status` or `get`) |
| List quality gate definitions | tools containing (`quality` or `gate`) + `list` |
| Get rule details | tools containing `rule` + (`show` or `get` or `detail`) |
| Get component metrics/measures | tools containing (`measure` or `metric` or `component`) |
| Search files by coverage | tools containing `coverage` + (`search` or `files`) |
| Get file-level coverage details | tools containing `coverage` + (`detail` or `file` or `get`) |
| Search available metrics | tools containing `metric` + (`search` or `list`) |
| Get duplication details | tools containing `duplication` + (`get` or `detail`) |
| Search duplicated files | tools containing (`duplicate` or `duplication`) + (`search` or `files`) |
| List pull requests | tools containing `pull_request` or `pr` + `list` |
| List branches | tools containing `branch` + `list` |
| Search dependency risks | tools containing `dependency` + (`risk` or `search` or `vulnerab`) |
| Analyze/verify a code snippet | tools containing (`analyze` or `verify`) + (`code` or `snippet`) |

### Fallback Strategy

If no tool closely matches an operation:
1. Look for a more general tool that could serve the same purpose (e.g., a generic `search` or `query` tool that accepts SonarQube API parameters).
2. Check if the operation can be approximated using a combination of available tools.
3. If no suitable tool exists, document the gap and skip that operation with a clear reason.

---

## Available SonarQube Tool Categories

All SonarQube data retrieval and status updates must use discovered MCP tools. There is **no** generic `fetch` tool — use only dedicated SonarQube MCP tools discovered via the protocol in STEP 0. The following categories of tools are expected to be available (discover the actual tool names at runtime):

| Category | Purpose |
|---|---|
| **Project Discovery** | Discover available SonarQube projects and retrieve project keys |
| **Issue Search** | Search for bugs, vulnerabilities, and code smells in a project |
| **Hotspot Search** | Search for security hotspots pending review |
| **Hotspot Detail** | Show full details of a specific security hotspot |
| **Hotspot Status Update** | Change the review status of a security hotspot |
| **Issue Status Update** | Change the status of a Sonar issue (e.g., resolve, won't fix, false positive) |
| **Quality Gate Status** | Get the overall quality gate status and per-condition details |
| **Quality Gate List** | List all available quality gate definitions |
| **Rule Detail** | Show full details of a specific Sonar rule (description, remediation, examples) |
| **Component Measures** | Get quality metrics/measures for a project component |
| **Coverage by File** | Search files by coverage metrics to find low-coverage files |
| **File Coverage Detail** | Get line-by-line and branch coverage details for a specific file |
| **Metrics Search** | Search and list available SonarQube metrics |
| **Duplication Detail** | Get duplication details for a component |
| **Duplicated Files Search** | Search for files with duplicated code blocks |
| **Pull Request List** | List pull requests associated with a project |
| **Branch List** | List branches for a project |
| **Dependency Risk Search** | Search for dependency/library security risks |
| **Code Snippet Analysis** | Analyze a code snippet to verify a fix before applying it |

---

## Inputs

Use the supplied project context, branch/analysis context, repository path, and prior handoff. If the project key is not already known, use the discovered **Project Discovery** tool first to discover it dynamically. Do not hardcode project keys, server URLs, or branch names.

### Generic Workflow — 6 Steps

Follow this workflow for every SonarQube remediation task:

#### Step 1: Detect Project Family

Run the detection in STEP -1 above to determine whether the target repository (or the specific module/file being fixed) is **Maven (Java)**, **Node/React**, or **Mixed**. Record this so the correct reference folder is used in Step 4.

#### Step 2: Discover the Project

If the project key is not already known from context, find and use the available **Project Discovery** tool (look for a tool whose name contains patterns like `project` + `search`/`list`/`my`) to list available projects and identify the relevant one:

```
[Use the discovered Project Discovery tool]
   Returns: list of projects with their keys, names, and last analysis dates
   Select the project matching the current repository/service name
   Capture: {project_key}
```

#### Step 3: Assess Overall Quality Gate Health

Find and use the available **Quality Gate Status** tool (look for a tool whose name contains patterns like `quality`/`gate` + `status`/`get`) with the discovered `{project_key}` to understand which dimensions are failing:

```
[Use the discovered Quality Gate Status tool](project_key={project_key})
   Returns: overall status (OK / WARN / ERROR) and per-condition details
   Identify: which metrics are failing and by how much
   Prioritize: failing dimensions for remediation
```

Optionally find and use the available **Component Measures** tool (look for a tool whose name contains patterns like `measure`/`metric`/`component`) to get a broader metrics snapshot:

```
[Use the discovered Component Measures tool](component={project_key}, metricKeys=coverage,duplicated_lines_density,bugs,vulnerabilities,code_smells,security_hotspots)
   Returns: current values for all key quality metrics
```

#### Step 4: Fetch Issues by Failing Dimension

Based on Step 3 results, find and use the appropriate dimension-specific tools discovered in STEP 0. This step is identical for Maven and Node/React projects — only the SonarQube language analyzer differs server-side (`java` vs `js`/`ts`), not the client-side tool usage.

**Bugs / Vulnerabilities / Code Smells:**
```
[Use the discovered Issue Search tool](projectKey={project_key}, types=BUG,VULNERABILITY,CODE_SMELL, resolved=false, severities=BLOCKER,CRITICAL,MAJOR)
   Returns: list of open issues with file, line, rule, message, severity
   Also call with severities=MINOR,INFO if needed for completeness
```

**Security Hotspots:**
```
[Use the discovered Hotspot Search tool](projectKey={project_key}, status=TO_REVIEW)
   Returns: list of hotspots pending review
[Use the discovered Hotspot Detail tool](hotspotKey={hotspot_key})
   Returns: full details, rule description, code context for a specific hotspot
```

**Coverage:**
```
[Use the discovered Coverage by File tool](projectKey={project_key})
   Returns: files with lowest coverage
[Use the discovered File Coverage Detail tool](component={file_component_key})
   Returns: line-by-line and branch coverage for a specific file
```

**Duplications:**
```
[Use the discovered Duplicated Files Search tool](projectKey={project_key})
   Returns: files with duplicated code blocks
[Use the discovered Duplication Detail tool](component={file_component_key})
   Returns: duplication block details for a specific file
```

**Dependency Risks:**
```
[Use the discovered Dependency Risk Search tool](projectKey={project_key})
   Returns: vulnerable dependencies with CVE details and severity
   (Java: Maven dependency CVEs. Node: npm/yarn/pnpm dependency CVEs.)
```

**Rule Details (before fixing):**
```
[Use the discovered Rule Detail tool](ruleKey={rule_key})
   Returns: rule description, why it matters, remediation guidance, and examples
   Call this before fixing any unfamiliar rule to understand the correct fix approach
```

**Branches / PRs (for branch-scoped analysis):**
```
[Use the discovered Branch List tool](projectKey={project_key})
   Returns: all branches with their quality gate status
[Use the discovered Pull Request List tool](projectKey={project_key})
   Returns: open pull requests with quality gate status per PR
```

#### Step 5: Fix Code Issues and Verify

- Read the affected source files from the workspace.
- Load the relevant dimension reference file from `references/maven/` or `references/node/` based on the file's language/project family (see STEP -1 and the Reference Files table).
- Apply the smallest safe fix that resolves the Sonar issue.
- Before applying a fix for an unfamiliar rule, use the discovered **Rule Detail** tool to understand the correct remediation approach.
- After writing the fix, optionally use the discovered **Code Snippet Analysis** tool to verify the fix is clean:

```
[Use the discovered Code Snippet Analysis tool](code={fixed_code_snippet}, language={java|javascript|typescript|...})
   Returns: any remaining issues in the snippet
   Use to confirm the fix does not introduce new issues
```

#### Step 6: Update Issue Statuses

After fixing or reviewing issues, update their statuses in SonarQube:

**For bugs, vulnerabilities, code smells:**
```
[Use the discovered Issue Status Update tool](issueKey={issue_key}, status=RESOLVED|WONTFIX|FALSE-POSITIVE, comment={reason})
   Use RESOLVED when the code fix is applied
   Use WONTFIX when the issue is acknowledged but intentionally not fixed
   Use FALSE-POSITIVE when the finding is incorrect
```

**For security hotspots:**
```
[Use the discovered Hotspot Status Update tool](hotspotKey={hotspot_key}, status=REVIEWED, resolution=SAFE|FIXED|ACKNOWLEDGED, comment={justification})
   Use SAFE when the code is reviewed and confirmed secure
   Use FIXED when the code was changed to eliminate the risk
   Use ACKNOWLEDGED when the risk is accepted with justification
```

---

## Tool Mapping by Quality Dimension

| Dimension | Primary Tool Categories | Secondary Tool Categories |
|---|---|---|
| **Reliability (Bugs)** | Issue Search (type=BUG) | Rule Detail, Issue Status Update |
| **Security (Vulnerabilities)** | Issue Search (type=VULNERABILITY) | Rule Detail, Dependency Risk Search, Issue Status Update |
| **Maintainability (Code Smells)** | Issue Search (type=CODE_SMELL) | Rule Detail, Issue Status Update |
| **Coverage** | Coverage by File, File Coverage Detail | Component Measures |
| **Duplications** | Duplicated Files Search, Duplication Detail | Component Measures |
| **Security Hotspots** | Hotspot Search, Hotspot Detail | Hotspot Status Update |
| **Quality Gate** | Quality Gate Status | Quality Gate List, Component Measures |
| **Metrics** | Metrics Search, Component Measures | |
| **Dependency Risks** | Dependency Risk Search | Rule Detail |
| **Code Verification** | Code Snippet Analysis | |
| **Branches / PRs** | Branch List, Pull Request List | |

> **Reminder:** All tool names in the table above refer to **categories** of tools, not exact tool names. Discover the actual tool names at runtime using the protocol in STEP 0. This mapping applies identically to Maven and Node/React projects.

---

## Issue Scope

- Fix only issues that affect the current quality gate or are explicitly assigned.
- Skip issues already marked `WONTFIX` or `FALSE-POSITIVE`.
- Prioritize by severity: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`.
- Group issues by file before editing.
- For each issue, read the file, understand the rule (use the discovered Rule Detail tool if needed) and surrounding code, then apply the smallest safe fix using the reference matching that file's project family.
- Address all 6 quality dimensions: Reliability (Bugs), Security (Vulnerabilities), Maintainability (Code Smells), Coverage (Unit Tests), Duplications, Security Hotspots.

## Fix Rules

- Preserve public APIs, runtime behavior, and test behavior.
- Prefer root-cause fixes over suppression.
- Do not refactor unrelated code.
- Keep diffs tight and scoped to the reported component/line.
- Do not change generated code unless the repo already treats that generated source as editable.
- Do not weaken validation, security, error handling, logging masks, or concurrency behavior to satisfy a rule.
- If a finding is ambiguous or risky, skip it with a concise reason instead of guessing.
- In Mixed repositories, never apply a Java-specific pattern to a JS/TS file or vice versa — always match the fix approach to the file's own language and reference folder.

## Suppression Rules

Use suppression only when:

- The finding is a genuine false positive.
- The rule conflicts with an established convention in the codebase.
- The issue cannot be fixed safely without changing behavior.

If suppression is necessary, use the repo's established suppression style for that language/tooling:

- **Java/Maven**: `// NOSONAR` with a short reason comment.
- **JS/TS (ESLint/SonarJS)**: `// NOSONAR` with a short reason comment, or the project's existing ESLint disable-comment convention if that is how the repo already suppresses findings — do not introduce a new suppression style.

Never suppress purely to pass the quality gate.

---

## Dimension 1: Reliability (Bugs)

**Scope:** Defects that represent incorrect behavior at runtime. Fix all BLOCKER and CRITICAL bugs before proceeding to lower severities.

**Common patterns (Maven/Java):** Null pointer dereferences, resource leaks, reactive stream error handling gaps, incorrect equals/hashCode, concurrency issues.

**Common patterns (Node/React):** Null/undefined dereferences, unhandled promise rejections, missing async/await error handling, React hook dependency/state bugs, strict-equality/type-coercion bugs, array/object mutation bugs.

**Tool Categories to Use:**
- Find and use the **Issue Search** tool (look for tools with `search`/`list` + `issues`/`sonar` in name) with `types=BUG` to list all open bugs
- Find and use the **Rule Detail** tool (look for tools with `rule` + `show`/`get` in name) to understand the specific rule before fixing
- Find and use the **Code Snippet Analysis** tool (look for tools with `analyze`/`verify` + `code`/`snippet` in name) to verify the fix
- Find and use the **Issue Status Update** tool (look for tools with `issue` + `change`/`update`/`status` in name) to mark as resolved after fixing

> See [references/maven/01-reliability.md](references/maven/01-reliability.md) for Java/Maven fix patterns and examples.
> See [references/node/01-reliability.md](references/node/01-reliability.md) for Node.js/React fix patterns and examples.

---

## Dimension 2: Security (Vulnerabilities)

**Scope:** Code flaws that attackers can exploit. Map each finding to OWASP Top 10 categories. Fix **ALL** security vulnerabilities regardless of severity.

**Common patterns (Maven/Java):** SQL injection, input validation gaps, dependency CVEs, sensitive data exposure, hardcoded credentials.

**Common patterns (Node/React):** XSS via `dangerouslySetInnerHTML`/`innerHTML`, SQL/NoSQL injection, missing input validation (zod/yup/joi), npm dependency CVEs, sensitive data in logs/localStorage, hardcoded API keys, SSRF via unchecked outbound requests.

**Tool Categories to Use:**
- Find and use the **Issue Search** tool with `types=VULNERABILITY` to list all open vulnerabilities
- Find and use the **Dependency Risk Search** tool (look for tools with `dependency` + `risk`/`search` in name) to find vulnerable library dependencies (Maven or npm/yarn/pnpm)
- Find and use the **Rule Detail** tool to understand the vulnerability rule and remediation guidance
- Find and use the **Code Snippet Analysis** tool to verify the fix
- Find and use the **Issue Status Update** tool to mark as resolved after fixing

> See [references/maven/02-security.md](references/maven/02-security.md) for Java/Maven fix patterns and examples.
> See [references/node/02-security.md](references/node/02-security.md) for Node.js/React fix patterns and examples.

---

## Dimension 3: Maintainability (Code Smells)

**Scope:** Issues that reduce readability and make future changes risky. Fix by reducing complexity, removing dead code, and improving naming.

**Common patterns (Maven/Java):** High cognitive complexity, long methods, dead code, magic numbers, poor naming, boolean expression verbosity.

**Common patterns (Node/React):** High cognitive complexity, oversized components/functions, dead code/unused imports, magic numbers/strings, poor naming, boolean expression verbosity, prop drilling, ESLint rule violations (`sonarjs/*`, `react-hooks/exhaustive-deps`).

**Tool Categories to Use:**
- Find and use the **Issue Search** tool with `types=CODE_SMELL` to list all open code smells
- Find and use the **Rule Detail** tool to understand the specific code smell rule
- Find and use the **Code Snippet Analysis** tool to verify the refactored code
- Find and use the **Issue Status Update** tool to mark as resolved after fixing

> See [references/maven/03-maintainability.md](references/maven/03-maintainability.md) for Java/Maven fix patterns and examples.
> See [references/node/03-maintainability.md](references/node/03-maintainability.md) for Node.js/React fix patterns and examples.

---

## Dimension 4: Coverage (Unit Test Coverage)

**Scope:** Line coverage and branch coverage gaps. The quality gate typically requires 80%+ overall coverage. New code often requires higher thresholds (e.g., 85% on new code).

**Common patterns (Maven/Java):** Missing test cases for service logic, uncovered branches, missing exception path tests, reactive stream test gaps (JUnit 5 + Mockito, JaCoCo).

**Common patterns (Node/React):** Missing test cases for services/hooks, uncovered branches, missing rejected-promise/error-path tests, untested React component states (Jest/Vitest + React Testing Library, LCOV coverage).

**Tool Categories to Use:**
- Find and use the **Component Measures** tool with `metricKeys=coverage,uncovered_lines,uncovered_conditions` to get overall coverage metrics
- Find and use the **Coverage by File** tool (look for tools with `coverage` + `search`/`files` in name) to find files with lowest coverage
- Find and use the **File Coverage Detail** tool (look for tools with `coverage` + `detail`/`file`/`get` in name) to see line-by-line and branch coverage for a specific file

> See [references/maven/04-coverage.md](references/maven/04-coverage.md) for Java/Maven (JaCoCo/JUnit) fix patterns and examples.
> See [references/node/04-coverage.md](references/node/04-coverage.md) for Node.js/React (Jest/Vitest, LCOV) fix patterns and examples.

---

## Dimension 5: Duplications (Code Duplication)

**Scope:** Duplicated blocks (default: 10+ identical lines in 3+ files, or 100+ tokens). Target: < 3% duplication.

**Common patterns (Maven/Java):** Duplicated validation logic, repeated pagination code, copy-pasted error handling, near-duplicate processing pipelines.

**Common patterns (Node/React):** Duplicated validation schemas, repeated data-fetching/loading-state logic across components, copy-pasted error-response construction, near-duplicate hooks/utility functions.

**Tool Categories to Use:**
- Find and use the **Component Measures** tool with `metricKeys=duplicated_lines_density,duplicated_blocks,duplicated_lines` to get overall duplication metrics
- Find and use the **Duplicated Files Search** tool (look for tools with `duplicate`/`duplication` + `search`/`files` in name) to find files with the most duplication
- Find and use the **Duplication Detail** tool (look for tools with `duplication` + `get`/`detail` in name) to see exact duplicated block details for a specific file

> See [references/maven/05-duplications.md](references/maven/05-duplications.md) for Java/Maven fix patterns and examples.
> See [references/node/05-duplications.md](references/node/05-duplications.md) for Node.js/React fix patterns and examples.

---

## Dimension 6: Security Hotspots

**Scope:** Security-sensitive code that requires manual review. Unlike Vulnerabilities, hotspots are not confirmed issues — they need human review to determine if they are safe or need fixing. Each hotspot must be either **Acknowledged as Safe** (with justification) or **Fixed**.

**Common patterns (Maven/Java):** SQL injection hotspots, XSS, CSRF, insecure randomness, weak cryptography, hardcoded credentials, path traversal, ReDoS, JWT handling, logging sensitive data.

**Common patterns (Node/React):** `eval()`/dynamic code execution, XSS via `dangerouslySetInnerHTML`/`innerHTML`, insecure randomness (`Math.random()` for tokens), weak cryptography, hardcoded credentials, path traversal, ReDoS, JWT handling/storage, CORS misconfiguration, logging sensitive data.

**Tool Categories to Use:**
- Find and use the **Hotspot Search** tool (look for tools with `hotspot` + `search`/`list` in name) with `status=TO_REVIEW` to list all unreviewed hotspots
- Find and use the **Hotspot Detail** tool (look for tools with `hotspot` + `show`/`get`/`detail` in name) to get full details and code context for a specific hotspot
- Find and use the **Hotspot Status Update** tool (look for tools with `hotspot` + `change`/`update`/`status` in name) to mark as SAFE, FIXED, or ACKNOWLEDGED after review

> See [references/maven/06-security-hotspots.md](references/maven/06-security-hotspots.md) for Java/Maven review patterns and examples.
> See [references/node/06-security-hotspots.md](references/node/06-security-hotspots.md) for Node.js/React review patterns, fix examples, and justification templates.

---

## Validation

After code changes:

- **Maven/Java projects**: use `build-project` (e.g., `mvn compile`/`mvn verify`) for compile/build validation, and `test-project` (e.g., `mvn test`) when a changed class already has focused tests or when the Sonar fix touches logic that should be verified.
- **Node/React projects**: use the project's existing build script (e.g., `npm run build`, `npm run lint`, `tsc --noEmit`) for compile/type validation, and the project's existing test script (e.g., `npm test`, `npm run test:coverage`) when a changed module/component already has focused tests or when the Sonar fix touches logic that should be verified.
- Use the discovered **Code Snippet Analysis** tool to pre-validate a fix before writing it to disk.
- Keep validation output quiet and targeted.
- For Mixed repositories, run the validation command appropriate to the module that was changed (Maven build for Java modules, npm/yarn/pnpm scripts for JS/TS modules).

## Result

Report:

- Detected project family (Maven, Node/React, or Mixed) and which reference folder(s) were used.
- Issues fixed, grouped by file and rule.
- Issues suppressed, with rule and reason.
- Issues skipped, with reason.
- Files changed, with a brief behavior-preserving summary.
- Validation command and result, or blocker if validation could not run.
