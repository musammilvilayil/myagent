from pathlib import Path
import pytest
from jsonschema import ValidationError
from app.security import RiskLevel
from app.tools.registry import ToolRegistry, ToolSpec
from app.tools.workspace import safe_path


def test_registry_validates_arguments():
    registry = ToolRegistry()
    registry.register(ToolSpec("example", "test", RiskLevel.READ, lambda value: {"ok": True},
        {"type": "object", "properties": {"value": {"type": "string"}}, "required": ["value"], "additionalProperties": False}))
    assert registry.execute("example", {"value": "ok"})["ok"]
    with pytest.raises(ValidationError):
        registry.execute("example", {"value": "ok", "unexpected": True})


def test_workspace_path_rejects_parent_traversal(tmp_path, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "workspace_root", str(tmp_path))
    with pytest.raises(ValueError):
        safe_path("../outside.txt")


def test_workspace_path_accepts_relative_file(tmp_path, monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "workspace_root", str(tmp_path))
    assert safe_path("notes/todo.txt") == Path(tmp_path).resolve() / "notes" / "todo.txt"
