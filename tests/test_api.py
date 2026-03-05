from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

THERMAL_PATH = Path("/sys/class/thermal/thermal_zone0/temp")

STATUS_FIELDS = {
    "ups": {
        "ok",
        "last_update_ms",
        "last_error",
        "battery_percent",
        "battery_voltage_v",
        "battery_current_a",
        "current_a",
        "remaining_capacity_mah",
        "runtime_s",
        "cell_voltages_v",
        "vbus_voltage_v",
        "vbus_current_a",
        "vbus_power_w",
        "state",
        "input_voltage_v",
        "output_voltage_v",
        "load_percent",
        "temperature_c",
        "on_battery",
    },
    "os": {
        "ok",
        "last_update_ms",
        "last_error",
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
        "last_error",
        "connected",
        "firmware_version",
        "device_uptime_ms",
        "seq",
        "rssi_dbm",
        "supply_voltage_v",
        "temperature_c",
    },
    "antsdr": {
        "ok",
        "last_update_ms",
        "last_error",
        "center_freq_hz",
        "sample_rate_hz",
        "gain_db",
        "rf_power_dbm",
        "stream_active",
    },
    "remoteid": {
        "ok",
        "last_update_ms",
        "last_error",
        "active_contacts",
    },
    "video": {
        "ok",
        "last_update_ms",
        "last_error",
        "stream_ok",
        "fps",
        "bitrate_kbps",
        "frame_width",
        "frame_height",
    },
}

HEALTH_FIELDS = {
    "ups": {"ok", "last_update_ms", "last_error", "comms_ok", "model", "serial", "firmware_version"},
    "os": {"ok", "last_update_ms", "last_error", "hostname", "os_version", "kernel_version", "time_sync_ok"},
    "esp32": {"ok", "last_update_ms", "last_error", "comms_ok"},
    "antsdr": {"ok", "last_update_ms", "last_error", "device_present", "driver_ok"},
    "remoteid": {"ok", "last_update_ms", "last_error", "input_stream_ok"},
    "video": {"ok", "last_update_ms", "last_error", "encoder_ok", "camera_ok"},
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


def _assert_placeholder(module_obj):
    assert module_obj["ok"] is False
    assert module_obj["last_error"] == "not_implemented"


def _assert_esp32_missing(module_obj):
    assert module_obj["ok"] is False
    assert module_obj["connected"] is False
    assert module_obj["last_error"] == "ESP32_SERIAL_NOT_CONNECTED"
    assert module_obj["device_uptime_ms"] is None
    assert module_obj["seq"] is None


def _assert_antsdr_missing(module_obj):
    assert module_obj["ok"] is False
    assert module_obj["last_update_ms"] is None
    assert module_obj["last_error"] in (
        "ANTSDR_NOT_CONNECTED",
        "ANTSDR_LIB_MISSING",
        "ANTSDR_INIT_FAILED",
    )


def _assert_remoteid_state(module_obj):
    if module_obj["ok"] is True:
        assert isinstance(module_obj["last_update_ms"], int)
        assert module_obj["last_update_ms"] >= 1_600_000_000_000
        assert module_obj["last_error"] is None
        assert isinstance(module_obj["active_contacts"], int)
        return
    assert module_obj["ok"] is False
    assert module_obj["last_update_ms"] is None
    assert module_obj["last_error"] in (
        "REMOTEID_FILE_MISSING",
        "REMOTEID_NO_DATA",
        "REMOTEID_PARSE_ERROR",
        "REMOTEID_READ_FAILED",
    )


def _assert_ups_values(ups_obj):
    assert ups_obj["ok"] is True
    assert ups_obj["last_error"] is None
    assert _is_number(ups_obj["battery_percent"])
    assert _is_number(ups_obj["battery_voltage_v"])
    assert ups_obj["battery_voltage_v"] > 0
    assert _is_number(ups_obj["input_voltage_v"]) or _is_number(ups_obj["output_voltage_v"])
    assert isinstance(ups_obj["cell_voltages_v"], list)
    assert len(ups_obj["cell_voltages_v"]) == 4
    assert all(_is_number(v) and v > 0 for v in ups_obj["cell_voltages_v"])


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
    assert os_module["ok"] is True
    assert os_module["last_error"] is None

    _assert_ups_values(data["modules"]["ups"])

    _assert_esp32_missing(data["modules"]["esp32"])

    _assert_antsdr_missing(data["modules"]["antsdr"])

    _assert_remoteid_state(data["modules"]["remoteid"])

    for module_name in ["video"]:
        _assert_placeholder(data["modules"][module_name])


def test_health_shape():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert set(["timestamp_ms", "overall_ok", "modules"]).issubset(data.keys())
    _assert_module_fields(data["modules"], HEALTH_FIELDS)

    os_health = data["modules"]["os"]
    assert os_health["ok"] is True
    assert os_health["last_error"] is None
    assert isinstance(os_health["hostname"], str)
    assert isinstance(os_health["os_version"], str)
    assert isinstance(os_health["kernel_version"], str)
    assert os_health["time_sync_ok"] in (True, False, None)

    ups_health = data["modules"]["ups"]
    assert ups_health["ok"] is True
    assert ups_health["last_error"] is None
    assert ups_health["comms_ok"] is True
    assert ups_health["model"] == "Waveshare UPS HAT (E)"

    esp32_health = data["modules"]["esp32"]
    assert esp32_health["ok"] is False
    assert esp32_health["comms_ok"] is False
    assert esp32_health["last_error"] == "ESP32_SERIAL_NOT_CONNECTED"

    antsdr_health = data["modules"]["antsdr"]
    assert antsdr_health["ok"] is False
    assert antsdr_health["last_error"] in (
        "ANTSDR_NOT_CONNECTED",
        "ANTSDR_LIB_MISSING",
        "ANTSDR_INIT_FAILED",
    )
    assert antsdr_health["device_present"] is False
    assert antsdr_health["driver_ok"] is False

    remoteid_health = data["modules"]["remoteid"]
    if remoteid_health["ok"] is True:
        assert isinstance(remoteid_health["last_update_ms"], int)
        assert remoteid_health["last_update_ms"] >= 1_600_000_000_000
        assert remoteid_health["last_error"] is None
        assert remoteid_health["input_stream_ok"] is True
    else:
        assert remoteid_health["ok"] is False
        assert remoteid_health["last_error"] in (
            "REMOTEID_FILE_MISSING",
            "REMOTEID_NO_DATA",
            "REMOTEID_PARSE_ERROR",
            "REMOTEID_READ_FAILED",
        )
        assert remoteid_health["input_stream_ok"] in (True, False, None)

    for module_name in ["video"]:
        _assert_placeholder(data["modules"][module_name])


def test_ws_hello():
    with client.websocket_connect("/api/v1/ws") as ws:
        data = ws.receive_json()
        assert set(["type", "timestamp_ms", "source", "data"]).issubset(data.keys())
        assert data["type"] == "HELLO"
