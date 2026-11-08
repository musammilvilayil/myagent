from __future__ import annotations
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, HTTPException, UploadFile, File
from starlette.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field
from app.agent.runtime import AgentRuntime
from app.config import settings
from app.tools.browser import close_browser_session, register_browser_tools
from app.tools.desktop import register_desktop_tools
from app.tools.desktop_automation import register_desktop_automation_tools, _pyautogui
from app.tools.registry import ToolRegistry
from app.tools.system import register_system_tools
from app.tools.workspace import register_workspace_tools

registry = ToolRegistry()
register_desktop_tools(registry)
register_system_tools(registry)
register_workspace_tools(registry)
register_desktop_automation_tools(registry)
register_browser_tools(registry)
runtime = AgentRuntime(registry)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_browser_session()


app = FastAPI(title=settings.app_name, version="0.4.0", lifespan=lifespan)


class ToolRequest(BaseModel):
    name: str
    arguments: dict = Field(default_factory=dict)
    approval_token: str | None = None


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)


@app.get("/api/health")
async def health():
    return {"ok": True, "app": settings.app_name, "version": "0.4.0"}


@app.get("/api/tools")
async def list_tools():
    return {"tools": registry.describe()}


@app.get("/api/screen")
async def capture_screen():
    try:
        image = _pyautogui().screenshot()
        from io import BytesIO
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return Response(content=buffer.getvalue(), media_type="image/png",
                        headers={"Cache-Control": "no-store"})
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@app.post("/api/tools/execute")
async def execute_tool(request: ToolRequest):
    try:
        return runtime.run_tool(request.name, request.arguments, request.approval_token)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown tool")


@app.post("/api/approvals/{token}/approve")
async def approve_action(token: str):
    result = runtime.approve(token)
    if result.get("status") == "failed":
        raise HTTPException(status_code=404, detail=result.get("error", "Approval not found"))
    return result


@app.post("/api/approvals/{token}/deny")
async def deny_action(token: str):
    result = runtime.deny(token)
    if result.get("status") == "failed":
        raise HTTPException(status_code=404, detail=result.get("error", "Approval not found"))
    return result


@app.post("/api/voice/transcribe")
async def voice_transcribe(file: UploadFile = File(...)):
    audio = await file.read(25 * 1024 * 1024 + 1)
    if len(audio) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio upload exceeds the 25 MB limit.")
    try:
        from app.agent.voice import transcribe_audio
        transcript = await run_in_threadpool(transcribe_audio, audio)
        if not transcript.get("ok"):
            return {"status": "no_speech", "transcription": transcript}
        agent_result = await runtime.chat(transcript["text"])
        return {"status": agent_result.get("status"), "transcription": transcript,
                "reply": agent_result.get("reply", ""),
                "pending_action": agent_result.get("pending_action")}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Model provider request failed: {exc}")


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        return await runtime.chat(request.message)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Model provider request failed: {exc}")


@app.get("/")
async def dashboard():
    return FileResponse("web/index.html")
