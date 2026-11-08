from __future__ import annotations

from io import BytesIO
import base64
from typing import Any

from app.security import RiskLevel
from app.tools.registry import ToolRegistry, ToolSpec


def _pyautogui():
    try:
        import pyautogui
    except ImportError as exc:
        raise RuntimeError("Desktop controls are optional. Install requirements-desktop.txt first.") from exc
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.15
    return pyautogui


def screen_capture() -> dict[str, Any]:
    gui = _pyautogui()
    image = gui.screenshot()
    original_width, original_height = image.size
    image.thumbnail((1600, 1200))
    buffer = BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return {"ok": True, "width": original_width, "height": original_height,
            "image_base64": base64.b64encode(buffer.getvalue()).decode("ascii"),
            "note": "Image is resized to fit within 1600x1200 for model vision."}


def mouse_click(x: int, y: int, button: str = "left", clicks: int = 1) -> dict[str, Any]:
    gui = _pyautogui()
    width, height = gui.size()
    if not (0 <= x < width and 0 <= y < height):
        return {"ok": False, "error": f"Coordinates must be within {width}x{height} screen bounds."}
    if button not in {"left", "right", "middle"} or not 1 <= clicks <= 2:
        return {"ok": False, "error": "Only left/right/middle and one or two clicks are allowed."}
    gui.click(x=x, y=y, button=button, clicks=clicks)
    return {"ok": True, "clicked": {"x": x, "y": y, "button": button, "clicks": clicks}}


def keyboard_type(text: str) -> dict[str, Any]:
    if len(text) > 2000:
        return {"ok": False, "error": "Typing is limited to 2,000 characters per action."}
    _pyautogui().write(text, interval=0.01)
    return {"ok": True, "characters_typed": len(text)}


def keyboard_press(key: str) -> dict[str, Any]:
    allowed = {"enter", "tab", "esc", "space", "up", "down", "left", "right",
               "home", "end", "pageup", "pagedown", "backspace"}
    if key.lower() not in allowed:
        return {"ok": False, "error": "Key is not in the permitted single-key list."}
    _pyautogui().press(key.lower())
    return {"ok": True, "key_pressed": key.lower()}


def register_desktop_automation_tools(registry: ToolRegistry) -> None:
    registry.register(ToolSpec("screen_capture", "Capture the current screen. Returns an image payload; requires optional desktop dependencies.", RiskLevel.READ, screen_capture,
        {"type": "object", "properties": {}, "additionalProperties": False}))
    registry.register(ToolSpec("mouse_click", "Click a screen coordinate. Requires explicit user approval.", RiskLevel.SENSITIVE, mouse_click,
        {"type": "object", "properties": {"x": {"type": "integer", "minimum": 0}, "y": {"type": "integer", "minimum": 0},
         "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"},
         "clicks": {"type": "integer", "minimum": 1, "maximum": 2}},
         "required": ["x", "y"], "additionalProperties": False}))
    registry.register(ToolSpec("keyboard_type", "Type text into the currently focused application. Requires explicit user approval.", RiskLevel.SENSITIVE, keyboard_type,
        {"type": "object", "properties": {"text": {"type": "string", "maxLength": 2000}},
         "required": ["text"], "additionalProperties": False}))
    registry.register(ToolSpec("keyboard_press", "Press one permitted navigation key in the focused application. Requires explicit user approval.", RiskLevel.SENSITIVE, keyboard_press,
        {"type": "object", "properties": {"key": {"type": "string", "enum": ["enter", "tab", "esc", "space", "up", "down", "left", "right", "home", "end", "pageup", "pagedown", "backspace"]}},
         "required": ["key"], "additionalProperties": False}))
