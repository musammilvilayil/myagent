from app.main import app, registry


def test_app_registers_desktop_and_browser_capabilities():
    names = {tool["name"] for tool in registry.describe()}
    expected = {
        "system_overview", "process_list", "process_terminate", "safe_command",
        "workspace_list", "workspace_read", "workspace_search", "workspace_write",
        "screen_capture", "mouse_click", "keyboard_type", "keyboard_press",
        "browser_open", "browser_read", "browser_click_text", "browser_fill",
        "open_application", "open_url",
    }
    assert expected.issubset(names)
    assert any(route.path == "/api/voice/transcribe" for route in app.routes)
