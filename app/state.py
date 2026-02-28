from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Dict, List

from .models import ModuleStatus, now_ms

MODULE_NAMES = ["ups", "os", "esp32", "antsdr", "remoteid", "video"]


def _default_modules() -> Dict[str, ModuleStatus]:
    return {name: ModuleStatus(ok=False, last_update_ms=None, detail=None) for name in MODULE_NAMES}


@dataclass
class StateStore:
    system: Dict[str, Any] = field(default_factory=dict)
    modules: Dict[str, ModuleStatus] = field(default_factory=_default_modules)
    contacts: List[Dict[str, Any]] = field(default_factory=list)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            modules_copy = {k: v for k, v in self.modules.items()}
            overall_ok = all(m.ok for m in modules_copy.values())
            return {
                "timestamp_ms": now_ms(),
                "overall_ok": overall_ok,
                "system": dict(self.system),
                "modules": modules_copy,
            }

    def health(self) -> Dict[str, Any]:
        with self._lock:
            modules_copy = {k: v for k, v in self.modules.items()}
            overall_ok = all(m.ok for m in modules_copy.values())
            return {
                "timestamp_ms": now_ms(),
                "overall_ok": overall_ok,
                "modules": modules_copy,
            }

    def contacts_snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {"contacts": list(self.contacts)}


STATE = StateStore()
