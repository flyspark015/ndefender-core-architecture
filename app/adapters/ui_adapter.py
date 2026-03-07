from __future__ import annotations

from typing import Any, Dict, List


def _ensure_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _ensure_str(value: Any, default: str | None = None) -> str | None:
    if value is None:
        return default
    return str(value)


def _normalize_contact(contact: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "contact_id": contact.get("contact_id"),
        "type": contact.get("type"),
        "remoteid_id": contact.get("remoteid_id"),
        "rf_sources": _ensure_list(contact.get("rf_sources")),
        "video_sources": _ensure_list(contact.get("video_sources")),
        "first_seen_ms": contact.get("first_seen_ms"),
        "last_seen_ms": contact.get("last_seen_ms"),
        "threat_score": contact.get("threat_score"),
    }


def _normalize_alert(alert: Dict[str, Any]) -> Dict[str, Any]:
    severity = alert.get("severity")
    if isinstance(severity, str):
        severity = severity.lower()
    return {
        "alert_id": alert.get("alert_id"),
        "contact_id": alert.get("contact_id"),
        "threat_score": alert.get("threat_score"),
        "severity": severity or "low",
        "first_seen_ms": alert.get("first_seen_ms"),
        "last_seen_ms": alert.get("last_seen_ms"),
        "state": _ensure_str(alert.get("state"), default="active"),
    }


def normalize_contacts(contacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = [_normalize_contact(c) for c in contacts or []]
    return sorted(normalized, key=lambda c: c.get("last_seen_ms") or 0, reverse=True)


def normalize_alerts(alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = [_normalize_alert(a) for a in alerts or []]
    return sorted(normalized, key=lambda a: a.get("last_seen_ms") or 0, reverse=True)


def normalize_status(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    modules = snapshot.get("modules") or {}
    if hasattr(modules, "model_dump"):
        modules = modules.model_dump()
    ups = modules.get("ups") or {}
    if ups.get("ok") is False and ups.get("cell_voltages_v") is None:
        ups["cell_voltages_v"] = []
    modules["ups"] = ups
    snapshot["modules"] = modules
    return snapshot


def normalize_health(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return snapshot


def normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    data = event.get("data") or {}
    event_type = event.get("type")

    if event_type in ("CONTACT_NEW", "CONTACT_UPDATE", "CONTACT_LOST"):
        data = _normalize_contact(data)
    elif event_type in ("ALERT_NEW", "ALERT_UPDATE"):
        data = _normalize_alert(data)
    elif event_type == "TELEMETRY_UPDATE":
        if "timestamp_ms" not in data:
            data["timestamp_ms"] = event.get("timestamp_ms")

    event["data"] = data
    return event
