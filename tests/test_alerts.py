from app.modules.alerts import AlertsEngine


def test_alert_new_update_lost():
    engine = AlertsEngine()
    base = {
        "contact_id": "fusion:drone123",
        "remoteid_id": "drone123",
        "video_sources": [],
        "rf_sources": [],
    }

    events = engine.process_event(
        {"type": "CONTACT_NEW", "source": "fusion", "data": base}, now=1_700_000_000_000
    )
    assert events
    event_type, payload = events[0]
    assert event_type == "ALERT_NEW"
    assert payload["threat_score"] == 2
    assert payload["severity"] == "medium"

    updated = dict(base)
    updated["video_sources"] = ["esp32"]
    events = engine.process_event(
        {"type": "CONTACT_UPDATE", "source": "fusion", "data": updated}, now=1_700_000_000_500
    )
    assert events
    event_type, payload = events[0]
    assert event_type == "ALERT_UPDATE"
    assert payload["threat_score"] == 3
    assert payload["severity"] == "high"

    events = engine.process_event(
        {"type": "CONTACT_LOST", "source": "fusion", "data": updated}, now=1_700_000_001_000
    )
    assert events == []
    assert engine.alerts_snapshot() == []
