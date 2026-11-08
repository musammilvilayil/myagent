# MyAgent roadmap

## Delivered foundation
- [x] FastAPI local service and browser dashboard
- [x] OpenAI-compatible bounded tool-calling loop
- [x] JSON-schema validation for tool arguments
- [x] System health and process listing
- [x] Safe diagnostic command allowlist (no arbitrary shell)
- [x] Workspace file listing, reading and text search
- [x] Workspace file writes with backup and explicit approval handoff
- [x] Approval and denial endpoints surfaced in dashboard
- [x] GitHub Actions CI

## Next implementation phases
- [ ] Restore/undo file versions and file deletion to recoverable trash
- [ ] Screen capture and OCR with explicit user consent
- [ ] Mouse/keyboard automation with per-action preview and kill switch
- [ ] Browser automation (navigate, inspect, click, fill) with untrusted-page isolation
- [ ] Full terminal sessions inside a disposable, workspace-scoped sandbox
- [ ] Application discovery and process termination with approval
- [ ] Provider adapters for Gemini, Ollama and local OpenAI-compatible models
- [ ] Persistent sessions, streaming and cancellation
- [ ] Voice input/output and optional wake word
- [ ] Multi-agent task delegation and long-term memory
- [ ] Secure device pairing before any phone/remote control

## Safety gates
- Localhost-only until authentication, TLS, CSRF protection and device permissions are implemented
- No unrestricted shell, arbitrary Python execution or model-created executable code
- File operations stay within the configured workspace and reject path traversal
- Sensitive actions require explicit user approval
- Every operation reports verified, failed or unverified outcomes honestly
- Windows 10/11 smoke tests required before release
