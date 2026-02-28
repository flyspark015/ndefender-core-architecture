from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

THERMAL_PATH = Path("/sys/class/thermal/thermal_zone0/temp")

STATUS_FIELDS = {
    "ups": {
        "ok",
        "last_update_ms",
        "battery_percent",
        "input_voltage_v",
        "output_voltage_v",
        "load_percent",
        "temperature_c",
        "runtime_s",
        "on_battery",
    },
    "os": {
        "ok",
        "last_update_ms",
        "cpu_temp_c",
        "cpu_percent",
        "mem_used_mb",
        "mem_total_mb",
        "disk_used_mb",
        "disk_total_mb",
        "uptime_s",
    },
    "esp32": {
        "ok",
        "last_update_ms",
        "connected",
        "firmware_version",
        "rssi_dbm",
        "supply_voltage_v",
        "temperature_c",
    },
    "antsdr": {
        "ok",
        "last_update_ms",
        "center_freq_hz",
        "sample_rate_hz",
        "gain_db",
        "rf_power_dbm",
        "stream_active",
    },
    "remoteid": {
        "ok",
        "last_update_ms",
        "contacts_count",
        "last_contact_ms",
        "latitude",
        "longitude",
    },
    "video": {
        "ok",
        "last_update_ms",
        "stream_ok",
        "fps",
        "bitrate_kbps",
        "frame_width",
        "frame_height",
    },
}

HEALTH_FIELDS = {
    "ups": {"ok", "last_update_ms", "comms_ok", "model", "serial", "firmware_version"},
    "os": {"ok", "last_update_ms", "hostname", "os_version", "kernel_version", "time_sync_ok"},
    "esp32": {"ok", "last_update_ms", "comms_ok", "last_error"},
    "antsdr": {"ok", "last_update_ms", "device_present", "driver_ok"},
    "remoteid": {"ok", "last_update_ms", "receiver_ok", "gps_ok"},
    "video": {"ok", "last_update_ms", "encoder_ok", "camera_ok"},
}

SYSTEM_FIELDS = {
    "timestamp_ms",
    "cpu_temp_c",
    "cpu_percent",
    "mem_used_mb",
    "mem_total_mb",
    "disk_used_mb",
    "disk_total_mb",
    "uptime_s",
}


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _assert_module_fields(modules, fields_map):
    for module_name, required in fields_map.items():
        assert module_name in modules
        module_obj = modules[module_name]
        assert required.issubset(set(module_obj.keys()))


def _assert_os_numbers(os_obj):
    for key in [
        "cpu_percent",
        "mem_used_mb",
        "mem_total_mb",
        "disk_used_mb",
        "disk_total_mb",
        "uptime_s",
    ]:
        assert _is_number(os_obj[key])

    if THERMAL_PATH.exists():
        assert _is_number(os_obj["cpu_temp_c"])
    else:
        assert os_obj["cpu_temp_c"] is None or _is_number(os_obj["cpu_temp_c"])


def test_status_shape():
    r = client.get("/api/v1/status")
    assert r.status_code == 200
    data = r.json()
    assert set(["timestamp_ms", "overall_ok", "system", "modules"]).issubset(data.keys())
    _assert_module_fields(data["modules"], STATUS_FIELDS)

    system = data["system"]
    assert SYSTEM_FIELDS.issubset(set(system.keys()))
    _assert_os_numbers(system)

    os_module = data["modules"]["os"]
    _assert_os_numbers(os_module)


def test_health_shape():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert set(["timestamp_ms", "overall_ok", "modules"]).issubset(data.keys())
    _assert_module_fields(data["modules"], HEALTH_FIELDS)

    os_health = data["modules"]["os"]
    assert isinstance(os_health["hostname"], str)
    assert isinstance(os_health["os_version"], str)
    assert isinstance(os_health["kernel_version"], str)
    assert os_health["time_sync_ok"] in (True, False, None)


def test_ws_hello():
    with client.websocket_connect("/api/v1/ws") as ws:
        data = ws.receive_json()
        assert set(["type", "timestamp_ms", "source", "data"]).issubset(data.keys())
        assert data["type"] == "HELLO"
