# Dimension 2: Security (Vulnerabilities) — Fix Patterns & Examples

## Overview

Security vulnerabilities are code flaws that attackers can exploit. Map each finding to OWASP Top 10 categories. Fix **ALL** security vulnerabilities regardless of severity.

---

## OWASP Top 10 Mapping

| SonarQube Rule | OWASP Category |
|---|---|
| SQL Injection | A03:2021 Injection |
| XSS | A03:2021 Injection |
| Insecure Deserialization | A08:2021 Software/Data Integrity |
| Broken Access Control | A01:2021 Broken Access Control |
| Sensitive Data Exposure | A02:2021 Cryptographic Failures |
| Hardcoded Credentials | A07:2021 Identification/Auth Failures |
| Vulnerable Dependencies | A06:2021 Vulnerable Components |

---

## SQL Injection Prevention

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

---

## Input Validation and Sanitization

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

---

## Dependency Vulnerability Remediation

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

---

## Sensitive Data Exposure

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

---

## Hardcoded Credentials

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
