from __future__ import annotations
import os
import platform
import subprocess
from typing import Any
import psutil
from app.security import RiskLevel
from app.tools.registry import ToolRegistry, ToolSpec
from app.tools.workspace import workspace_root


def system_overview() -> dict[str, Any]:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(os.path.abspath(os.sep))
    return {"ok": True, "platform": platform.platform(), "hostname": platform.node(),
            "python": platform.python_version(), "cpu_percent": psutil.cpu_percent(interval=0.25),
            "memory": {"total_gb": round(memory.total / 1024**3, 2), "used_percent": memory.percent},
            "disk": {"total_gb": round(disk.total / 1024**3, 2), "used_percent": disk.percent}}


def list_processes(limit: int = 40) -> dict[str, Any]:
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info", "status"]):
        try:
            info = proc.info
            processes.append({"pid": info["pid"], "name": info.get("name") or "unknown",
                              "cpu_percent": info.get("cpu_percent") or 0,
                              "memory_mb": round(info["memory_info"].rss / 1024**2, 1) if info.get("memory_info") else 0,
                              "status": info.get("status")})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    processes.sort(key=lambda p: p["memory_mb"], reverse=True)
    return {"ok": True, "processes": processes[:max(1, min(limit, 100))]}


def safe_command(command: str) -> dict[str, Any]:
    commands = {"python_version": ["python", "--version"], "node_version": ["node", "--version"],
                "npm_version": ["npm", "--version"], "git_version": ["git", "--version"],
                "git_status": ["git", "status", "--short", "--branch"], "whoami": ["whoami"]}
    argv = commands.get(command)
    if not argv:
        return {"ok": False, "error": "Command is not in the safe command allowlist."}
    try:
        result = subprocess.run(argv, cwd=str(workspace_root()), shell=False, capture_output=True,
                                text=True, timeout=15)
        return {"ok": result.returncode == 0, "command": command, "exit_code": result.returncode,
                "stdout": result.stdout[-12000:], "stderr": result.stderr[-4000:]}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "command": command, "error": str(exc)}


def register_system_tools(registry: ToolRegistry) -> None:
    registry.register(ToolSpec("system_overview", "Read CPU, memory, disk, hostname and OS information.", RiskLevel.READ, system_overview,
        {"type": "object", "properties": {}, "additionalProperties": False}))
    registry.register(ToolSpec("process_list", "List running processes and resource usage. Does not terminate processes.", RiskLevel.READ, list_processes,
        {"type": "object", "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 100}},
         "additionalProperties": False}))
    registry.register(ToolSpec("safe_command", "Run one fixed diagnostic command; arbitrary shell commands and arguments are not accepted.", RiskLevel.READ, safe_command,
        {"type": "object", "properties": {"command": {"type": "string", "enum": ["python_version", "node_version", "npm_version", "git_version", "git_status", "whoami"]}},
         "required": ["command"], "additionalProperties": False}))
