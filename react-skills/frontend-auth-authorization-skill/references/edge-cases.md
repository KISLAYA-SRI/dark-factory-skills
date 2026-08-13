# Frontend Auth Edge Cases
- Client-only role checks can leak protected data already rendered by the server.
- Middleware redirects can loop if public/authenticated route groups are not separated.
- Refresh flows must handle expiry, replay, and concurrent requests safely.