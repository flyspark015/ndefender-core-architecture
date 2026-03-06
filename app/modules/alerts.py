from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from app.models import AlertsHealth, AlertsStatus, now_ms


@dataclass
class Alert:
    alert_id: str
    contact_id: str
    threat_score: int
    severity: str
    first_seen_ms: int
    last_seen_ms: int
    state: str = "active"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "contact_id": self.contact_id,
            "threat_score": self.threat_score,
            "severity": self.severity,
            "first_seen_ms": self.first_seen_ms,
            "last_seen_ms": self.last_seen_ms,
            "state": self.state,
        }


class AlertsEngine:
    def __init__(self) -> None:
        self._alerts: Dict[str, Alert] = {}
        self._last_update_ms: Optional[int] = None
        self._last_error: Optional[str] = None

    def _score(self, data: Dict[str, Any]) -> int:
        score = 1
        if data.get("remoteid_id"):
            score += 1
        if data.get("video_sources"):
            score += 1
        if data.get("rf_sources"):
            score += 1
        return score

    def _severity(self, score: int) -> str:
        if score >= 3:
            return "high"
        if score == 2:
            return "medium"
        return "low"

    def process_event(self, event: Dict[str, Any], now: Optional[int] = None) -> List[Tuple[str, Dict[str, Any]]]:
        now_ms_val = now if now is not None else now_ms()
        event_type = event.get("type")
        source = event.get("source")
        data = event.get("data") or {}
        if source != "fusion" or event_type not in ("CONTACT_NEW", "CONTACT_UPDATE", "CONTACT_LOST"):
            return []

        contact_id = data.get("contact_id")
        if not contact_id:
            return []
        contact_id = str(contact_id)
        alert_id = f"alert:{contact_id}"

        if event_type == "CONTACT_LOST":
            if alert_id in self._alerts:
                del self._alerts[alert_id]
                self._last_update_ms = now_ms_val
            return []

        score = self._score(data)
        severity = self._severity(score)
        alert = self._alerts.get(alert_id)
        events: List[Tuple[str, Dict[str, Any]]] = []
        if alert is None:
            alert = Alert(
                alert_id=alert_id,
                contact_id=contact_id,
                threat_score=score,
                severity=severity,
                first_seen_ms=now_ms_val,
                last_seen_ms=now_ms_val,
            )
            self._alerts[alert_id] = alert
            events.append(("ALERT_NEW", alert.to_dict()))
        else:
            alert.threat_score = score
            alert.severity = severity
            alert.last_seen_ms = now_ms_val
            events.append(("ALERT_UPDATE", alert.to_dict()))

        self._last_update_ms = now_ms_val
        return events

    def alerts_snapshot(self) -> List[Dict[str, Any]]:
        return [alert.to_dict() for alert in self._alerts.values()]

    def status(self, now: Optional[int] = None) -> AlertsStatus:
        now_ms_val = now if now is not None else now_ms()
        self._last_update_ms = now_ms_val
        return AlertsStatus(
            ok=True,
            active_alerts=len(self._alerts),
            last_update_ms=self._last_update_ms,
            last_error=self._last_error,
        )

    def health(self, now: Optional[int] = None) -> AlertsHealth:
        now_ms_val = now if now is not None else now_ms()
        self._last_update_ms = now_ms_val
        return AlertsHealth(
            ok=True,
            active_alerts=len(self._alerts),
            last_update_ms=self._last_update_ms,
            last_error=self._last_error,
        )
