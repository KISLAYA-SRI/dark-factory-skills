# Frontend Foundation Edge Cases
- Brownfield repos may have custom configs; preserve them unless explicitly replacing.
- Monorepo work must not break unrelated packages.
- Next.js environment variables with NEXT_PUBLIC_ are client-visible and must not contain secrets.