# MyAgent — Personal PC Agent

MyAgent is a locally hosted desktop AI agent designed to help you operate your own Windows PC through natural language, voice (planned), browser workflows, files, applications and developer tools.

## Current status
The first foundation provides a FastAPI local API, a lightweight browser dashboard, a permission-aware tool registry, safe starter desktop actions, short-lived approval records and an OpenAI-compatible model endpoint.

**This is not yet unrestricted PC control.** Screen understanding, browser automation, voice, file editing, terminal workflows and multi-agent planning are roadmap items.

## Requirements
- Windows 10/11 (primary target)
- Python 3.11+
- Optional: Ollama or an OpenAI-compatible model endpoint

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
Set MODEL_BASE_URL, MODEL_API_KEY and MODEL_NAME in .env for an OpenAI-compatible provider. Keep the API bound to localhost until authentication and transport security are configured.

## Safety model
- Tools declare risk levels and permissions.
- Sensitive actions require short-lived approval.
- No model-generated shell string is executed.
- An attempted action is not treated as proof of success.

See [Security](docs/SECURITY.md) and [Roadmap](docs/ROADMAP.md).

## License
No project license has been selected yet. Third-party components retain their original licenses.
