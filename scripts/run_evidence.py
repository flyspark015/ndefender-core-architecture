from __future__ import annotations

import asyncio
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple

import httpx
import websockets

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import HOST, PORT  # noqa: E402

BASE_URL = f"http://{HOST}:{PORT}"
WS_URL = f"ws://{HOST}:{PORT}/api/v1/ws"
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


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_keys(obj: Dict[str, Any], keys: List[str]) -> Tuple[bool, str]:
    missing = [k for k in keys if k not in obj]
    if missing:
        return False, f"missing_keys={missing}"
    return True, "ok"


def _check_module_fields(modules: Dict[str, Any], fields_map: Dict[str, set]) -> Tuple[bool, str]:
    for module_name, required in fields_map.items():
        if module_name not in modules:
            return False, f"missing_modules={[module_name]}"
        module_obj = modules.get(module_name, {})
        missing = [k for k in required if k not in module_obj]
        if missing:
            return False, f"missing_fields={module_name}:{missing}"
    return True, "ok"


def _check_os_populated(status_obj: Dict[str, Any]) -> Tuple[bool, str]:
    system = status_obj.get("system", {})
    missing = [k for k in SYSTEM_FIELDS if k not in system]
    if missing:
        return False, f"missing_system_fields={missing}"

    for key in [
        "cpu_percent",
        "mem_used_mb",
        "mem_total_mb",
        "disk_used_mb",
        "disk_total_mb",
        "uptime_s",
    ]:
        if not _is_number(system.get(key)):
            return False, f"system_field_not_number={key}"

    if THERMAL_PATH.exists():
        if not _is_number(system.get("cpu_temp_c")):
            return False, "system_cpu_temp_not_number"

    os_module = status_obj.get("modules", {}).get("os", {})
    if os_module.get("ok") is not True:
        return False, "os_ok_not_true"
    if os_module.get("last_error") is not None:
        return False, "os_last_error_not_null"
    for key in [
        "cpu_percent",
        "mem_used_mb",
        "mem_total_mb",
        "disk_used_mb",
        "disk_total_mb",
        "uptime_s",
    ]:
        if not _is_number(os_module.get(key)):
            return False, f"os_field_not_number={key}"

    if THERMAL_PATH.exists():
        if not _is_number(os_module.get("cpu_temp_c")):
            return False, "os_cpu_temp_not_number"

    return True, "ok"


def _check_placeholders(modules: Dict[str, Any]) -> Tuple[bool, str]:
    for module_name in ["video"]:
        mod = modules.get(module_name, {})
        if mod.get("ok") is not False:
            return False, f"{module_name}_ok_not_false"
        if mod.get("last_error") != "not_implemented":
            return False, f"{module_name}_last_error_not_not_implemented"
    return True, "ok"


def _check_remoteid_status(status_obj: Dict[str, Any]) -> Tuple[bool, str]:
    rid = status_obj.get("modules", {}).get("remoteid", {})
    if rid.get("ok") is True:
        if rid.get("last_error") is not None:
            return False, "remoteid_last_error_not_null"
        if not isinstance(rid.get("last_update_ms"), int):
            return False, "remoteid_last_update_not_int"
        if rid.get("last_update_ms") < 1_600_000_000_000:
            return False, "remoteid_last_update_not_epoch"
        if not isinstance(rid.get("active_contacts"), int):
            return False, "remoteid_active_contacts_not_int"
        return True, "ok"
    if rid.get("ok") is not False:
        return False, "remoteid_ok_not_false"
    if rid.get("last_update_ms") is not None:
        return False, "remoteid_last_update_not_null"
    if rid.get("last_error") not in (
        "REMOTEID_FILE_MISSING",
        "REMOTEID_NO_DATA",
        "REMOTEID_PARSE_ERROR",
        "REMOTEID_READ_FAILED",
    ):
        return False, "remoteid_last_error_not_expected"
    return True, "ok"


def _check_antsdr_status(status_obj: Dict[str, Any]) -> Tuple[bool, str]:
    antsdr = status_obj.get("modules", {}).get("antsdr", {})
    if antsdr.get("ok") is True:
        if antsdr.get("last_error") is not None:
            return False, "antsdr_last_error_not_null"
        if not isinstance(antsdr.get("last_update_ms"), int):
            return False, "antsdr_last_update_not_int"
        if antsdr.get("last_update_ms") < 1_600_000_000_000:
            return False, "antsdr_last_update_not_epoch"
        return True, "ok"
    if antsdr.get("ok") is not False:
        return False, "antsdr_ok_not_false"
    if antsdr.get("last_update_ms") is not None:
        return False, "antsdr_last_update_not_null"
    if antsdr.get("last_error") not in (
        "ANTSDR_NOT_CONNECTED",
        "ANTSDR_LIB_MISSING",
        "ANTSDR_INIT_FAILED",
    ):
        return False, "antsdr_last_error_not_expected"
    return True, "ok"


def _check_esp32_status(status_obj: Dict[str, Any]) -> Tuple[bool, str]:
    esp32 = status_obj.get("modules", {}).get("esp32", {})
    if esp32.get("ok") is True:
        if esp32.get("connected") is not True:
            return False, "esp32_connected_not_true"
        if esp32.get("last_error") is not None:
            return False, "esp32_last_error_not_null"
        if not isinstance(esp32.get("firmware_version"), str):
            return False, "esp32_fw_not_string"
        if not isinstance(esp32.get("last_update_ms"), int):
            return False, "esp32_last_update_not_int"
        if esp32.get("last_update_ms") < 1_600_000_000_000:
            return False, "esp32_last_update_not_epoch"
        if esp32.get("device_uptime_ms") is not None and not isinstance(
            esp32.get("device_uptime_ms"), int
        ):
            return False, "esp32_device_uptime_not_int"
        if esp32.get("seq") is not None and not isinstance(esp32.get("seq"), int):
            return False, "esp32_seq_not_int"
        return True, "ok"
    if esp32.get("ok") is not False:
        return False, "esp32_ok_not_false"
    if esp32.get("connected") is not False:
        return False, "esp32_connected_not_false"
    if esp32.get("last_error") != "ESP32_SERIAL_NOT_CONNECTED":
        return False, "esp32_last_error_not_expected"
    return True, "ok"


def _check_ups_populated(status_obj: Dict[str, Any]) -> Tuple[bool, str]:
    ups = status_obj.get("modules", {}).get("ups", {})
    if ups.get("ok") is not True:
        last_error = ups.get("last_error") or ""
        if last_error.startswith("UPS_NOT_DETECTED") or last_error.startswith("UPS_READ_FAILED"):
            return True, "ok"
        return False, "ups_missing_no_error"
    if ups.get("last_error") is not None:
        return False, "ups_last_error_not_null"
    if not _is_number(ups.get("battery_percent")):
        return False, "ups_battery_percent_not_number"
    if not _is_number(ups.get("battery_voltage_v")):
        return False, "ups_battery_voltage_not_number"
    if ups.get("battery_voltage_v") is not None and ups.get("battery_voltage_v") <= 0:
        return False, "ups_battery_voltage_not_positive"
    if not (_is_number(ups.get("input_voltage_v")) or _is_number(ups.get("output_voltage_v"))):
        return False, "ups_input_output_missing"
    cells = ups.get("cell_voltages_v")
    if not isinstance(cells, list):
        return False, "ups_cells_not_list"
    if len(cells) != 4:
        return False, "ups_cells_len_not_4"
    if not all(_is_number(v) and v > 0 for v in cells):
        return False, "ups_cells_not_positive"
    return True, "ok"


def _check_os_health(health_obj: Dict[str, Any]) -> Tuple[bool, str]:
    os_module = health_obj.get("modules", {}).get("os", {})
    if os_module.get("ok") is not True:
        return False, "os_health_ok_not_true"
    if os_module.get("last_error") is not None:
        return False, "os_health_last_error_not_null"
    if not isinstance(os_module.get("hostname"), str):
        return False, "os_health_hostname_not_string"
    if not isinstance(os_module.get("os_version"), str):
        return False, "os_health_os_version_not_string"
    if not isinstance(os_module.get("kernel_version"), str):
        return False, "os_health_kernel_version_not_string"
    if os_module.get("time_sync_ok") not in (True, False, None):
        return False, "os_health_time_sync_invalid"
    return True, "ok"


def _check_esp32_health(health_obj: Dict[str, Any]) -> Tuple[bool, str]:
    esp32 = health_obj.get("modules", {}).get("esp32", {})
    if esp32.get("ok") is True:
        if esp32.get("comms_ok") is not True:
            return False, "esp32_health_comms_not_true"
        if esp32.get("last_error") is not None:
            return False, "esp32_health_last_error_not_null"
        if not isinstance(esp32.get("last_update_ms"), int):
            return False, "esp32_health_last_update_not_int"
        if esp32.get("last_update_ms") < 1_600_000_000_000:
            return False, "esp32_health_last_update_not_epoch"
        return True, "ok"
    if esp32.get("ok") is not False:
        return False, "esp32_health_ok_not_false"
    if esp32.get("comms_ok") is not False:
        return False, "esp32_health_comms_not_false"
    if esp32.get("last_error") != "ESP32_SERIAL_NOT_CONNECTED":
        return False, "esp32_health_last_error_not_expected"
    return True, "ok"


def _check_ups_health(health_obj: Dict[str, Any]) -> Tuple[bool, str]:
    ups = health_obj.get("modules", {}).get("ups", {})
    if ups.get("ok") is not True:
        last_error = ups.get("last_error") or ""
        if last_error.startswith("UPS_NOT_DETECTED") or last_error.startswith("UPS_READ_FAILED"):
            return True, "ok"
        return False, "ups_health_missing_no_error"
    if ups.get("last_error") is not None:
        return False, "ups_health_last_error_not_null"
    if ups.get("comms_ok") is not True:
        return False, "ups_health_comms_not_true"
    if ups.get("model") != "Waveshare UPS HAT (E)":
        return False, "ups_health_model_mismatch"
    return True, "ok"


def _check_antsdr_health(health_obj: Dict[str, Any]) -> Tuple[bool, str]:
    antsdr = health_obj.get("modules", {}).get("antsdr", {})
    if antsdr.get("ok") is True:
        if antsdr.get("comms_ok") is not None:
            return False, "antsdr_health_comms_unexpected"
        if antsdr.get("last_error") is not None:
            return False, "antsdr_health_last_error_not_null"
        if not isinstance(antsdr.get("last_update_ms"), int):
            return False, "antsdr_health_last_update_not_int"
        if antsdr.get("last_update_ms") < 1_600_000_000_000:
            return False, "antsdr_health_last_update_not_epoch"
        if antsdr.get("device_present") is not True:
            return False, "antsdr_health_device_present_not_true"
        if antsdr.get("driver_ok") is not True:
            return False, "antsdr_health_driver_ok_not_true"
        return True, "ok"
    if antsdr.get("ok") is not False:
        return False, "antsdr_health_ok_not_false"
    if antsdr.get("last_update_ms") is not None:
        return False, "antsdr_health_last_update_not_null"
    if antsdr.get("last_error") not in (
        "ANTSDR_NOT_CONNECTED",
        "ANTSDR_LIB_MISSING",
        "ANTSDR_INIT_FAILED",
    ):
        return False, "antsdr_health_last_error_not_expected"
    if antsdr.get("device_present") is not False:
        return False, "antsdr_health_device_present_not_false"
    if antsdr.get("driver_ok") is not False:
        return False, "antsdr_health_driver_ok_not_false"
    return True, "ok"


def _check_remoteid_health(health_obj: Dict[str, Any]) -> Tuple[bool, str]:
    rid = health_obj.get("modules", {}).get("remoteid", {})
    if rid.get("ok") is True:
        if rid.get("last_error") is not None:
            return False, "remoteid_health_last_error_not_null"
        if not isinstance(rid.get("last_update_ms"), int):
            return False, "remoteid_health_last_update_not_int"
        if rid.get("last_update_ms") < 1_600_000_000_000:
            return False, "remoteid_health_last_update_not_epoch"
        if rid.get("input_stream_ok") is not True:
            return False, "remoteid_input_stream_not_true"
        return True, "ok"
    if rid.get("ok") is not False:
        return False, "remoteid_health_ok_not_false"
    if rid.get("last_update_ms") is not None:
        return False, "remoteid_health_last_update_not_null"
    if rid.get("last_error") not in (
        "REMOTEID_FILE_MISSING",
        "REMOTEID_NO_DATA",
        "REMOTEID_PARSE_ERROR",
        "REMOTEID_READ_FAILED",
    ):
        return False, "remoteid_health_last_error_not_expected"
    return True, "ok"


async def _ws_hello_check() -> Tuple[bool, str]:
    try:
        async with websockets.connect(WS_URL, open_timeout=1, close_timeout=1) as ws:
            msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
            data = json.loads(msg)
            ok, detail = _check_keys(data, ["type", "timestamp_ms", "source", "data"])
            if not ok:
                return False, detail
            if data.get("type") != "HELLO":
                return False, f"type={data.get('type')}"
            return True, "ok"
    except Exception as exc:
        return False, f"error={exc}"


def run() -> int:
    results: List[Tuple[str, bool, str]] = []

    with httpx.Client(timeout=2.0) as client:
        try:
            r = client.get(f"{BASE_URL}/api/v1/status")
            status_json = r.json()
            ok, detail = _check_keys(status_json, ["timestamp_ms", "overall_ok", "system", "modules"])
            if ok:
                ok, detail = _check_module_fields(status_json.get("modules", {}), STATUS_FIELDS)
            results.append(("status_keys", ok, detail))

            ok, detail = _check_os_populated(status_json)
            results.append(("os_populated", ok, detail))

            ok, detail = _check_ups_populated(status_json)
            results.append(("ups_populated", ok, detail))

            ok, detail = _check_esp32_status(status_json)
            results.append(("esp32_status", ok, detail))

            ok, detail = _check_antsdr_status(status_json)
            results.append(("antsdr_status", ok, detail))

            ok, detail = _check_remoteid_status(status_json)
            results.append(("remoteid_status", ok, detail))

            ok, detail = _check_placeholders(status_json.get("modules", {}))
            results.append(("placeholders_status", ok, detail))
        except Exception as exc:
            results.append(("status_keys", False, f"error={exc}"))
            results.append(("os_populated", False, f"error={exc}"))
            results.append(("ups_populated", False, f"error={exc}"))
            results.append(("placeholders_status", False, f"error={exc}"))

        try:
            r = client.get(f"{BASE_URL}/api/v1/health")
            health_json = r.json()
            ok, detail = _check_keys(health_json, ["timestamp_ms", "overall_ok", "modules"])
            if ok:
                ok, detail = _check_module_fields(health_json.get("modules", {}), HEALTH_FIELDS)
            results.append(("health_keys", ok, detail))

            ok, detail = _check_os_health(health_json)
            results.append(("os_health", ok, detail))

            ok, detail = _check_ups_health(health_json)
            results.append(("ups_health", ok, detail))

            ok, detail = _check_esp32_health(health_json)
            results.append(("esp32_health", ok, detail))

            ok, detail = _check_antsdr_health(health_json)
            results.append(("antsdr_health", ok, detail))

            ok, detail = _check_remoteid_health(health_json)
            results.append(("remoteid_health", ok, detail))

            ok, detail = _check_placeholders(health_json.get("modules", {}))
            results.append(("placeholders_health", ok, detail))
        except Exception as exc:
            results.append(("health_keys", False, f"error={exc}"))
            results.append(("os_health", False, f"error={exc}"))
            results.append(("ups_health", False, f"error={exc}"))
            results.append(("esp32_health", False, f"error={exc}"))
            results.append(("placeholders_health", False, f"error={exc}"))

        try:
            r = client.get(f"{BASE_URL}/api/v1/contacts")
            ok, detail = _check_keys(r.json(), ["contacts"])
            results.append(("contacts_keys", ok, detail))
        except Exception as exc:
            results.append(("contacts_keys", False, f"error={exc}"))

    ws_ok, ws_detail = asyncio.run(_ws_hello_check())
    results.append(("ws_hello", ws_ok, ws_detail))

    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    skipped = 0

    summary = f"SUMMARY Total={total} PASS={passed} FAIL={failed} SKIP={skipped}"

    report_lines = [f"# Test Results {date.today().isoformat()}"]
    for name, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        report_lines.append(f"- {name}: {status} ({detail})")
    report_lines.append("")
    report_lines.append(summary)

    report_path = Path("docs") / f"TEST_RESULTS_{date.today().isoformat()}.md"
    report_path.write_text("\n".join(report_lines) + "\n")

    print(summary)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run())
