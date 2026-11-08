from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from app.agent.runtime import AgentRuntime
from app.config import settings
from app.tools.desktop import register_desktop_tools
from app.tools.registry import ToolRegistry

registry = ToolRegistry()
register_desktop_tools(registry)
runtime = AgentRuntime(registry)
app = FastAPI(title=settings.app_name, version="0.1.0")


class ToolRequest(BaseModel):
    name: str
    arguments: dict = Field(default_factory=dict)
    approval_token: str | None = None


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)


@app.get("/api/health")
async def health():
    return {"ok": True, "app": settings.app_name, "version": "0.1.0"}


@app.get("/api/tools")
async def list_tools():
    return {"tools": registry.describe()}


@app.post("/api/tools/execute")
async def execute_tool(request: ToolRequest):
    try:
        return runtime.run_tool(request.name, request.arguments, request.approval_token)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown tool")


@app.post("/api/chat")
async def chat(request: ChatRequest):
    result = await runtime.ask_model([{"role": "user", "content": request.message}])
    if not result.get("configured"):
        return {"status": "not_configured", "reply": "Model provider is not configured yet. Test available PC tools from the Tools panel."}
    return {"status": "completed", "reply": result.get("content", "")}


@app.get("/")
async def dashboard():
    return FileResponse("web/index.html")
