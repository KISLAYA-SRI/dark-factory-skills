# Security Review — Node.js / React / TypeScript

## Role

Review changed JS/TS code as an expert Application Security Engineer. Flag exploitable flaws in the diff; do not flag theoretical concerns with no realistic attack path in the changed code.

## OWASP Top 10 Mapping

| Pattern to Look For | OWASP Category | Default Severity |
|---|---|---|
| `dangerouslySetInnerHTML` / `innerHTML` with unsanitized data | A03:2021 Injection (XSS) | [BLOCKER] |
| String-concatenated SQL or unchecked NoSQL operator input (`{$ne: ...}` style) | A03:2021 Injection | [BLOCKER] |
| `eval()`, `new Function(...)`, or dynamic `require()` on user-influenced input | A03:2021 Injection | [BLOCKER] |
| Missing auth/role guard on a new API route/handler that sibling routes protect | A01:2021 Broken Access Control | [BLOCKER] |
| Token/PII logged or stored in `localStorage`/`sessionStorage` | A02:2021 Cryptographic Failures / sensitive data exposure | [ISSUE] (BLOCKER if it's a raw credential/token) |
| Hardcoded API key, secret, or connection string in source, `.env` committed with real values, or test fixtures | A07:2021 Identification/Auth Failures | [BLOCKER] |
| New npm dependency with a known CVE or an unpinned wide version range for a security-sensitive package | A06:2021 Vulnerable Components | [ISSUE] (BLOCKER if CVSS is Critical/High and exploitable server-side) |
| Outbound `fetch`/`axios` call built from an unchecked user-supplied URL/host | A10:2021 SSRF | [BLOCKER] |
| `Math.random()` used to generate a token, session ID, or password-reset code | A02:2021 Cryptographic Failures | [BLOCKER] |

## Examples

### Cross-Site Scripting (XSS)

```tsx
// FLAG — [BLOCKER] raw HTML injection from untrusted data
function Comment({ text }: { text: string }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />;
}

// ACCEPTABLE — React escapes text content by default
function Comment({ text }: { text: string }) {
  return <div>{text}</div>;
}

// ACCEPTABLE — sanitized if rich text is genuinely required
import DOMPurify from 'dompurify';
function RichComment({ html }: { html: string }) {
  const safeHtml = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: safeHtml }} />;
}
```

### SQL / NoSQL Injection

```ts
// FLAG — [BLOCKER] string-concatenated query
const query = `SELECT * FROM users WHERE email = '${email}'`;
await db.query(query);

// ACCEPTABLE — parameterized
await db.query('SELECT * FROM users WHERE email = $1', [email]);

// FLAG — [BLOCKER] unchecked NoSQL operator injection
const user = await User.findOne({ email: req.body.email }); // email could be {$ne: null}

// ACCEPTABLE — validate shape first
const email = z.string().email().parse(req.body.email);
const user = await User.findOne({ email });
```

### Hardcoded Secrets

```ts
// FLAG — [BLOCKER]
const API_KEY = 'sk-abc123xyz';
const GITLAB_PAT = 'glpat-xxxxxxxxxxxx';

// ACCEPTABLE
const apiKey = process.env.EXTERNAL_API_KEY;
```

Also check `.env` files, CI config (`.gitlab-ci.yml`, GitHub Actions workflows), and test fixtures for committed real-looking secrets.

### Sensitive Data Exposure

```ts
// FLAG — [BLOCKER] token/credential logged
console.log('Login attempt', { username, password });
logger.debug('Auth token', token);

// FLAG — [ISSUE] token stored insecurely
localStorage.setItem('authToken', token);

// ACCEPTABLE
logger.info('Login attempt', { username });
// Prefer httpOnly, secure, sameSite cookies set by the server
```

### Missing Input Validation at a Route Boundary

```ts
// FLAG — [ISSUE] no schema validation on request body
app.post('/users', async (req, res) => {
  const user = await userService.create(req.body);
  res.json(user);
});

// ACCEPTABLE
const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
});
app.post('/users', async (req, res, next) => {
  try {
    const payload = createUserSchema.parse(req.body);
    res.json(await userService.create(payload));
  } catch (error) {
    next(error);
  }
});
```

### SSRF

```ts
// FLAG — [BLOCKER] fetching a client-supplied URL with no allowlist
app.post('/proxy', async (req, res) => {
  const response = await fetch(req.body.url);
  res.send(await response.text());
});

// ACCEPTABLE — allowlist host/scheme before fetching
```

## Dependency Risk Check

For any new or version-bumped dependency in the diff's `package.json`/lockfile:
1. Note the dependency and version added/changed.
2. If a known-vulnerable version is recognizable without external lookup, flag `[ISSUE]`; otherwise note it as a follow-up for `npm audit` / a dependency-scanning tool (`fix-sonar-issues`) rather than guessing a CVE.

## When Nothing Is Found

If the diff introduces no security-relevant pattern from the table above, state plainly: **"No security issues found."** Do not invent findings to pad the review.
