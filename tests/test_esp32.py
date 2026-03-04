import serial
from fastapi.testclient import TestClient

from app.main import app
from app.modules.esp32 import Esp32SerialReader

client = TestClient(app)


def test_esp32_serial_missing(monkeypatch):
    def _raise(*_args, **_kwargs):
        raise serial.SerialException("missing")

    monkeypatch.setattr(serial, "Serial", _raise)
    reader = Esp32SerialReader("/dev/ttyFAKE0", 115200, 0.1, 0.1)
    assert reader._open_serial() is False
    status, health = reader.not_connected()
    assert status.last_error == "ESP32_SERIAL_NOT_CONNECTED"
    assert health.last_error == "ESP32_SERIAL_NOT_CONNECTED"


def test_auto_port_detect_prefers_by_id(monkeypatch):
    def fake_glob(pattern):
        if pattern == "/dev/serial/by-id/*":
            return ["/dev/serial/by-id/usb-CH340-esp32"]
        if pattern == "/dev/ttyACM*":
            return ["/dev/ttyACM0"]
        if pattern == "/dev/ttyUSB*":
            return ["/dev/ttyUSB0"]
        return []

    chosen = {}

    def fake_serial(port, baud, timeout):  # noqa: ARG001
        chosen["port"] = port
        raise serial.SerialException("missing")

    monkeypatch.setattr("app.modules.esp32.glob.glob", fake_glob)
    monkeypatch.setattr(serial, "Serial", fake_serial)

    reader = Esp32SerialReader("auto", 115200, 0.1, 0.1)
    assert reader._open_serial() is False
    assert chosen["port"] == "/dev/serial/by-id/usb-CH340-esp32"


def test_command_ack_when_serial_missing():
    with client.websocket_connect("/api/v1/ws") as ws:
        hello = ws.receive_json()
        assert hello["type"] == "HELLO"

        resp = client.post(
            "/api/v1/commands",
            json={"command": "video/select", "payload": {"sel": 1}, "confirm": False},
        )
        assert resp.status_code == 409
        assert resp.json() == {
            "detail": "precondition_failed",
            "code": "ESP32_SERIAL_NOT_CONNECTED",
        }

        ack = ws.receive_json()
        assert ack["type"] == "COMMAND_ACK"
        assert ack["data"]["command"] == "video/select"
        assert ack["data"]["ok"] is False
        assert ack["data"]["code"] == "ESP32_SERIAL_NOT_CONNECTED"
        assert isinstance(ack["data"]["timestamp_ms"], int)
