---
name: clean-code-architecture
description: Use when reviewing, refactoring, or designing Java Spring Boot backend API microservices, async microservices, or adapter libraries for clean code and software architecture quality. Triggers include clean code, code smell, refactor, SOLID, single responsibility, tight coupling, God class, architecture review, layering violation, dependency direction, naming review, cyclomatic complexity, duplicate code, DRY violation, or design quality feedback.
---

# Clean Code and Software Architecture Design

Apply clean-code and software-architecture principles to Java Spring Boot backend API microservices, async microservices, and adapter libraries. Use this skill for design review, refactoring, and architecture guidance across the codebase produced by `backend-api-microservice`, `backend-async-microservice`, and `adapter-lib`. This skill does not change public API contracts, event contracts, or existing layering conventions — it improves the quality of code within those boundaries.

> **Important:** This skill does NOT introduce a new architecture, framework, or package layout. It enforces clean structure, naming, and dependency direction within the repository's existing layered shape (`Controller/Listener -> Service interface -> ServiceImpl -> adapter/shared-lib client`).

> **No Human-in-the-Loop:** This skill runs as an autonomous step in an agentic workflow. It never pauses for user confirmation, style preference, or approval of a finding. Scope resolution, severity classification, and fix-vs-report decisions are driven by the deterministic rules in this document and by standard industry static-analysis thresholds. There is no pass/fail gate — the skill works through the checklist below and applies fixes directly.

---

## Code-Context Check (Perform Before Any Tool Calls)

This skill runs unattended inside an agentic workflow. There is no human in the loop to answer clarifying questions, so scope must be resolved autonomously from available signals, never by pausing for user input.

```
IF code-context already contains:
  - the changed/target files or classes
  - the reason for review (new code review, pre-existing smell, architecture question)
THEN:
  → Proceed directly to Step 1 (Inspect Current Structure)
ELSE:
  → Resolve scope autonomously using this precedence:
    1. Files changed in the current diff/branch/commit (git status/diff).
    2. Files or classes just produced/modified by an upstream skill in this workflow
       (backend-api-microservice, backend-async-microservice, adapter-lib).
    3. If neither is available, default to the smallest identifiable unit passed in
       the task (named module, package, or file) and proceed with that.
  → If truly no scope signal exists anywhere, skip this skill run and report that no
    target was resolvable rather than blocking the workflow.
```

Do not run a repository-wide refactor sweep unless explicitly requested. Default to the smallest scope that satisfies the request: a changed file, a changed class, or a named package.

---

## Step 1 — Inspect Current Structure

1. Identify the repository shape (`backend-api-microservice`, `backend-async-microservice`, or `adapter-lib`) and confirm the existing layer boundaries.
2. Read the target class(es) fully before proposing changes.
3. Identify existing naming, mapping, logging, and exception conventions nearby, and treat them as the baseline style.
4. Note any test coverage for the target class so behavior-preserving refactors can be verified afterward.

---

## Clean Code Principles

Apply these checks to any class under review:

- **Naming**: classes, methods, and variables state intent without needing a comment. Avoid abbreviations, Hungarian notation, and generic names like `data`, `helper`, `manager` unless the codebase already uses that convention consistently.
- **Single Responsibility**: a class should have one reason to change. Split classes that mix HTTP/listener concerns, orchestration, mapping, and downstream calls.
- **Method size and depth**: prefer short methods with a single level of abstraction. Extract private helper methods for repeated validation, mapping, or branching logic instead of nesting conditionals.
- **Function arguments**: prefer 3 or fewer parameters; introduce a request/parameter object when a method needs more.
- **Avoid duplication (DRY)**: extract shared logic into existing mapper, helper, or utility classes rather than copy-pasting across controllers, listeners, services, or adapters.
- **Comments**: prefer self-explanatory code. Use comments only for non-obvious business rules, external constraints, or workarounds, not to explain what the code does line by line.
- **Error handling**: fail fast with clear exceptions; do not swallow exceptions or return sentinel values (`null`, `-1`, empty string) to signal failure when the codebase uses exceptions elsewhere.
- **Immutability**: prefer immutable DTOs and `final` fields where the existing code style already supports it; avoid introducing mutable shared state.
- **Magic values**: replace repeated literals and magic numbers with named constants, enums, or existing constants classes.
- **Boy Scout Rule**: when touching a file for an unrelated change, leave adjacent code slightly cleaner without expanding the diff into unrelated refactors.

---

## Software Architecture Principles

Apply these checks at the class-collaboration and layer level:

- **Dependency direction**: dependencies must point inward/downward through the existing layers (`Controller/Listener -> Service -> ServiceImpl -> adapter/shared-lib client`). Never let adapters depend on service-layer or controller-layer types, and never let controllers/listeners call adapter/shared-lib clients directly.
- **SOLID**:
  - *Single Responsibility*: one class, one concern (see Clean Code above).
  - *Open/Closed*: extend behavior through new implementations, strategy objects, or configuration rather than editing unrelated branches inside a shared class.
  - *Liskov Substitution*: subtypes and interface implementations must honor the behavior and contracts callers already rely on.
  - *Interface Segregation*: keep service/client interfaces focused; do not force implementers to support unrelated methods.
  - *Dependency Inversion*: depend on interfaces (service interfaces, client ports) rather than concrete implementations; inject dependencies through the constructor.
- **Coupling and cohesion**: favor high cohesion within a class/package and low coupling between packages. Flag classes that reach across multiple unrelated packages' internals instead of using their public interfaces.
- **God classes / feature envy**: split classes that have grown to own controller, orchestration, mapping, and downstream-call responsibilities together; move logic to the class that owns the data it operates on.
- **Reactive integrity**: keep `Mono`/`Flux` chains non-blocking end-to-end; never introduce `block()` to simplify a refactor.
- **Configuration over hardcoding**: externalize environment-specific values (URLs, timeouts, feature toggles) through existing configuration properties classes instead of embedding them in business logic.
- **Testability**: prefer constructor injection and small collaborators so classes can be unit tested without a full Spring context; flag static/singleton access that blocks testability.

---

## Refactor Workflow

This skill operates without human-in-the-loop approval. Do not pause to ask whether a finding should be fixed — apply the decision rules below deterministically and proceed.

1. Identify one concrete smell or violation at a time (for example: "ServiceImpl directly builds HTTP headers and calls WebClient" or "controller method exceeds 40 lines with 3 responsibilities").
2. Classify it using the Severity Model below.
3. Decide automatically:
   - **Blocker/Major** → propose the minimal structural change that resolves it within the existing layering (extract method, extract class, introduce interface, move method, replace magic value with constant) and apply it.
   - **Minor** → apply only if it is a same-file, no-contract-impact change (Boy Scout Rule); otherwise log it as a finding without editing.
   - **Info/style preference with no objective standard backing it** → report only, do not edit.
4. Preserve public API contracts, event contracts, method signatures used by other classes, and existing package boundaries. Never perform a breaking boundary change autonomously, even if a Blocker finding suggests one — downgrade to a reported finding with a recommended follow-up ticket instead.
5. Apply the change.
6. Re-run or point to `test-project` for any existing tests covering the refactored class to confirm behavior is unchanged. Treat a failing post-refactor test run as a signal to revert that specific change, not to proceed regardless.
7. If no tests exist for the refactored behavior, name `unit-testing` as a follow-up in the Completion Summary rather than silently skipping verification.

Do not perform large-scale rewrites in a single pass. Prefer a sequence of small, verifiable refactors over one sweeping change. Cap autonomous refactors per run to keep diffs reviewable in CI (default: no more than 10 classes per invocation unless the task explicitly raises the limit).

### Severity Model (Standard Industry Practice)

| Severity | Criteria |
|---|---|
| **Blocker** | Layering/dependency-direction violation, blocking call (`block()`) in reactive code, swallowed exception (empty catch or catch-and-return-null), hardcoded secret/credential/environment URL, public contract breakage. |
| **Major** | God class (see thresholds below), SRP violation, missing constructor injection for testable collaborators, duplicated logic across 3+ locations, missing/incorrect error propagation for downstream failures. |
| **Minor** | Method/parameter-count thresholds exceeded (see below), magic values, naming inconsistent with local convention, missing `final`/immutability where locally idiomatic. |
| **Info** | Subjective style preferences not backed by an objective threshold or an existing local convention. |

Use industry-standard static-analysis thresholds as the objective bar (aligned with common Sonar/Checkstyle/PMD defaults) when no stricter local convention exists:

- Cyclomatic complexity per method: flag above 10 (Major), above 15 (Blocker-level refactor candidate).
- Method length: flag above ~40 executable lines.
- Class length: flag above ~500 lines or clear multi-responsibility mixing.
- Parameter count: flag above 4 (prefer 3 or fewer per Clean Code Principles).
- Nesting depth: flag above 3 levels of nested conditionals/loops.
- Duplicate code blocks: flag blocks of 6+ duplicated lines appearing in 2+ places.
- Cognitive complexity: treat any method mixing validation, orchestration, and downstream I/O in one block as Major regardless of line count.

These thresholds are defaults for autonomous triage, not hard rules that override an existing project-specific static-analysis configuration (e.g., `sonar-project.properties`, Checkstyle/PMD rulesets already in the repo). When the repo defines its own thresholds, those take precedence.

---

## Review Checklist (Standard Industry Practice)

When asked to review rather than refactor — or as the standard pass after any autonomous refactor — work through this checklist in order for the target scope. There is no reviewer to consult and no gate to pass or fail; the checklist is the fixed procedure to follow to completion. This checklist mirrors widely adopted static-analysis and architecture-review standards (SonarQube quality-gate categories, Google/OWASP secure-coding baselines, and standard SOLID/Clean Code criteria) so the process is reproducible across runs.

1. **Correctness & Contracts**
   - Public API/event contracts, method signatures used elsewhere, and response/error shapes are unchanged unless explicitly requested.
   - No behavior change introduced outside the stated intent of the review/refactor.
2. **Security baseline**
   - No hardcoded secrets, tokens, credentials, or environment-specific URLs.
   - No sensitive data (PII, tokens, full downstream payloads) logged.
   - Input validation present at trust boundaries (controller/listener entry points).
3. **Reliability & error handling**
   - No empty catch blocks or catch-and-swallow patterns.
   - No sentinel-value error signaling (`null`/`-1`/empty string) where exceptions are the local convention.
   - Downstream/adapter errors are mapped through the existing exception/handler convention.
4. **Reactive correctness** (when reactive types are in scope)
   - No `block()`, `subscribe()` for control flow, or unmanaged threads/executors.
   - `Mono`/`Flux` chains complete with explicit success/error handling.
5. **Architecture & dependency direction**
   - Dependency direction respects `Controller/Listener -> Service -> ServiceImpl -> adapter/shared-lib client`.
   - No adapter-layer dependency on service/controller-layer types.
   - Interfaces/ports depended upon, not concrete implementations, at layer boundaries (Dependency Inversion).
6. **Responsibility & cohesion**
   - No God classes: class length, responsibility count, and cyclomatic/cognitive complexity within the thresholds defined in the Severity Model.
   - No feature envy: logic operates on the data owned by its own class rather than reaching into another class's internals.
7. **Duplication**
   - No duplicate blocks of 6+ lines repeated across 2+ locations without extraction to a shared helper/mapper.
8. **Naming & readability**
   - Names state intent; no ambiguous single-letter or generic (`data`, `helper`, `manager`) names outside established local convention.
   - Comments explain non-obvious rules only, not restate code.
9. **Testability**
   - Constructor injection used for collaborators; no static/singleton access blocking isolated unit testing.
   - Existing or newly required tests for changed behavior are identified.

### Handling Findings

Work through every checklist item for the target scope; do not stop partway or skip items. For each item found to be non-compliant, apply the corresponding fix-vs-report decision from the Refactor Workflow's Severity Model (Blocker/Major → fix directly within existing boundaries; Minor → fix only if same-file and contract-safe, otherwise note it; Info → note it only). Once every item has been worked through, the pass is complete — move straight to the Completion Summary without producing a separate findings report.

---

## Completion Summary

Once the Refactor Workflow and Review Checklist have been worked through, emit a short, non-blocking summary and let the workflow continue — this skill never halts or gates subsequent steps:

- **Scope**: files/classes touched.
- **Changes/findings**: one line per item, e.g. `ServiceImpl.java: extracted header-building to HeaderMapper (Major)`. Only note items that were fixed or deliberately left for a follow-up ticket; skip a line-by-line restatement of the checklist.
- **Follow-up**: name any skill worth queuing next (`test-project`, `unit-testing`) only if a change needs verification; otherwise omit this line.

Keep the summary to a few lines. Any unresolved item (including a deliberately-skipped boundary change) is noted inline as a follow-up, not treated as a blocker — this skill always completes and hands control back to the workflow.
