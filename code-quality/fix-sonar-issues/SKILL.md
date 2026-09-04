---
name: sonar-analysis
description: Use when fetching, triaging, fixing, or summarizing SonarQube quality gate issues for a Java Maven backend microservice or adapter library. Triggers include SonarQube, Sonar quality gate, projectKey, current analysis issues, blocker/critical/major/minor issues, code smell, vulnerability, security hotspot, unit test coverage, code duplication, or any of the 6 SonarQube quality dimensions: Reliability, Security, Maintainability, Coverage, Duplications, Security Hotspots.
---

# SonarQube Issue Remediation Skill

Use this skill for comprehensive SonarQube quality gate remediation across all 6 quality dimensions. Keep fixes minimal, behavior-preserving, and scoped to issues reported for the current analysis.

## Reference Files (Lazy Loading)

This skill uses a lazy-loading pattern for dimension-specific fix patterns and examples. **When a specific dimension fails or requires attention, read the corresponding reference file from the `references/` folder before applying fixes.** Do not load all reference files upfront — only load the ones relevant to the failing dimensions in the current analysis.

| Dimension | Reference File | When to Load |
|---|---|---|
| Reliability (Bugs) | [`references/01-reliability.md`](references/01-reliability.md) | When Reliability gate fails or Bug issues are reported |
| Security (Vulnerabilities) | [`references/02-security.md`](references/02-security.md) | When Security gate fails or Vulnerability issues are reported |
| Maintainability (Code Smells) | [`references/03-maintainability.md`](references/03-maintainability.md) | When Maintainability gate fails or Code Smell issues are reported |
| Coverage (Unit Tests) | [`references/04-coverage.md`](references/04-coverage.md) | When Coverage gate fails or coverage drops below threshold |
| Duplications | [`references/05-duplications.md`](references/05-duplications.md) | When Duplications gate fails or duplication density exceeds threshold |
| Security Hotspots | [`references/06-security-hotspots.md`](references/06-security-hotspots.md) | When Security Hotspots require review or are unresolved |

---

## Inputs

Use the supplied project key, branch/analysis context, repository path, prior handoff, and assigned Sonar tooling. If issue details are already provided in context, use them. Otherwise, use the assigned Sonar MCP/tooling to fetch only unresolved issues for the given project key and current analysis.

## Issue Scope

- Fix only issues that affect the current quality gate or are explicitly assigned.
- Skip issues already marked `WONTFIX` or `FALSE-POSITIVE`.
- Prioritize by severity: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`.
- Group issues by file before editing.
- For each issue, read the file, understand the rule and surrounding code, then apply the smallest safe fix.
- Address all 6 quality dimensions: Reliability (Bugs), Security (Vulnerabilities), Maintainability (Code Smells), Coverage (Unit Tests), Duplications, Security Hotspots.

## Fix Rules

- Preserve public APIs, runtime behavior, and test behavior.
- Prefer root-cause fixes over suppression.
- Do not refactor unrelated code.
- Keep diffs tight and scoped to the reported component/line.
- Do not change generated code unless the repo already treats that generated source as editable.
- Do not weaken validation, security, error handling, logging masks, or concurrency behavior to satisfy a rule.
- If a finding is ambiguous or risky, skip it with a concise reason instead of guessing.

## Suppression Rules

Use suppression only when:

- The finding is a genuine false positive.
- The rule conflicts with an established convention in the codebase.
- The issue cannot be fixed safely without changing behavior.

If suppression is necessary, use the repo's established suppression style. `// NOSONAR` must include a short reason comment. Never suppress purely to pass the quality gate.

---

## Dimension 1: Reliability (Bugs)

**Scope:** Defects that represent incorrect behavior at runtime. Fix all BLOCKER and CRITICAL bugs before proceeding to lower severities.

**Common patterns:** Null pointer dereferences, resource leaks, reactive stream error handling gaps, incorrect equals/hashCode, concurrency issues.

> 📖 See [references/01-reliability.md](references/01-reliability.md) for detailed fix patterns and examples.

---

## Dimension 2: Security (Vulnerabilities)

**Scope:** Code flaws that attackers can exploit. Map each finding to OWASP Top 10 categories. Fix **ALL** security vulnerabilities regardless of severity.

**Common patterns:** SQL injection, input validation gaps, dependency CVEs, sensitive data exposure, hardcoded credentials.

> 📖 See [references/02-security.md](references/02-security.md) for detailed fix patterns and examples.

---

## Dimension 3: Maintainability (Code Smells)

**Scope:** Issues that reduce readability and make future changes risky. Fix by reducing complexity, removing dead code, and improving naming.

**Common patterns:** High cognitive complexity, long methods, dead code, magic numbers, poor naming, boolean expression verbosity.

> 📖 See [references/03-maintainability.md](references/03-maintainability.md) for detailed fix patterns and examples.

---

## Dimension 4: Coverage (Unit Test Coverage)

**Scope:** Line coverage and branch coverage gaps. The quality gate typically requires 80%+ overall coverage. New code often requires higher thresholds (e.g., 85% on new code).

**Common patterns:** Missing test cases for service logic, uncovered branches, missing exception path tests, reactive stream test gaps.

> 📖 See [references/04-coverage.md](references/04-coverage.md) for detailed fix patterns and examples.

---

## Dimension 5: Duplications (Code Duplication)

**Scope:** Duplicated blocks (default: 10+ identical lines in 3+ files, or 100+ tokens). Target: < 3% duplication.

**Common patterns:** Duplicated validation logic, repeated pagination code, copy-pasted error handling, near-duplicate processing pipelines.

> 📖 See [references/05-duplications.md](references/05-duplications.md) for detailed fix patterns and examples.

---

## Dimension 6: Security Hotspots

**Scope:** Security-sensitive code that requires manual review. Unlike Vulnerabilities, hotspots are not confirmed issues — they need human review to determine if they are safe or need fixing. Each hotspot must be either **Acknowledged as Safe** (with justification) or **Fixed**.

**Common patterns:** SQL injection hotspots, XSS, CSRF, insecure randomness, weak cryptography, hardcoded credentials, path traversal, ReDoS, JWT handling, logging sensitive data.

> 📖 See [references/06-security-hotspots.md](references/06-security-hotspots.md) for detailed review patterns, fix examples, and justification templates.

---

## Validation

After code changes:

- Use `build-project` for compile/build validation.
- Use `test-project` when a changed class already has focused tests or when the Sonar fix touches logic that should be verified.
- Keep validation output quiet and targeted.

## Result

Report:

- Issues fixed, grouped by file and rule.
- Issues suppressed, with rule and reason.
- Issues skipped, with reason.
- Files changed, with a brief behavior-preserving summary.
- Validation command and result, or blocker if validation could not run.
