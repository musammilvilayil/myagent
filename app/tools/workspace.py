from __future__ import annotations
import os
import shutil
import time
from pathlib import Path
from typing import Any
from app.config import settings
from app.security import RiskLevel
from app.tools.registry import ToolRegistry, ToolSpec


def workspace_root() -> Path:
    root = Path(settings.workspace_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def safe_path(relative_path: str) -> Path:
    if not relative_path or Path(relative_path).is_absolute():
        raise ValueError("Use a non-empty path relative to the MyAgent workspace.")
    root = workspace_root()
    target = (root / relative_path).resolve()
    if target != root and root not in target.parents:
        raise ValueError("Path escapes the MyAgent workspace.")
    return target


def list_files(path: str = ".") -> dict[str, Any]:
    folder = workspace_root() if path == "." else safe_path(path)
    if not folder.exists() or not folder.is_dir():
        return {"ok": False, "error": "Directory does not exist."}
    entries = []
    for item in sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))[:200]:
        entries.append({"name": item.name, "type": "directory" if item.is_dir() else "file",
                        "size_bytes": item.stat().st_size if item.is_file() else None})
    return {"ok": True, "path": "." if folder == workspace_root() else str(folder.relative_to(workspace_root())),
            "entries": entries}


def read_file(path: str, max_chars: int = 30000) -> dict[str, Any]:
    target = safe_path(path)
    if not target.exists() or not target.is_file():
        return {"ok": False, "error": "File does not exist."}
    if target.stat().st_size > 2_000_000:
        return {"ok": False, "error": "File is larger than the 2 MB read limit."}
    try:
        content = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"ok": False, "error": "File is not valid UTF-8 text."}
    return {"ok": True, "path": path, "content": content[:max_chars],
            "truncated": len(content) > max_chars}


def search_files(query: str, path: str = ".") -> dict[str, Any]:
    if not query.strip():
        return {"ok": False, "error": "Search query cannot be empty."}
    folder = workspace_root() if path == "." else safe_path(path)
    if not folder.is_dir():
        return {"ok": False, "error": "Search folder does not exist."}
    matches = []
    for candidate in folder.rglob("*"):
        if len(matches) >= 100:
            break
        if not candidate.is_file() or candidate.stat().st_size > 1_000_000:
            continue
        if any(part.startswith(".") for part in candidate.relative_to(workspace_root()).parts):
            continue
        try:
            for line_number, line in enumerate(candidate.read_text(encoding="utf-8").splitlines(), 1):
                if query.casefold() in line.casefold():
                    matches.append({"path": str(candidate.relative_to(workspace_root())),
                                    "line": line_number, "text": line[:500]})
                    if len(matches) >= 100:
                        break
        except (UnicodeDecodeError, OSError):
            continue
    return {"ok": True, "matches": matches, "truncated": len(matches) >= 100}


def write_file(path: str, content: str) -> dict[str, Any]:
    target = safe_path(path)
    if len(content) > 1_000_000:
        return {"ok": False, "error": "Write limit is 1 MB per file."}
    target.parent.mkdir(parents=True, exist_ok=True)
    backup_path = None
    if target.exists():
        if not target.is_file():
            return {"ok": False, "error": "Target is not a regular file."}
        backup_dir = workspace_root() / ".myagent_backups"
        backup_dir.mkdir(exist_ok=True)
        backup = backup_dir / f"{int(time.time() * 1000)}-{target.name}.bak"
        shutil.copy2(target, backup)
        backup_path = str(backup.relative_to(workspace_root()))
    temp = target.with_name(target.name + ".myagent-tmp")
    temp.write_text(content, encoding="utf-8")
    os.replace(temp, target)
    return {"ok": True, "path": path, "bytes_written": len(content.encode("utf-8")), "backup": backup_path}


def register_workspace_tools(registry: ToolRegistry) -> None:
    registry.register(ToolSpec("workspace_list", "List files and folders inside the MyAgent workspace only.", RiskLevel.READ, list_files,
        {"type": "object", "properties": {"path": {"type": "string", "default": "."}}, "additionalProperties": False}))
    registry.register(ToolSpec("workspace_read", "Read a UTF-8 text file inside the MyAgent workspace.", RiskLevel.READ, read_file,
        {"type": "object", "properties": {"path": {"type": "string"}, "max_chars": {"type": "integer", "minimum": 1, "maximum": 30000}},
         "required": ["path"], "additionalProperties": False}))
    registry.register(ToolSpec("workspace_search", "Search text in files inside the MyAgent workspace.", RiskLevel.READ, search_files,
        {"type": "object", "properties": {"query": {"type": "string"}, "path": {"type": "string", "default": "."}},
         "required": ["query"], "additionalProperties": False}))
    registry.register(ToolSpec("workspace_write", "Create or replace a text file inside the workspace. Requires user approval; existing files are backed up.", RiskLevel.SENSITIVE, write_file,
        {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
         "required": ["path", "content"], "additionalProperties": False}))
