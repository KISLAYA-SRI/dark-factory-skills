# Dimension 6: Security Hotspots — Review Patterns & Examples

## Overview

Security Hotspots are security-sensitive code that requires **manual review**. Unlike Vulnerabilities, they are not confirmed issues — they need human review to determine if they are safe or need fixing. SonarQube requires each hotspot to be either **Acknowledged as Safe** (with justification) or **Fixed**.

---

## Hotspot Review Workflow

1. In SonarQube UI → Project → **Security Hotspots** tab.
2. For each hotspot:
   - Read the hotspot description and the flagged code.
   - Determine: Is this actually safe in context, or is it a real risk?
   - If **safe**: Mark as “Safe” with a clear justification comment.
   - If **risky**: Fix the code, then mark as “Fixed”.
3. Never mark as “Safe” without understanding why it’s safe.

---

## SQL Injection Hotspot

```java
// Hotspot: Dynamic query construction
// Review: Is user input ever passed to this query?

// SAFE if: only internal/system values used, never user input
@Query("SELECT u FROM User u WHERE u.status = :#{#status.name()}")
List<User> findByStatus(@Param("status") UserStatus status); // enum, not user string - SAFE

// UNSAFE if: user-controlled string in query
String query = "SELECT * FROM users WHERE role = '" + userInput + "'"; // FIX THIS
```

---

## XSS (Cross-Site Scripting) Hotspot

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

---

## CSRF Hotspot

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

---

## Insecure Randomness Hotspot

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

---

## Weak Cryptography Hotspot

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

---

## Hardcoded Credentials Hotspot

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

---

## Path Traversal Hotspot

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

---

## ReDoS (Regex Denial of Service) Hotspot

This is a critical hotspot category. Vulnerable regex patterns with catastrophic backtracking can cause CPU exhaustion under adversarial input.

### Identifying Vulnerable Patterns

Patterns with catastrophic backtracking typically contain:
- Nested quantifiers: `(a+)+`, `(a*)*`
- Alternation with overlap: `(a|a)+`
- `.*` followed by a specific character in the same character class

```java
// VULNERABLE - these cause catastrophic backtracking on long strings without the required char:
@Pattern(regexp = ".*[A-Z].*")           // ReDoS vulnerable
@Pattern(regexp = ".*[!@#$%^&*(),.?\":{}|<>].*")  // ReDoS vulnerable
@Pattern(regexp = ".*\\d.*")             // ReDoS vulnerable

// WHY: ".*" can match in exponentially many ways before failing,
// causing O(n^2) or O(2^n) backtracking on strings that don't match.
```

### Safe Alternatives — Option 1: Rewrite without backtracking

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

### Safe Alternatives — Option 2: Use possessive quantifiers (Java 8+)

```java
// SAFE - possessive quantifiers prevent backtracking
// [^A-Z]*+ consumes all non-uppercase chars without backtracking
@Pattern(regexp = "[^A-Z]*+[A-Z].*",
         message = "Must contain at least one uppercase letter")

@Pattern(regexp = "[^\\d]*+\\d.*",
         message = "Must contain at least one digit")
```

### Safe Alternatives — Option 3: Use Passay library (RECOMMENDED for passwords)

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

### Testing ReDoS Fixes

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

---

## JWT/Token Handling Hotspots

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

---

## Logging Sensitive Data Hotspot

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

---

## Spring Security Specific Hotspot Resolutions

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

---

## Hotspot Justification Templates

When marking a hotspot as **Safe**, always provide a clear justification:

| Hotspot Type | Safe Justification Template |
|---|---|
| CSRF disabled | "API is stateless (JWT Bearer token auth). No session cookies used. CSRF attacks require session cookies to exploit." |
| MD5/SHA-1 | "MD5 used only for [cache key / file dedup], not for security or authentication. No sensitive data involved." |
| Random | "java.util.Random used for [load balancing / test data generation], not for security tokens or cryptographic purposes." |
| HTTP URL | "Internal service-to-service call within trusted network. No user-controlled data in URL." |
| Logging | "Only non-sensitive identifiers (user ID, request ID) are logged. No PII or secrets." |
