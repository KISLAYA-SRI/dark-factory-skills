# Dark Factory Skills

This folder contains skills for FAB platform common libraries. Each skill is self-contained in its own directory with a `SKILL.md` entry point and optional `references/` files for details that should be loaded only when needed.

## Available Skills

- `platform-rest-client` - Use FAB platform REST client for outbound HTTP calls, `HttpService`, `ReactiveHttpService`, authentication, caching, timeouts, and replacing raw HTTP clients.
- `platform-security` - Use FAB platform security for user tokens, service tokens, ACR, scopes, stepup authentication, and security context.
- `platform-logging` - Use FAB platform logging for structured logging, correlation context, reactive logging, and masking.
- `platform-exception` - Use FAB platform exception handling for standardized exceptions, global error responses, correlation IDs, and masking.
- `platform-events` - Use FAB platform events for event publishing, event consumption, handlers, retries, DLQ, and topic routing.
