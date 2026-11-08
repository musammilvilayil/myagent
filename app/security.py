from __future__ import annotations
import secrets
import time
from dataclasses import dataclass
from enum import StrEnum


class RiskLevel(StrEnum):
    READ = "read"
    LOW = "low"
    SENSITIVE = "sensitive"
    DESTRUCTIVE = "destructive"


@dataclass
class Approval:
    token: str
    action: str
    expires_at: float
    used: bool = False


class ApprovalStore:
    """In-memory, one-use approvals. Persisted approvals are deliberately not supported yet."""
    def __init__(self, ttl_seconds: int = 120) -> None:
        self.ttl_seconds = ttl_seconds
        self._items: dict[str, Approval] = {}

    def request(self, action: str) -> Approval:
        token = secrets.token_urlsafe(24)
        approval = Approval(token, action, time.time() + self.ttl_seconds)
        self._items[token] = approval
        return approval

    def consume(self, token: str, action: str) -> bool:
        approval = self._items.get(token)
        if not approval or approval.used or approval.action != action:
            return False
        if approval.expires_at < time.time():
            self._items.pop(token, None)
            return False
        approval.used = True
        return True
