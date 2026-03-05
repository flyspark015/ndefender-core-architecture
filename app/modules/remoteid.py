from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from app.models import RemoteIdHealth, RemoteIdStatus, now_ms


def _to_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return None


def _to_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None


@dataclass
class Contact:
    contact_id: str
    basic_id: str
    lat: Optional[float]
    lon: Optional[float]
    alt_m: Optional[float]
    speed_mps: Optional[float]
    heading_deg: Optional[float]
    first_seen_ms: int
    last_seen_ms: int
    last_signature: Tuple[Any, ...] = field(default_factory=tuple)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contact_id": self.contact_id,
            "basic_id": self.basic_id,
            "lat": self.lat,
            "lon": self.lon,
            "alt_m": self.alt_m,
            "speed_mps": self.speed_mps,
            "heading_deg": self.heading_deg,
            "first_seen_ms": self.first_seen_ms,
            "last_seen_ms": self.last_seen_ms,
        }


class RemoteIdIngestor:
    def __init__(self, path: str, ttl_s: float = 15.0) -> None:
        self._path = path
        self._ttl_ms = int(ttl_s * 1000)
        self._contacts: Dict[str, Contact] = {}
        self._last_update_ms: Optional[int] = None
        self._last_error: Optional[str] = None
        self._input_ok = False
        self._file = None
        self._file_pos = 0
        self._seen_any = False

    def _status(self) -> RemoteIdStatus:
        return RemoteIdStatus(
            ok=self._input_ok and self._seen_any,
            last_update_ms=self._last_update_ms,
            last_error=None if (self._input_ok and self._seen_any) else self._last_error,
            active_contacts=len(self._contacts),
        )

    def _health(self) -> RemoteIdHealth:
        return RemoteIdHealth(
            ok=self._input_ok and self._seen_any,
            last_update_ms=self._last_update_ms,
            last_error=None if (self._input_ok and self._seen_any) else self._last_error,
            input_stream_ok=self._input_ok,
        )

    def _open_file(self) -> bool:
        if not self._path:
            self._input_ok = False
            self._last_error = "REMOTEID_FILE_MISSING"
            return False
        if not os.path.exists(self._path):
            self._input_ok = False
            self._last_error = "REMOTEID_FILE_MISSING"
            return False
        try:
            self._file = open(self._path, "r", encoding="utf-8")
            self._file_pos = 0
            self._input_ok = True
            self._last_error = "REMOTEID_NO_DATA"
            return True
        except Exception:
            self._input_ok = False
            self._last_error = "REMOTEID_FILE_MISSING"
            return False

    def _read_lines(self, max_lines: int = 50) -> List[str]:
        if self._file is None:
            if not self._open_file():
                return []
        if self._file is None:
            return []
        try:
            self._file.seek(0, os.SEEK_END)
            end_pos = self._file.tell()
            if end_pos < self._file_pos:
                self._file_pos = 0
            self._file.seek(self._file_pos)
            lines = []
            for _ in range(max_lines):
                line = self._file.readline()
                if not line:
                    break
                lines.append(line)
            self._file_pos = self._file.tell()
            return lines
        except Exception:
            self._input_ok = False
            self._last_error = "REMOTEID_READ_FAILED"
            return []

    def _parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        try:
            data = json.loads(line)
            if not isinstance(data, dict):
                return None
            return data
        except Exception:
            if not self._seen_any:
                self._last_error = "REMOTEID_PARSE_ERROR"
            return None

    def _record_signature(self, record: Dict[str, Any]) -> Tuple[Any, ...]:
        return (
            record.get("lat"),
            record.get("lon"),
            record.get("alt"),
            record.get("speed"),
            record.get("heading"),
            record.get("timestamp"),
        )

    def process_record(self, record: Dict[str, Any], now: int) -> Optional[Tuple[str, Dict[str, Any]]]:
        basic_id = record.get("basic_id")
        if not basic_id:
            return None

        lat = _to_float(record.get("lat"))
        lon = _to_float(record.get("lon"))
        alt = _to_float(record.get("alt"))
        speed = _to_float(record.get("speed"))
        heading = _to_float(record.get("heading"))
        signature = self._record_signature(record)

        contact = self._contacts.get(basic_id)
        if contact is None:
            contact = Contact(
                contact_id=f"rid:{basic_id}",
                basic_id=str(basic_id),
                lat=lat,
                lon=lon,
                alt_m=alt,
                speed_mps=speed,
                heading_deg=heading,
                first_seen_ms=now,
                last_seen_ms=now,
                last_signature=signature,
            )
            self._contacts[basic_id] = contact
            return "CONTACT_NEW", contact.to_dict()

        contact.last_seen_ms = now
        if contact.last_signature == signature:
            return None

        contact.lat = lat
        contact.lon = lon
        contact.alt_m = alt
        contact.speed_mps = speed
        contact.heading_deg = heading
        contact.last_signature = signature
        return "CONTACT_UPDATE", contact.to_dict()

    def expire(self, now: int) -> List[Dict[str, Any]]:
        lost: List[Dict[str, Any]] = []
        for key in list(self._contacts.keys()):
            contact = self._contacts[key]
            if now - contact.last_seen_ms > self._ttl_ms:
                lost.append(contact.to_dict())
                del self._contacts[key]
        return lost

    def contacts_snapshot(self) -> List[Dict[str, Any]]:
        return [c.to_dict() for c in self._contacts.values()]

    def poll(self) -> Tuple[RemoteIdStatus, RemoteIdHealth, List[Tuple[str, Dict[str, Any]]]]:
        now = now_ms()
        events: List[Tuple[str, Dict[str, Any]]] = []
        for line in self._read_lines():
            record = self._parse_line(line)
            if record is None:
                continue
            event = self.process_record(record, now)
            if event:
                events.append(event)
            self._last_update_ms = now
            self._seen_any = True
            self._input_ok = True
            self._last_error = None

        for contact in self.expire(now):
            events.append(("CONTACT_LOST", contact))

        status = self._status()
        health = self._health()
        return status, health, events
