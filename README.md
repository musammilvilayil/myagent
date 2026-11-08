# MyAgent — Personal PC Agent

A local-first assistant being developed to operate a Windows PC through natural language, approved desktop tools, workspace files and developer workflows.

## Current capabilities
- Local FastAPI service and browser dashboard
- OpenAI-compatible model tool-calling loop
- System overview (CPU, memory, disk, OS and hostname)
- Running-process listing (read-only)
- Fixed diagnostic commands: Python, Node, npm, Git versions, Git status and current user
- Workspace file listing, reading and text search
- Workspace text-file creation/replacement with explicit approval and automatic backup
- Allowlisted app launching and validated HTTP(S) URL opening

## Safety
This is not unrestricted computer control. The model cannot execute arbitrary shell/Python code. File operations are limited to the configured workspace; writes require approval. The API has no authentication yet and must remain bound to localhost. See [Security](docs/SECURITY.md).

## Setup (PowerShell)
```powershell
git clone -b feature/desktop-agent-foundation https://github.com/musammilvilayil/myagent.git
cd myagent
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000.

## Model provider
Set MODEL_BASE_URL, MODEL_API_KEY and MODEL_NAME in .env. The provider must support OpenAI-compatible chat completions and function/tool calling. Do not commit .env.

## Workspace
By default, files are restricted to ./workspace. Set WORKSPACE_ROOT in .env to a dedicated folder you want MyAgent to manage. Do not point it at your entire user profile or a folder containing secrets.

## Roadmap
See [Roadmap](docs/ROADMAP.md) for screen awareness, mouse/keyboard control, browser automation, voice, terminal sandboxing and multi-agent support.

## License
No project license has been selected yet. Third-party components retain their original licenses.
