from pathlib import Path
import json

def _items(values, fallback):
    if not values:
        return [f'- {fallback}']
    return [f'- {value}' for value in values]

def _runtime_contract():
    path = Path('runtime-manifest.json')
    if not path.exists():
        return []
    manifest = json.loads(path.read_text(encoding='utf-8'))
    context_budget = manifest.get('context_budget') or {}
    mode_selection = manifest.get('mode_selection') or {}
    modes = mode_selection.get('modes') or []
    evidence_contract = manifest.get('evidence_contract') or {}
    lines = [
        '## Runtime Use Contract',
        '',
        'Read `runtime-manifest.json` first. Treat it as the routing and context-loading contract for this skill, not as optional metadata.',
        '',
        '### Use This Skill When',
        *_items(manifest.get('activation_scope'), 'Use only when the request clearly matches the skill trigger scope.'),
        '',
        '### Do Not Use This Skill When',
        *_items(manifest.get('non_activation_scope'), 'Do not use when the request is outside this skill scope.'),
        '',
        '### Operating Mode Selection',
        f"- Default mode: `{mode_selection.get('default_mode', 'brownfield_change')}`.",
        f"- Prefer lowest-cost valid mode: {mode_selection.get('prefer_lowest_cost_valid_mode', True)}.",
        '- Do not use `greenfield_build` when repository files, failing tests, logs, diffs, or a narrow change request already exist.',
        '- Select the mode before loading rules, then apply that mode max_rules_initial and workflow.',
        '- Use `delta_change` for incremental changes and `debug_fix` for symptom-driven investigation before considering broader modes.',
    ]
    if modes:
        for mode in modes:
            mode_id = mode.get('id', 'unknown_mode')
            lines.append(f"- `{mode_id}`: {mode.get('use_when', 'Use when this mode fits the task.')}")
            lines.append(f"  Max initial rules: {mode.get('max_rules_initial', 3)}; strategy: {mode.get('load_strategy', 'targeted_rules_only')}.")
            for label, key in [('Required inputs', 'required_inputs'), ('Issue classifications', 'issue_classifications'), ('Workflow', 'workflow'), ('Escalate when', 'escalate_when'), ('Output', 'output_format'), ('Full mode triggers', 'full_mode_triggers')]:
                values = mode.get(key) or []
                if values:
                    lines.append(f'  {label}:')
                    lines.extend(f'  - {value}' for value in values)
    else:
        lines.append('- No modes declared; default to `brownfield_change` and targeted rule loading.')
    lines.extend([
        '',
        '### Context Budget',
        f"- Initial rule load limit: {context_budget.get('max_rules_initial', 3)} rule files.",
        f"- Load references conditionally: {context_budget.get('load_references_conditionally', True)}.",
        f"- Full pack review only on explicit request: {context_budget.get('full_pack_review_only_on_request', True)}.",
        f"- Prefer `runtime-manifest.json` `rule_index` before bulk-loading `AGENTS.md`: {context_budget.get('prefer_rule_index_before_agents_md', True)}.",
        '- Do not bulk-load every rule by default. Start with `rule_index` entries whose `load_when`, `tags`, and risk match the task.',
        '- Skip rules whose `does_not_apply_to` matches the task; state skipped high-risk rules in the final evidence summary when relevant.',
        '',
        '### Rule Loading Order',
        '1. Check `activation_scope` and `non_activation_scope`.',
        '2. Select the smallest relevant set from `rule_index` using `load_when`, `tags`, `risk`, and `cost_hint`.',
        '3. Load referenced files only when their `load_when` condition is met.',
        '4. Load companion skills when the task crosses their stated boundary.',
        '5. Stop and ask for missing contract, context, policy, repository, or command evidence when a stop condition applies.',
        '',
        '### Companion Skill Triggers',
    ])
    companion_skills = manifest.get('companion_skills') or []
    if companion_skills:
        for skill in companion_skills:
            trigger = skill.get('trigger') or skill.get('required_when') or 'Use when this companion boundary is in scope.'
            lines.append(f"- `{skill.get('skill_id', 'unknown-skill')}`: {trigger}")
    else:
        lines.append('- No companion skills declared.')
    lines.extend(['', '### Stop Conditions'])
    lines.extend(_items(manifest.get('stop_conditions'), 'Stop when required evidence or context is missing.'))
    lines.extend(['', '### Evidence Summary Required'])
    fields = evidence_contract.get('required_summary_fields') or []
    if fields:
        lines.extend(f'- `{field}`' for field in fields)
    else:
        lines.append('- `rules_loaded`, `references_loaded`, `commands_run`, `residual_risks`.')
    claim_policy = evidence_contract.get('claim_policy')
    if claim_policy:
        lines.extend(['', f'**Claim Policy:** {claim_policy}'])
    lines.extend(['', '### Runtime Rule Index'])
    for item in manifest.get('rule_index') or []:
        lines.append(f"- `{item.get('file', '')}` - {item.get('title', '')} | risk: {item.get('risk') or 'unspecified'} | cost: {item.get('cost_hint') or 'unspecified'}")
        applies_to_modes = item.get('applies_to_modes') or []
        does_not_apply_to_modes = item.get('does_not_apply_to_modes') or []
        if applies_to_modes:
            lines.append(f"  Applies to modes: {', '.join(applies_to_modes)}")
        if does_not_apply_to_modes:
            lines.append(f"  Skip modes: {', '.join(does_not_apply_to_modes)}")
        if item.get('load_when'):
            lines.append(f"  Load when: {item['load_when']}")
        does_not_apply_to = item.get('does_not_apply_to') or []
        if does_not_apply_to:
            lines.append(f'  Do not load when: {does_not_apply_to[0]}')
    if not manifest.get('rule_index'):
        lines.append('- No rule index declared; use the rule files below.')
    return lines

def run() -> int:
    rules_dir = Path('rules')
    chunks = ['# Compiled Agent Rules', '']
    chunks.extend(_runtime_contract())
    if chunks[-1:] != ['']:
        chunks.append('')
    for path in sorted(rules_dir.glob('*.md')):
        if path.name.startswith('_'):
            continue
        chunks.append(f'<!-- {path.name} -->')
        chunks.append(path.read_text(encoding='utf-8'))
        chunks.append('')
    Path('AGENTS.md').write_text('\n'.join(chunks).strip() + '\n', encoding='utf-8')
    print('AGENTS.md rebuilt')
    return 0

if __name__ == '__main__':
    raise SystemExit(run())