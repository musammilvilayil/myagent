from __future__ import annotations
from typing import Any
import httpx
from app.config import settings
from app.security import ApprovalStore, RiskLevel
from app.tools.registry import ToolRegistry


class AgentRuntime:
    """Permission-aware tool runtime. Model planning is a separate implementation phase."""
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

    async def ask_model(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        if not settings.model_base_url or not settings.model_name:
            return {"configured": False, "message": "Configure MODEL_BASE_URL and MODEL_NAME to enable model responses."}
        url = settings.model_base_url.rstrip("/") + "/chat/completions"
        headers = {"Authorization": f"Bearer {settings.model_api_key}"} if settings.model_api_key else {}
        async with httpx.AsyncClient(timeout=settings.model_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json={"model": settings.model_name, "messages": messages})
            response.raise_for_status()
            payload = response.json()
        return {"configured": True, "content": payload.get("choices", [{}])[0].get("message", {}).get("content", "")}
