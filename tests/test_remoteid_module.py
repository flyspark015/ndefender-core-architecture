from app.modules.remoteid import RemoteIdIngestor


def test_contact_new_and_update():
    ingestor = RemoteIdIngestor(path="dummy")
    now = 1_700_000_000_000
    record = {
        "basic_id": "drone123",
        "lat": 22.303,
        "lon": 70.802,
        "alt": 120,
        "speed": 15,
        "heading": 180,
        "timestamp": 1700000000000,
    }

    event = ingestor.process_record(record, now)
    assert event is not None
    event_type, contact = event
    assert event_type == "CONTACT_NEW"
    assert contact["basic_id"] == "drone123"
    assert contact["first_seen_ms"] == now

    # changed frame should trigger update
    record2 = dict(record)
    record2["lat"] = 22.304
    event2 = ingestor.process_record(record2, now + 1000)
    assert event2 is not None
    event_type2, contact2 = event2
    assert event_type2 == "CONTACT_UPDATE"
    assert contact2["lat"] == 22.304


def test_contact_lost_ttl():
    ingestor = RemoteIdIngestor(path="dummy", ttl_s=15.0)
    now = 1_700_000_000_000
    record = {
        "basic_id": "drone123",
        "lat": 22.303,
        "lon": 70.802,
        "alt": 120,
        "speed": 15,
        "heading": 180,
        "timestamp": 1700000000000,
    }

    ingestor.process_record(record, now)
    lost = ingestor.expire(now + 16_000)
    assert len(lost) == 1
    assert lost[0]["basic_id"] == "drone123"
