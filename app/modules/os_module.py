from __future__ import annotations

import platform
import socket
import subprocess
from pathlib import Path
from typing import Optional

import psutil

from app.models import OsHealth, OsStatus, now_ms


THERMAL_PATH = Path("/sys/class/thermal/thermal_zone0/temp")
OS_RELEASE_PATH = Path("/etc/os-release")
UPTIME_PATH = Path("/proc/uptime")


def _read_cpu_temp_c() -> Optional[float]:
    if not THERMAL_PATH.exists():
        return None
    try:
        raw = THERMAL_PATH.read_text().strip()
        return float(raw) / 1000.0
    except Exception:
        return None


def _read_uptime_s() -> Optional[int]:
    try:
        raw = UPTIME_PATH.read_text().strip().split()[0]
        return int(float(raw))
    except Exception:
        return None


def _read_os_version() -> Optional[str]:
    if not OS_RELEASE_PATH.exists():
        return None
    try:
        for line in OS_RELEASE_PATH.read_text().splitlines():
            if line.startswith("PRETTY_NAME="):
                value = line.split("=", 1)[1].strip().strip('"')
                return value or None
    except Exception:
        return None
    return None


def _read_time_sync_ok() -> Optional[bool]:
    try:
        result = subprocess.run(
            ["timedatectl", "show", "-p", "NTPSynchronized", "--value"],
            check=False,
            capture_output=True,
            text=True,
            timeout=1,
        )
    except FileNotFoundError:
        return None
    except Exception:
        return None

    if result.returncode != 0:
        return None
    value = result.stdout.strip().lower()
    if value == "yes":
        return True
    if value == "no":
        return False
    return None


def read_os_status() -> OsStatus:
    cpu_percent = psutil.cpu_percent(interval=0.0)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    uptime_s = _read_uptime_s()
    cpu_temp_c = _read_cpu_temp_c()

    ok = all(
        value is not None
        for value in [cpu_percent, mem.total, mem.used, disk.total, disk.used, uptime_s]
    )

    return OsStatus(
        ok=ok,
        last_update_ms=now_ms(),
        last_error=None if ok else "os_telemetry_unavailable",
        cpu_temp_c=cpu_temp_c,
        cpu_percent=float(cpu_percent) if cpu_percent is not None else None,
        mem_used_mb=mem.used / (1024 * 1024),
        mem_total_mb=mem.total / (1024 * 1024),
        disk_used_mb=disk.used / (1024 * 1024),
        disk_total_mb=disk.total / (1024 * 1024),
        uptime_s=uptime_s,
    )


def read_os_health() -> OsHealth:
    hostname = socket.gethostname()
    os_version = _read_os_version()
    kernel_version = platform.release()
    time_sync_ok = _read_time_sync_ok()

    ok = all([hostname, os_version, kernel_version])

    return OsHealth(
        ok=ok,
        last_update_ms=now_ms(),
        last_error=None if ok else "os_health_unavailable",
        hostname=hostname,
        os_version=os_version,
        kernel_version=kernel_version,
        time_sync_ok=time_sync_ok,
    )


def status_to_system(status: OsStatus) -> dict:
    return {
        "timestamp_ms": status.last_update_ms,
        "cpu_temp_c": status.cpu_temp_c,
        "cpu_percent": status.cpu_percent,
        "mem_used_mb": status.mem_used_mb,
        "mem_total_mb": status.mem_total_mb,
        "disk_used_mb": status.disk_used_mb,
        "disk_total_mb": status.disk_total_mb,
        "uptime_s": status.uptime_s,
    }
