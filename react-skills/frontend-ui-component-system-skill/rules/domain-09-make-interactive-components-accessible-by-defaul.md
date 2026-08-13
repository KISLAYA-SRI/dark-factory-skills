---
title: "Make Interactive Components Accessible By Default"
impact: "HIGH"
impactDescription: "Prevents fragile UI APIs and inaccessible reusable components."
tags: accessibility, aria, keyboard
costHint: "load_for_interactive_accessibility"
risk: "critical"
appliesToModes: ["delta_change", "review_judge"]
doesNotApplyToModes: ["greenfield_build", "brownfield_change", "debug_fix"]
---

## Make Interactive Components Accessible By Default

Interactive components need semantic elements, accessible names, keyboard behavior, visible focus, and ARIA only where needed.

**Incorrect:**

A clickable div opens a menu, has no role, no keyboard support, and loses focus after selection.

**Correct:**

The component uses a button/menu primitive with accessible name, keyboard navigation, visible focus, and tested open/close states.

## Applies To Modes
- delta_change
- review_judge

## Does Not Apply To Modes
- greenfield_build
- brownfield_change
- debug_fix

## When To Apply
- Adding buttons, menus, dialogs, tabs, popovers, accordions, or custom interactive controls

## Does Not Apply To
- The task does not touch this rule boundary.

## Evidence And Validation
- Keyboard path works.
- Accessible names and focus management are present.

## References
- references/tools.md
- references/compliance.md
- references/edge-cases.md
