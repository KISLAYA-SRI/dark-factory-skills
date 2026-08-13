---
title: "Validate Frontend Foundation With Project Native Commands"
impact: "HIGH"
impactDescription: ""
tags: frontend, foundation, tooling
costHint: "load_only_when_matched"
risk: "medium"
appliesToModes: ["greenfield_build", "brownfield_change", "debug_fix", "review_judge"]
doesNotApplyToModes: ["delta_change"]
---

## Validate Frontend Foundation With Project Native Commands

Project foundation changes must be verified with repo-native lint, typecheck, build, and env validation evidence.

**Incorrect:**

The agent adds tsconfig and env files but does not inspect package scripts or run validation.

**Correct:**

The agent preserves package manager conventions, updates scripts, runs lint/typecheck/build or reports blockers, and lists foundation evidence.

## Applies To Modes
- greenfield_build
- brownfield_change
- debug_fix
- review_judge

## Does Not Apply To Modes
- delta_change

## When To Apply
- Scaffolding or modifying frontend project foundation

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Relevant config files are inspected.
- Commands run or blockers reported.
- Secrets boundaries are preserved.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
