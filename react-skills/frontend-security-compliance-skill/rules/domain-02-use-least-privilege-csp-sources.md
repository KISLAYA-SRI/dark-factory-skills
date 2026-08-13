---
title: "Use Least Privilege CSP Sources"
impact: "HIGH"
impactDescription: "Prevents browser-side credential leakage, XSS exposure, and unsupported compliance claims."
tags: csp, headers
costHint: "load_when_matched"
risk: "high"
appliesToModes: ["review_judge"]
doesNotApplyToModes: ["greenfield_build", "delta_change", "brownfield_change", "debug_fix"]
---

## Use Least Privilege CSP Sources

CSP should allow only required sources and avoid unsafe-inline/wildcards unless justified by source evidence.

**Incorrect:**

The agent sets script-src * unsafe-inline to make a widget work.

**Correct:**

The agent identifies required widget domains, uses nonces/hashes where available, and documents any unavoidable exception.

## Applies To Modes
- review_judge

## Does Not Apply To Modes
- greenfield_build
- delta_change
- brownfield_change
- debug_fix

## When To Apply
- Changing CSP or security headers

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Allowed domains are justified.
- Unsafe directives are avoided or explicitly risk-owned.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
