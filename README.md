# MyAgent — Personal PC Agent

A local-first AI assistant being developed to operate your Windows PC through natural language, approved desktop controls, browser workflows, workspace files and developer tools.

## Current capabilities in this branch
- Local FastAPI service and responsive browser dashboard
- OpenAI-compatible model tool-calling loop with bounded turns
- System overview: CPU, memory, disk, OS and hostname
- Running-process inspection and approval-gated termination of current-user processes
- Fixed diagnostic commands: Python, Node, npm, Git versions, Git status and current user
- Workspace file listing, reading and text search
- Workspace file creation/replacement with explicit approval and automatic backups
- Screen capture with vision handoff to a vision-capable model provider
- Approval-gated mouse clicks, typing and a restricted navigation-key set
- Isolated Playwright Chromium session: navigate, read page text, click exact text and fill labelled fields (click/fill require approval)
- Allowlisted app launching and validated HTTP(S) URL opening

## Windows setup
Install Python 3.11 first. Then open PowerShell in the repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

Open http://127.0.0.1:8000.

Manual setup is also possible:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-desktop.txt
python -m playwright install chromium
Copy-Item .env.example .env
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Model provider
Set MODEL_BASE_URL, MODEL_API_KEY and MODEL_NAME in .env. The provider must support OpenAI-compatible chat completions and function/tool calling. Screen understanding also requires image/vision input support. Do not commit .env.

## Workspace boundary
By default, file tools operate only in ./workspace. Set WORKSPACE_ROOT in .env to a dedicated project folder you want MyAgent to manage. Do not point it at your entire user profile or a folder containing secrets.

## Safety and limitations
- Sensitive actions display a preview and require your explicit dashboard approval.
- No arbitrary model-generated shell or Python is executed.
- Mouse/keyboard actions affect the currently focused desktop app; keep the dashboard visible and review each approval.
- Browser content is untrusted. Form filling does not submit forms.
- The API has no authentication yet. Keep it on localhost; remote/phone control is not safe to enable yet.
- This is not a fully autonomous unrestricted PC controller. Read [Security](docs/SECURITY.md) and [Roadmap](docs/ROADMAP.md).

## License
No project license has been selected yet. Third-party components retain their original licenses.
