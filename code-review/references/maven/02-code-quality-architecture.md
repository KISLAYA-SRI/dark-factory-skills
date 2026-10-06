# Code Quality & Architecture Review — Java / Maven / Spring Boot

## Role

Review changed Java code as a Senior Software Architect would: naming, structure, architectural alignment, performance, and test coverage for the **changed/added lines**, not a full-file sweep.

## Expected Layering (Baseline to Check Against)

```text
Controller/Listener -> Service interface -> ServiceImpl -> adapter/shared-lib client
```

- Controllers/listeners validate and delegate; they must not call adapter/shared-lib clients directly.
- Only `ServiceImpl` talks to adapter/shared-lib clients.
- Adapters must not depend on service- or controller-layer types.
- Dependencies are injected through the constructor, not field injection or static access.

## Checklist

1. **Naming & readability** — classes/methods/variables state intent without a comment; no generic names (`data`, `helper`, `manager`) unless already the local convention.
2. **Single Responsibility** — flag a changed class that now mixes HTTP/listener concerns, orchestration, mapping, and downstream calls in one place.
3. **Method size/complexity** — flag new/changed methods over ~40 executable lines, cyclomatic complexity over 10, or nesting deeper than 3 levels.
4. **Function arguments** — flag new methods with more than 3-4 parameters; suggest a request/parameter object.
5. **Duplication (DRY)** — flag 6+ duplicated lines introduced by the diff that already exist elsewhere (mapper, helper, utility) instead of being reused.
6. **Architecture/dependency direction** — flag any new call that skips a layer (e.g., controller directly invoking an adapter client) or that makes an adapter depend on service/controller types.
7. **Error handling** — flag empty `catch` blocks, catch-and-return-`null`/`-1` patterns where the codebase uses exceptions elsewhere, and unmapped downstream/adapter errors.
8. **Reactive correctness** (if `Mono`/`Flux` are in scope) — flag any new `block()` call, `subscribe()` used for control flow, or an unmanaged executor/thread introduced in reactive code.
9. **Constants over magic values** — flag new repeated literals (numeric, string, duration/threshold) that should be named `static final` constants.
10. **Dead code & redundancy** — flag unused imports/fields/parameters introduced by the diff, unreachable branches, or unnecessary `else` after `return`/`throw`.
11. **Resource & API hygiene** — flag missing try-with-resources for new `Closeable`/`AutoCloseable` usage, `==` for object comparison instead of `equals()`/`Objects.equals()`, and `System.out`/`printStackTrace` instead of the existing logging framework.
12. **Testability** — flag new collaborators wired via static/singleton access instead of constructor injection.
13. **Test coverage** — flag non-trivial new business logic, new branches, or new exception paths introduced by the diff with no corresponding new/updated test.

## Examples

### Layering Violation

```java
// FLAG — [ISSUE] controller calling adapter client directly, skipping Service/ServiceImpl
@RestController
public class AccountController {
    private final NiAdapterClient niAdapterClient; // should go through AccountService

    @GetMapping("/accounts/{id}")
    public ResponseEntity<AccountDto> get(@PathVariable String id) {
        return ResponseEntity.ok(niAdapterClient.fetch(id)); // ARCHITECTURE VIOLATION
    }
}
```

### Swallowed Exception

```java
// FLAG — [BLOCKER] empty catch hides a real failure
try {
    downstreamClient.notify(event);
} catch (Exception e) {
    // nothing — swallowed
}

// ACCEPTABLE
try {
    downstreamClient.notify(event);
} catch (DownstreamException e) {
    log.error("Failed to notify downstream for event {}", event.getId(), e);
    throw new ServiceException("Notification failed", e);
}
```

### Blocking Call in Reactive Code

```java
// FLAG — [BLOCKER] block() defeats the reactive chain and can exhaust the event loop
Account account = accountClient.getAccount(id).block();

// ACCEPTABLE
return accountClient.getAccount(id)
    .doOnSuccess(a -> log.debug("fetched account {}", a.getId()))
    .doOnError(e -> log.error("failed to fetch account {}", id, e));
```

### Magic Values

```java
// FLAG — [SUGGESTION] magic number with unclear intent
if (retryCount > 3) { ... }

// ACCEPTABLE
private static final int MAX_RETRY_ATTEMPTS = 3;
if (retryCount > MAX_RETRY_ATTEMPTS) { ... }
```

### Missing Test Coverage

```java
// New branch added in the diff:
if (request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
    throw new ValidationException("Amount must be positive");
}
// FLAG — [ISSUE] no corresponding test asserting ValidationException for a zero/negative amount
```

## Severity Guidance for This Dimension

- **[BLOCKER]**: blocking call in reactive code, swallowed exception that hides a failure, public API/event contract breakage.
- **[ISSUE]**: layering/dependency-direction violation, SRP violation, missing constructor injection, duplicated logic (3+ places), missing tests for new non-trivial logic, missing/incorrect error propagation.
- **[SUGGESTION]**: naming, magic values, minor same-file duplication, missing `final`/immutability, comment hygiene, verbose conditionals.

## When Nothing Is Found

If the diff introduces no quality/architecture concern from the checklist above, state plainly that the code quality and architecture of the change are sound. Do not invent findings to pad the review.
