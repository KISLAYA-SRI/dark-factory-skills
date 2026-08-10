# Generate API Code

Small Codex skill for generating or extending Spring Boot backend API microservices.

## Use This For

- Adding REST endpoints to Java Spring Boot services.
- Wiring controller, service interface, and `ServiceImpl` layers.
- Reusing adapter-lib or shared-lib clients for downstream calls.
- Adding DTO validation, OpenAPI annotations, and error handling in the project's existing style.

## Expected Flow

```text
Controller -> Service interface -> ServiceImpl -> adapter/shared-lib client
```

Controllers validate requests and delegate. `ServiceImpl` owns orchestration, mapping, downstream calls, and reactive behavior when present.

## Key Rules

- Follow nearby controller, service, mapper, and exception patterns.
- Reuse existing response envelopes and public error structures.
- Keep downstream client calls out of controllers.
- Use existing adapter/shared-library dependencies before adding local downstream code.
- Preserve non-blocking reactive chains; do not call `block()` inside services.
- Keep headers, validation rules, and OpenAPI annotations aligned with the provided contract.

See [SKILL.md](./SKILL.md) for the full instructions.
