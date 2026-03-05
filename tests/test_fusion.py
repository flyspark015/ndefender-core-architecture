from app.modules.fusion import FusionEngine


def test_remoteid_plus_esp32_merge():
    engine = FusionEngine(ttl_s=20.0)
    now = 1_700_000_000_000
    rid_event = {
        "type": "CONTACT_NEW",
        "source": "remoteid",
        "data": {"basic_id": "drone123", "contact_id": "rid:drone123"},
    }
    events = engine.process_event(rid_event, now=now)
    assert events and events[0][0] == "CONTACT_NEW"

    esp_event = {"type": "TELEMETRY_UPDATE", "source": "esp32", "data": {"sel": 1}}
    events2 = engine.process_event(esp_event, now=now + 1000)
    assert events2 and events2[0][0] == "CONTACT_UPDATE"
    contact = events2[0][1]
    assert "esp32" in contact["video_sources"]


def test_remoteid_plus_antsdr_merge():
    engine = FusionEngine(ttl_s=20.0)
    now = 1_700_000_000_000
    rid_event = {
        "type": "CONTACT_NEW",
        "source": "remoteid",
        "data": {"basic_id": "drone123", "contact_id": "rid:drone123"},
    }
    engine.process_event(rid_event, now=now)

    rf_event = {
        "type": "RF_CONTACT_NEW",
        "source": "antsdr",
        "data": {"basic_id": "drone123"},
    }
    events = engine.process_event(rf_event, now=now + 500)
    assert events and events[0][0] == "CONTACT_UPDATE"
    contact = events[0][1]
    assert "antsdr" in contact["rf_sources"]


def test_ttl_expiry():
    engine = FusionEngine(ttl_s=20.0)
    now = 1_700_000_000_000
    rid_event = {
        "type": "CONTACT_NEW",
        "source": "remoteid",
        "data": {"basic_id": "drone123", "contact_id": "rid:drone123"},
    }
    engine.process_event(rid_event, now=now)
    lost = engine.expire(now=now + 21_000)
    assert lost and lost[0][0] == "CONTACT_LOST"
