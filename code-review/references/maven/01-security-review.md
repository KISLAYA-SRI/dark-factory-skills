# Security Review — Java / Maven / Spring Boot

## Role

Review changed Java code as an expert Application Security Engineer. Flag exploitable flaws; do not flag theoretical concerns with no realistic attack path in the changed code.

## OWASP Top 10 Mapping

| Pattern to Look For | OWASP Category | Default Severity |
|---|---|---|
| String-concatenated SQL/JPQL queries | A03:2021 Injection | [BLOCKER] |
| Unsanitized input passed to `ProcessBuilder`/`Runtime.exec` | A03:2021 Injection | [BLOCKER] |
| Reflected/stored value rendered without escaping (e.g., raw HTML in a Thymeleaf/JSP template) | A03:2021 Injection (XSS) | [BLOCKER] |
| `ObjectInputStream.readObject` on untrusted input | A08:2021 Software/Data Integrity | [BLOCKER] |
| Missing `@PreAuthorize`/method-security or missing role/scope check on a new endpoint that other sibling endpoints protect | A01:2021 Broken Access Control | [BLOCKER] |
| New field/log statement exposing PII, tokens, passwords, or full downstream payloads | A02:2021 Cryptographic Failures / sensitive data exposure | [ISSUE] (BLOCKER if it's a credential/token) |
| Hardcoded credential, API key, JWT secret, or connection string in source/`application.yml` | A07:2021 Identification/Auth Failures | [BLOCKER] |
| New dependency added in `pom.xml` with a known CVE or no version pin inherited from a vulnerable BOM | A06:2021 Vulnerable Components | [ISSUE] (BLOCKER if CVSS is Critical/High and exploitable server-side) |
| New outbound call (`WebClient`/`RestTemplate`) built from unchecked user-supplied host/URL | A10:2021 SSRF | [BLOCKER] |
| Weak/broken crypto (`MD5`, `SHA-1` for passwords, ECB mode, `new Random()` for tokens) | A02:2021 Cryptographic Failures | [BLOCKER] |

## Examples

### SQL Injection

```java
// FLAG — [BLOCKER] SQL injection via string concatenation
String query = "SELECT * FROM users WHERE name = '" + name + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);

// ACCEPTABLE — parameterized query / Spring Data JPA
@Query("SELECT u FROM User u WHERE u.name = :name")
List<User> findByName(@Param("name") String name);
```

### Hardcoded Secrets

```java
// FLAG — [BLOCKER] hardcoded credential
private static final String DB_PASSWORD = "mySecret123";
private static final String GITLAB_PAT = "glpat-xxxxxxxxxxxx";

// ACCEPTABLE — externalized
@Value("${db.password}")
private String dbPassword;
```

Also flag hardcoded secrets found in YAML/properties files, CI config (`.gitlab-ci.yml`), or test fixtures committed with real-looking tokens — not just `.java` source.

### Sensitive Data in Logs/Responses

```java
// FLAG — [BLOCKER] token/credential logged
log.info("User login: username={}, password={}", username, password);

// FLAG — [ISSUE] PII/internal payload logged
log.debug("Downstream response: {}", fullCustomerPayload);

// ACCEPTABLE
log.info("User login attempt: username={}", username);
```

```java
// FLAG — [ISSUE] response DTO exposes sensitive field
public class UserResponse {
    private String password;
    private String ssn;
}
```

### Broken Access Control

```java
// Sibling endpoint has @PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/accounts/{id}")
public ResponseEntity<Void> deleteAccount(@PathVariable String id) { ... } // existing, protected

// FLAG — [BLOCKER] new endpoint in the same controller missing equivalent protection
@PostMapping("/accounts/{id}/close")
public ResponseEntity<Void> closeAccount(@PathVariable String id) { ... } // no @PreAuthorize
```

### Reactive / Blocking Security Gaps

```java
// FLAG — [ISSUE] security context not propagated through a new reactive chain,
// leading to an unauthenticated downstream call
return downstreamClient.call(request); // missing .contextWrite(...) / ReactiveSecurityContextHolder usage
```

## Dependency Risk Check

For any new or version-bumped dependency in the diff's `pom.xml`:
1. Note the dependency and version added/changed.
2. If a known-vulnerable version is recognizable without external lookup (e.g., a long-unpatched major version of a commonly-CVE'd library), flag `[ISSUE]` with the concern; otherwise note it as a follow-up for a dependency-scanning tool (`fix-sonar-issues`, OWASP dependency-check) rather than guessing a CVE.

## When Nothing Is Found

If the diff introduces no security-relevant pattern from the table above, state plainly: **"No security issues found."** Do not invent findings to pad the review.
