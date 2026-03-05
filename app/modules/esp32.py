from __future__ import annotations

import glob
import json
import logging
import time
from threading import Lock
from typing import Any, Dict, Optional, Tuple

import serial
from serial import SerialException

from app.models import Esp32Health, Esp32Status, now_ms


class Esp32NotConnected(Exception):
    pass


AUTO_HINTS = [
    "CP210",
    "CH340",
    "USB",
    "UART",
    "Silicon_Labs",
    "wch",
]


def _matches_hint(path: str) -> bool:
    lower = path.lower()
    return any(hint.lower() in lower for hint in AUTO_HINTS)


def _first_value(data: Dict[str, Any], *keys: str) -> Optional[Any]:
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return None


def _to_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return None


def _mv_to_v(value: Any) -> Optional[float]:
    val = _to_float(value)
    if val is None:
        return None
    return val / 1000.0


class Esp32SerialReader:
    def __init__(self, port_setting: str, baud: int, read_timeout_s: float, reconnect_s: float) -> None:
        self._port_setting = port_setting or "auto"
        self._baud = baud
        self._read_timeout_s = read_timeout_s
        self._reconnect_s = reconnect_s
        self._serial: Optional[serial.Serial] = None
        self._lock = Lock()
        self._last_update_ms: Optional[int] = None
        self._last_error: Optional[str] = "ESP32_SERIAL_NOT_CONNECTED"
        self._connected = False
        self._firmware_version: Optional[str] = None
        self._device_uptime_ms: Optional[int] = None
        self._seq: Optional[int] = None
        self._supply_voltage_v: Optional[float] = None
        self._temperature_c: Optional[float] = None
        self._logger = logging.getLogger("ndefender.esp32")
        self._last_log_s: float = 0.0

    def _log_throttled(self, message: str) -> None:
        now = time.monotonic()
        if now - self._last_log_s >= 10.0:
            self._logger.warning(message)
            self._last_log_s = now

    def _resolve_ports(self) -> list[str]:
        setting = (self._port_setting or "auto").strip()
        if setting and setting.lower() not in ("auto", "none"):
            return [setting]

        by_id = sorted(glob.glob("/dev/serial/by-id/*"))
        matches = [path for path in by_id if _matches_hint(path)]
        if matches:
            return matches

        acm = sorted(glob.glob("/dev/ttyACM*"))
        if acm:
            return acm

        usb = sorted(glob.glob("/dev/ttyUSB*"))
        if usb:
            return usb

        return []

    def _open_serial(self) -> bool:
        ports = self._resolve_ports()
        if not ports:
            self._log_throttled("esp32 serial: no ports found for auto detection")
            self._serial = None
            self._connected = False
            self._last_error = "ESP32_SERIAL_NOT_CONNECTED"
            return False

        self._log_throttled(f"esp32 serial candidates: {ports}")
        for port in ports:
            try:
                self._serial = serial.Serial(port, self._baud, timeout=self._read_timeout_s)
                self._connected = True
                self._last_error = None
                if self._last_update_ms is None:
                    self._last_update_ms = now_ms()
                self._logger.info("esp32 serial connected port=%s", port)
                return True
            except SerialException as exc:
                self._log_throttled(f"esp32 serial open failed port={port} error={exc}")
                continue
        self._serial = None
        self._connected = False
        self._last_error = "ESP32_SERIAL_NOT_CONNECTED"
        return False

    def _close_serial(self) -> None:
        if self._serial is not None:
            try:
                self._serial.close()
            except Exception:
                pass
        self._serial = None
        self._connected = False

    def not_connected(self) -> Tuple[Esp32Status, Esp32Health]:
        status = Esp32Status(
            ok=False,
            connected=False,
            last_update_ms=self._last_update_ms,
            last_error="ESP32_SERIAL_NOT_CONNECTED",
            firmware_version=self._firmware_version,
            device_uptime_ms=self._device_uptime_ms,
            seq=self._seq,
            supply_voltage_v=self._supply_voltage_v,
            temperature_c=self._temperature_c,
        )
        health = Esp32Health(
            ok=False,
            comms_ok=False,
            last_update_ms=self._last_update_ms,
            last_error="ESP32_SERIAL_NOT_CONNECTED",
        )
        return status, health

    def _build_status(self) -> Esp32Status:
        return Esp32Status(
            ok=self._connected,
            connected=self._connected,
            last_update_ms=self._last_update_ms,
            last_error=self._last_error,
            firmware_version=self._firmware_version,
            device_uptime_ms=self._device_uptime_ms,
            seq=self._seq,
            supply_voltage_v=self._supply_voltage_v,
            temperature_c=self._temperature_c,
        )

    def _build_health(self) -> Esp32Health:
        return Esp32Health(
            ok=self._connected,
            comms_ok=self._connected,
            last_update_ms=self._last_update_ms,
            last_error=self._last_error,
        )

    def _handle_telemetry(self, data: Dict[str, Any]) -> None:
        fw = _first_value(data, "firmware_version", "fw_version", "fw")
        if fw:
            self._firmware_version = str(fw)

        seq = _first_value(data, "seq")
        if seq is not None:
            try:
                self._seq = int(seq)
            except Exception:
                self._seq = None

        supply_v = _first_value(data, "supply_voltage_v")
        if supply_v is None:
            supply_v = _mv_to_v(_first_value(data, "supply_mv", "vcc_mv"))
        if supply_v is not None:
            self._supply_voltage_v = _to_float(supply_v)

        temp_c = _first_value(data, "temperature_c", "temp_c", "temp")
        if temp_c is not None:
            self._temperature_c = _to_float(temp_c)

        device_ts = _first_value(data, "timestamp_ms", "ts_ms", "uptime_ms")
        if device_ts is not None:
            try:
                self._device_uptime_ms = int(device_ts)
            except Exception:
                self._device_uptime_ms = None

        self._last_update_ms = now_ms()

        self._connected = True
        self._last_error = None
        return {
            "device_uptime_ms": self._device_uptime_ms,
            "seq": self._seq,
            "fw_version": self._firmware_version,
            "sel": data.get("sel"),
            "vrx": data.get("vrx"),
            "video": data.get("video"),
            "led": data.get("led"),
            "sys": data.get("sys"),
            "raw": data,
        }

    def send_command(self, command: str, payload: Dict[str, Any], timestamp_ms: int) -> None:
        with self._lock:
            if self._serial is None or not self._connected:
                raise Esp32NotConnected()
            message = {
                "type": "command",
                "command": command,
                "payload": payload,
                "timestamp_ms": timestamp_ms,
            }
            data = (json.dumps(message) + "\n").encode("utf-8")
            self._serial.write(data)
            self._serial.flush()

    def loop(self, stop_event, on_update, on_telemetry) -> None:
        while not stop_event.is_set():
            if self._serial is None:
                if not self._open_serial():
                    status, health = self.not_connected()
                    on_update(status, health)
                    time.sleep(self._reconnect_s)
                    continue
                on_update(self._build_status(), self._build_health())

            try:
                with self._lock:
                    line = self._serial.readline() if self._serial is not None else b""
                if not line:
                    continue
                try:
                    decoded = line.decode("utf-8", errors="ignore").strip()
                    if not decoded:
                        continue
                    data = json.loads(decoded)
                    if isinstance(data, dict):
                        if data.get("type") == "telemetry" or "type" not in data:
                            payload = self._handle_telemetry(data)
                            on_update(self._build_status(), self._build_health())
                            if payload:
                                on_telemetry(payload)
                except json.JSONDecodeError:
                    self._last_error = "esp32_parse_error"
                except Exception:
                    self._last_error = "esp32_telemetry_error"
            except SerialException:
                self._close_serial()
                status, health = self.not_connected()
                on_update(status, health)
            except Exception:
                self._close_serial()
                status, health = self.not_connected()
                on_update(status, health)
