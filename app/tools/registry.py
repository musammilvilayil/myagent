from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from jsonschema import validate
from app.security import RiskLevel


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    risk: RiskLevel
    handler: Callable[..., dict[str, Any]]
    parameters: dict[str, Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"Tool already registered: {spec.name}")
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        if name not in self._tools:
            raise KeyError(name)
        return self._tools[name]

    def describe(self) -> list[dict[str, str]]:
        return [{"name": t.name, "description": t.description, "risk": t.risk.value} for t in self._tools.values()]

    def model_schemas(self) -> list[dict[str, Any]]:
        return [{"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.parameters}}
                for t in self._tools.values()]

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        tool = self.get(name)
        validate(instance=arguments, schema=tool.parameters)
        return tool.handler(**arguments)
