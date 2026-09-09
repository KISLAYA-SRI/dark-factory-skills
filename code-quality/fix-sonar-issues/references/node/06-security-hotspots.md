# Dimension 6: Security Hotspots — Node/React Review Patterns & Examples

## Overview

Security Hotspots are security-sensitive code that requires **manual review**. Unlike Vulnerabilities, they are not confirmed issues — they need human review to determine if they are safe or need fixing. SonarQube requires each hotspot to be either **Acknowledged as Safe** (with justification) or **Fixed**.

---

## Hotspot Review Workflow

1. In SonarQube UI → Project → **Security Hotspots** tab.
2. For each hotspot:
   - Read the hotspot description and the flagged code.
   - Determine: is this actually safe in context, or is it a real risk?
   - If **safe**: mark as "Safe" with a clear justification comment.
   - If **risky**: fix the code, then mark as "Fixed".
3. Never mark as "Safe" without understanding why it's safe.

---

## `eval()` / `new Function()` Hotspot

```ts
// Hotspot: dynamic code execution
// Review: does this ever execute user-controlled or external input?

// UNSAFE - executing a string built from user input
eval(`process(${userInput})`); // FIX THIS

// SAFE-ish alternative when dynamic behavior is genuinely needed
const allowedOperations: Record<string, (a: number, b: number) => number> = {
  add: (a, b) => a + b,
  subtract: (a, b) => a - b,
};
const result = allowedOperations[operationName]?.(a, b);
```

---

## XSS via `dangerouslySetInnerHTML` / `innerHTML`

```tsx
// Hotspot: raw HTML rendering
// Review: is the HTML source trusted, and is it sanitized?

// UNSAFE - unsanitized user content rendered as HTML
<div dangerouslySetInnerHTML={{ __html: userComment }} />

// SAFE - sanitized with DOMPurify before rendering
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userComment) }} />

// SAFE - content is fully static/author-controlled (e.g., CMS-rendered trusted markup)
// Justification: HTML sourced from an internal CMS with editor access control, not user input.
```

---

## Insecure Randomness Hotspot

```ts
// Hotspot: Math.random() used for a token/id
// Review: is this for security-sensitive purposes?

// UNSAFE - Math.random for session tokens or password reset codes
const token = Math.random().toString(36).slice(2); // predictable

// SAFE - use crypto for security tokens
import { randomBytes } from 'node:crypto';
const token = randomBytes(32).toString('hex');

// Browser equivalent
const array = new Uint8Array(32);
crypto.getRandomValues(array);

// SAFE - Math.random for non-security use (e.g., UI shuffling, sample IDs in tests)
const shuffledIndex = Math.floor(Math.random() * items.length); // not security-sensitive - SAFE
```

---

## Weak Cryptography Hotspot

```ts
// Hotspot: weak hashing algorithm (MD5, SHA-1) or weak cipher
// Review: is this for password hashing or other security purposes?

// UNSAFE - MD5/SHA-1 for password hashing
import { createHash } from 'node:crypto';
const hash = createHash('md5').update(password).digest('hex');

// SAFE - use bcrypt/argon2 for passwords
import bcrypt from 'bcrypt';
const passwordHash = await bcrypt.hash(password, 12);

// SAFE - SHA-256+ for non-password integrity checks
const checksum = createHash('sha256').update(fileBuffer).digest('hex');

// SAFE justification example: "MD5 used only for cache key generation on
// non-sensitive data, not for authentication or integrity verification."
```

---

## Hardcoded Credentials / API Keys Hotspot

```ts
// Hotspot: string literal that looks like a credential
// Review: is this a real secret or a placeholder/test value?

// UNSAFE - real credential
const SECRET = 'prod-secret-key-abc123';

// SAFE - clearly a test/example placeholder
// Mark as Safe: "This is a test fixture value, not a real credential."
const TEST_PASSWORD = 'test-password-placeholder';

// GOOD - externalize real secrets
const jwtSecret = process.env.JWT_SECRET;
if (!jwtSecret) {
  throw new Error('JWT_SECRET environment variable must be set');
}
```

---

## Path Traversal Hotspot

```ts
// Hotspot: file path constructed from user input
// Review: is the path validated/normalized against a base directory?

// UNSAFE - direct user input in a file path
app.get('/files/:name', (req, res) => {
  res.sendFile(path.join('/uploads', req.params.name)); // path traversal risk
});

// SAFE - validate and normalize against the base directory
import path from 'node:path';

app.get('/files/:name', (req, res) => {
  const baseDir = path.resolve('/uploads');
  const resolvedPath = path.resolve(baseDir, req.params.name);
  if (!resolvedPath.startsWith(baseDir + path.sep)) {
    return res.status(400).json({ error: 'Invalid filename' });
  }
  res.sendFile(resolvedPath);
});
```

---

## ReDoS (Regex Denial of Service) Hotspot

Vulnerable regex patterns with catastrophic backtracking can cause CPU exhaustion (event-loop blocking) under adversarial input — especially damaging in single-threaded Node.js servers.

### Identifying Vulnerable Patterns

- Nested quantifiers: `(a+)+`, `(a*)*`
- Alternation with overlap: `(a|a)+`
- `.*` combined with backtracking-heavy lookaheads on untrusted input

```ts
// VULNERABLE - catastrophic backtracking on crafted long input
const emailRegex = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
```

### Safe Alternatives

```ts
// SAFE - simpler, linear-time pattern (sufficient for basic format checks; pair with a real validator for strict RFC compliance)
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// BETTER - use a maintained validation library instead of a hand-rolled regex
import validator from 'validator';
const isValidEmail = validator.isEmail(email);
```

```ts
// SAFE - bound input length before applying any regex to reduce backtracking blast radius
function safeMatch(pattern: RegExp, input: string, maxLength = 256): boolean {
  if (input.length > maxLength) return false;
  return pattern.test(input);
}
```

### Testing ReDoS Fixes

```ts
it('completes validation quickly for adversarial input', () => {
  const adversarialInput = 'a'.repeat(50) + '!';
  const start = Date.now();
  const result = emailRegex.test(adversarialInput);
  const elapsed = Date.now() - start;

  expect(elapsed).toBeLessThan(100);
  expect(result).toBe(false);
});
```

---

## JWT / Token Handling Hotspots

```ts
// Hotspot: JWT secret strength, algorithm choice, or storage location
// Review: is the secret strong enough? Is "none" algorithm blocked? Where is the token stored client-side?

// UNSAFE - weak/default secret
const jwtSecret = process.env.JWT_SECRET || 'secret';

// UNSAFE - accepting the "none" algorithm
jwt.verify(token, secret, { algorithms: ['none'] });

// SAFE - strong required secret, explicit algorithm allowlist
const jwtSecret = process.env.JWT_SECRET;
if (!jwtSecret || jwtSecret.length < 32) {
  throw new Error('JWT_SECRET must be set and at least 32 characters');
}
const payload = jwt.verify(token, jwtSecret, { algorithms: ['HS256'] });

// Hotspot: storing JWT in localStorage/sessionStorage (readable by any injected script)
// SAFE alternative: store in an httpOnly, Secure, SameSite cookie set by the server
```

---

## CORS Misconfiguration Hotspot

```ts
// Hotspot: overly permissive CORS configuration
// Review: does this endpoint need to be reachable from any origin?

// UNSAFE - reflects any origin and allows credentials
app.use(cors({ origin: true, credentials: true }));

// SAFE - explicit allowlist of trusted origins
const allowedOrigins = ['https://app.example.com'];
app.use(
  cors({
    origin: (origin, callback) => {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error('Not allowed by CORS'));
      }
    },
    credentials: true,
  }),
);
```

---

## Logging Sensitive Data Hotspot

```ts
// Hotspot: logging user-controlled data or sensitive fields
// Review: does the logged data contain PII or secrets?

// UNSAFE - logging full request body (may contain passwords/tokens)
logger.debug('Incoming request', req.body);

// SAFE - log only safe identifiers, mask sensitive fields
logger.debug('Incoming request', { userId: req.user?.id, path: req.path });

function maskEmail(email: string): string {
  const [local, domain] = email.split('@');
  if (!domain) return '***';
  return `${local[0]}***@${domain}`;
}
```

---

## Hotspot Justification Templates

When marking a hotspot as **Safe**, always provide a clear justification:

| Hotspot Type | Safe Justification Template |
|---|---|
| `dangerouslySetInnerHTML` | "Content is sanitized with DOMPurify before rendering" or "Content is author-controlled from a trusted CMS, not user input." |
| MD5/SHA-1 | "MD5 used only for [cache key / file dedup], not for security or authentication. No sensitive data involved." |
| `Math.random()` | "Math.random used for [UI shuffling / non-security sample data], not for security tokens or cryptographic purposes." |
| CORS `origin: true` | "Endpoint is public and read-only, no credentials/cookies involved." (otherwise this must be fixed) |
| Logging | "Only non-sensitive identifiers (user ID, request ID) are logged. No PII or secrets." |
| JWT in storage | "Token is short-lived and scoped to a non-sensitive read-only API; refresh flow uses httpOnly cookie." |
