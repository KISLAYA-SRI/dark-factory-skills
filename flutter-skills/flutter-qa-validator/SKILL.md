---
name: flutter-qa-validator
description: Automatically validates, formats, analyzes, and tests Flutter projects using dedicated MCP tools.
---

# Flutter QA and Validation Pipeline

Use this skill when requested to validate code quality, install dependencies, run code formatting checks, run static analysis, or execute unit/widget tests on a Flutter project.

## 1. Context Configuration
* Every MCP tool in this playbook requires a target directory.
* Always pass the absolute or relative project root directory to the `path` argument.
* Do **not** pass `workspace_id` when using the `path` argument.

## 2. Core Execution Workflows

### A. Fresh Environment Setup & Validation
When checking a fresh repository or verifying system readiness:
1. Call `validate_project` with `path` to ensure the Flutter SDK is available and the project structure is valid.
2. Call `run_pub_get` with `path` to resolve and download all required project dependencies.

### B. Pre-Commit / Code Quality Check
When verifying code health before merge or testing:
1. Call `run_format` with `path` to check if all Dart files conform to official style guidelines.
2. Call `run_analyze` with `path` to trigger static analysis. 
3. Evaluate the structured issues returned by `run_analyze`. Do not proceed to testing if blocker/error-level issues are present.

### C. Test Execution
When verifying functional stability:
1. Call `run_tests` with `path` to execute the Flutter test suite.
2. Parse the structured results to isolate failures by file and test name.

## 3. Pipeline Order & Step-by-Step Chain
When asked to run a **complete validation pipeline**, the agent must execute tools in this exact strict order:
1. `validate_project` (Fails fast if SDK is missing)
2. `run_pub_get` (Fails fast if dependencies are broken)
3. `run_format` (Identifies styling discrepancies)
4. `run_analyze` (Catches compilation and syntax issues)
5. `run_tests` (Runs final test suites)

## 4. Error Mitigation and Recovery
* **Missing Dependencies**: If `run_analyze` or `run_tests` reports missing packages or generated files, re-run `run_pub_get`.
* **Formatting Errors**: If `run_format` fails due to unformatted code, explicitly inform the user or agent sub-routines to run format fixes before committing.
* **Analysis Failures**: Treat any errors returned by `run_analyze` as fatal pipeline breaks. Stop execution immediately and report the file line/column details.
