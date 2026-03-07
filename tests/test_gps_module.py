import socket

from app.modules.gps import GpsdReader


def test_gpsd_unavailable(monkeypatch):
    def _fail(*_args, **_kwargs):
        raise OSError("no gpsd")

    monkeypatch.setattr(socket, "create_connection", _fail)
    reader = GpsdReader(host="127.0.0.1", port=2947)
    status, health = reader.poll()
    assert status.ok is False
    assert status.last_error == "GPSD_UNAVAILABLE"
    assert health.ok is False
    assert health.last_error == "GPSD_UNAVAILABLE"
