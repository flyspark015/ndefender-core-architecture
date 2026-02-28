from __future__ import annotations

from dataclasses import dataclass, field
from threading import Event, Lock, Thread
from time import sleep
from typing import Any, Dict, List

import os

from .config import UPS_POLL_INTERVAL_S
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
from .modules.os_module import read_os_health, read_os_status, status_to_system
from .modules.ups_hat_e import FakeUpsHatEReader, UpsHatEReader


def _default_status_modules() -> StatusModules:
    return StatusModules(
        ups=UpsStatus(ok=False, last_error="ups_starting"),
        os=OsStatus(ok=False, last_error=None),
        esp32=Esp32Status(ok=False, last_error="not_implemented"),
        antsdr=AntsdrStatus(ok=False, last_error="not_implemented"),
        remoteid=RemoteIdStatus(ok=False, last_error="not_implemented"),
        video=VideoStatus(ok=False, last_error="not_implemented"),
    )


def _default_health_modules() -> HealthModules:
    return HealthModules(
        ups=UpsHealth(ok=False, last_error="ups_starting"),
        os=OsHealth(ok=False, last_error=None),
        esp32=Esp32Health(ok=False, last_error="not_implemented"),
        antsdr=AntsdrHealth(ok=False, last_error="not_implemented"),
        remoteid=RemoteIdHealth(ok=False, last_error="not_implemented"),
        video=VideoHealth(ok=False, last_error="not_implemented"),
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
    _pollers_started: bool = field(default=False, init=False)
    _stop_event: Event = field(default_factory=Event, init=False, repr=False)
    _ups_thread: Thread | None = field(default=None, init=False, repr=False)

    def refresh_os(self) -> None:
        status = read_os_status()
        health = read_os_health()
        with self._lock:
            self.modules_status.os = status
            self.modules_health.os = health
            self.system = status_to_system(status)

    def start_pollers(self) -> None:
        if self._pollers_started:
            return
        self._pollers_started = True
        reader: UpsHatEReader
        if os.getenv("NDEFENDER_UPS_FAKE", "0") == "1":
            reader = FakeUpsHatEReader()
        else:
            reader = UpsHatEReader()
        status, health = reader.poll()
        with self._lock:
            self.modules_status.ups = status
            self.modules_health.ups = health
        self._ups_thread = Thread(target=self._ups_loop, args=(reader,), daemon=True)
        self._ups_thread.start()

    def _ups_loop(self, reader: UpsHatEReader) -> None:
        while not self._stop_event.is_set():
            status, health = reader.poll()
            with self._lock:
                self.modules_status.ups = status
                self.modules_health.ups = health
            sleep(UPS_POLL_INTERVAL_S)

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
