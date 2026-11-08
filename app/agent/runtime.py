from __future__ import annotations
import json
from typing import Any
import httpx
from app.config import settings
from app.security import ApprovalStore, RiskLevel
from app.tools.registry import ToolRegistry


class AgentRuntime:
    """Bounded model/tool loop. Only registered tools and their schemas can be invoked."""
    def __init__(self, tools: ToolRegistry) -> None:
        self.tools = tools
        self.approvals = ApprovalStore()

    def run_tool(self, name: str, arguments: dict[str, Any], approval_token: str | None = None) -> dict[str, Any]:
        spec = self.tools.get(name)
        if spec.risk in {RiskLevel.SENSITIVE, RiskLevel.DESTRUCTIVE}:
            if not approval_token or not self.approvals.consume(approval_token, name):
                approval = self.approvals.request(name)
                return {"status": "approval_required", "approval_token": approval.token,
                        "expires_in_seconds": self.approvals.ttl_seconds, "tool": name}
        try:
            result = self.tools.execute(name, arguments)
            return {"status": "completed" if result.get("ok") else "unverified_or_failed", "tool": name, "result": result}
        except Exception as exc:
            return {"status": "failed", "tool": name, "error": str(exc)}

    async def chat(self, user_message: str, max_tool_rounds: int = 5) -> dict[str, Any]:
        if not settings.model_base_url or not settings.model_name:
            return {"status": "not_configured", "reply": "Configure MODEL_BASE_URL and MODEL_NAME in .env first."}

        messages: list[dict[str, Any]] = [
            {"role": "system", "content": (
                "You are MyAgent, a careful Windows PC assistant. Use registered tools for PC actions. "
                "Never claim an action succeeded unless its tool result confirms it. "
                "Only use tools for the user's requested task. Explain when an action is unavailable."
            )},
            {"role": "user", "content": user_message},
        ]
        url = settings.model_base_url.rstrip("/") + "/chat/completions"
        headers = {"Authorization": f"Bearer {settings.model_api_key}"} if settings.model_api_key else {}
        async with httpx.AsyncClient(timeout=settings.model_timeout_seconds) as client:
            for round_index in range(max_tool_rounds + 1):
                payload: dict[str, Any] = {
                    "model": settings.model_name,
                    "messages": messages,
                    "tools": self.tools.model_schemas(),
                    "tool_choice": "auto",
                }
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                choice = (data.get("choices") or [{}])[0]
                message = choice.get("message") or {}
                tool_calls = message.get("tool_calls") or []
                if not tool_calls:
                    return {"status": "completed", "reply": message.get("content") or ""}
                messages.append({"role": "assistant", "content": message.get("content"), "tool_calls": tool_calls})
                if round_index == max_tool_rounds:
                    return {"status": "limit_reached", "reply": "I stopped after reaching the tool-call limit to avoid an uncontrolled loop."}
                for call in tool_calls:
                    function = call.get("function") or {}
                    name = function.get("name", "")
                    try:
                        arguments = json.loads(function.get("arguments") or "{}")
                        if not isinstance(arguments, dict):
                            raise ValueError("Tool arguments must be a JSON object.")
                        result = self.run_tool(name, arguments)
                    except (ValueError, TypeError, KeyError) as exc:
                        result = {"status": "failed", "error": str(exc)}
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.get("id", ""),
                        "content": json.dumps(result, ensure_ascii=False),
                    })
        return {"status": "failed", "reply": "The agent could not complete this request."}
