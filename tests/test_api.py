from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


REQUIRED_MODULES = {"ups", "os", "esp32", "antsdr", "remoteid", "video"}


def test_status_shape():
    r = client.get("/api/v1/status")
    assert r.status_code == 200
    data = r.json()
    assert set(["timestamp_ms", "overall_ok", "system", "modules"]).issubset(data.keys())
    assert REQUIRED_MODULES.issubset(set(data["modules"].keys()))


def test_health_shape():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert set(["timestamp_ms", "overall_ok", "modules"]).issubset(data.keys())
    assert REQUIRED_MODULES.issubset(set(data["modules"].keys()))


def test_ws_hello():
    with client.websocket_connect("/api/v1/ws") as ws:
        data = ws.receive_json()
        assert set(["type", "timestamp_ms", "source", "data"]).issubset(data.keys())
        assert data["type"] == "HELLO"
