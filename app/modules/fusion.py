from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from app.models import FusionHealth, FusionStatus, now_ms


VIDEO_MATCH_WINDOW_MS = 5000


@dataclass
class FusedContact:
    contact_id: str
    type: str
    remoteid_id: Optional[str]
    rf_sources: List[str] = field(default_factory=list)
    video_sources: List[str] = field(default_factory=list)
    first_seen_ms: int = 0
    last_seen_ms: int = 0
    threat_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contact_id": self.contact_id,
            "type": self.type,
            "remoteid_id": self.remoteid_id,
            "rf_sources": list(self.rf_sources),
            "video_sources": list(self.video_sources),
            "first_seen_ms": self.first_seen_ms,
            "last_seen_ms": self.last_seen_ms,
            "threat_score": self.threat_score,
        }


class FusionEngine:
    def __init__(self, ttl_s: float = 20.0) -> None:
        self._ttl_ms = int(ttl_s * 1000)
        self._contacts: Dict[str, FusedContact] = {}
        self._last_update_ms: Optional[int] = None
        self._last_error: Optional[str] = None

    def _calc_threat(self, contact: FusedContact) -> float:
        return float(1 + len(contact.rf_sources) + len(contact.video_sources))

    def _get_remoteid_key(self, data: Dict[str, Any]) -> Optional[str]:
        rid = data.get("basic_id") or data.get("remoteid_id")
        if rid:
            return str(rid)
        contact_id = data.get("contact_id")
        if isinstance(contact_id, str) and contact_id.startswith("rid:"):
            return contact_id.split("rid:", 1)[1]
        return None

    def _choose_recent_contact(self, now_ms: int) -> Optional[FusedContact]:
        if not self._contacts:
            return None
        contact = max(self._contacts.values(), key=lambda c: c.last_seen_ms)
        if now_ms - contact.last_seen_ms <= VIDEO_MATCH_WINDOW_MS:
            return contact
        return None

    def _handle_remoteid(self, event_type: str, data: Dict[str, Any], now_ms: int) -> List[Tuple[str, Dict[str, Any]]]:
        events: List[Tuple[str, Dict[str, Any]]] = []
        rid = self._get_remoteid_key(data)
        if not rid:
            return events
        key = rid
        contact = self._contacts.get(key)
        if event_type == "CONTACT_LOST":
            if contact:
                del self._contacts[key]
                events.append(("CONTACT_LOST", contact.to_dict()))
            return events

        if contact is None:
            contact = FusedContact(
                contact_id=f"fusion:{rid}",
                type="remoteid",
                remoteid_id=rid,
                rf_sources=[],
                video_sources=[],
                first_seen_ms=now_ms,
                last_seen_ms=now_ms,
                threat_score=1.0,
            )
            self._contacts[key] = contact
            events.append(("CONTACT_NEW", contact.to_dict()))
        else:
            contact.last_seen_ms = now_ms
            contact.threat_score = self._calc_threat(contact)
            events.append(("CONTACT_UPDATE", contact.to_dict()))
        return events

    def _handle_esp32(self, now_ms: int) -> List[Tuple[str, Dict[str, Any]]]:
        events: List[Tuple[str, Dict[str, Any]]] = []
        contact = self._choose_recent_contact(now_ms)
        if not contact:
            return events
        if "esp32" not in contact.video_sources:
            contact.video_sources.append("esp32")
        contact.last_seen_ms = now_ms
        contact.threat_score = self._calc_threat(contact)
        events.append(("CONTACT_UPDATE", contact.to_dict()))
        return events

    def _handle_antsdr(self, event_type: str, data: Dict[str, Any], now_ms: int) -> List[Tuple[str, Dict[str, Any]]]:
        events: List[Tuple[str, Dict[str, Any]]] = []
        rid = self._get_remoteid_key(data)
        contact = self._contacts.get(rid) if rid else self._choose_recent_contact(now_ms)
        if not contact:
            return events

        if event_type == "RF_CONTACT_LOST":
            if "antsdr" in contact.rf_sources:
                contact.rf_sources.remove("antsdr")
                contact.threat_score = self._calc_threat(contact)
                events.append(("CONTACT_UPDATE", contact.to_dict()))
            return events

        if "antsdr" not in contact.rf_sources:
            contact.rf_sources.append("antsdr")
        contact.last_seen_ms = now_ms
        contact.threat_score = self._calc_threat(contact)
        events.append(("CONTACT_UPDATE", contact.to_dict()))
        return events

    def process_event(self, event: Dict[str, Any], now: Optional[int] = None) -> List[Tuple[str, Dict[str, Any]]]:
        now_ms = now if now is not None else now_ms()
        event_type = event.get("type")
        source = event.get("source")
        data = event.get("data") or {}
        if source == "fusion":
            return []
        events: List[Tuple[str, Dict[str, Any]]] = []
        if source == "remoteid" and event_type in ("CONTACT_NEW", "CONTACT_UPDATE", "CONTACT_LOST"):
            events = self._handle_remoteid(event_type, data, now_ms)
        elif source == "esp32" and event_type == "TELEMETRY_UPDATE":
            events = self._handle_esp32(now_ms)
        elif source == "antsdr" and event_type in (
            "RF_CONTACT_NEW",
            "RF_CONTACT_UPDATE",
            "RF_CONTACT_LOST",
        ):
            events = self._handle_antsdr(event_type, data, now_ms)

        self._last_update_ms = now_ms
        return events

    def expire(self, now: Optional[int] = None) -> List[Tuple[str, Dict[str, Any]]]:
        now_ms_val = now if now is not None else now_ms()
        events: List[Tuple[str, Dict[str, Any]]] = []
        for key in list(self._contacts.keys()):
            contact = self._contacts[key]
            if now_ms_val - contact.last_seen_ms > self._ttl_ms:
                events.append(("CONTACT_LOST", contact.to_dict()))
                del self._contacts[key]
        if events:
            self._last_update_ms = now_ms_val
        return events

    def contacts_snapshot(self) -> List[Dict[str, Any]]:
        return [c.to_dict() for c in self._contacts.values()]

    def status(self, now: Optional[int] = None) -> FusionStatus:
        now_ms_val = now if now is not None else now_ms()
        self._last_update_ms = now_ms_val
        return FusionStatus(
            ok=True,
            last_update_ms=self._last_update_ms,
            last_error=self._last_error,
            active_contacts=len(self._contacts),
        )

    def health(self, now: Optional[int] = None) -> FusionHealth:
        now_ms_val = now if now is not None else now_ms()
        self._last_update_ms = now_ms_val
        return FusionHealth(
            ok=True,
            last_update_ms=self._last_update_ms,
            last_error=self._last_error,
            active_contacts=len(self._contacts),
        )
