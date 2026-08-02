---
name: sonar-analysis
description: Use when fetching, triaging, fixing, or summarizing SonarQube quality gate issues for a Java Maven backend microservice or adapter library. Triggers include SonarQube, Sonar quality gate, projectKey, current analysis issues, blocker/critical/major/minor issues, code smell, vulnerability, or security hotspot remediation.
---

# Sonar Analysis

Use this skill for SonarQube quality gate remediation. Keep fixes minimal, behavior-preserving, and scoped to issues reported for the current analysis.

## Inputs

Use the supplied project key, branch/analysis context, repository path, prior handoff, and assigned Sonar tooling. If issue details are already provided in context, use them. Otherwise, use the assigned Sonar MCP/tooling to fetch only unresolved issues for the given project key and current analysis.

## Issue Scope

- Fix only issues that affect the current quality gate or are explicitly assigned.
- Skip issues already marked `WONTFIX` or `FALSE-POSITIVE`.
- Prioritize by severity: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`.
- Group issues by file before editing.
- For each issue, read the file, understand the rule and surrounding code, then apply the smallest safe fix.

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
