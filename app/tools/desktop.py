from __future__ import annotations
import os
import platform
import subprocess
import webbrowser
from typing import Any
from urllib.parse import urlparse
import psutil
from app.security import RiskLevel
from app.tools.registry import ToolRegistry, ToolSpec


def system_info() -> dict[str, Any]:
    return {"ok": True, "platform": platform.platform(), "python": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(interval=0.2),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage(os.path.abspath(os.sep)).percent}


def open_url(url: str) -> dict[str, Any]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {"ok": False, "error": "Only valid http/https URLs are allowed."}
    opened = webbrowser.open(url, new=2)
    return {"ok": bool(opened), "message": "Browser open requested." if opened else "Browser could not confirm opening."}


def open_application(app: str) -> dict[str, Any]:
    """Launch a small allowlist of common apps without invoking a shell."""
    commands = {"notepad": ["notepad.exe"], "calculator": ["calc.exe"], "explorer": ["explorer.exe"],
                "vscode": ["code"], "terminal": ["wt.exe"]}
    command = commands.get(app.lower().strip())
    if not command:
        return {"ok": False, "error": "Application is not in the approved launch list."}
    try:
        subprocess.Popen(command, shell=False, close_fds=True)
        return {"ok": True, "message": f"Launch requested for {app}."}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "error": str(exc)}


def register_desktop_tools(registry: ToolRegistry) -> None:
    registry.register(ToolSpec("system_info", "Read basic PC health and platform information.", RiskLevel.READ, system_info))
    registry.register(ToolSpec("open_url", "Open a validated HTTP or HTTPS URL in the default browser.", RiskLevel.LOW, open_url))
    registry.register(ToolSpec("open_application", "Launch an application from the built-in allowlist.", RiskLevel.LOW, open_application))
