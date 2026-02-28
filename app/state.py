from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Dict, List

from .models import (
    AntsdrHealth,
    AntsdrStatus,
    Esp32Health,
    Esp32Status,
    HealthModules,
    OsHealth,
    OsStatus,
    RemoteIdHealth,
    RemoteIdStatus,
    StatusModules,
    UpsHealth,
    UpsStatus,
    VideoHealth,
    VideoStatus,
    now_ms,
)


def _default_status_modules() -> StatusModules:
    return StatusModules(
        ups=UpsStatus(ok=False),
        os=OsStatus(ok=False),
        esp32=Esp32Status(ok=False),
        antsdr=AntsdrStatus(ok=False),
        remoteid=RemoteIdStatus(ok=False),
        video=VideoStatus(ok=False),
    )


def _default_health_modules() -> HealthModules:
    return HealthModules(
        ups=UpsHealth(ok=False),
        os=OsHealth(ok=False),
        esp32=Esp32Health(ok=False),
        antsdr=AntsdrHealth(ok=False),
        remoteid=RemoteIdHealth(ok=False),
        video=VideoHealth(ok=False),
    )


def _overall_ok(modules_dump: Dict[str, Dict[str, Any]]) -> bool:
    return all(mod.get("ok") for mod in modules_dump.values())


@dataclass
class StateStore:
    system: Dict[str, Any] = field(default_factory=dict)
    modules_status: StatusModules = field(default_factory=_default_status_modules)
    modules_health: HealthModules = field(default_factory=_default_health_modules)
    contacts: List[Dict[str, Any]] = field(default_factory=list)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            modules_copy = self.modules_status
            modules_dump = modules_copy.model_dump()
            overall_ok = _overall_ok(modules_dump)
            return {
                "timestamp_ms": now_ms(),
                "overall_ok": overall_ok,
                "system": dict(self.system),
                "modules": modules_copy,
            }

    def health(self) -> Dict[str, Any]:
        with self._lock:
            modules_copy = self.modules_health
            modules_dump = modules_copy.model_dump()
            overall_ok = _overall_ok(modules_dump)
            return {
                "timestamp_ms": now_ms(),
                "overall_ok": overall_ok,
                "modules": modules_copy,
            }

    def contacts_snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {"contacts": list(self.contacts)}


STATE = StateStore()
