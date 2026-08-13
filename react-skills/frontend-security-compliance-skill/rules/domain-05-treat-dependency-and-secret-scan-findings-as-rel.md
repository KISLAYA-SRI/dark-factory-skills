---
title: "Treat Dependency And Secret Scan Findings As Release Evidence"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: sca, secrets, dependency
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Treat Dependency And Secret Scan Findings As Release Evidence

Frontend supply-chain checks and secret scans should be run or listed as pending before release/security claims.

**Incorrect:**

The agent upgrades dependencies and claims secure without checking audit/SCA or secrets scan.

**Correct:**

The agent runs configured audit/SCA/secrets checks or reports unavailable CI gates as pending.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Changing dependencies or claiming secure/release readiness

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Configured scans run or blockers listed.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
