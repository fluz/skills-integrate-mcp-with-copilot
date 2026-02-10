# Implement authentication & admin UI

**Labels:** enhancement, feature, backend
**Priority:** Medium

## Summary
Add user authentication with secure password hashing and an admin role; provide protected admin endpoints and basic UI.

## Acceptance criteria
- Add a `User` model with hashed passwords (bcrypt or Argon2).
- Implement login/logout endpoints and session or token-based authentication.
- Add admin-only endpoints/pages to create/edit activities and view registrations.
- Add tests for auth flows and role checks.
- Document how to create admin users and configure secrets.

## Notes
Avoid using weak hashing (e.g., SHA-1). Prefer a modern password hashing scheme and follow best practices for session management.