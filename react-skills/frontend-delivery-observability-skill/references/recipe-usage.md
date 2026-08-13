# Recipe Usage Boundary

This skill is generated to be invoked as a bounded recipe step. It does not define, certify, or persist recipes, context packs, or control packs.

## Skill Owns
- bounded technology or process action
- local execution guidance
- local preflight validation
- local references and helper scripts
- explicit assumptions and escalation signals

## Recipe Owns
- business outcome
- step ordering
- context pack selection
- control pack selection
- human approval gates
- cross-skill evidence aggregation

## External Systems Own
- context pack lifecycle
- control pack lifecycle
- recipe registry
- policy registry
- audit and evidence store

## Context Pack Usage
- Mode: accepted_from_recipe
- Skill Forge builds context packs: False
- Expected fields: id, version, domain, retrieval_ref, summary, source
- Use: Use supplied context packs for domain vocabulary, examples, business rules, and field semantics.

## Control Pack Usage
- Mode: accepted_from_recipe
- Skill Forge builds control packs: False
- Expected fields: id, version, risk_tier, mandatory_checks, evidence_requirements, escalation_policy
- Use: Use supplied control packs for mandatory validation, policy checks, human gates, and evidence requirements.

## Invocation Rule
- If a recipe supplies context_pack_refs or control_pack_refs, load and apply them before executing workflow steps.
- If required context or controls are missing, stop and escalate instead of inventing domain rules or policy gates.
- Return assumptions, checks run, checks not run, and escalation reasons so the external recipe can aggregate evidence.