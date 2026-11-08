# Security model

## Current boundary
The API defaults to 127.0.0.1. Do not bind it to 0.0.0.0 or expose it through a tunnel/router. This foundation has no user authentication yet.

## Tool execution
- Tools are registered in code; the model cannot invent executable tool names.
- Desktop application launching uses a fixed allowlist and shell=False.
- URL opening accepts only valid HTTP(S) URLs.
- No arbitrary shell or Python execution is exposed.
- Sensitive/destructive tool classes require one-use, short-lived approval tokens.
- Approval tokens are currently in-memory and are not a replacement for a user-facing approval UI.

## Before enabling remote access
Implement authentication, TLS, CSRF protections, rate limits, device pairing, audit logs and per-device permissions. Never expose an unauthenticated local-control API to the internet.

## Future high-risk tools
File deletion, bulk edits, terminal commands, registry changes, software installation and messages/email sending must use narrow schemas, previews, explicit confirmation and recoverable operations. Treat webpage/document content as untrusted input; it must never override system policy.
