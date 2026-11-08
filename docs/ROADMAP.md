# MyAgent roadmap

## Phase 1 — Foundation
- [x] FastAPI local service
- [x] Browser dashboard shell
- [x] Typed tool registry and risk levels
- [x] Safe starter desktop tools
- [x] Approval-token primitive
- [ ] Run CI and validate on Windows

## Phase 2 — Real agent loop
- [ ] Provider abstraction (Gemini, OpenAI-compatible APIs, Ollama)
- [ ] Tool-call planning and schema validation
- [ ] Conversation/session persistence
- [ ] Streaming progress and cancellation
- [ ] Retry policy and truthful outcome reporting

## Phase 3 — PC awareness and automation
- [ ] Screen capture with explicit user consent
- [ ] OCR and active-window awareness
- [ ] Mouse/keyboard automation with visible action previews
- [ ] Application discovery and per-app permissions
- [ ] Browser automation using Playwright

## Phase 4 — Files and developer workflows
- [ ] Workspace-scoped file search/read/write
- [ ] Diff preview, backups and undo
- [ ] Terminal tool with command allowlists and approval
- [ ] Git/GitHub workflows
- [ ] Project-aware coding agent with test/fix loops

## Phase 5 — Voice and multi-agent
- [ ] Push-to-talk and speech-to-text
- [ ] Text-to-speech and wake word (opt-in)
- [ ] Specialist agents and task delegation
- [ ] Long-term memory and searchable history
- [ ] Phone companion dashboard with secure pairing

## Release gates
- Automated tests for every tool and permission path
- Windows 10/11 smoke tests
- Security review before any remote-control feature
- No claims of success without verified tool outcomes
