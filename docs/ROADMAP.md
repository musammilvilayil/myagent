# MyAgent roadmap

## Implemented in this branch
- [x] FastAPI local service and dashboard
- [x] OpenAI-compatible bounded tool-calling loop
- [x] JSON-schema argument validation
- [x] System health and process listing
- [x] Approval-gated process termination for current-user processes with protected process denylist
- [x] Fixed diagnostic command allowlist (no arbitrary shell)
- [x] Workspace file list/read/search/write with traversal checks and backups
- [x] Dashboard approval/deny workflow for sensitive actions
- [x] Screen capture and vision-capable model handoff
- [x] Approval-gated mouse click, text typing and restricted key press
- [x] Playwright browser navigation, page reading, exact-text click and labelled form fill
- [x] Playwright shutdown cleanup
- [x] Optional local Whisper speech-to-text endpoint and dashboard microphone capture
- [x] Optional browser speech synthesis for spoken replies
- [x] Windows setup/run scripts and GitHub Actions CI

## Remaining engineering work
- [ ] File restore/undo and recoverable delete
- [ ] OCR fallback when provider has no vision support
- [ ] Persistent chat sessions and searchable conversation memory
- [ ] Browser download/upload handling with user confirmation
- [ ] Browser session UI and tab management
- [ ] App discovery and window focus controls
- [ ] Terminal sessions inside a disposable workspace sandbox
- [ ] Git project-aware coding agent and test/fix workflow
- [ ] Provider adapters for Gemini Live and local Ollama models
- [ ] Persistent sessions, streaming, cancellation and audit history
- [ ] Voice input/output and optional wake word
- [ ] Multi-agent delegation and long-term memory
- [ ] Secure device pairing before phone/remote control

## Release gates
- Localhost-only until authentication, TLS, CSRF protection, rate limiting and device permissions exist
- No unrestricted shell, arbitrary Python execution or model-created executable code
- File operations stay inside configured workspace and reject path traversal
- Sensitive actions require explicit approval
- Tool results distinguish verified, failed and unverified outcomes
- Windows 10/11 smoke tests and security review before release
