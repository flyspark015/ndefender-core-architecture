# UI ↔ Backend Contract (Frozen)

**Scope:** UI-facing endpoints and WebSocket events only. This document is the source of truth for UI integration.

**Base URL (local):** `http://127.0.0.1:8000`

**Timestamp units:** All `*_ms` fields are **epoch milliseconds** unless explicitly noted.

---

## 1) GET `/api/v1/status`

**Response (StatusSnapshot):**

```json
{
  "timestamp_ms": 1700000000000,
  "overall_ok": true,
  "system": {
    "timestamp_ms": 1700000000000,
    "cpu_temp_c": 54.2,
    "cpu_percent": 12.3,
    "mem_used_mb": 834.2,
    "mem_total_mb": 3894.1,
    "disk_used_mb": 5120.0,
    "disk_total_mb": 29491.0,
    "uptime_s": 123456
  },
  "modules": { "ups": { ... }, "os": { ... }, "esp32": { ... }, "antsdr": { ... }, "remoteid": { ... }, "fusion": { ... }, "alerts": { ... }, "video": { ... } }
}
```

**Required top-level fields:**
- `timestamp_ms` (int)
- `overall_ok` (bool)
- `system` (object)
- `modules` (object)

### `system` object (required keys)
- `timestamp_ms` (int)
- `cpu_temp_c` (float|null)
- `cpu_percent` (float)
- `mem_used_mb` (float)
- `mem_total_mb` (float)
- `disk_used_mb` (float)
- `disk_total_mb` (float)
- `uptime_s` (int)

### `modules` object (required keys)
All module objects include at least:
- `ok` (bool)
- `last_update_ms` (int|null)
- `last_error` (string|null)

#### `modules.ups`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `battery_percent` (float|null)
- `battery_voltage_v` (float|null)
- `battery_current_a` (float|null)
- `current_a` (float|null)
- `remaining_capacity_mah` (float|null)
- `cell_voltages_v` (list[float]|null)
- `vbus_voltage_v` (float|null)
- `vbus_current_a` (float|null)
- `vbus_power_w` (float|null)
- `state` (string|null)
- `input_voltage_v` (float|null)
- `output_voltage_v` (float|null)
- `load_percent` (float|null)
- `temperature_c` (float|null)
- `runtime_s` (float|null)
- `on_battery` (bool|null)

#### `modules.os`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `cpu_temp_c` (float|null)
- `cpu_percent` (float|null)
- `mem_used_mb` (float|null)
- `mem_total_mb` (float|null)
- `disk_used_mb` (float|null)
- `disk_total_mb` (float|null)
- `uptime_s` (int|null)

#### `modules.esp32`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `connected` (bool|null)
- `firmware_version` (string|null)
- `device_uptime_ms` (int|null) **(device uptime, not epoch)**
- `seq` (int|null)
- `rssi_dbm` (float|null)
- `supply_voltage_v` (float|null)
- `temperature_c` (float|null)

#### `modules.antsdr`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `device_present` (bool|null)
- `driver_ok` (bool|null)
- `center_freq_hz` (int|null)
- `sample_rate_hz` (int|null)
- `rf_bw_hz` (int|null)
- `gain_db` (float|null)
- `rf_power_dbm` (float|null)
- `noise_floor_dbm` (float|null)
- `stream_active` (bool|null)

#### `modules.remoteid`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `active_contacts` (int|null)

#### `modules.fusion`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `active_contacts` (int|null)

#### `modules.alerts`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `active_alerts` (int|null)

#### `modules.video`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `stream_ok` (bool|null)
- `fps` (float|null)
- `bitrate_kbps` (float|null)
- `frame_width` (int|null)
- `frame_height` (int|null)

---

## 2) GET `/api/v1/health`

**Response (DeepHealth):**

```json
{
  "timestamp_ms": 1700000000000,
  "overall_ok": true,
  "modules": { "ups": { ... }, "os": { ... }, "esp32": { ... }, "antsdr": { ... }, "remoteid": { ... }, "fusion": { ... }, "alerts": { ... }, "video": { ... } }
}
```

**Required top-level fields:**
- `timestamp_ms` (int)
- `overall_ok` (bool)
- `modules` (object)

### `modules` object (required keys)
All module objects include at least:
- `ok` (bool)
- `last_update_ms` (int|null)
- `last_error` (string|null)

#### `modules.ups`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `comms_ok` (bool|null)
- `model` (string|null)
- `serial` (string|null)
- `firmware_version` (string|null)

#### `modules.os`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `hostname` (string|null)
- `os_version` (string|null)
- `kernel_version` (string|null)
- `time_sync_ok` (bool|null)

#### `modules.esp32`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `comms_ok` (bool|null)

#### `modules.antsdr`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `device_present` (bool|null)
- `driver_ok` (bool|null)

#### `modules.remoteid`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `input_stream_ok` (bool|null)

#### `modules.fusion`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `active_contacts` (int|null)

#### `modules.alerts`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `active_alerts` (int|null)

#### `modules.video`
Required keys:
- `ok`, `last_update_ms`, `last_error`
- `encoder_ok` (bool|null)
- `camera_ok` (bool|null)

---

## 3) GET `/api/v1/contacts`

**Response:** JSON **array** of fused contact objects.

**Contact object (required keys):**
- `contact_id` (string)
- `type` (string)
- `remoteid_id` (string|null)
- `rf_sources` (list[string])
- `video_sources` (list[string])
- `first_seen_ms` (int)
- `last_seen_ms` (int)
- `threat_score` (float)

**Example:**
```json
[
  {
    "contact_id": "fusion:drone123",
    "type": "remoteid",
    "remoteid_id": "drone123",
    "rf_sources": ["antsdr"],
    "video_sources": ["esp32"],
    "first_seen_ms": 1700000000000,
    "last_seen_ms": 1700000005000,
    "threat_score": 3.0
  }
]
```

---

## 4) GET `/api/v1/alerts`

**Response:** JSON **array** of alert objects.

**Alert object (required keys):**
- `alert_id` (string)
- `contact_id` (string)
- `threat_score` (int)
- `severity` (string: `low|medium|high`)
- `first_seen_ms` (int)
- `last_seen_ms` (int)
- `state` (string, currently always `active`)

**Example:**
```json
[
  {
    "alert_id": "alert:fusion:drone123",
    "contact_id": "fusion:drone123",
    "threat_score": 3,
    "severity": "high",
    "first_seen_ms": 1700000000000,
    "last_seen_ms": 1700000005000,
    "state": "active"
  }
]
```

---

## 5) POST `/api/v1/commands`

**Request body:**

```json
{
  "timestamp_ms": 1700000000000,
  "command": "video/select",
  "confirm": false,
  "payload": { "sel": 1 }
}
```

**Fields:**
- `timestamp_ms` (int, optional) — if omitted, backend fills with current epoch ms
- `command` (string, required)
- `confirm` (bool, optional, default `false`)
- `payload` (object, optional)

**Supported commands:**
- `video/select`
- `scan/start`
- `scan/stop`
- `vrx/tune`
- `antsdr/start`
- `antsdr/stop`

**Success response:**
```json
{ "ok": true }
```

**Error responses (deterministic):**
- 409 `{"detail":"precondition_failed","code":"NOT_IMPLEMENTED"}`
- 409 `{"detail":"precondition_failed","code":"ESP32_SERIAL_NOT_CONNECTED"}`
- 409 `{"detail":"precondition_failed","code":"ANTSDR_NOT_CONNECTED"}`
- 502 `{"detail":"upstream_unreachable","code":"ANTSDR_DRIVER_UNAVAILABLE"}`

---

## 6) WebSocket `/api/v1/ws`

**Event envelope (all WS events):**

```json
{
  "type": "EVENT_TYPE",
  "timestamp_ms": 1700000000000,
  "source": "module_name",
  "data": { }
}
```

**On connect:**
- `HELLO` event from `source="core"`

**Event types currently emitted:**
- `HELLO` (core)
- `COMMAND_ACK` (esp32/antsdr/core)
- `TELEMETRY_UPDATE` (esp32)
- `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_LOST` (remoteid / fusion)
- `ALERT_NEW`, `ALERT_UPDATE` (alerts)
- `RF_SCAN_STATE`, `RF_CONTACT_NEW`, `RF_CONTACT_UPDATE`, `RF_CONTACT_LOST` (antsdr)

**`COMMAND_ACK` data payload:**
- `command` (string)
- `ok` (bool)
- `code` (string)
- `detail` (string)
- `timestamp_ms` (int, echoes request timestamp)

**`TELEMETRY_UPDATE` data payload:**
- Free-form telemetry map from ESP32; expected keys may include:
  - `fw_version` (string)
  - `timestamp_ms` (device uptime ms)
  - `seq` (int)
  - `vrx` (list)
  - `video` (object)
  - `led` (object)
  - `sys` (object)

**`CONTACT_*` data payload:**
- Same shape as `/api/v1/contacts` objects

**`ALERT_*` data payload:**
- Same shape as `/api/v1/alerts` objects

**`RF_CONTACT_*` data payload:**
- `contact_id` (string)
- `center_freq_hz` (int)
- `peak_dbm` (float|null)
- `snr_db` (float|null)
- `band` (string|null)
- `timestamp_ms` (int)

---

## Notes

- No auth or API keys are used; security is via local-only binding and network gating.
- Timestamps are epoch milliseconds except `esp32.device_uptime_ms` which is device uptime.
- All module objects contain `ok`, `last_update_ms`, `last_error` keys even when null.
- UI compatibility layer normalizes list fields (`rf_sources`, `video_sources`) to empty arrays when missing.
- Alerts `severity` is normalized to lowercase (`low|medium|high`) if present.
- WS `TELEMETRY_UPDATE` ensures `data.timestamp_ms` is present (fallback to envelope timestamp).
