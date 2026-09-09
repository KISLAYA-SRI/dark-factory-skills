# Dimension 3: Maintainability (Code Smells) — Fix Patterns & Examples

## Overview

Code smells reduce readability and make future changes risky. Fix by reducing complexity, removing dead code, and improving naming.

---

## Cognitive Complexity Reduction

SonarQube flags methods with cognitive complexity > 15. Strategies:

```java
// BAD - high cognitive complexity (nested ifs, loops, conditions)
public String processOrder(Order order) {
    if (order != null) {
        if (order.getStatus() == OrderStatus.PENDING) {
            if (order.getItems() != null && !order.getItems().isEmpty()) {
                for (OrderItem item : order.getItems()) {
                    if (item.getQuantity() > 0) {
                        if (item.getPrice() > 0) {
                            // process
                        }
                    }
                }
            }
        }
    }
    return "done";
}

// GOOD - extract methods, use guard clauses, streams
public String processOrder(Order order) {
    validateOrder(order);
    processValidItems(order.getItems());
    return "done";
}

private void validateOrder(Order order) {
    Objects.requireNonNull(order, "Order must not be null");
    if (order.getStatus() != OrderStatus.PENDING) {
        throw new IllegalStateException("Order is not in PENDING status");
    }
}

private void processValidItems(List<OrderItem> items) {
    if (items == null || items.isEmpty()) return;
    items.stream()
        .filter(item -> item.getQuantity() > 0 && item.getPrice() > 0)
        .forEach(this::processItem);
}
```

---

## Method Length and Class Size

- Methods: Keep under 30 lines (SonarQube default threshold: 150 lines).
- Classes: Keep under 200 lines of code (excluding comments/blanks).
- Extract private helper methods for distinct logical steps.
- Split large classes using Single Responsibility Principle.

---

## Dead Code Removal

```java
// BAD - unused private method
private String formatLegacy(String input) { ... } // never called

// BAD - unused import
import java.util.Vector; // Vector not used anywhere

// BAD - unreachable code
public String getValue() {
    return result;
    log.debug("returned"); // unreachable
}

// FIX - remove all dead code
```

---

## Magic Numbers and Strings

```java
// BAD
if (user.getAge() > 18) { ... }
if (status.equals("ACTIVE")) { ... }
Thread.sleep(5000);

// GOOD - named constants
private static final int MINIMUM_AGE = 18;
private static final String STATUS_ACTIVE = "ACTIVE";
private static final long RETRY_DELAY_MS = 5_000L;

if (user.getAge() > MINIMUM_AGE) { ... }
if (STATUS_ACTIVE.equals(status)) { ... }
Thread.sleep(RETRY_DELAY_MS);

// BETTER - use enums for status
public enum UserStatus { ACTIVE, INACTIVE, SUSPENDED }
if (user.getStatus() == UserStatus.ACTIVE) { ... }
```

---

## Naming Conventions

```java
// BAD
public class Mgr { ... }           // abbreviation
private int d;                     // single letter
public void doIt() { ... }         // vague
public List<User> getUsrs() { ... } // typo

// GOOD
public class UserManager { ... }
private int durationInSeconds;
public void processUserRegistration() { ... }
public List<User> getUsers() { ... }
```

---

## Boolean Expression Simplification

```java
// BAD
if (isValid == true) { ... }
if (isActive != false) { ... }
return (count > 0) ? true : false;

// GOOD
if (isValid) { ... }
if (isActive) { ... }
return count > 0;
```
