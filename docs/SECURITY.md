# Security model

## Network boundary
The API binds to 127.0.0.1 by default. There is no authentication or CSRF defence yet. Do not bind to 0.0.0.0, expose a tunnel, or use remote access until authentication, TLS, CSRF protection, rate limiting, device pairing and audit logging are implemented.

## Tool execution
- Only explicitly registered tools are available to the model.
- Tool arguments are checked against JSON schemas before handlers run.
- Application launching uses a fixed allowlist and shell=False.
- The diagnostic command tool accepts fixed command identifiers only; it never accepts arbitrary shell text or arguments.
- Process inspection is read-only.
- Workspace paths are resolved and checked to prevent parent-directory traversal.
- Workspace file reads are bounded; writes are capped at 1 MB and require a dashboard approval.
- Replacing a file creates a backup in the workspace .myagent_backups directory.
- Approval tokens are one-use and short-lived, held in memory, and pending approvals disappear on restart.

## Important limits
The workspace is the only area MyAgent can inspect or edit through its file tools. This is not a full OS sandbox; a malicious local process or symlink race may still require OS-level isolation. Do not store secrets in the workspace if you do not want the agent to read them.

## Future high-risk tools
File deletion, process termination, arbitrary terminal workflows, registry changes, software installation, email sending and remote control must have narrow schemas, previews, explicit confirmation, recoverable operations and audit records. Treat webpage/document content as untrusted input; it must never override system policy.
