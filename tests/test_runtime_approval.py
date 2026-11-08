from app.agent.runtime import AgentRuntime
from app.security import RiskLevel
from app.tools.registry import ToolRegistry, ToolSpec


def test_sensitive_tool_requires_approval_and_executes_once():
    registry = ToolRegistry()
    calls = []
    registry.register(ToolSpec("change", "test", RiskLevel.SENSITIVE,
        lambda value: calls.append(value) or {"ok": True, "value": value},
        {"type": "object", "properties": {"value": {"type": "string"}},
         "required": ["value"], "additionalProperties": False}))
    runtime = AgentRuntime(registry)

    pending = runtime.run_tool("change", {"value": "approved"})
    assert pending["status"] == "approval_required"
    assert calls == []

    completed = runtime.approve(pending["approval_token"])
    assert completed["status"] == "completed"
    assert calls == ["approved"]

    repeated = runtime.approve(pending["approval_token"])
    assert repeated["status"] == "failed"
    assert calls == ["approved"]


def test_deny_does_not_execute_sensitive_tool():
    registry = ToolRegistry()
    calls = []
    registry.register(ToolSpec("change", "test", RiskLevel.DESTRUCTIVE,
        lambda: calls.append(True) or {"ok": True},
        {"type": "object", "properties": {}, "additionalProperties": False}))
    runtime = AgentRuntime(registry)
    pending = runtime.run_tool("change", {})
    denied = runtime.deny(pending["approval_token"])
    assert denied["status"] == "denied"
    assert calls == []
