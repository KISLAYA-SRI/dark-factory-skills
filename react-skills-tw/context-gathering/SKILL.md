---
name: context-gathering
description: Use to acquire all external context for a story — Sitecore API JSON, BFF API specs, and Figma Design Intent JSONs — and write them to disk for downstream analysis phases. Performs acquisition only; no reconciliation and no analysis. Triggers include context gathering, fetch context, Figma fetch, Sitecore API fetch, BFF spec fetch, or gather story context.
---

## Context Gathering

### Purpose

This skill is **single acquisition phase**. It reads the JIRA story once, fetches every external artefact the story depends on, and writes them to fixed locations on disk.

It performs **acquisition only**:

- ✅ Extract endpoints and URLs from the JIRA story
- ✅ Fetch Sitecore API JSON, BFF API specs, and Figma Design Intent JSONs
- ✅ Write each artefact to its canonical path
- ✅ Report what was fetched, what was missing, and what failed
- ❌ No reconciliation
- ❌ No contract analysis
- ❌ No component planning, no story interpretation, no validation judgement

⚠️ **This Skill does not judge whether a missing artefact matters.** It cannot — classification does not exist yet. It records outcomes;

---

### Output Locations (Canonical)

| Artefact                      | Path                                                |
| ----------------------------- | --------------------------------------------------- |
| Sitecore API JSON             | .SC_API_SPEC/sitecore-api.json`                     |
| BFF API spec (per operation)  | `.BFF_API_SPEC/{operationId}.json`                  |
| Figma Design Intent (per URL) | `figma-output/figma_design_{Node_id}_-context.json` |

These are the locations Phases 4, 5 and 6 read from. Do not vary them.

---

## ⚠️ SITECORE FETCH — USE THE PROJECT SCRIPT, NOT THE HTTP TOOL

The Sitecore endpoint **must** be fetched using the bundled script:

```bash
bash scripts/fetch-sitecore-api.sh "<complete-endpoint-url>"
```

**Do NOT use the generic http tool for Sitecore.** Do NOT construct an ad-hoc `curl` command.

### Why a script

| Concern                     | How the script handles it                                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Self-signed certificate** | `-k` is applied **inside** the script. Never pass TLS flags from the caller.                                             |
| **Silent-but-loud errors**  | `-sS` is applied inside the script.                                                                                      |
| **Timeouts**                | Connect 15s / total 60s — a hung endpoint cannot stall the phase.                                                        |
| **Redirects**               | Followed, capped at 5.                                                                                                   |
| **Partial writes**          | Response is staged to a temp file; the canonical path is written **only** after HTTP status and JSON validity both pass. |
| **Consistency**             | Every run uses identical flags. No drift between invocations.                                                            |

### Usage

```bash
# Default output path (.SC_API_SPEC/sitecore-api.json)
bash scripts/fetch-sitecore-api.sh "https://cm.dev.internal.example.net/sitecore/api/layout/render/jss?item=/path&sc_apikey=XXX"
# Explicit output path (rarely needed)
bash scripts/fetch-sitecore-api.sh "<endpoint>" "./src/.SC_API_SPEC/sitecore-api.json"
```

Pass the **complete endpoint** exactly as derived from the JIRA story — full scheme, host, path, and query string. The script rejects anything that is not a complete `http://` or `https://` URL.

### Exit Codes — Map Directly to the Manifest

| Exit  | Meaning                                                    | CONTEXT_MANIFEST status           |
| ----- | ---------------------------------------------------------- | --------------------------------- |
| **0** | Valid JSON written                                         | `Fetched`                         |
| **1** | Usage error — missing/malformed endpoint                   | `Fetch Failed — invalid endpoint` |
| **2** | Network/transport failure — unreachable, DNS, timeout, TLS | `Fetch Failed — transport`        |
| **3** | HTTP error — non-2xx returned                              | `Fetch Failed — HTTP <status>`    |
| **4** | Empty body or unparseable JSON                             | `Fetch Failed — invalid payload`  |
| **5** | Filesystem error — could not write                         | `Fetch Failed — filesystem`       |

⚠️ **On any non-zero exit the output file is not created.** This is deliberate: Phase 4 treats an empty or unreadable artefact as **not materialised**, so a junk file would produce a false pass. Record the failure and move on to the BFF and Figma tasks.
Always capture the script's exit code and stderr text — the manifest note should carry the actual reason, not a generic "failed".

---

### ⚠️ TASK-LEVEL FAIL-STOP RULE

This skill runs **three independent tasks**: Sitecore, BFF, and Figma.

> If fetching fails for Sitecore, BFF, or Figma, **stop that task only**. Do not invent details or properties. Do not abort the other tasks. Do not abort the phase or the agent.

```text
Sitecore fetch fails  → record SITECORE FETCH FAILED  → BFF and Figma still run
BFF fetch fails       → record BFF FETCH FAILED       → Sitecore and Figma still run
Figma fetch fails     → record FIGMA FETCH FAILED     → Sitecore and BFF still run
```

⚠️ **Scope clarification for the embedded prompt below:** where the prompt says _"SKIP the whole task"_ for missing Backend API details, "the whole task" means **the BFF task only**. Sitecore extraction and Figma extraction always proceed independently, regardless of BFF availability.

**Never** invent an endpoint, field, node, token, or component to fill a gap. A missing artefact is recorded as missing.

---

### THE CONTEXT SYNTHESISOR PROMPT (Use Verbatim)

Execute the following prompt exactly as written. It is validated in production — do not paraphrase, reorder, or optimise it.

---

You are context Context synthesisor.

Read the JIRA User story to extract out the -

- Sitecore API Endpoints - Analyse the story to fetch the complete endpoint of Sitecore API. Always use the complete endpoint.
  and then save the output in .SC_API_SPEC/sitecore-api.json
- BFF Endpoints - use open-api-spec MCP Tool to get data for all the operation ids mentioned in the Jira story. Save the output inside .BFF_API_SPEC/.json. If NO Backend API details are provided, do not invent API fields or endpoints, THEN SKIP the whole task and output with just "API NOT FOUND". Never use Yaml Spec file name as the operationId or Endpoint. Endpoint or operationId is different from name of Yaml spec file and is mentioned indvidually.

FOLDER / FILE STRUCTURE VIOLATIONS (HARD RULES — Zero Exceptions):

- Do NOT create a new src folder — it already exists at the repository root; use the existing one
- The skill never write any file outside "src" folder. This is the root folder and all files are to be created inside `src` folder. Path of files to be created are relative to `src` folder.

From the data of JIRA Story, find all the Figma URL endpoints which are mentioned in it.

Your responsibility is to connect to the Figma MCP Server, analyse all provided Figma design, and generate a Design Intent JSON file optimised for downstream frontend code generation.

Mention all the FIGMA URLs found.

HARD RULES -

The output MUST focus on design intent and implementation guidance.

DO NOT return raw Figma node data.

DO NOT return unnecessary MCP payloads.

DO NOT return variable definitions, design token definitions, full vector data, or verbose style definitions.

Your objective is to minimise tokens while maximising implementation accuracy.

## INPUT

READ the JIRA Data to extract all the FIGMA URLS and repeat the steps for all URLs one by one -

## STEP 1 - CONNECT TO FIGMA

Use the Figma MCP server to:

Open the supplied node.

Traverse all nested children.

Identify screen hierarchy.

Identify reusable components.

Extract only implementation-relevant metadata.

## STEP 2 - ANALYSE SCREEN STRUCTURE

Identify:

Page Name

Screen Name

Node ID

Frame Dimensions

Device Type

Primary Layout Pattern

Classify screen as:

Page

Modal

Drawer

Bottom Sheet

Tab View

Wizard

Dashboard

List View

Form

Detail View

Other

## STEP 3 - EXTRACT LAYOUT GRID INFORMATION

Extract all layout guide details.

Capture:

Grid Type

Column Count

Row Count

Gutter Width

Margins

Grid Alignment

Grid Width Behaviour

Stretch Behaviour

This information is mandatory.

The Coding Agent will use this to recreate responsive layouts.

Extract how all components are structured and fit on the Desktop and Mobile gird in terms of columns.

## STEP 4 - EXTRACT RESPONSIVE BEHAVIOUR

For every frame and component extract:

#### Constraints

Capture:

Horizontal Constraint

Vertical Constraint

Examples:

Left

Right

LeftRight

TopBottom

Centre

Scale

#### Resizing Behaviour

Capture:

Fixed Width

Fixed Height

Hug Content

Fill Container

#### Size Limits

Capture when defined:

Min Width

Max Width

Min Height

Max Height

This information is mandatory.

## STEP 5 - EXTRACT AUTO LAYOUT INFORMATION

For every auto-layout container capture:

Direction

Padding

Gap

Cross-Axis Alignment

Main-Axis Alignment

Wrap Setting

Fill/Hug Settings

Represent using implementation-friendly values.

The Coding Agent should be able to directly map this to Flexbox or CSS Grid.

## STEP 6 - BUILD COMPONENT HIERARCHY

Generate complete parent-child hierarchy.

Capture:

Component Name

Component Type

Parent Component

Child Components

Text/Name if present on that component

Preserve nesting.

Never flatten the structure.

The hierarchy should represent actual component composition.

Instead of mentioning ids and leaving coding agent to connect them and read its complete data; add nested component with details as per hierarchy inside childComponents array

## STEP 7 - EXTRACT COMPONENT INSTANCE INFORMATION

Capture only:

Referenced Component Name

Variant Selection

Component State

Examples:

State:

Default

Hover

Focus

Active

Disabled

Error

Loading

DO NOT return the full component instance payload.

## STEP 8 - EXTRACT DESIGN TOKEN USAGE

IMPORTANT

DO NOT extract:

Variable Definitions

Token Definitions

Token Values

Extract only token references used by components.

Examples:

colour-primary-500

spacing-4

font-body-md

radius-md

Capture usage under:

Colours

Typography

Spacing

Border Radius

Shadows

Elevation

Borders

- NEVER hardcode any value - Use only token names.
- Values without a token name go into missing_tokens.

## STEP 9 - IDENTIFY SEMANTIC COMPONENT TYPES

For every component based on component COMPONENT INSTANCE INFORMATION, NAME, TYPE infer the most likely semantic type.

For Example - For an element which is visually a link but is built using Button Component then should be a "Button" with Design tokens and Variants of that element from COMPONENT INSTANCE INFORMATION.

Use classifications such as:

Button

Link

Input

Text Area

Select

Radio

Checkbox

Switch

Card

Table

Tabs

Badge

Chip

Banner

Alert

Header

Footer

Navigation

Breadcrumb

Pagination

Modal

Drawer

Accordion

Carousel

Skeleton

Progress Indicator

Assign one primary semantic type.

## STEP 10 - TYPOGRAPHY INTENT

Capture:

Semantic Role

Token Name

Text Style Usage

Examples:

Heading XL

Heading LG

Body MD

Caption SM

DO NOT capture verbose text style metadata.

## STEP 11 - ICON INVENTORY

Capture:

For icons:

Icon Name

Semantic Meaning

DO NOT export binary image content.

DO NOT export SVG path data.

## OUTPUT FORMAT

Return a single JSON structure.

Structure:

{

"screenMetadata": ,

"layoutGrid": ,

"responsiveRules": ,

"componentHierarchy": [],

missing_tokens:[]

}

## DO NOT INCLUDE

Raw MCP response

Raw Figma JSON

Variable definitions

Variable values

Token definitions

Complete text content

Full vector geometry

Raw paint definitions

Raw effect definitions

Image binaries

SVG paths

Unused metadata

Only return information that directly improves frontend code generation quality.

Repeat the above steps for all the Figma URLS found and Save the output in figma-output folder with name : figma*design*{Node*id}*-context.json

---

### END OF VERBATIM PROMPT

---

### File Naming Clarifications

These clarify the prompt's intent without altering its instructions:

| Artefact | Written as                                                                                      |
| -------- | ----------------------------------------------------------------------------------------------- |
| Sitecore | `.SC_API_SPEC/sitecore-api.json` — one file, fixed name                                         |
| BFF      | `.BFF_API_SPEC/{operationId}.json` — **one file per operationId**, named after that operationId |
| Figma    | `figma-output/figma_design_{Node_id}_-context.json` — one file per Figma URL                    |

⚠️ **Figma filenames do not carry a viewport marker.** The viewport is recorded **inside** each file, in `screenMetadata` (Device Type and Frame Dimensions). Phase 5 identifies mobile vs desktop from that content, not from the filename. Ensure `screenMetadata` is fully populated for every extracted file — it is the only viewport signal available downstream.

### Required Output: CONTEXT_MANIFEST

---

### Required Output: CONTEXT_MANIFEST

After executing the prompt, report a manifest of what was acquired. **Phase 4 (Context Validation) depends on this**, and Phases 5 and 6 use it to avoid re-scanning the JIRA story.

```text
CONTEXT MANIFEST — {{ticket_id}}

SITECORE
  Status:    Fetched | Not Found in Story | Fetch Failed
  Endpoint:    [complete endpoint used, or: None found in story]
  Fetched via: scripts/fetch-sitecore-api.sh
  Script exit: [0–5]
  File:        .SC_API_SPEC/sitecore-api.json | Not written
  Note:        [exact failure reason from the script's stderr, if applicable]

SITECORE
  Status:    Fetched | Not Found in Story | Fetch Failed
  Endpoint:  [complete endpoint used, or: None found in story]
  File:      .SC_API_SPEC/sitecore-api.json | Not written
  Note:      [failure reason if applicable]

BFF
  Status:    Fetched | API NOT FOUND | Fetch Failed
  Operation IDs found in story: [id1, id2, …] | None
  Files written:
    -.BFF_API_SPEC/{operationId}.json
  Not retrieved: [operationIds that could not be fetched, with reason]

FIGMA
  Status:    Fetched | No Figma URLs in Story | Fetch Failed
  URLs found: [list every Figma URL found in the story]
  Files written:
    - figma-output/figma_design_{Node_id}_-context.json  (Device Type: mobile|desktop, Frame: NNNpx)
  Not retrieved: [URLs that could not be extracted, with reason]

VIEWPORT COVERAGE
  Mobile context present:  Yes | No
  Desktop context present: Yes | No
  Reconciliation required in Phase 5: Yes (both present) | No (single viewport)
```

Report counts accurately — Phase 4 compares _endpoints found_ against _artefacts written_, and a partial result is a validation failure.

---

### Guardrails

#### Always Do

- Read the JIRA story **once** and extract all Sitecore endpoints, BFF operationIds, and Figma URLs in that single pass.
- **Fetch Sitecore via `scripts/fetch-sitecore-api.sh`.**
- Pass the **complete endpoint URL** to the script, exactly as derived from the story.
- **Capture the script's exit code and stderr** and record the real reason in the manifest.- Write every artefact to its canonical path.
- Name each BFF spec file after its `operationId`.
- Populate `screenMetadata` fully for every Figma file — it carries the only viewport signal.
- List every Figma URL, endpoint and operationId found, **including ones that failed**.
- Report the CONTEXT_MANIFEST at the end, with accurate counts.
- **On any fetch failure, stop that task only** and record the failure with its reason.

#### Never Do

- **Never invent an endpoint, field, node, token, or component** to fill a gap.
- **Never abort the phase or the agent because one task failed** — the other two still run.
- **Never treat "SKIP the whole task" as covering Sitecore or Figma** — it scopes to the BFF task only.
- **Never judge whether a missing artefact is acceptable** — that is Phase 4's job.
- **Never use the generic http tool for the Sitecore endpoint** — use the script.
- **Never construct an ad-hoc curl command for Sitecore** — the script owns the flags.
- **Never pass `-k`, `-sS`, or any TLS/transport flag to the script** — they are internal to it.
- **Never write `.SC_API_SPEC/sitecore-api.json` by hand** or from a partial response.
- **Never treat a non-zero script exit as success**, and never fabricate the artefact it did not write.
- For BFF API, Never use Yaml Spec file name as the operationId or Endpoint. Endpoint or operationId is different from name of Yaml spec file.
- Never reconcile mobile and desktop here — that is Phase 5.
- Never analyse contracts, plan components, or interpret the story here.
- Never return raw MCP payloads, raw Figma node data, token definitions, SVG paths, or image binaries.
- Never create a new `src` folder — use the existing one at the repository root.
- Never write artefacts anywhere other than the canonical paths.

---

### Gate: Phase 2 Complete When

- [ ] JIRA story read once; all Sitecore endpoints, BFF operationIds, and Figma URLs extracted.
- [ ] Sitecore task completed — fetched to `.SC_API_SPEC/sitecore-api.json`, or recorded as Not Found / Fetch Failed.
- [ ] BFF task completed — each operationId written to `.BFF_API_SPEC/{operationId}.json`, or recorded as API NOT FOUND / Fetch Failed.
- [ ] Figma task completed — each URL written to `figma-output/figma_design_{Node_id}_-context.json`, or recorded as Fetch Failed.
- [ ] Every Figma file has fully populated `screenMetadata` including Device Type and Frame Dimensions.
- [ ] No invented endpoints, fields, nodes, or components anywhere.
- [ ] A failure in one task did not stop the other two.
- [ ] CONTEXT_MANIFEST reported with accurate counts, including VIEWPORT COVERAGE.
