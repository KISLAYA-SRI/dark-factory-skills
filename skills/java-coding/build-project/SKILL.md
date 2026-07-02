---
name: build-project
description: Use when compiling a Java Maven backend API microservice or adapter library after code changes. Triggers include build project, compile project, package project, Maven compile, Maven package, Java 25 build failure, annotation processor failure, dependency resolution during build, or keep building until success.
---

# Build Project

Use this skill for build validation only. Test execution belongs to `test-project`; implementation output belongs to `code-output-handoff`.

## Commands

Prefer quiet, targeted Maven commands so only relevant errors reach the context:

```bash
mvn -q compile
```

- Use `mvn -q -Dstyle.color=never compile` as the default implementation build check.
- Avoid `mvn clean` unless generated/stale files are clearly causing the failure.
- Avoid `-X`, full debug logs, dependency trees, and verbose plugin output unless a specific build failure requires them.
- If output is still too large, keep the full log in a temporary file and pass the concise failing module, goal, exception, and first actionable compiler error back into context.

## Build Loop

1. Run the narrowest build command that proves the requested change compiles.
2. Fix every relevant compile, annotation processor, package, import, missing symbol, bean signature, or compatibility error.
3. Re-run the same quiet command.
4. Continue until the command succeeds or the failure is clearly blocked by missing credentials, unavailable repositories, network restrictions, or external tooling.

Do not mark the build complete after a partial fix. The final build command must be successful unless there is a real environment blocker.

## Failure Triage

- Missing symbol/import: verify package names and generated classes before creating new abstractions.
- Lombok/MapStruct/annotation processing: check compiler plugin configuration, Java release, and annotation processor paths.
- Dependency resolution: report the missing artifact/repository concisely; do not rewrite code to hide a dependency issue.
- Spring bean compile errors: align constructor signatures and auto-configuration bean methods.

## Result

Report the exact command that succeeded. If blocked, report the command, the concise blocker, and the smallest relevant error excerpt.
