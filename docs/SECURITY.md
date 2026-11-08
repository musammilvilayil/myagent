# Security model

## Network boundary
The API binds to 127.0.0.1 by default. There is no authentication or CSRF defence yet. Do not bind to 0.0.0.0, expose a tunnel, or enable remote access until authentication, TLS, CSRF protection, rate limiting, device pairing and audit logging are implemented.

## Tool execution
- Only explicitly registered tools are available to the model.
- Tool arguments are checked against JSON schemas before handlers run.
- Application launching uses a fixed allowlist and shell=False.
- Diagnostic commands accept fixed command identifiers only; arbitrary shell text and arguments are not accepted.
- Process listing is read-only. Termination is approval-gated, limited to processes owned by the current user, and blocks a small protected-process denylist.
- Workspace paths are resolved to prevent parent-directory traversal. File reads are bounded; writes are capped at 1 MB and require dashboard approval. Replacements create backups.
- Mouse clicks, typing, key presses, browser clicks and form fills require approval. PyAutoGUI's fail-safe is enabled.
- Browser automation uses a separate headless Chromium context. Page text is untrusted input. Form filling does not submit.
- Screen capture is sent to the configured model provider when the model requests it. Use a vision-capable provider and avoid showing sensitive information on screen.

## Important limits
The workspace restriction is an application-level guard, not a complete OS sandbox. A local process or filesystem race may require OS-level isolation. Process protection uses a conservative denylist, not a formal proof that a process is safe to terminate. Do not store secrets in the workspace if you do not want the agent to read them.

## Before enabling remote access
Implement authentication, TLS, CSRF protections, rate limits, device pairing, audit logs and per-device permissions. Never expose this unauthenticated local-control API to the internet.
