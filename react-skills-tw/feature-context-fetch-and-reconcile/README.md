# feature-context-fetch-and-reconcile

A single Claude skill that acquires **all** context a downstream Analysis Agent
needs from a JIRA user story — Sitecore API contracts, BFF/OpenAPI operation
contracts, and Figma design intent — grouped **feature-wise**, reconciled across
viewports, and gated on completeness.

The skill produces context artifacts only. It never analyses the story, plans an
implementation, or generates code.

---

## Why this skill exists

Previously three responsibilities were spread across separate prompts:

1. Sitecore API context fetch
2. BFF API context fetch
3. Figma fetch and mobile/desktop reconciliation

That split caused inconsistent paths, duplicated fetches, and — most importantly
— no single place where the workflow could assert *"we have everything we need
before we start analysing"*.

This skill merges all three, supports **multiple features per story**, and adds a
**hard completeness gate** so a workflow can never proceed to analysis or code
generation on a partial context bundle.

---

## Installation

```text
.claude/skills/feature-context-fetch-and-reconcile/
├── SKILL.md
└── README.md
```

Place the folder in your skills directory. The skill is discovered via the
`description` field in the SKILL.md frontmatter.

---

## Required inputs

| Input | Source | Required |
| --- | --- | --- |
| JIRA user story | `.SS_WF/{{$var[ticket_id]s}}_jira_output.json` | Mandatory |

### Required tools

| Tool | Used for |
| --- | --- |
| HTTP tool or shell `curl` | Sitecore endpoint fetch |
| OpenAPI specification MCP server | BFF operation contracts |
| Figma MCP server | Figma design intent extraction |
| Filesystem write access | Artifact and manifest creation |

---

## Output structure

Everything is written under the **existing** `src` folder. The skill never
creates a new `src` or a `.src` folder.

```text
src/.feature-context/
├── context-manifest.json
├── sitecore/
│   └── {feature-key}/
│       ├── {endpoint-key}.json
│       └── index.json
├── bff/
│   └── {feature-key}/
│       ├── {operation-id}.json
│       └── index.json
└── figma/
    └── {feature-key}/
        ├── figma-design-{node-id}-mobile-context.json
        ├── figma-design-{node-id}-desktop-context.json
        ├── responsive-design-intent.json
        └── index.json
```

`context-manifest.json` is the single entry point for the Analysis Agent.

---

## Execution flow

```text
1  Read JIRA story (once)
2  Discover all Sitecore, BFF, and Figma references
3  Group sources into logical features
4  Classify each feature: presentational or transactional
5  Fetch Sitecore API context        → sitecore/{feature}/
6  Fetch BFF API context             → bff/{feature}/
7  Extract Figma design intent       → figma/{feature}/
8  Reconcile mobile + desktop        → responsive-design-intent.json
9  Evaluate completeness gate per feature
10 Write context-manifest.json
11 Mechanical write verification
12 Hard stop → Success or REQUIRED CONTEXT NOT FOUND
```

Acquisition never aborts on the first missing source. All failures are collected
so the gate report is complete and actionable in one run.

---

## Feature type classification

Every feature is classified as exactly one of `presentational` or
`transactional`. The classification decides which gate applies.

Evidence order — first conclusive signal wins:

1. Explicit JIRA label (presentational / static / display-only, or transactional / API-driven).
2. Feature references a BFF or backend operation → `transactional`.
3. Story explicitly states no backend API is required → `presentational`.
4. Acceptance criteria describe submission, retrieval, auth, service validation, or persistence → `transactional`.
5. Feature only renders Sitecore-authored content, static copy, imagery, navigation, or layout → `presentational`.

**Default when ambiguous:** `transactional`.

The stricter default is deliberate — it prevents a data-driven feature from
silently passing with missing backend context.

> Absence of a BFF reference is **not** evidence of a presentational component.
> The skill will not reclassify a feature to make a failing run pass.

---

## The completeness gate

### What "satisfied" means

A source type is satisfied for a feature **only** when all of these hold:

1. At least one source of that type was discovered.
2. Every discovered source was fetched successfully.
3. Every corresponding artifact file was written.
4. Every artifact is non-empty and parses as valid JSON.
5. The feature index for that source type was written.

A partial fetch is not satisfied. **One** failed endpoint, operation, or Figma
node makes the whole source type unsatisfied for that feature.

### Presentational feature

| Source | Required |
| --- | --- |
| Sitecore | ✅ Yes |
| Figma | ✅ Yes |
| BFF | ⚪ Optional |

```text
PASS  when  sitecore == satisfied AND figma == satisfied
```

Fails when a Sitecore endpoint or Figma design is missing, fails to fetch, or its
artifact is not created.

BFF nuance:

- No BFF operation referenced → `bff.status = "not-required"`, gate unaffected.
- BFF operation **referenced but failed** → gate **fails**. The story declared the
  dependency, so it must resolve.

### Transactional feature

| Source | Required |
| --- | --- |
| Sitecore | ✅ Yes |
| BFF | ✅ Yes |
| Figma | ✅ Yes |

```text
PASS  when  sitecore == satisfied AND bff == satisfied AND figma == satisfied
```

Fails when any one of the three is missing, fails to fetch, or its artifact is
not created.

### Run-level result

The run passes **only** when every feature passes its own gate. There is no
partial-success outcome.

---

## Final output contract

| Condition | Final response |
| --- | --- |
| All features passed the gate | `{"status":"Success"}` |
| One or more features failed | `{"status":"failed","reason":"REQUIRED CONTEXT NOT FOUND"}` |
| JIRA input unreadable / output root not creatable | `{"status":"failed","reason":"REQUIRED CONTEXT NOT FOUND"}` |

Maximum final response: 20 tokens. All diagnostic detail lives in
`context-manifest.json`, never in the final response.

---

## Worked examples

### Example 1 — Presentational feature, passes

Story references a Sitecore layout endpoint and mobile + desktop Figma links for
a marketing hero band. No backend API.

```json
{
  "featureKey": "hero-band",
  "featureType": "presentational",
  "gateResult": "passed",
  "sitecore": { "status": "satisfied", "required": true },
  "bff": { "status": "not-required", "required": false },
  "figma": { "status": "satisfied", "reconciliationStatus": "completed" }
}
```

Final response: `{"status":"Success"}`

### Example 2 — Presentational feature, fails on missing Figma

Sitecore endpoint fetched successfully, but no Figma link exists for the feature.

```json
{
  "featureKey": "policy-disclaimer",
  "featureType": "presentational",
  "gateResult": "failed",
  "failures": [
    {
      "sourceType": "figma",
      "reason": "SOURCE_NOT_REFERENCED",
      "detail": "No Figma URL was found for this feature in the JIRA story."
    }
  ]
}
```

Final response: `{"status":"failed","reason":"REQUIRED CONTEXT NOT FOUND"}`

### Example 3 — Transactional feature, fails on missing BFF operation

Sitecore and Figma resolved, but one referenced operation ID was not found in the
OpenAPI specification.

```json
{
  "featureKey": "otp-verification",
  "featureType": "transactional",
  "gateResult": "failed",
  "failures": [
    {
      "sourceType": "bff",
      "sourceId": "bff-002",
      "reference": "verifyOtpCode",
      "reason": "FETCH_FAILED",
      "detail": "OPERATION_NOT_FOUND in OpenAPI specification."
    }
  ]
}
```

Final response: `{"status":"failed","reason":"REQUIRED CONTEXT NOT FOUND"}`

### Example 4 — Mixed story, one feature fails

A story with `login-form` (transactional, passes) and `login-illustration`
(presentational, Sitecore endpoint returned HTTP 500).

Run status is `failed`. `login-form` artifacts are still written and recorded, so
the next run can be diagnosed and re-driven without losing prior work.

---

## Single viewport vs. reconciliation

Reconciliation runs **only** when a feature has both a mobile and a desktop
context that provably represent the same logical screen, component, or state.

| Situation | Behaviour | Gate impact |
| --- | --- | --- |
| Mobile + desktop, matched | Produce `responsive-design-intent.json` | Must be created, else gate fails |
| Single viewport only | `reconciliation.status = "not-applicable"`, reason `SINGLE_VIEWPORT_ONLY` | No impact — gate needs Figma context, not both viewports |
| Both present but mapping ambiguous | Preserve both contexts, record ambiguity | Recorded as `unresolvedMappings` |

The reconciliation JSON, when it exists, is the **authoritative** responsive
contract for the Analysis Agent. Viewport contexts are lookup references only.

---

## Design guarantees

**Failure isolation.** A missing BFF reference never blocks Sitecore or Figma
processing. All failures are aggregated into one report.

**Deduplication.** Each unique Sitecore URL, operation ID, and Figma file-key +
node-ID pair is fetched exactly once, even when referenced by multiple features.

**Shared sources.** A source explicitly shared by several features is stored once
under `shared` and referenced from each feature. It satisfies the gate for every
referencing feature.

**No fabrication.** The skill never creates a placeholder, empty, or invented
artifact to satisfy the gate, and never invents API fields, operation IDs, or
design behaviour for a missing viewport.

**Cost control.** Every source is read once per execution; artifacts are never
reread or re-validated by the model; features are processed one at a time to keep
the working context small.

**Security.** `-k` is applied per Sitecore request only, never globally. Tokens,
API keys, and cookies are never logged or written into artifacts or the manifest.
Discovered URLs are treated as untrusted input and never executed as shell
content.

---

## Downstream contract

The Analysis Agent should:

1. Read `src/.feature-context/context-manifest.json`.
2. Proceed **only** when `runStatus` is `success`.
3. Treat `responsive-design-intent.json` as authoritative for responsive
   interpretation and not re-reconcile viewports.
4. Use viewport contexts only to confirm component references, variants, states,
   labels, tokens, and hierarchy.
5. Report any conflict as an analysis risk without overriding the reconciliation
   artifact.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `REQUIRED CONTEXT NOT FOUND` with `SOURCE_NOT_REFERENCED` for figma | Story has no Figma link for that feature | Add the Figma URL to the story |
| Sitecore `FETCH_FAILED` with a TLS error | `-k` not applied, or endpoint unreachable from the runner | Verify network reachability to the CM host |
| BFF `OPERATION_NOT_FOUND` | Operation ID typo, or spec repo not cloned/refreshed | Correct the operation ID, refresh the OpenAPI source |
| Feature unexpectedly gated as transactional | Classification defaulted due to ambiguity | Add an explicit feature-type label to the story |
| `reconciliation.status = not-applicable` unexpectedly | Only one viewport link present, or viewport labels ambiguous | Add the missing viewport link or label the frames clearly |
| Sources landed in `shared-unassigned` | No explicit feature association in the story | Add a feature heading or an API-to-design mapping table |

---

## Version

Schema version `1.0`.

Changes to the manifest shape, gate semantics, or artifact paths require a
schema version bump so downstream agents can detect the contract change.
