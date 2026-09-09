# Dimension 2: Security (Vulnerabilities) — Node/React Fix Patterns & Examples

## Overview

Security vulnerabilities are code flaws that attackers can exploit. Map each finding to OWASP Top 10 categories. Fix **ALL** security vulnerabilities regardless of severity, across Node.js backends and React frontends.

---

## OWASP Top 10 Mapping

| SonarQube Rule | OWASP Category |
|---|---|
| XSS (innerHTML / dangerouslySetInnerHTML) | A03:2021 Injection |
| SQL/NoSQL Injection | A03:2021 Injection |
| Insecure Deserialization (`JSON.parse` of untrusted eval-like input) | A08:2021 Software/Data Integrity |
| Broken Access Control (missing route/API guard) | A01:2021 Broken Access Control |
| Sensitive Data Exposure (tokens in storage/logs) | A02:2021 Cryptographic Failures |
| Hardcoded Credentials/API Keys | A07:2021 Identification/Auth Failures |
| Vulnerable npm Dependencies | A06:2021 Vulnerable Components |
| SSRF via unchecked outbound requests | A10:2021 Server-Side Request Forgery |

---

## Cross-Site Scripting (XSS) in React

```tsx
// BAD - raw HTML injection from untrusted data
function Comment({ text }: { text: string }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />;
}

// GOOD - render as text; React escapes by default
function Comment({ text }: { text: string }) {
  return <div>{text}</div>;
}

// If rich text rendering is genuinely required, sanitize first
import DOMPurify from 'dompurify';

function RichComment({ html }: { html: string }) {
  const safeHtml = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: safeHtml }} />;
}
```

```ts
// BAD - direct DOM injection in vanilla/Node-rendered templates
element.innerHTML = userInput;

// GOOD - use textContent or an escaping/templating library
element.textContent = userInput;
```

---

## SQL / NoSQL Injection Prevention

```ts
// BAD - string concatenation building a SQL query
const query = `SELECT * FROM users WHERE email = '${email}'`;
await db.query(query);

// GOOD - parameterized query
await db.query('SELECT * FROM users WHERE email = $1', [email]);

// BAD - NoSQL operator injection (MongoDB)
const user = await User.findOne({ email: req.body.email }); // if email is an object like {$ne: null}

// GOOD - validate/sanitize input shape before querying
import { z } from 'zod';
const emailSchema = z.string().email();
const email = emailSchema.parse(req.body.email);
const user = await User.findOne({ email });
```

---

## Input Validation and Sanitization

```ts
// BAD - no validation on request body
app.post('/users', async (req, res) => {
  const user = await userService.create(req.body);
  res.json(user);
});

// GOOD - schema validation at the boundary (zod, yup, joi, class-validator)
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
});

app.post('/users', async (req, res, next) => {
  try {
    const payload = createUserSchema.parse(req.body);
    const user = await userService.create(payload);
    res.json(user);
  } catch (error) {
    next(error);
  }
});
```

---

## npm Dependency Vulnerability Remediation

Steps to remediate:

1. Run `npm audit` (or `yarn audit` / `pnpm audit`) to list known CVEs.
2. Prefer `npm audit fix` for patch/minor-level fixes that do not break the API.
3. For vulnerabilities requiring a major version bump, review the changelog before upgrading and re-run tests.
4. For transitive dependencies, pin a safe version using `overrides` (npm) or `resolutions` (yarn):

```jsonc
// package.json (npm)
{
  "overrides": {
    "vulnerable-package": "^2.1.0"
  }
}
```

```jsonc
// package.json (yarn classic)
{
  "resolutions": {
    "vulnerable-package": "^2.1.0"
  }
}
```

5. Re-run `npm audit` / the SonarQube dependency scan after upgrading to confirm the CVE is resolved.

---

## Sensitive Data Exposure

```ts
// BAD - logging sensitive data
console.log('Login attempt', { username, password });
logger.debug('Auth token', token);

// GOOD - log only safe identifiers
logger.info('Login attempt', { username });
logger.debug('Token issued for user', { userId });

// BAD - storing tokens in localStorage (accessible to any injected script)
localStorage.setItem('authToken', token);

// GOOD - prefer httpOnly, secure, sameSite cookies set by the server
// Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict
```

```ts
// BAD - returning sensitive fields from an API response
res.json({ id: user.id, email: user.email, passwordHash: user.passwordHash });

// GOOD - use a response DTO/serializer that excludes sensitive fields
res.json({ id: user.id, email: user.email });
```

---

## Hardcoded Credentials and API Keys

```ts
// BAD
const API_KEY = 'sk-abc123xyz';
const DB_PASSWORD = 'mySecret123';

// GOOD - externalize via environment variables
const apiKey = process.env.EXTERNAL_API_KEY;
const dbPassword = process.env.DB_PASSWORD;
```

```env
# .env.example - commit only placeholders, never real secrets
EXTERNAL_API_KEY=
DB_PASSWORD=
```

Ensure `.env` (with real values) is excluded via `.gitignore` and never committed.

---

## Server-Side Request Forgery (SSRF)

```ts
// BAD - fetching a URL directly supplied by the client
app.post('/proxy', async (req, res) => {
  const response = await fetch(req.body.url); // can target internal services
  res.send(await response.text());
});

// GOOD - allowlist permitted hosts/schemes before fetching
const ALLOWED_HOSTS = new Set(['api.partner.com']);

app.post('/proxy', async (req, res, next) => {
  try {
    const target = new URL(req.body.url);
    if (target.protocol !== 'https:' || !ALLOWED_HOSTS.has(target.hostname)) {
      throw new ValidationError('URL not allowed');
    }
    const response = await fetch(target.toString());
    res.send(await response.text());
  } catch (error) {
    next(error);
  }
});
```
