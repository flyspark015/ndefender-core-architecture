from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from typing import Optional, Tuple

from app.models import GpsHealth, GpsStatus, now_ms


def _to_float(value) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return None


def _to_int(value) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None


@dataclass
class GpsdReader:
    host: str
    port: int
    _sock: Optional[socket.socket] = None
    _file: Optional[object] = None
    _last_update_ms: Optional[int] = None
    _last_error: Optional[str] = "GPSD_UNAVAILABLE"
    _input_ok: bool = False
    _fix_mode: Optional[int] = None
    _lat: Optional[float] = None
    _lon: Optional[float] = None
    _alt: Optional[float] = None
    _speed: Optional[float] = None
    _track: Optional[float] = None

    def _disconnect(self) -> None:
        try:
            if self._file:
                self._file.close()
        except Exception:
            pass
        try:
            if self._sock:
                self._sock.close()
        except Exception:
            pass
        self._sock = None
        self._file = None

    def _connect(self) -> bool:
        if self._sock is not None:
            return True
        try:
            sock = socket.create_connection((self.host, self.port), timeout=1.0)
            sock.settimeout(1.0)
            self._sock = sock
            self._file = sock.makefile("r")
            sock.sendall(b'?WATCH={"enable":true,"json":true}\\n')
            self._input_ok = True
            if self._last_error == "GPSD_UNAVAILABLE":
                self._last_error = "GPS_NO_DATA"
            return True
        except Exception:
            self._disconnect()
            self._input_ok = False
            self._last_error = "GPSD_UNAVAILABLE"
            return False

    def _read_line(self) -> Optional[str]:
        if self._file is None:
            return None
        try:
            line = self._file.readline()
        except socket.timeout:
            return None
        except Exception:
            self._disconnect()
            self._input_ok = False
            self._last_error = "GPSD_UNAVAILABLE"
            return None
        if not line:
            return None
        return line.strip()

    def _update_from_tpv(self, data: dict, now: int) -> None:
        self._fix_mode = _to_int(data.get("mode"))
        self._lat = _to_float(data.get("lat"))
        self._lon = _to_float(data.get("lon"))
        self._alt = _to_float(data.get("alt"))
        self._speed = _to_float(data.get("speed"))
        self._track = _to_float(data.get("track"))
        self._last_update_ms = now

    def _status(self) -> GpsStatus:
        fix_ok = (
            self._fix_mode is not None
            and self._fix_mode >= 2
            and self._lat is not None
            and self._lon is not None
        )
        if not self._input_ok:
            last_error = "GPSD_UNAVAILABLE"
        elif self._fix_mode is None:
            last_error = "GPS_NO_DATA"
        elif not fix_ok:
            last_error = "GPS_NO_FIX"
        else:
            last_error = None
        return GpsStatus(
            ok=bool(self._input_ok and fix_ok),
            last_update_ms=self._last_update_ms,
            last_error=last_error,
            latitude=self._lat,
            longitude=self._lon,
            altitude_m=self._alt,
            speed_mps=self._speed,
            heading_deg=self._track,
            fix_mode=self._fix_mode,
        )

    def _health(self) -> GpsHealth:
        status = self._status()
        return GpsHealth(
            ok=status.ok,
            last_update_ms=status.last_update_ms,
            last_error=status.last_error,
            fix_mode=status.fix_mode,
            input_stream_ok=self._input_ok,
        )

    def poll(self) -> Tuple[GpsStatus, GpsHealth]:
        now = now_ms()
        if not self._connect():
            return self._status(), self._health()

        got_tpv = False
        for _ in range(5):
            line = self._read_line()
            if not line:
                break
            try:
                payload = json.loads(line)
            except Exception:
                continue
            if payload.get("class") == "TPV":
                self._update_from_tpv(payload, now)
                got_tpv = True
                break

        if not got_tpv and self._last_update_ms is None:
            self._last_error = "GPS_NO_DATA"

        return self._status(), self._health()
