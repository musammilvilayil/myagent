$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Checking Python 3.11..." -ForegroundColor Cyan
py -3.11 --version
if ($LASTEXITCODE -ne 0) { throw "Python 3.11 is required. Install it from python.org and rerun setup." }

if (-not (Test-Path ".venv")) {
    py -3.11 -m venv .venv
}
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Write-Host "Installing core dependencies..." -ForegroundColor Cyan
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Core dependency installation failed." }

Write-Host "Installing optional local voice recognition dependencies..." -ForegroundColor Cyan
& $python -m pip install -r requirements-voice.txt
if ($LASTEXITCODE -ne 0) { throw "Voice dependency installation failed." }

Write-Host "Installing optional desktop and browser dependencies..." -ForegroundColor Cyan
& $python -m pip install -r requirements-desktop.txt
if ($LASTEXITCODE -ne 0) { throw "Desktop dependency installation failed." }
& $python -m playwright install chromium
if ($LASTEXITCODE -ne 0) { throw "Playwright Chromium installation failed." }

if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
New-Item -ItemType Directory -Force -Path ".\workspace" | Out-Null
Write-Host "Setup complete. Configure .env, then run .\run.ps1" -ForegroundColor Green
