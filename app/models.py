from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def now_ms() -> int:
    import time

    return int(time.time() * 1000)


class EventEnvelope(BaseModel):
    type: str
    timestamp_ms: int
    source: str
    data: Dict[str, Any]


class UpsStatus(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    battery_percent: Optional[float] = None
    battery_voltage_v: Optional[float] = None
    battery_current_a: Optional[float] = None
    current_a: Optional[float] = None
    remaining_capacity_mah: Optional[float] = None
    cell_voltages_v: Optional[List[float]] = None
    vbus_voltage_v: Optional[float] = None
    vbus_current_a: Optional[float] = None
    vbus_power_w: Optional[float] = None
    state: Optional[str] = None
    input_voltage_v: Optional[float] = None
    output_voltage_v: Optional[float] = None
    load_percent: Optional[float] = None
    temperature_c: Optional[float] = None
    runtime_s: Optional[float] = None
    on_battery: Optional[bool] = None


class UpsHealth(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    comms_ok: Optional[bool] = None
    model: Optional[str] = None
    serial: Optional[str] = None
    firmware_version: Optional[str] = None


class OsStatus(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    cpu_temp_c: Optional[float] = None
    cpu_percent: Optional[float] = None
    mem_used_mb: Optional[float] = None
    mem_total_mb: Optional[float] = None
    disk_used_mb: Optional[float] = None
    disk_total_mb: Optional[float] = None
    uptime_s: Optional[int] = None


class OsHealth(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    hostname: Optional[str] = None
    os_version: Optional[str] = None
    kernel_version: Optional[str] = None
    time_sync_ok: Optional[bool] = None


class Esp32Status(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    connected: Optional[bool] = None
    firmware_version: Optional[str] = None
    device_uptime_ms: Optional[int] = None
    seq: Optional[int] = None
    rssi_dbm: Optional[float] = None
    supply_voltage_v: Optional[float] = None
    temperature_c: Optional[float] = None


class Esp32Health(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    comms_ok: Optional[bool] = None


class AntsdrStatus(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    device_present: Optional[bool] = None
    driver_ok: Optional[bool] = None
    center_freq_hz: Optional[int] = None
    sample_rate_hz: Optional[int] = None
    rf_bw_hz: Optional[int] = None
    gain_db: Optional[float] = None
    rf_power_dbm: Optional[float] = None
    noise_floor_dbm: Optional[float] = None
    stream_active: Optional[bool] = None


class AntsdrHealth(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    device_present: Optional[bool] = None
    driver_ok: Optional[bool] = None


class RemoteIdStatus(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    active_contacts: Optional[int] = None


class RemoteIdHealth(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    input_stream_ok: Optional[bool] = None


class FusionStatus(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    active_contacts: Optional[int] = None


class FusionHealth(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    active_contacts: Optional[int] = None


class VideoStatus(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    stream_ok: Optional[bool] = None
    fps: Optional[float] = None
    bitrate_kbps: Optional[float] = None
    frame_width: Optional[int] = None
    frame_height: Optional[int] = None


class VideoHealth(BaseModel):
    ok: bool
    last_update_ms: Optional[int] = None
    last_error: Optional[str] = None
    encoder_ok: Optional[bool] = None
    camera_ok: Optional[bool] = None


class StatusModules(BaseModel):
    ups: UpsStatus
    os: OsStatus
    esp32: Esp32Status
    antsdr: AntsdrStatus
    remoteid: RemoteIdStatus
    fusion: FusionStatus
    video: VideoStatus


class HealthModules(BaseModel):
    ups: UpsHealth
    os: OsHealth
    esp32: Esp32Health
    antsdr: AntsdrHealth
    remoteid: RemoteIdHealth
    fusion: FusionHealth
    video: VideoHealth


class StatusSnapshot(BaseModel):
    timestamp_ms: int
    overall_ok: bool
    system: Dict[str, Any]
    modules: StatusModules


class DeepHealth(BaseModel):
    timestamp_ms: int
    overall_ok: bool
    modules: HealthModules


class CommandRequest(BaseModel):
    timestamp_ms: Optional[int] = None
    command: str
    confirm: Optional[bool] = False
    payload: Optional[Dict[str, Any]] = None


class ContactsResponse(BaseModel):
    contacts: List[Dict[str, Any]] = Field(default_factory=list)
