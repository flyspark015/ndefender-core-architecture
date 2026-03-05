from app.modules.antsdr import AntsdrReader


class FakeAdiModule:
    class ad9364:  # noqa: N801 - match adi API
        def __init__(self, uri):  # noqa: ARG002
            pass


class FakeAdiFailModule:
    class ad9364:  # noqa: N801 - match adi API
        def __init__(self, uri):  # noqa: ARG002
            raise RuntimeError("init failed")


def test_antsdr_lib_missing(monkeypatch):
    def _missing():
        raise ImportError("missing")

    monkeypatch.setattr("app.modules.antsdr._import_adi", _missing)
    reader = AntsdrReader(uri="ip:192.168.10.2")
    status, health = reader.poll()
    assert status.ok is False
    assert status.last_error == "ANTSDR_LIB_MISSING"
    assert status.last_update_ms is None
    assert health.ok is False
    assert health.last_error == "ANTSDR_LIB_MISSING"
    assert health.device_present is False
    assert health.driver_ok is False


def test_antsdr_init_failed(monkeypatch):
    monkeypatch.setattr("app.modules.antsdr._import_adi", lambda: FakeAdiFailModule())
    reader = AntsdrReader(uri="ip:192.168.10.2")
    status, health = reader.poll()
    assert status.ok is False
    assert status.last_error == "ANTSDR_INIT_FAILED"
    assert status.last_update_ms is None
    assert health.ok is False
    assert health.last_error == "ANTSDR_INIT_FAILED"
    assert health.device_present is False
    assert health.driver_ok is False


def test_antsdr_init_success(monkeypatch):
    monkeypatch.setattr("app.modules.antsdr._import_adi", lambda: FakeAdiModule())
    reader = AntsdrReader(uri="ip:192.168.10.2")
    status, health = reader.poll()
    assert status.ok is True
    assert status.last_error is None
    assert isinstance(status.last_update_ms, int)
    assert status.last_update_ms >= 1_600_000_000_000
    assert health.ok is True
    assert health.last_error is None
    assert health.device_present is True
    assert health.driver_ok is True
