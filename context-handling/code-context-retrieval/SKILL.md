---
name: code-context-retrieval
description: Use when an implementation agent needs external code context from RAG before editing, including adapter-lib usage, shared library APIs, reusable client contracts, fintech/downstream integration context, or any referenced codebase resource. For domain services, this skill enforces using a context-retrieval sub-agent with Account Name, Project Name, Resource Name, and query, and prevents direct fintech API calls when an adapter/shared library must be used.
---

# Code Context Retrieval

Use this skill to obtain concise codebase context from RAG before implementation when the required API, adapter, shared library, or reusable contract is not fully present in the local repository or supplied `code-context.md`.

## Calling-Agent Workflow

When you are a domain, adapter, test, or review agent that needs code context from another codebase:

1. Identify the needed context from `code-context.md`, the assigned task, and the local repo.
2. Start or call a context-retrieval sub-agent instead of querying RAG directly.
3. Pass these fields to the sub-agent:
   - `Account Name`
   - `Project Name`
   - `Resource Name`
   - `Query`
4. Make the query specific to the code you need: target class, method, package, contract, configuration, DTO, error behavior, or usage example.
5. Use only the returned context plus local code. Do not invent missing APIs, DTOs, config keys, headers, or behavior.

## Fintech / Downstream Rule For Domain Agents

Domain services must not call fintech systems directly when an adapter/shared library is required or available.

- If `code-context.md` names an adapter/shared library, use this skill before implementing the fintech/downstream interaction.
- Ask the context-retrieval sub-agent for the adapter/shared library client, method contract, DTOs, required configuration, headers, errors, and a minimal usage example.
- If no adapter/shared library can be found, stop before editing the fintech integration and report the blocker.
- Do not use raw REST clients, `WebClient`, `RestTemplate`, Feign, or `$platform-rest-client` to bypass an adapter/shared library for fintech calls.

## Required Sub-Agent Request Shape

Use a compact request like:

```text
Account Name: <account>
Project Name: <project>
Resource Name: <resource>
Query: <specific code context needed>
```

Example for adapter context:

```text
Account Name: FABKSA
Project Name: BackendJavaAdapterLib
Resource Name: adapter_lib_ni_adaptor
Query: Find the client method, request/response DTOs, required headers, configuration properties, and example usage for the NI adapter operation needed by this domain API.
```

## Stop Conditions

Stop and communicate the blocker when:

- The task needs external code context but any of `Account Name`, `Project Name`, or `Resource Name` is missing.
- The context-retrieval sub-agent returns no relevant result after retries.
- The returned context does not include enough contract detail to implement safely.
- A domain fintech call would require direct fintech API access because no adapter/shared library was found.

## Using Returned Context

- Prefer existing local imports, beans, and patterns over adding new wiring.
- Reuse the exact client names, method names, DTOs, config keys, and headers from the returned context.
- Keep implementation scope limited to the assigned task.
- Record unresolved gaps in the final response or `ss_code_gen.md` when required by the stage prompt.
