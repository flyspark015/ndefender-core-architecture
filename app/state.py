from __future__ import annotations

from dataclasses import dataclass, field
from threading import Event, Lock, Thread
from time import sleep
from typing import Any, Dict, List

import os

from .config import (
    ESP32_BAUD,
    ESP32_PORT,
    ESP32_READ_TIMEOUT_S,
    ESP32_RECONNECT_S,
    ANTSDR_POLL_INTERVAL_S,
    ANTSDR_URI,
    REMOTEID_EK_PATH,
    REMOTEID_POLL_INTERVAL_S,
    REMOTEID_TTL_S,
    UPS_POLL_INTERVAL_S,
)
from .models import (
    AntsdrHealth,
    AntsdrStatus,
    Esp32Health,
    Esp32Status,
    EventEnvelope,
    FusionHealth,
    FusionStatus,
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
from .events import EVENT_HUB
from .modules.os_module import read_os_health, read_os_status, status_to_system
from .modules.ups_hat_e import FakeUpsHatEReader, UpsHatEReader
from .modules.esp32 import Esp32SerialReader, Esp32NotConnected
from .modules.antsdr import AntsdrReader
from .modules.remoteid import RemoteIdIngestor
from .modules.fusion import FusionEngine


def _default_status_modules() -> StatusModules:
    return StatusModules(
        ups=UpsStatus(ok=False, last_error="ups_starting"),
        os=OsStatus(ok=False, last_error=None),
        esp32=Esp32Status(ok=False, connected=False, last_error="ESP32_SERIAL_NOT_CONNECTED"),
        antsdr=AntsdrStatus(ok=False, last_error="ANTSDR_NOT_CONNECTED"),
        remoteid=RemoteIdStatus(ok=False, last_error="REMOTEID_FILE_MISSING"),
        fusion=FusionStatus(ok=True, last_error=None, active_contacts=0, last_update_ms=now_ms()),
        video=VideoStatus(ok=False, last_error="not_implemented"),
    )


def _default_health_modules() -> HealthModules:
    return HealthModules(
        ups=UpsHealth(ok=False, last_error="ups_starting"),
        os=OsHealth(ok=False, last_error=None),
        esp32=Esp32Health(ok=False, last_error="ESP32_SERIAL_NOT_CONNECTED"),
        antsdr=AntsdrHealth(ok=False, last_error="ANTSDR_NOT_CONNECTED", device_present=False, driver_ok=False),
        remoteid=RemoteIdHealth(ok=False, last_error="REMOTEID_FILE_MISSING", input_stream_ok=False),
        fusion=FusionHealth(ok=True, last_error=None, active_contacts=0, last_update_ms=now_ms()),
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
    _esp32_thread: Thread | None = field(default=None, init=False, repr=False)
    _esp32_reader: Esp32SerialReader | None = field(default=None, init=False, repr=False)
    _antsdr_thread: Thread | None = field(default=None, init=False, repr=False)
    _antsdr_reader: AntsdrReader | None = field(default=None, init=False, repr=False)
    _remoteid_thread: Thread | None = field(default=None, init=False, repr=False)
    _remoteid_reader: RemoteIdIngestor | None = field(default=None, init=False, repr=False)
    _fusion_thread: Thread | None = field(default=None, init=False, repr=False)
    _fusion_engine: FusionEngine | None = field(default=None, init=False, repr=False)
    _fusion_queue: Any = field(default=None, init=False, repr=False)

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

        self._esp32_reader = Esp32SerialReader(
            port_setting=ESP32_PORT,
            baud=ESP32_BAUD,
            read_timeout_s=ESP32_READ_TIMEOUT_S,
            reconnect_s=ESP32_RECONNECT_S,
        )
        status, health = self._esp32_reader.not_connected()
        with self._lock:
            self.modules_status.esp32 = status
            self.modules_health.esp32 = health
        self._esp32_thread = Thread(target=self._esp32_loop, args=(self._esp32_reader,), daemon=True)
        self._esp32_thread.start()

        self._antsdr_reader = AntsdrReader(uri=ANTSDR_URI)
        status, health = self._antsdr_reader.poll()
        with self._lock:
            self.modules_status.antsdr = status
            self.modules_health.antsdr = health
        self._antsdr_thread = Thread(target=self._antsdr_loop, args=(self._antsdr_reader,), daemon=True)
        self._antsdr_thread.start()

        self._remoteid_reader = RemoteIdIngestor(path=REMOTEID_EK_PATH, ttl_s=REMOTEID_TTL_S)
        status, health, _ = self._remoteid_reader.poll()
        with self._lock:
            self.modules_status.remoteid = status
            self.modules_health.remoteid = health
        self._remoteid_thread = Thread(
            target=self._remoteid_loop, args=(self._remoteid_reader,), daemon=True
        )
        self._remoteid_thread.start()

        self._fusion_engine = FusionEngine()
        with self._lock:
            self.modules_status.fusion = self._fusion_engine.status()
            self.modules_health.fusion = self._fusion_engine.health()
            self.contacts = self._fusion_engine.contacts_snapshot()
        self._fusion_queue = EVENT_HUB.subscribe()
        self._fusion_thread = Thread(
            target=self._fusion_loop, args=(self._fusion_engine, self._fusion_queue), daemon=True
        )
        self._fusion_thread.start()

    def _ups_loop(self, reader: UpsHatEReader) -> None:
        while not self._stop_event.is_set():
            status, health = reader.poll()
            with self._lock:
                self.modules_status.ups = status
                self.modules_health.ups = health
            sleep(UPS_POLL_INTERVAL_S)

    def _esp32_loop(self, reader: Esp32SerialReader) -> None:
        def _update(status: Esp32Status, health: Esp32Health) -> None:
            with self._lock:
                self.modules_status.esp32 = status
                self.modules_health.esp32 = health

        def _telemetry(data) -> None:
            payload: Dict[str, Any]
            if isinstance(data, dict):
                payload = dict(data)
                if "raw" not in payload:
                    payload["raw"] = data
            else:
                payload = {"raw": data}

            event = EventEnvelope(
                type="TELEMETRY_UPDATE",
                timestamp_ms=now_ms(),
                source="esp32",
                data=payload,
            )
            EVENT_HUB.publish(event.model_dump())

        reader.loop(self._stop_event, _update, _telemetry)

    def _antsdr_loop(self, reader: AntsdrReader) -> None:
        while not self._stop_event.is_set():
            status, health = reader.poll()
            with self._lock:
                self.modules_status.antsdr = status
                self.modules_health.antsdr = health
            sleep(ANTSDR_POLL_INTERVAL_S)

    def _remoteid_loop(self, reader: RemoteIdIngestor) -> None:
        while not self._stop_event.is_set():
            status, health, events = reader.poll()
            with self._lock:
                self.modules_status.remoteid = status
                self.modules_health.remoteid = health
            for event_type, payload in events:
                EVENT_HUB.publish(
                    EventEnvelope(
                        type=event_type,
                        timestamp_ms=now_ms(),
                        source="remoteid",
                        data=payload,
                    ).model_dump()
                )
            sleep(REMOTEID_POLL_INTERVAL_S)

    def _fusion_loop(self, engine: FusionEngine, queue) -> None:
        from queue import Empty

        while not self._stop_event.is_set():
            try:
                event = queue.get(timeout=1.0)
            except Empty:
                event = None

            now = now_ms()
            events = []
            if event:
                events.extend(engine.process_event(event, now=now))
            events.extend(engine.expire(now=now))

            with self._lock:
                self.modules_status.fusion = engine.status(now=now)
                self.modules_health.fusion = engine.health(now=now)
                self.contacts = engine.contacts_snapshot()

            for event_type, payload in events:
                EVENT_HUB.publish(
                    EventEnvelope(
                        type=event_type,
                        timestamp_ms=now,
                        source="fusion",
                        data=payload,
                    ).model_dump()
                )

    def esp32_connected(self) -> bool:
        with self._lock:
            return bool(self.modules_status.esp32.connected)

    def esp32_send_command(self, command: str, payload: Dict[str, Any], timestamp_ms: int) -> None:
        if self._esp32_reader is None:
            raise Esp32NotConnected()
        self._esp32_reader.send_command(command, payload, timestamp_ms)

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
            return list(self.contacts)


STATE = StateStore()
