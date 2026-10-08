# Defect Reporting (Stage 8)
Use only facts from Stages 1–7, test run folders, the impact map and `git -C src diff --stat`.

## A. Parent code-generation document
`src/.SS_WF/Agent/CODE/<parent_ticket_id>_CODE_GENERATION.md` (missing → skip and say why)
1. `grep -n` rows for the files and ACs you touched; update only those, tagged `[<ticket_id>]`. Never edit historical sections.
2. Add new files (tests, utils) to the files section, tagged.
3. Append to `## Defect Change Log` (create if missing):
```markdown
### <ticket_id> — <YYYY-MM-DD>
| Issue | Status | Root cause (file → mechanism) | Fix | Regression test |
| --- | --- | --- | --- | --- |
Dev notes applied: ... | none
Contract changes in ticket: ... | none
Conflicts recorded (ticket vs AC/plan/design): ... | none
Found, not fixed: ... | none
Existing tests changed: <test: old → new → why> | none
Drift / outside story scope: ... | none
Impact map: <path>  (<n> rows)
Test runs: <label → verdict → folder>
Gate: <GATE line per issue>
Diff: <git diff --stat>
Learning: <written | candidate: reason | none>
```
4. Write back without append mode; re-read to confirm.

## B. Learning gate
`src/.project/learnings/CODING_AGENT_LEARNINGS.md`. Write only if all three hold:
1. **Proven** — gate passed.
2. **Generic** — no error codes, file names, AC numbers, endpoints or story fields; applies to another component.
3. **New** — no existing learning or coding-skill rule covers it.
Else record `candidate: <rule> — <failed check>` in the change log.
If written: 2–4 lines under UI / LOGIC / TEST:
```markdown
- <Area>: <rule — do / don't>. <why>.
  Refs: <ticket_id>
```
Equal rule exists → add the ticket to its Refs. Never delete or rewrite entries.
