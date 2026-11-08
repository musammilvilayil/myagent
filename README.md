# MyAgent — Personal PC Agent

MyAgent is a locally hosted desktop AI agent designed to help you operate your own Windows PC through natural language, browser workflows, files, applications and developer tools. Voice, screen understanding and advanced automation are planned.

## Current status
The initial foundation provides:
- FastAPI local service and a browser dashboard
- Permission-aware typed tool registry and risk levels
- Bounded OpenAI-compatible tool-calling loop
- Starter PC tools: system health, allowlisted app launching and validated URL opening
- Short-lived, one-use approval primitive for future sensitive actions
- Security documentation, roadmap, tests and CI workflow

**This is not yet unrestricted PC control.** The current toolset is intentionally small. Screen understanding, browser automation, voice, file editing, terminal workflows, persistent sessions and multi-agent planning are still roadmap items.

## Requirements
- Windows 10/11 (primary target)
- Python 3.11+
- Optional: Ollama or an OpenAI-compatible model endpoint that supports tool calling

## Setup (PowerShell)
```powershell
git clone https://github.com/musammilvilayil/myagent.git
cd myagent
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000.

## Configuration
Set MODEL_BASE_URL, MODEL_API_KEY and MODEL_NAME in .env for an OpenAI-compatible provider. The configured model must support function/tool calling for natural-language PC actions. Keep the API bound to localhost until authentication and transport security are configured.

## Safety model
- Only explicitly registered tools can be called by the model.
- Tool arguments are validated against registered JSON schemas by the provider and checked again by Python handlers.
- Desktop launching uses an allowlist and shell=False.
- No arbitrary model-generated shell or Python is executed.
- Sensitive actions are designed to require short-lived approval.
- An attempted action is not treated as proof of success.

See [Security](docs/SECURITY.md) and [Roadmap](docs/ROADMAP.md).

## License
No project license has been selected yet. Third-party components retain their original licenses.
