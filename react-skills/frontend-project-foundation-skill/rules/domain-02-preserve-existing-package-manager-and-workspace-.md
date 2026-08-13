---
title: "Preserve Existing Package Manager And Workspace Boundaries"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: package-manager, workspace
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["brownfield_change", "debug_fix"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "review_judge"]
---

## Preserve Existing Package Manager And Workspace Boundaries

Do not introduce npm/yarn/pnpm/Turborepo/Nx changes that conflict with existing repo conventions.

**Incorrect:**

The repo uses pnpm workspaces but the agent adds npm scripts and package-lock.json.

**Correct:**

The agent uses pnpm, updates workspace files consistently, and avoids unrelated package churn.

## Applies To Modes
- brownfield_change
- debug_fix

## Does Not Apply To Modes
- greenfield_build
- delta_change
- review_judge

## When To Apply
- Changing dependencies, scripts, or monorepo setup

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Lockfile/package manager is identified.
- Workspace packages remain valid.
- No unrelated package config is rewritten.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
