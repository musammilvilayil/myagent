$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "Virtual environment not found. Run .\setup.ps1 first." }
& $python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
