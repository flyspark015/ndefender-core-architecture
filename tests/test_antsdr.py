from app.modules.antsdr import AntsdrController


class FakeAdiModule:
    class ad9364:  # noqa: N801 - match adi API
        def __init__(self, uri):  # noqa: ARG002
            pass


class FakeAdiFailModule:
    class ad9364:  # noqa: N801 - match adi API
        def __init__(self, uri):  # noqa: ARG002
            raise RuntimeError("init failed")


def _controller(on_event=None):
    return AntsdrController(
        uri="ip:192.168.10.2",
        enabled=True,
        sample_rate_hz=2_000_000,
        rf_bw_hz=2_000_000,
        sweep_plan="VTX_58",
        step_hz=2_000_000,
        on_event=on_event,
    )


def test_antsdr_lib_missing(monkeypatch):
    def _missing():
        raise ImportError("missing")

    monkeypatch.setattr("app.modules.antsdr._import_adi", _missing)
    controller = _controller()
    status, health = controller.poll()
    assert status.ok is False
    assert status.last_error == "ANTSDR_LIB_MISSING"
    assert status.last_update_ms is None
    assert health.ok is False
    assert health.last_error == "ANTSDR_LIB_MISSING"
    assert health.device_present is False
    assert health.driver_ok is False


def test_antsdr_init_failed(monkeypatch):
    monkeypatch.setattr("app.modules.antsdr._import_adi", lambda: FakeAdiFailModule())
    controller = _controller()
    status, health = controller.poll()
    assert status.ok is False
    assert status.last_error == "ANTSDR_INIT_FAILED"
    assert status.last_update_ms is None
    assert health.ok is False
    assert health.last_error == "ANTSDR_INIT_FAILED"
    assert health.device_present is False
    assert health.driver_ok is False


def test_antsdr_init_success(monkeypatch):
    monkeypatch.setattr("app.modules.antsdr._import_adi", lambda: FakeAdiModule())
    controller = _controller()
    status, health = controller.poll()
    assert status.ok is True
    assert status.last_error is None
    assert isinstance(status.last_update_ms, int)
    assert status.last_update_ms >= 1_600_000_000_000
    assert health.ok is True
    assert health.last_error is None
    assert health.device_present is True
    assert health.driver_ok is True


def test_antsdr_start_stop(monkeypatch):
    monkeypatch.setattr("app.modules.antsdr._import_adi", lambda: FakeAdiModule())
    controller = _controller()
    controller._scan_loop = lambda: None  # type: ignore[assignment]
    ok, err = controller.start_scan()
    assert ok is True
    assert err is None
    assert controller._stream_active is True
    controller.stop_scan()
    assert controller._stream_active is False


def test_antsdr_contact_events():
    events = []

    def _on_event(event_type, payload):
        events.append((event_type, payload))

    controller = _controller(on_event=_on_event)
    controller._process_contact(5_800_000_000, [1 + 0j], 1000)
    controller._process_contact(5_800_000_000, [1 + 0j], 2000)
    controller._expire_contacts(20_000)

    event_types = [event[0] for event in events]
    assert "RF_CONTACT_NEW" in event_types
    assert "RF_CONTACT_UPDATE" in event_types
    assert "RF_CONTACT_LOST" in event_types
