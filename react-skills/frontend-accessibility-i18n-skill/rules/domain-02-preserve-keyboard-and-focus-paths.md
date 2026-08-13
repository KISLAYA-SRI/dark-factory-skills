---
title: "Preserve Keyboard And Focus Paths"
impact: "HIGH"
impactDescription: "Prevents backend endpoint implementation and contract regressions across supported stacks."
tags: keyboard, focus
costHint: "load_when_matched"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Preserve Keyboard And Focus Paths

Interactive flows must support keyboard operation, visible focus, focus restoration, and escape/close behavior where applicable.

**Incorrect:**

A dialog opens without moving focus and cannot be closed by keyboard.

**Correct:**

The dialog traps focus, restores focus to trigger, supports Escape, and exposes visible focus states.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding dialogs, menus, tabs, popovers, modals, or custom controls

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Keyboard path verified.
- Focus lifecycle documented.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
