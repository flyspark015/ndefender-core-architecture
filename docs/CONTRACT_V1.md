# N-Defender Unified Backend Contract v1 (Phase A/B)

## Global Event Envelope
All events follow:

```
{ "type": "...", "timestamp_ms": 0, "source": "...", "data": {} }
```

## REST API
Base: `/api/v1`

### GET `/status`
Always 200.

Response:
```
{
  "timestamp_ms": 0,
  "overall_ok": false,
  "system": {},
  "modules": {
    "ups": { ... },
    "os": { ... },
    "esp32": { ... },
    "antsdr": { ... },
    "remoteid": { ... },
    "video": { ... }
  }
}
```

### GET `/health`
Always 200. Same module keys as `/status`.

```
{
  "timestamp_ms": 0,
  "overall_ok": false,
  "modules": { ... }
}
```

### GET `/contacts`
Always 200.

```
{ "contacts": [] }
```

### POST `/commands`
Accepts:
```
{ "timestamp_ms": 0, "command": "...", "confirm": false, "payload": {} }
```

Phase A/B behavior:
- Currently returns HTTP 409
```
{ "detail": "precondition_failed", "code": "NOT_IMPLEMENTED" }
```

## Module Contracts (TX/RX)

### ups
Status object fields:
- ok: bool
- last_update_ms: int
- battery_percent: float
- input_voltage_v: float
- output_voltage_v: float
- load_percent: float
- temperature_c: float
- runtime_s: int
- on_battery: bool

Health object fields:
- ok: bool
- last_update_ms: int
- comms_ok: bool
- model: string
- serial: string
- firmware_version: string

WS events:
- UPS_STATUS: { ok, last_update_ms, battery_percent, input_voltage_v, output_voltage_v, load_percent, temperature_c, runtime_s, on_battery }
- UPS_HEALTH: { ok, last_update_ms, comms_ok, model, serial, firmware_version }

Commands:
- UPS_SELF_TEST
  - payload: {}
  - success: 200 {"detail":"ok","code":"UPS_SELF_TEST_ACCEPTED"}
- UPS_BEEP
  - payload: {"enable": bool}
  - success: 200 {"detail":"ok","code":"UPS_BEEP_ACCEPTED"}
- UPS_SHUTDOWN (dangerous)
  - payload: {"delay_s": int}
  - success: 200 {"detail":"ok","code":"UPS_SHUTDOWN_ACCEPTED"}

Preconditions:
- Missing hardware: 409 {"detail":"precondition_failed","code":"UPS_MISSING"}
- Upstream unreachable: 502 {"detail":"upstream_unreachable","code":"UPS_UPSTREAM"}
- Dangerous without confirm=true: 400 {"detail":"confirm_required"}

### os
Status object fields:
- ok: bool
- last_update_ms: int
- cpu_temp_c: float
- cpu_percent: float
- mem_used_mb: float
- mem_total_mb: float
- disk_used_mb: float
- disk_total_mb: float
- uptime_s: int

Health object fields:
- ok: bool
- last_update_ms: int
- hostname: string
- os_version: string
- kernel_version: string
- time_sync_ok: bool

WS events:
- OS_STATUS: { ok, last_update_ms, cpu_temp_c, cpu_percent, mem_used_mb, mem_total_mb, disk_used_mb, disk_total_mb, uptime_s }
- OS_HEALTH: { ok, last_update_ms, hostname, os_version, kernel_version, time_sync_ok }

Commands:
- OS_REBOOT (dangerous)
  - payload: {"delay_s": int}
  - success: 200 {"detail":"ok","code":"OS_REBOOT_ACCEPTED"}
- OS_SHUTDOWN (dangerous)
  - payload: {"delay_s": int}
  - success: 200 {"detail":"ok","code":"OS_SHUTDOWN_ACCEPTED"}

Preconditions:
- Missing capability: 409 {"detail":"precondition_failed","code":"OS_UNSUPPORTED"}
- Dangerous without confirm=true: 400 {"detail":"confirm_required"}

### esp32
Status object fields:
- ok: bool
- last_update_ms: int
- connected: bool
- firmware_version: string
- rssi_dbm: float
- supply_voltage_v: float
- temperature_c: float

Health object fields:
- ok: bool
- last_update_ms: int
- comms_ok: bool
- last_error: string

WS events:
- ESP32_STATUS: { ok, last_update_ms, connected, firmware_version, rssi_dbm, supply_voltage_v, temperature_c }
- ESP32_HEALTH: { ok, last_update_ms, comms_ok, last_error }

Commands:
- ESP32_REBOOT
  - payload: {}
  - success: 200 {"detail":"ok","code":"ESP32_REBOOT_ACCEPTED"}
- ESP32_SET_RELAY
  - payload: {"relay_id": int, "state": bool}
  - success: 200 {"detail":"ok","code":"ESP32_SET_RELAY_ACCEPTED"}

Preconditions:
- Missing hardware: 409 {"detail":"precondition_failed","code":"ESP32_MISSING"}
- Upstream unreachable: 502 {"detail":"upstream_unreachable","code":"ESP32_UPSTREAM"}

### antsdr
Status object fields:
- ok: bool
- last_update_ms: int
- center_freq_hz: float
- sample_rate_hz: float
- gain_db: float
- rf_power_dbm: float
- stream_active: bool

Health object fields:
- ok: bool
- last_update_ms: int
- device_present: bool
- driver_ok: bool

WS events:
- ANTSDR_STATUS: { ok, last_update_ms, center_freq_hz, sample_rate_hz, gain_db, rf_power_dbm, stream_active }
- ANTSDR_HEALTH: { ok, last_update_ms, device_present, driver_ok }

Commands:
- ANTSDR_START
  - payload: {"center_freq_hz": float, "sample_rate_hz": float}
  - success: 200 {"detail":"ok","code":"ANTSDR_START_ACCEPTED"}
- ANTSDR_STOP
  - payload: {}
  - success: 200 {"detail":"ok","code":"ANTSDR_STOP_ACCEPTED"}
- ANTSDR_SET_GAIN
  - payload: {"gain_db": float}
  - success: 200 {"detail":"ok","code":"ANTSDR_SET_GAIN_ACCEPTED"}

Preconditions:
- Missing hardware: 409 {"detail":"precondition_failed","code":"ANTSDR_MISSING"}
- Upstream unreachable: 502 {"detail":"upstream_unreachable","code":"ANTSDR_UPSTREAM"}

### remoteid
Status object fields:
- ok: bool
- last_update_ms: int
- contacts_count: int
- last_contact_ms: int
- latitude: float
- longitude: float

Health object fields:
- ok: bool
- last_update_ms: int
- receiver_ok: bool
- gps_ok: bool

WS events:
- REMOTEID_STATUS: { ok, last_update_ms, contacts_count, last_contact_ms, latitude, longitude }
- REMOTEID_CONTACT: { contact_id, timestamp_ms, latitude, longitude, altitude_m, speed_mps }
- REMOTEID_HEALTH: { ok, last_update_ms, receiver_ok, gps_ok }

Commands:
- REMOTEID_START
  - payload: {"region": string}
  - success: 200 {"detail":"ok","code":"REMOTEID_START_ACCEPTED"}
- REMOTEID_STOP
  - payload: {}
  - success: 200 {"detail":"ok","code":"REMOTEID_STOP_ACCEPTED"}

Preconditions:
- Missing hardware: 409 {"detail":"precondition_failed","code":"REMOTEID_MISSING"}
- Upstream unreachable: 502 {"detail":"upstream_unreachable","code":"REMOTEID_UPSTREAM"}

### video
Status object fields:
- ok: bool
- last_update_ms: int
- stream_ok: bool
- fps: float
- bitrate_kbps: float
- frame_width: int
- frame_height: int

Health object fields:
- ok: bool
- last_update_ms: int
- encoder_ok: bool
- camera_ok: bool

WS events:
- VIDEO_STATUS: { ok, last_update_ms, stream_ok, fps, bitrate_kbps, frame_width, frame_height }
- VIDEO_HEALTH: { ok, last_update_ms, encoder_ok, camera_ok }

Commands:
- VIDEO_START
  - payload: {"profile": string}
  - success: 200 {"detail":"ok","code":"VIDEO_START_ACCEPTED"}
- VIDEO_STOP
  - payload: {}
  - success: 200 {"detail":"ok","code":"VIDEO_STOP_ACCEPTED"}
- VIDEO_SET_PROFILE
  - payload: {"profile": string}
  - success: 200 {"detail":"ok","code":"VIDEO_SET_PROFILE_ACCEPTED"}

Preconditions:
- Missing hardware: 409 {"detail":"precondition_failed","code":"VIDEO_MISSING"}
- Upstream unreachable: 502 {"detail":"upstream_unreachable","code":"VIDEO_UPSTREAM"}

## Common Error Rules
- Preconditions missing: HTTP 409 {"detail":"precondition_failed","code":"..."}
- Upstream dependency unreachable: HTTP 502 {"detail":"upstream_unreachable","code":"..."}
- Confirm-gated dangerous commands: HTTP 400 {"detail":"confirm_required"}
