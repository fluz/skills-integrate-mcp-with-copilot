# Add bulk mailer & mailing lists (CSV import + SMTP)

**Labels:** enhancement, feature, backend
**Priority:** Medium

## Summary
Add functionality for admins to upload CSV mailing lists and send HTML bulk emails via configurable SMTP.

## Acceptance criteria
- Add upload endpoint for CSV to create/maintain mailing lists (persisted in DB).
- Add email template rendering and preview functionality (Jinja templates).
- Add SMTP configuration via environment variables and a safe sending flow (with rate limiting or preview mode).
- Add unit tests for CSV import and email sending (mocking SMTP).
- Add documentation describing usage and configuration.

## Notes
Ensure email sending is testable offline and avoid leaking SMTP credentials; use environment config.