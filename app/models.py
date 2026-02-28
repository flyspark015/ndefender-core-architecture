from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def now_ms() -> int:
    import time

    return int(time.time() * 1000)


class EventEnvelope(BaseModel):
    type: str
    timestamp_ms: int
    source: str
    data: Dict[str, Any]


class ModuleStatus(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    detail: Optional[Dict[str, Any]] = None


class StatusSnapshot(BaseModel):
    timestamp_ms: int
    overall_ok: bool
    system: Dict[str, Any]
    modules: Dict[str, ModuleStatus]


class DeepHealth(BaseModel):
    timestamp_ms: int
    overall_ok: bool
    modules: Dict[str, ModuleStatus]


class CommandRequest(BaseModel):
    timestamp_ms: int
    command: str
    confirm: Optional[bool] = False
    payload: Optional[Dict[str, Any]] = None


class ContactsResponse(BaseModel):
    contacts: List[Dict[str, Any]] = Field(default_factory=list)
