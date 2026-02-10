# Add persistent database for activities & registrations

**Labels:** enhancement, feature, backend
**Priority:** Medium

## Summary
Replace the current in-memory `activities` store with a persistent database and add models + migrations.

## Acceptance criteria
- Add DB configuration with a sensible default (SQLite for local dev) and support for env var-based production DB.
- Add SQLAlchemy models for `Activity` and `Registration` (with foreign keys and timestamps).
- Add Alembic migrations (or equivalent) and update README with setup instructions.
- Replace endpoints to use the DB for listing activities, signups and unregistrations.
- Add unit tests covering CRUD and signup/unregister flows.

## Notes
This enables persistence and opens the path to other features (forms, CSV export, admin UI).