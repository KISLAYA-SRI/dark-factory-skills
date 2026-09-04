---
name: sonar-analysis
description: Use when fetching, triaging, fixing, or summarizing SonarQube quality gate issues for a Java Maven backend microservice or adapter library. Triggers include SonarQube, Sonar quality gate, projectKey, current analysis issues, blocker/critical/major/minor issues, code smell, vulnerability, security hotspot, unit test coverage, code duplication, or any of the 6 SonarQube quality dimensions: Reliability, Security, Maintainability, Coverage, Duplications, Security Hotspots.
---

# SonarQube Issue Remediation Skill

Use this skill for comprehensive SonarQube quality gate remediation across all 6 quality dimensions. Keep fixes minimal, behavior-preserving, and scoped to issues reported for the current analysis.

## Inputs

Use the supplied project key, branch/analysis context, repository path, prior handoff, and assigned Sonar tooling. If issue details are already provided in context, use them. Otherwise, use the assigned Sonar MCP/tooling to fetch only unresolved issues for the given project key and current analysis.

## Issue Scope

- Fix only issues that affect the current quality gate or are explicitly assigned.
- Skip issues already marked `WONTFIX` or `FALSE-POSITIVE`.
- Prioritize by severity: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`.
- Group issues by file before editing.
- For each issue, read the file, understand the rule and surrounding code, then apply the smallest safe fix.
- Address all 6 quality dimensions: Reliability (Bugs), Security (Vulnerabilities), Maintainability (Code Smells), Coverage (Unit Tests), Duplications, Security Hotspots.

## Fix Rules

- Preserve public APIs, runtime behavior, and test behavior.
- Prefer root-cause fixes over suppression.
- Do not refactor unrelated code.
- Keep diffs tight and scoped to the reported component/line.
- Do not change generated code unless the repo already treats that generated source as editable.
- Do not weaken validation, security, error handling, logging masks, or concurrency behavior to satisfy a rule.
- If a finding is ambiguous or risky, skip it with a concise reason instead of guessing.

## Suppression Rules

Use suppression only when:

- The finding is a genuine false positive.
- The rule conflicts with an established convention in the codebase.
- The issue cannot be fixed safely without changing behavior.

If suppression is necessary, use the repo's established suppression style. `// NOSONAR` must include a short reason comment. Never suppress purely to pass the quality gate.

---

## Dimension 1: Reliability (Bugs)

### Overview
Reliability issues are defects that represent incorrect behavior at runtime. SonarQube flags these as Bugs. Fix all BLOCKER and CRITICAL bugs before proceeding to lower severities.

### Null Pointer Dereference

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

### Resource Leaks

```java
// BAD - stream not closed
InputStream is = new FileInputStream(file);
byte[] data = is.readAllBytes();

// GOOD - try-with-resources
try (InputStream is = new FileInputStream(file)) {
    byte[] data = is.readAllBytes();
}
```

### Reactive Stream Error Handling (Mono/Flux)

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

### Exception Handling Best Practices

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

### Incorrect Equals / HashCode

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

### Concurrency Issues

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

---

## Dimension 2: Security (Vulnerabilities)

### Overview
Security vulnerabilities are code flaws that attackers can exploit. Map each finding to OWASP Top 10 categories. Fix ALL security vulnerabilities regardless of severity.

### OWASP Top 10 Mapping

| SonarQube Rule | OWASP Category |
|---|---|
| SQL Injection | A03:2021 Injection |
| XSS | A03:2021 Injection |
| Insecure Deserialization | A08:2021 Software/Data Integrity |
| Broken Access Control | A01:2021 Broken Access Control |
| Sensitive Data Exposure | A02:2021 Cryptographic Failures |
| Hardcoded Credentials | A07:2021 Identification/Auth Failures |
| Vulnerable Dependencies | A06:2021 Vulnerable Components |

### SQL Injection Prevention

```java
// BAD - string concatenation in query
String query = "SELECT * FROM users WHERE name = '" + name + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);

// GOOD - parameterized query
String query = "SELECT * FROM users WHERE name = ?";
PreparedStatement ps = conn.prepareStatement(query);
ps.setString(1, name);
ResultSet rs = ps.executeQuery();

// GOOD - Spring Data JPA (preferred)
@Query("SELECT u FROM User u WHERE u.name = :name")
List<User> findByName(@Param("name") String name);
```

### Input Validation and Sanitization

```java
// BAD - no validation
@PostMapping("/users")
public ResponseEntity<UserDto> createUser(@RequestBody UserRequest request) {
    return ResponseEntity.ok(userService.create(request));
}

// GOOD - Bean Validation + explicit sanitization
@PostMapping("/users")
public ResponseEntity<UserDto> createUser(
        @Valid @RequestBody UserRequest request) {
    return ResponseEntity.ok(userService.create(request));
}

// In UserRequest
public class UserRequest {
    @NotBlank
    @Size(min = 2, max = 100)
    @Pattern(regexp = "^[a-zA-Z\\s'-]+$", message = "Name contains invalid characters")
    private String name;

    @NotBlank
    @Email
    private String email;
}
```

### Dependency Vulnerability Remediation

```xml
<!-- Check for vulnerable dependencies with OWASP plugin -->
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>9.0.9</version>
    <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>
    </configuration>
</plugin>
```

Steps to remediate:
1. Run `mvn dependency-check:check` to identify CVEs.
2. Check the CVE's fix version in the NVD database.
3. Update the dependency version in `pom.xml`.
4. If the vulnerable library is a transitive dependency, use `<dependencyManagement>` to force a safe version:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.15.4</version> <!-- force safe version -->
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Sensitive Data Exposure

```java
// BAD - logging sensitive data
log.info("User login: username={}, password={}", username, password);
log.debug("Token: {}", jwtToken);

// GOOD - mask sensitive fields
log.info("User login attempt: username={}", username);
log.debug("Token issued for user: {}", username); // log identity, not token

// BAD - returning sensitive data in API response
public class UserResponse {
    private String password;   // never expose
    private String ssn;        // never expose raw
    private String creditCard; // never expose raw
}

// GOOD - use DTOs that exclude sensitive fields
public class UserResponse {
    private String id;
    private String username;
    private String email;
    // no password, no ssn, no creditCard
}
```

### Hardcoded Credentials

```java
// BAD
private static final String DB_PASSWORD = "mySecret123";
private static final String API_KEY = "sk-abc123xyz";

// GOOD - externalize to environment variables or secrets manager
@Value("${db.password}")
private String dbPassword;

@Value("${external.api.key}")
private String apiKey;
```

```yaml
# application.yml - use placeholders, never literal secrets
spring:
  datasource:
    password: ${DB_PASSWORD}
external:
  api:
    key: ${EXTERNAL_API_KEY}
```

---

## Dimension 3: Maintainability (Code Smells)

### Overview
Code smells reduce readability and make future changes risky. Fix by reducing complexity, removing dead code, and improving naming.

### Cognitive Complexity Reduction

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

### Method Length and Class Size

- Methods: Keep under 30 lines (SonarQube default threshold: 150 lines).
- Classes: Keep under 200 lines of code (excluding comments/blanks).
- Extract private helper methods for distinct logical steps.
- Split large classes using Single Responsibility Principle.

### Dead Code Removal

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

### Magic Numbers and Strings

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

### Naming Conventions

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

### Boolean Expression Simplification

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

---

## Dimension 4: Coverage (Unit Test Coverage)

### Overview
SonarQube measures line coverage and branch coverage. The quality gate typically requires 80%+ overall coverage. New code often requires higher thresholds (e.g., 85% on new code).

### Identifying Uncovered Code from SonarQube

1. In SonarQube UI → Project → **Coverage** tab.
2. Click on a file to see line-by-line coverage (green = covered, red = uncovered).
3. Branch coverage shows uncovered `if/else`, `switch`, ternary branches.
4. Use the SonarQube API to fetch uncovered lines programmatically:
   ```
   GET /api/measures/component?component={projectKey}&metricKeys=uncovered_lines,uncovered_conditions
   ```

### JaCoCo Configuration

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <configuration>
        <excludes>
            <!-- Exclude generated code -->
            <exclude>**/*MapperImpl.class</exclude>      <!-- MapStruct -->
            <exclude>**/*_.class</exclude>               <!-- JPA metamodel -->
            <exclude>**/Q*.class</exclude>               <!-- QueryDSL -->
            <exclude>**/*Application.class</exclude>     <!-- Spring Boot main -->
            <exclude>**/config/**</exclude>              <!-- Config classes -->
            <exclude>**/dto/**</exclude>                 <!-- DTOs (POJOs) -->
            <exclude>**/entity/**</exclude>              <!-- JPA entities -->
            <exclude>**/exception/**</exclude>           <!-- Exception classes -->
        </excludes>
    </configuration>
    <executions>
        <execution>
            <id>prepare-agent</id>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
        <execution>
            <id>check</id>
            <goals><goal>check</goal></goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                            <limit>
                                <counter>BRANCH</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.75</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### Excluding Generated Code from Coverage

For MapStruct mappers, Lombok-generated code, and JPA entities:

```java
// Option 1: @Generated annotation on the class
@Generated("mapstruct")
public class UserMapperImpl implements UserMapper { ... }

// Option 2: sonar-project.properties exclusions
// sonar.coverage.exclusions=**/mapper/**/*MapperImpl.java,**/entity/**,**/dto/**

// Option 3: JaCoCo excludes in pom.xml (shown above)
```

### Writing Unit Tests - JUnit 5 + Mockito

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private UserService userService;

    @Test
    @DisplayName("Should return user DTO when user exists")
    void getUserById_whenUserExists_returnsDto() {
        // Arrange
        Long userId = 1L;
        User user = User.builder().id(userId).name("Alice").build();
        UserDto expectedDto = new UserDto(userId, "Alice");

        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        when(userMapper.toDto(user)).thenReturn(expectedDto);

        // Act
        UserDto result = userService.getUserById(userId);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(userId);
        assertThat(result.getName()).isEqualTo("Alice");
        verify(userRepository).findById(userId);
    }

    @Test
    @DisplayName("Should throw ResourceNotFoundException when user not found")
    void getUserById_whenUserNotFound_throwsException() {
        // Arrange
        Long userId = 99L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // Act + Assert
        assertThatThrownBy(() -> userService.getUserById(userId))
            .isInstanceOf(ResourceNotFoundException.class)
            .hasMessageContaining("99");
    }

    @Test
    @DisplayName("Should cover both branches of conditional logic")
    void processUser_coversBothBranches() {
        // Test branch 1: active user
        User activeUser = User.builder().status(UserStatus.ACTIVE).build();
        assertThat(userService.canLogin(activeUser)).isTrue();

        // Test branch 2: inactive user
        User inactiveUser = User.builder().status(UserStatus.INACTIVE).build();
        assertThat(userService.canLogin(inactiveUser)).isFalse();
    }
}
```

### Testing Reactive Code (Mono/Flux)

```java
@ExtendWith(MockitoExtension.class)
class ReactiveUserServiceTest {

    @Mock
    private ReactiveUserRepository userRepository;

    @InjectMocks
    private ReactiveUserService userService;

    @Test
    void getUserById_whenExists_returnsUser() {
        User user = new User(1L, "Alice");
        when(userRepository.findById(1L)).thenReturn(Mono.just(user));

        StepVerifier.create(userService.getUserById(1L))
            .expectNextMatches(dto -> dto.getName().equals("Alice"))
            .verifyComplete();
    }

    @Test
    void getUserById_whenNotFound_emitsError() {
        when(userRepository.findById(99L)).thenReturn(Mono.empty());

        StepVerifier.create(userService.getUserById(99L))
            .expectError(ResourceNotFoundException.class)
            .verify();
    }

    @Test
    void getAllUsers_returnsFluxOfUsers() {
        List<User> users = List.of(new User(1L, "Alice"), new User(2L, "Bob"));
        when(userRepository.findAll()).thenReturn(Flux.fromIterable(users));

        StepVerifier.create(userService.getAllUsers())
            .expectNextCount(2)
            .verifyComplete();
    }

    @Test
    void processUser_onError_emitsFallback() {
        when(userRepository.findById(1L))
            .thenReturn(Mono.error(new DataAccessException("DB down") {}));

        StepVerifier.create(userService.getUserById(1L))
            .expectError(ServiceException.class)
            .verify();
    }
}
```

### Coverage Strategy for Uncovered Lines

1. **Identify uncovered lines**: Use SonarQube UI or JaCoCo HTML report at `target/site/jacoco/index.html`.
2. **Prioritize by risk**: Cover service layer > controller layer > repository layer.
3. **Cover all branches**: For each `if/else`, write at least one test per branch.
4. **Exception paths**: Write tests that trigger each `catch` block and `throw` statement.
5. **Null/empty inputs**: Test with `null`, empty strings, empty lists.
6. **Edge cases**: Test boundary values (0, -1, MAX_VALUE, empty string, etc.).

### Coverage Thresholds by Layer

| Layer | Recommended Coverage |
|---|---|
| Service (business logic) | 90%+ |
| Controller (REST endpoints) | 80%+ |
| Repository (custom queries) | 70%+ |
| Utility/Helper classes | 85%+ |
| Generated code (MapStruct, Lombok) | Exclude |
| Configuration classes | Exclude |

---

## Dimension 5: Duplications (Code Duplication)

### Overview
SonarQube flags duplicated blocks (default: 10+ identical lines in 3+ files, or 100+ tokens). Target: < 3% duplication.

### Identifying Duplicated Code from SonarQube

1. In SonarQube UI → Project → **Duplications** tab.
2. Click on a file to see highlighted duplicated blocks.
3. SonarQube shows the other files where the same block appears.
4. Use the API: `GET /api/measures/component?metricKeys=duplicated_lines_density,duplicated_blocks`

### Refactoring Strategy: Extract Method

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

### Refactoring Strategy: Extract Class

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

### Refactoring Strategy: Template Method Pattern

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

### Consolidating Spring Boot @RequestMapping Patterns

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

### Shared Validation Logic

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

### Near-Duplicates vs Exact Duplicates

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

### Utility vs Inheritance Decision

- Use **utility/helper classes** (static methods) when: logic is stateless, no Spring beans needed, purely functional transformation.
- Use **inheritance/composition** when: shared behavior requires state, Spring lifecycle management, or polymorphism.
- Prefer **composition over inheritance** for Spring services.

---

## Dimension 6: Security Hotspots

### Overview
Security Hotspots are security-sensitive code that requires manual review. Unlike Vulnerabilities, they are not confirmed issues — they need human review to determine if they are safe or need fixing. SonarQube requires each hotspot to be either **Acknowledged as Safe** (with justification) or **Fixed**.

### Hotspot Review Workflow

1. In SonarQube UI → Project → **Security Hotspots** tab.
2. For each hotspot:
   - Read the hotspot description and the flagged code.
   - Determine: Is this actually safe in context, or is it a real risk?
   - If **safe**: Mark as "Safe" with a clear justification comment.
   - If **risky**: Fix the code, then mark as "Fixed".
3. Never mark as "Safe" without understanding why it's safe.

### Common Hotspot Categories and Resolutions

#### SQL Injection Hotspot

```java
// Hotspot: Dynamic query construction
// Review: Is user input ever passed to this query?

// SAFE if: only internal/system values used, never user input
@Query("SELECT u FROM User u WHERE u.status = :#{#status.name()}")
List<User> findByStatus(@Param("status") UserStatus status); // enum, not user string - SAFE

// UNSAFE if: user-controlled string in query
String query = "SELECT * FROM users WHERE role = '" + userInput + "'"; // FIX THIS
```

#### XSS (Cross-Site Scripting) Hotspot

```java
// Hotspot: Output written directly to response
// Review: Is the output HTML-encoded?

// BAD - raw user input in response
response.getWriter().write("<p>" + userInput + "</p>"); // XSS risk

// GOOD - HTML encode output
import org.springframework.web.util.HtmlUtils;
response.getWriter().write("<p>" + HtmlUtils.htmlEscape(userInput) + "</p>");

// BETTER - use Thymeleaf/template engine which auto-escapes
// th:text="${userInput}" -- auto-escaped in Thymeleaf
```

#### CSRF Hotspot

```java
// Hotspot: CSRF protection disabled
// Review: Is this a stateless REST API with JWT?

// SAFE for stateless REST APIs (JWT-based auth)
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable()) // SAFE: stateless JWT API, no session cookies
            // Justification: API uses Bearer token auth, not session cookies.
            // CSRF only applies to cookie-based auth. Mark hotspot as Safe.
            .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
        return http.build();
    }
}

// UNSAFE if: using session-based auth with cookies - must enable CSRF
```

#### Insecure Randomness Hotspot

```java
// Hotspot: Use of java.util.Random
// Review: Is this for security-sensitive purposes?

// BAD - java.util.Random for security tokens
Random random = new Random();
String token = String.valueOf(random.nextLong()); // predictable!

// GOOD - use SecureRandom for security tokens
SecureRandom secureRandom = new SecureRandom();
byte[] tokenBytes = new byte[32];
secureRandom.nextBytes(tokenBytes);
String token = Base64.getUrlEncoder().withoutPadding().encodeToString(tokenBytes);

// SAFE - java.util.Random for non-security use (e.g., load balancing, test data)
Random random = new Random();
int serverIndex = random.nextInt(servers.size()); // not security-sensitive - SAFE
```

#### Weak Cryptography Hotspot

```java
// Hotspot: Weak hashing algorithm (MD5, SHA-1)
// Review: Is this for password hashing or security?

// BAD - MD5 for password hashing
MessageDigest md = MessageDigest.getInstance("MD5");
byte[] hash = md.digest(password.getBytes());

// BAD - SHA-1 for password hashing
MessageDigest sha1 = MessageDigest.getInstance("SHA-1");

// GOOD - use BCrypt for passwords (Spring Security)
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12); // strength 12
}

// GOOD - use SHA-256+ for non-password integrity checks
MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
byte[] hash = sha256.digest(data.getBytes(StandardCharsets.UTF_8));

// SAFE - MD5 for non-security checksums (file dedup, caching keys)
// Mark hotspot as Safe with justification: "MD5 used only for cache key generation,
// not for security or authentication purposes."
```

#### Hardcoded Credentials Hotspot

```java
// Hotspot: String literal that looks like a credential
// Review: Is this an actual secret or a placeholder/test value?

// BAD - real credential
private static final String SECRET = "prod-secret-key-abc123";

// SAFE - placeholder in test/example code
// Mark as Safe: "This is a test placeholder, not a real credential."
private static final String TEST_PASSWORD = "test-password-placeholder";

// GOOD - externalize real secrets
@Value("${jwt.secret}")
private String jwtSecret;
```

#### Path Traversal Hotspot

```java
// Hotspot: File path constructed from user input
// Review: Is the path validated/sanitized?

// BAD - direct user input in file path
File file = new File("/uploads/" + userFilename); // path traversal risk

// GOOD - validate and normalize path
public File safeResolve(String baseDir, String userFilename) {
    // Reject path separators and dangerous characters
    if (userFilename.contains("/") || userFilename.contains("\\") ||
            userFilename.contains("..")) {
        throw new ValidationException("Invalid filename: " + userFilename);
    }
    Path basePath = Paths.get(baseDir).toAbsolutePath().normalize();
    Path resolvedPath = basePath.resolve(userFilename).normalize();
    // Ensure resolved path is still within base directory
    if (!resolvedPath.startsWith(basePath)) {
        throw new SecurityException("Path traversal attempt detected");
    }
    return resolvedPath.toFile();
}
```

#### ReDoS (Regex Denial of Service) Hotspot

This is a critical hotspot category. Vulnerable regex patterns with catastrophic backtracking can cause CPU exhaustion under adversarial input.

**Identifying Vulnerable Patterns:**

Patterns with catastrophic backtracking typically contain:
- Nested quantifiers: `(a+)+`, `(a*)*`
- Alternation with overlap: `(a|a)+`
- `.*` followed by a specific character in the same character class

```java
// VULNERABLE - LoginRequest.java style patterns
// These cause catastrophic backtracking on long strings without the required char:
@Pattern(regexp = ".*[A-Z].*")           // ReDoS vulnerable
@Pattern(regexp = ".*[!@#$%^&*(),.?\":{}|<>].*")  // ReDoS vulnerable
@Pattern(regexp = ".*\\d.*")             // ReDoS vulnerable

// WHY: ".*" can match in exponentially many ways before failing,
// causing O(n^2) or O(2^n) backtracking on strings that don't match.
```

**Safe Alternatives - Option 1: Rewrite without backtracking**

```java
// SAFE - use character class complement to avoid backtracking
// "contains at least one uppercase letter"
@Pattern(regexp = "[^A-Z]*[A-Z][\\s\\S]*",
         message = "Must contain at least one uppercase letter")

// "contains at least one digit"
@Pattern(regexp = "[^\\d]*\\d[\\s\\S]*",
         message = "Must contain at least one digit")

// "contains at least one special character"
@Pattern(regexp = "[^!@#$%^&*(),.?\":{}|<>]*[!@#$%^&*(),.?\":{}|<>][\\s\\S]*",
         message = "Must contain at least one special character")
```

**Safe Alternatives - Option 2: Use possessive quantifiers (Java 8+)**

```java
// SAFE - possessive quantifiers prevent backtracking
// [^A-Z]*+ consumes all non-uppercase chars without backtracking
@Pattern(regexp = "[^A-Z]*+[A-Z].*",
         message = "Must contain at least one uppercase letter")

@Pattern(regexp = "[^\\d]*+\\d.*",
         message = "Must contain at least one digit")
```

**Safe Alternatives - Option 3: Use Passay library (RECOMMENDED for passwords)**

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.passay</groupId>
    <artifactId>passay</artifactId>
    <version>1.6.4</version>
</dependency>
```

```java
// Custom Passay-based password validator
@Documented
@Constraint(validatedBy = PasswordConstraintValidator.class)
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidPassword {
    String message() default "Password does not meet requirements";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

public class PasswordConstraintValidator
        implements ConstraintValidator<ValidPassword, String> {

    @Override
    public boolean isValid(String password, ConstraintValidatorContext context) {
        if (password == null) return false;

        PasswordValidator validator = new PasswordValidator(List.of(
            new LengthRule(8, 128),
            new CharacterRule(EnglishCharacterData.UpperCase, 1),
            new CharacterRule(EnglishCharacterData.LowerCase, 1),
            new CharacterRule(EnglishCharacterData.Digit, 1),
            new CharacterRule(EnglishCharacterData.Special, 1),
            new WhitespaceRule()
        ));

        RuleResult result = validator.validate(new PasswordData(password));
        if (result.isValid()) return true;

        // Customize violation messages
        context.disableDefaultConstraintViolation();
        context.buildConstraintViolationWithTemplate(
            String.join(", ", validator.getMessages(result))
        ).addConstraintViolation();
        return false;
    }
}

// Usage in LoginRequest / RegisterRequest
public class RegisterRequest {
    @NotBlank
    @ValidPassword
    private String password;
}
```

**Testing ReDoS Fixes:**

```java
@Test
void password_validation_completesInReasonableTime() {
    // A string designed to trigger catastrophic backtracking in vulnerable regex
    String adversarialInput = "a".repeat(100); // no uppercase, digit, or special char

    long start = System.currentTimeMillis();
    // This should complete in < 100ms with safe regex
    boolean valid = password.matches("[^A-Z]*+[A-Z].*");
    long elapsed = System.currentTimeMillis() - start;

    assertThat(elapsed).isLessThan(100L);
    assertThat(valid).isFalse();
}
```

#### JWT/Token Handling Hotspots

```java
// Hotspot: JWT secret key length or algorithm
// Review: Is the secret strong enough? Is the algorithm secure?

// BAD - weak secret
@Value("${jwt.secret:secret}")
private String jwtSecret; // default "secret" is too short and weak

// BAD - none algorithm
Jwts.builder().setAlgorithm("none"); // no signature!

// GOOD - strong secret, secure algorithm
@Value("${jwt.secret}")
private String jwtSecret; // no default; must be set in environment

// Validate key length on startup
@PostConstruct
void validateJwtSecret() {
    if (jwtSecret == null || jwtSecret.length() < 32) {
        throw new IllegalStateException(
            "JWT secret must be at least 32 characters. " +
            "Set JWT_SECRET environment variable.");
    }
}

// Use HS256 with proper key
SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
String token = Jwts.builder()
    .setSubject(username)
    .setExpiration(Date.from(Instant.now().plusSeconds(3600)))
    .signWith(key, SignatureAlgorithm.HS256)
    .compact();
```

#### Logging Sensitive Data Hotspot

```java
// Hotspot: Logging user-controlled data or sensitive fields
// Review: Does the logged data contain PII or secrets?

// BAD - logging full request body (may contain passwords)
log.debug("Received request: {}", request.toString());
log.info("User data: {}", objectMapper.writeValueAsString(user));

// BAD - logging exception message that may contain sensitive data
log.error("Auth failed: {}", e.getMessage()); // message may contain password

// GOOD - log only safe identifiers
log.debug("Processing request for user: {}", request.getUsername());
log.info("User updated: id={}, email={}", user.getId(), maskEmail(user.getEmail()));
log.error("Auth failed for user: {}, reason: {}", username, e.getClass().getSimpleName());

// GOOD - mask sensitive fields
private String maskEmail(String email) {
    if (email == null || !email.contains("@")) return "***";
    String[] parts = email.split("@");
    String local = parts[0];
    return local.charAt(0) + "***@" + parts[1];
}

private String maskPhone(String phone) {
    if (phone == null || phone.length() < 4) return "***";
    return "***" + phone.substring(phone.length() - 4);
}
```

#### Spring Security Specific Hotspot Resolutions

```java
// Hotspot: HTTP Security configuration
@Bean
public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    http
        // CSRF: Safe to disable for stateless REST APIs with JWT
        // Justification: Stateless JWT auth, no session cookies used.
        .csrf(AbstractHttpConfigurer::disable)

        // Frame options: Deny by default (prevent clickjacking)
        .headers(headers -> headers
            .frameOptions(HeadersConfigurer.FrameOptionsConfig::deny)
            .contentTypeOptions(Customizer.withDefaults())
            .xssProtection(Customizer.withDefaults())
        )

        // Session: Stateless for REST APIs
        .sessionManagement(sm ->
            sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))

        // Authorization: Explicit rules
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/public/**", "/actuator/health").permitAll()
            .requestMatchers("/actuator/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        )

        .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

    return http.build();
}
```

### Hotspot Justification Templates

When marking a hotspot as **Safe**, always provide a clear justification:

| Hotspot Type | Safe Justification Template |
|---|---|
| CSRF disabled | "API is stateless (JWT Bearer token auth). No session cookies used. CSRF attacks require session cookies to exploit." |
| MD5/SHA-1 | "MD5 used only for [cache key / file dedup], not for security or authentication. No sensitive data involved." |
| Random | "java.util.Random used for [load balancing / test data generation], not for security tokens or cryptographic purposes." |
| HTTP URL | "Internal service-to-service call within trusted network. No user-controlled data in URL." |
| Logging | "Only non-sensitive identifiers (user ID, request ID) are logged. No PII or secrets." |

---

## Validation

After code changes:

- Use `build-project` for compile/build validation.
- Use `test-project` when a changed class already has focused tests or when the Sonar fix touches logic that should be verified.
- Keep validation output quiet and targeted.

## Result

Report:

- Issues fixed, grouped by file and rule.
- Issues suppressed, with rule and reason.
- Issues skipped, with reason.
- Files changed, with a brief behavior-preserving summary.
- Validation command and result, or blocker if validation could not run.
