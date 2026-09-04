# Dimension 1: Reliability (Bugs) — Fix Patterns & Examples

## Overview

Reliability issues are defects that represent incorrect behavior at runtime. SonarQube flags these as **Bugs**. Fix all BLOCKER and CRITICAL bugs before proceeding to lower severities.

---

## Null Pointer Dereference

```java
// BAD - potential NPE
String value = map.get(key).toString();

// GOOD - null-safe
String value = Optional.ofNullable(map.get(key))
    .map(Object::toString)
    .orElse("");

// GOOD - Objects.requireNonNullElse (Java 9+)
String value = Objects.requireNonNullElse(map.get(key), "").toString();
```

---

## Resource Leaks

```java
// BAD - stream not closed
InputStream is = new FileInputStream(file);
byte[] data = is.readAllBytes();

// GOOD - try-with-resources
try (InputStream is = new FileInputStream(file)) {
    byte[] data = is.readAllBytes();
}
```

---

## Reactive Stream Error Handling (Mono/Flux)

For Spring WebFlux projects, always handle errors in reactive chains:

```java
// BAD - no error handling
return userRepository.findById(id)
    .map(UserMapper::toDto);

// GOOD - explicit error handling
return userRepository.findById(id)
    .map(UserMapper::toDto)
    .switchIfEmpty(Mono.error(new ResourceNotFoundException("User not found: " + id)))
    .onErrorMap(DataAccessException.class, ex ->
        new ServiceException("Database error fetching user", ex));

// GOOD - doOnError for logging without swallowing
return externalService.call(request)
    .doOnError(ex -> log.error("External call failed: {}", ex.getMessage()))
    .onErrorReturn(fallbackResponse);
```

---

## Exception Handling Best Practices

```java
// BAD - swallowing exception
try {
    process();
} catch (Exception e) {
    // silent
}

// BAD - catching generic Exception when specific is known
try {
    Integer.parseInt(value);
} catch (Exception e) { ... }

// GOOD - catch specific, log, rethrow or handle
try {
    Integer.parseInt(value);
} catch (NumberFormatException e) {
    log.warn("Invalid numeric value: {}", value);
    throw new ValidationException("Value must be numeric", e);
}

// BAD - throwing generic exception
public void process() throws Exception { ... }

// GOOD - throw specific checked or runtime exception
public void process() throws ProcessingException { ... }
```

---

## Incorrect Equals / HashCode

```java
// BAD - comparing strings with ==
if (status == "ACTIVE") { ... }

// GOOD
if ("ACTIVE".equals(status)) { ... }

// BAD - mutable field in hashCode
@Override
public int hashCode() {
    return Objects.hash(id, mutableList); // mutableList changes break contracts
}

// GOOD - use only immutable/identity fields
@Override
public int hashCode() {
    return Objects.hash(id);
}
```

---

## Concurrency Issues

```java
// BAD - non-thread-safe lazy init
private static Config instance;
public static Config getInstance() {
    if (instance == null) instance = new Config(); // race condition
    return instance;
}

// GOOD - double-checked locking
private static volatile Config instance;
public static Config getInstance() {
    if (instance == null) {
        synchronized (Config.class) {
            if (instance == null) instance = new Config();
        }
    }
    return instance;
}

// BETTER - initialization-on-demand holder
private static class Holder {
    static final Config INSTANCE = new Config();
}
public static Config getInstance() { return Holder.INSTANCE; }
```
