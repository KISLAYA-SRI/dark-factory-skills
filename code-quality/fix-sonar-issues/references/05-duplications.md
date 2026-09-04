# Dimension 5: Duplications (Code Duplication) — Fix Patterns & Examples

## Overview

SonarQube flags duplicated blocks (default: 10+ identical lines in 3+ files, or 100+ tokens). Target: **< 3% duplication**.

---

## Identifying Duplicated Code from SonarQube

1. In SonarQube UI → Project → **Duplications** tab.
2. Click on a file to see highlighted duplicated blocks.
3. SonarQube shows the other files where the same block appears.
4. Use the API: `GET /api/measures/component?metricKeys=duplicated_lines_density,duplicated_blocks`

---

## Refactoring Strategy: Extract Method

```java
// BAD - same validation logic duplicated in 3 controllers
// UserController.java
if (request.getName() == null || request.getName().isBlank()) {
    throw new ValidationException("Name is required");
}
if (request.getEmail() == null || !request.getEmail().contains("@")) {
    throw new ValidationException("Valid email is required");
}

// ProfileController.java - SAME block duplicated
if (request.getName() == null || request.getName().isBlank()) {
    throw new ValidationException("Name is required");
}
...

// GOOD - extract to a shared validator
@Component
public class UserRequestValidator {
    public void validate(UserRequest request) {
        if (request.getName() == null || request.getName().isBlank()) {
            throw new ValidationException("Name is required");
        }
        if (request.getEmail() == null || !request.getEmail().contains("@")) {
            throw new ValidationException("Valid email is required");
        }
    }
}

// Use in both controllers
@Autowired
private UserRequestValidator validator;

// In controller method:
validator.validate(request);
```

---

## Refactoring Strategy: Extract Class

```java
// BAD - duplicate pagination logic in multiple service classes
// UserService.java
public Page<UserDto> getUsers(int page, int size) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
    return userRepository.findAll(pageable).map(userMapper::toDto);
}

// ProductService.java - SAME pattern
public Page<ProductDto> getProducts(int page, int size) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
    return productRepository.findAll(pageable).map(productMapper::toDto);
}

// GOOD - extract pagination utility
public class PaginationUtils {
    public static Pageable defaultPageable(int page, int size) {
        return PageRequest.of(page, size, Sort.by("createdAt").descending());
    }

    public static Pageable pageableWithSort(int page, int size, String sortField) {
        return PageRequest.of(page, size, Sort.by(sortField).descending());
    }
}

// Usage
Pageable pageable = PaginationUtils.defaultPageable(page, size);
```

---

## Refactoring Strategy: Template Method Pattern

```java
// BAD - duplicated processing pipeline in multiple classes
// EmailNotificationService.java
public void send(Notification notification) {
    validate(notification);           // same
    enrich(notification);             // same
    String content = buildEmail(notification);  // different
    emailClient.send(content);        // different
    audit(notification);              // same
}

// SmsNotificationService.java - 3 of 5 steps duplicated
public void send(Notification notification) {
    validate(notification);           // duplicated
    enrich(notification);             // duplicated
    String content = buildSms(notification);    // different
    smsClient.send(content);          // different
    audit(notification);              // duplicated
}

// GOOD - Template Method pattern
public abstract class BaseNotificationService {
    public final void send(Notification notification) {
        validate(notification);
        enrich(notification);
        String content = buildContent(notification); // abstract
        deliver(content);                            // abstract
        audit(notification);
    }

    protected abstract String buildContent(Notification notification);
    protected abstract void deliver(String content);

    private void validate(Notification n) { ... }
    private void enrich(Notification n) { ... }
    private void audit(Notification n) { ... }
}

public class EmailNotificationService extends BaseNotificationService {
    @Override
    protected String buildContent(Notification n) { return buildEmail(n); }
    @Override
    protected void deliver(String content) { emailClient.send(content); }
}
```

---

## Consolidating Spring Boot @RequestMapping Patterns

```java
// BAD - duplicated error response construction in multiple controllers
// UserController.java
catch (ResourceNotFoundException e) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(Map.of("error", e.getMessage(), "timestamp", Instant.now()));
}

// OrderController.java - SAME pattern
catch (ResourceNotFoundException e) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(Map.of("error", e.getMessage(), "timestamp", Instant.now()));
}

// GOOD - centralized @RestControllerAdvice
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getMessage(), Instant.now()));
    }
}
// Remove try-catch from individual controllers
```

---

## Shared Validation Logic

```java
// BAD - same @Pattern annotations duplicated across multiple request DTOs
public class LoginRequest {
    @Pattern(regexp = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")
    private String email;
}
public class RegisterRequest {
    @Pattern(regexp = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$") // duplicated
    private String email;
}

// GOOD - custom constraint annotation
@Documented
@Constraint(validatedBy = {})
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Email(message = "Must be a valid email address")
public @interface ValidEmail {
    String message() default "Invalid email format";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

// Usage in multiple DTOs
@ValidEmail
private String email;
```

---

## Near-Duplicates vs Exact Duplicates

- **Exact duplicates** (same tokens): Extract to shared method/class immediately.
- **Near-duplicates** (slight variations): Parameterize the varying parts:

```java
// Near-duplicate: same logic, different field names
private String buildUserAuditMessage(User user) {
    return String.format("[%s] User %s action at %s", user.getId(), user.getName(), Instant.now());
}
private String buildOrderAuditMessage(Order order) {
    return String.format("[%s] Order %s action at %s", order.getId(), order.getRef(), Instant.now());
}

// GOOD - parameterize
private String buildAuditMessage(String entityId, String entityName) {
    return String.format("[%s] %s action at %s", entityId, entityName, Instant.now());
}
```

---

## Utility vs Inheritance Decision

- Use **utility/helper classes** (static methods) when: logic is stateless, no Spring beans needed, purely functional transformation.
- Use **inheritance/composition** when: shared behavior requires state, Spring lifecycle management, or polymorphism.
- Prefer **composition over inheritance** for Spring services.
