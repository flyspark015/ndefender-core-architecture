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
        except Exception as exc:
            results.append(("status_keys", False, f"error={exc}"))
            results.append(("os_populated", False, f"error={exc}"))

        try:
            r = client.get(f"{BASE_URL}/api/v1/health")
            ok, detail = _check_keys(r.json(), ["timestamp_ms", "overall_ok", "modules"])
            if ok:
                ok, detail = _check_module_fields(r.json().get("modules", {}), HEALTH_FIELDS)
            results.append(("health_keys", ok, detail))
        except Exception as exc:
            results.append(("health_keys", False, f"error={exc}"))

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
