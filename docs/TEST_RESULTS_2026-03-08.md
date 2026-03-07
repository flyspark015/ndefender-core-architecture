# Test Results 2026-03-08

## UI Contract Freeze Evidence

### /api/v1/health
{
  "timestamp_ms": 1772910538473,
  "overall_ok": false,
  "modules": {
    "ups": {
      "ok": true,
      "last_update_ms": 1772910538237,
      "last_error": null,
      "comms_ok": true,
      "model": "Waveshare UPS HAT (E)",
      "serial": null,
      "firmware_version": null
    },
    "os": {
      "ok": true,
      "last_update_ms": 1772910538473,
      "last_error": null,
      "hostname": "ndefender-pi",
      "os_version": "Debian GNU/Linux 12 (bookworm)",
      "kernel_version": "6.12.62+rpt-rpi-2712",
      "time_sync_ok": null
    },
    "esp32": {
      "ok": true,
      "last_update_ms": 1772907985102,
      "last_error": null,
      "comms_ok": true
    },
    "antsdr": {
      "ok": true,
      "last_update_ms": 1772910537884,
      "last_error": null,
      "device_present": true,
      "driver_ok": true
    },
    "remoteid": {
      "ok": false,
      "last_update_ms": null,
      "last_error": "REMOTEID_NO_DATA",
      "input_stream_ok": true
    },
    "fusion": {
      "ok": true,
      "last_update_ms": 1772910537931,
      "last_error": null,
      "active_contacts": 0
    },
    "alerts": {
      "ok": true,
      "active_alerts": 0,
      "last_update_ms": 1772910537949,
      "last_error": null
    },
    "video": {
      "ok": false,
      "last_update_ms": null,
      "last_error": "not_implemented",
      "encoder_ok": null,
      "camera_ok": null
    }
  }
}

### /api/v1/status
{
  "timestamp_ms": 1772910538753,
  "overall_ok": false,
  "system": {
    "timestamp_ms": 1772910538495,
    "cpu_temp_c": 39.15,
    "cpu_percent": 26,
    "mem_used_mb": 1419.546875,
    "mem_total_mb": 16215.046875,
    "disk_used_mb": 66713.98828125,
    "disk_total_mb": 119404.86328125,
    "uptime_s": 7352
  },
  "modules": {
    "ups": {
      "ok": true,
      "last_update_ms": 1772910538237,
      "last_error": null,
      "battery_percent": 98,
      "battery_voltage_v": 16.694,
      "battery_current_a": -0.004,
      "current_a": -0.004,
      "remaining_capacity_mah": 4702,
      "cell_voltages_v": [
        4.174,
        4.174,
        4.171,
        4.175
      ],
      "vbus_voltage_v": 15.026,
      "vbus_current_a": 1.288,
      "vbus_power_w": 19.406,
      "state": "discharging",
      "input_voltage_v": 15.026,
      "output_voltage_v": 16.694,
      "load_percent": null,
      "temperature_c": null,
      "runtime_s": 3932100,
      "on_battery": false
    },
    "os": {
      "ok": true,
      "last_update_ms": 1772910538495,
      "last_error": null,
      "cpu_temp_c": 39.15,
      "cpu_percent": 26,
      "mem_used_mb": 1419.546875,
      "mem_total_mb": 16215.046875,
      "disk_used_mb": 66713.98828125,
      "disk_total_mb": 119404.86328125,
      "uptime_s": 7352
    },
    "esp32": {
      "ok": true,
      "last_update_ms": 1772907985102,
      "last_error": null,
      "connected": true,
      "firmware_version": null,
      "device_uptime_ms": null,
      "seq": null,
      "rssi_dbm": null,
      "supply_voltage_v": null,
      "temperature_c": null
    },
    "antsdr": {
      "ok": true,
      "last_update_ms": 1772910537884,
      "last_error": null,
      "device_present": true,
      "driver_ok": true,
      "center_freq_hz": null,
      "sample_rate_hz": 2000000,
      "rf_bw_hz": 2000000,
      "gain_db": null,
      "rf_power_dbm": null,
      "noise_floor_dbm": null,
      "stream_active": null
    },
    "remoteid": {
      "ok": false,
      "last_update_ms": null,
      "last_error": "REMOTEID_NO_DATA",
      "active_contacts": 0
    },
    "fusion": {
      "ok": true,
      "last_update_ms": 1772910537931,
      "last_error": null,
      "active_contacts": 0
    },
    "alerts": {
      "ok": true,
      "active_alerts": 0,
      "last_update_ms": 1772910537949,
      "last_error": null
    },
    "video": {
      "ok": false,
      "last_update_ms": null,
      "last_error": "not_implemented",
      "stream_ok": null,
      "fps": null,
      "bitrate_kbps": null,
      "frame_width": null,
      "frame_height": null
    }
  }
}

### /api/v1/contacts (first item)
null

### /api/v1/alerts (first item)
null

### WebSocket events (captured)


#### HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772910548699,
  "source": "core",
  "data": {}
}
```

#### TELEMETRY_UPDATE
Not observed within 5s.

#### ALERT_NEW / ALERT_UPDATE
Not observed within 5s.

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: FAIL (esp32_fw_not_string)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=21 PASS=20 FAIL=1 SKIP=0

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0


### WebSocket events (retry capture)

#### HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772910597503,
  "source": "core",
  "data": {}
}
```

#### TELEMETRY_UPDATE
Not observed within 10s.

#### ALERT_NEW / ALERT_UPDATE
Not observed within 10s.

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0


## Step 2 — UI Compatibility Layer Gates

### pytest -q
```
23 passed, 2 warnings in 0.80s
```

### run_evidence.py
```
SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0
```

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0


### Step 2 Re-run (post-doc updates)
```
pytest -q: 23 passed, 2 warnings
run_evidence.py: SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0
```

## Step 3 — Live Data Flow Validation (BEFORE)

### systemctl status ndefender-unified
● ndefender-unified.service - N-Defender Unified Backend (FastAPI)
     Loaded: loaded (/etc/systemd/system/ndefender-unified.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-03-07 23:56:24 IST; 1h 0min ago
   Main PID: 11667 (python)
      Tasks: 12 (limit: 19359)
        CPU: 10.034s
     CGroup: /system.slice/ndefender-unified.service
             └─11667 /home/toybook/ndefender-unified-backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

Mar 08 00:51:16 ndefender-pi python[11667]: INFO:     127.0.0.1:43140 - "WebSocket /api/v1/ws" [accepted]
Mar 08 00:51:16 ndefender-pi python[11667]: INFO:     connection open
Mar 08 00:51:16 ndefender-pi python[11667]: INFO:     connection closed
Mar 08 00:51:43 ndefender-pi python[11667]: INFO:     127.0.0.1:34404 - "GET /api/v1/status HTTP/1.1" 200 OK
Mar 08 00:51:43 ndefender-pi python[11667]: INFO:     127.0.0.1:34404 - "GET /api/v1/health HTTP/1.1" 200 OK
Mar 08 00:51:43 ndefender-pi python[11667]: INFO:     127.0.0.1:34404 - "GET /api/v1/contacts HTTP/1.1" 200 OK
Mar 08 00:51:43 ndefender-pi python[11667]: INFO:     127.0.0.1:34404 - "GET /api/v1/alerts HTTP/1.1" 200 OK
Mar 08 00:51:43 ndefender-pi python[11667]: INFO:     127.0.0.1:34408 - "WebSocket /api/v1/ws" [accepted]
Mar 08 00:51:43 ndefender-pi python[11667]: INFO:     connection open
Mar 08 00:51:43 ndefender-pi python[11667]: INFO:     connection closed

### /api/v1/health
{
  "timestamp_ms": 1772911603000,
  "overall_ok": false,
  "modules": {
    "ups": {
      "ok": true,
      "last_update_ms": 1772911601985,
      "last_error": null,
      "comms_ok": true,
      "model": "Waveshare UPS HAT (E)",
      "serial": null,
      "firmware_version": null
    },
    "os": {
      "ok": true,
      "last_update_ms": 1772911603000,
      "last_error": null,
      "hostname": "ndefender-pi",
      "os_version": "Debian GNU/Linux 12 (bookworm)",
      "kernel_version": "6.12.62+rpt-rpi-2712",
      "time_sync_ok": null
    },
    "esp32": {
      "ok": true,
      "last_update_ms": 1772907985102,
      "last_error": null,
      "comms_ok": true
    },
    "antsdr": {
      "ok": true,
      "last_update_ms": 1772911602162,
      "last_error": null,
      "device_present": true,
      "driver_ok": true
    },
    "remoteid": {
      "ok": false,
      "last_update_ms": null,
      "last_error": "REMOTEID_NO_DATA",
      "input_stream_ok": true
    },
    "fusion": {
      "ok": true,
      "last_update_ms": 1772911602202,
      "last_error": null,
      "active_contacts": 0
    },
    "alerts": {
      "ok": true,
      "active_alerts": 0,
      "last_update_ms": 1772911602202,
      "last_error": null
    },
    "video": {
      "ok": false,
      "last_update_ms": null,
      "last_error": "not_implemented",
      "encoder_ok": null,
      "camera_ok": null
    }
  }
}

### /api/v1/status modules
{
  "ups": {
    "ok": true,
    "last_update_ms": 1772911601985,
    "last_error": null,
    "battery_percent": 98,
    "battery_voltage_v": 16.696,
    "battery_current_a": 0,
    "current_a": 0,
    "remaining_capacity_mah": 4702,
    "cell_voltages_v": [
      4.175,
      4.175,
      4.171,
      4.176
    ],
    "vbus_voltage_v": 15.028,
    "vbus_current_a": 1.108,
    "vbus_power_w": 16.686,
    "state": "discharging",
    "input_voltage_v": 15.028,
    "output_voltage_v": 16.696,
    "load_percent": null,
    "temperature_c": null,
    "runtime_s": 0,
    "on_battery": false
  },
  "os": {
    "ok": true,
    "last_update_ms": 1772911603014,
    "last_error": null,
    "cpu_temp_c": 38.05,
    "cpu_percent": 31.6,
    "mem_used_mb": 1365.6875,
    "mem_total_mb": 16215.046875,
    "disk_used_mb": 66714.70703125,
    "disk_total_mb": 119404.86328125,
    "uptime_s": 8416
  },
  "esp32": {
    "ok": true,
    "last_update_ms": 1772907985102,
    "last_error": null,
    "connected": true,
    "firmware_version": null,
    "device_uptime_ms": null,
    "seq": null,
    "rssi_dbm": null,
    "supply_voltage_v": null,
    "temperature_c": null
  },
  "antsdr": {
    "ok": true,
    "last_update_ms": 1772911603162,
    "last_error": null,
    "device_present": true,
    "driver_ok": true,
    "center_freq_hz": null,
    "sample_rate_hz": 2000000,
    "rf_bw_hz": 2000000,
    "gain_db": null,
    "rf_power_dbm": null,
    "noise_floor_dbm": null,
    "stream_active": null
  },
  "remoteid": {
    "ok": false,
    "last_update_ms": null,
    "last_error": "REMOTEID_NO_DATA",
    "active_contacts": 0
  },
  "fusion": {
    "ok": true,
    "last_update_ms": 1772911603202,
    "last_error": null,
    "active_contacts": 0
  },
  "alerts": {
    "ok": true,
    "active_alerts": 0,
    "last_update_ms": 1772911603202,
    "last_error": null
  },
  "video": {
    "ok": false,
    "last_update_ms": null,
    "last_error": "not_implemented",
    "stream_ok": null,
    "fps": null,
    "bitrate_kbps": null,
    "frame_width": null,
    "frame_height": null
  }
}

### /api/v1/contacts type,length
"array"
0

### /api/v1/alerts type,length
"array"
0

## Step 3 — Stimulus + REST checks

### POST /api/v1/commands antsdr/start
{"ok":true}
HTTP_STATUS:200

### /api/v1/contacts type,length
"array"
1

### /api/v1/contacts first item
{
  "contact_id": "fusion:ui_test_drone",
  "type": "remoteid",
  "remoteid_id": "ui_test_drone",
  "rf_sources": [],
  "video_sources": [],
  "first_seen_ms": 1772911624326,
  "last_seen_ms": 1772911624326,
  "threat_score": 1
}

### /api/v1/alerts type,length
"array"
1

### /api/v1/alerts first item
{
  "alert_id": "alert:fusion:ui_test_drone",
  "contact_id": "fusion:ui_test_drone",
  "threat_score": 2,
  "severity": "medium",
  "first_seen_ms": 1772911624326,
  "last_seen_ms": 1772911624326,
  "state": "active"
}


## Step 3 — WebSocket runtime capture

### HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772911645337,
  "source": "core",
  "data": {}
}
```

### TELEMETRY_UPDATE
Not observed within 15s.

### CONTACT_NEW
Not observed within 15s.

### CONTACT_UPDATE
Not observed within 15s.

### ALERT_NEW
Not observed within 15s.

### ALERT_UPDATE
Not observed within 15s.

### RF_SCAN_STATE
Not observed within 15s.


## Step 3 — WebSocket + RemoteID Injection (live)

### antsdr/start response
```
(200, '{"ok":true}')
```

### HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772911717786,
  "source": "core",
  "data": {}
}
```

### TELEMETRY_UPDATE
Not observed within 15s.

### CONTACT_NEW
```json
{
  "type": "CONTACT_NEW",
  "timestamp_ms": 1772911718351,
  "source": "remoteid",
  "data": {
    "contact_id": "rid:ui_live_1772911717",
    "basic_id": "ui_live_1772911717",
    "lat": 22.305,
    "lon": 70.804,
    "alt_m": 122.0,
    "speed_mps": 14.0,
    "heading_deg": 179.0,
    "first_seen_ms": 1772911718351,
    "last_seen_ms": 1772911718351
  }
}
```

### CONTACT_UPDATE
```json
{
  "type": "CONTACT_UPDATE",
  "timestamp_ms": 1772911718519,
  "source": "fusion",
  "data": {
    "contact_id": "fusion:ui_live_1772911717",
    "type": "remoteid",
    "remoteid_id": "ui_live_1772911717",
    "rf_sources": [
      "antsdr"
    ],
    "video_sources": [],
    "first_seen_ms": 1772911718351,
    "last_seen_ms": 1772911718519,
    "threat_score": 2.0
  }
}
```

### ALERT_NEW
```json
{
  "type": "ALERT_NEW",
  "timestamp_ms": 1772911718351,
  "source": "alerts",
  "data": {
    "alert_id": "alert:fusion:ui_live_1772911717",
    "contact_id": "fusion:ui_live_1772911717",
    "threat_score": 2,
    "severity": "medium",
    "first_seen_ms": 1772911718351,
    "last_seen_ms": 1772911718351,
    "state": "active"
  }
}
```

### ALERT_UPDATE
```json
{
  "type": "ALERT_UPDATE",
  "timestamp_ms": 1772911718519,
  "source": "alerts",
  "data": {
    "alert_id": "alert:fusion:ui_live_1772911717",
    "contact_id": "fusion:ui_live_1772911717",
    "threat_score": 3,
    "severity": "high",
    "first_seen_ms": 1772911718351,
    "last_seen_ms": 1772911718519,
    "state": "active"
  }
}
```

### RF_SCAN_STATE
Not observed within 15s.

## Step 3 — REST after injection

### /api/v1/contacts type,length
"array"
0

### /api/v1/contacts first item
null

### /api/v1/alerts type,length
"array"
0

### /api/v1/alerts first item
null


## Step 3 — WebSocket capture (after live inject)

### HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772911810515,
  "source": "core",
  "data": {}
}
```

### TELEMETRY_UPDATE
Not observed within 12s.

### CONTACT_NEW
```json
{
  "type": "CONTACT_NEW",
  "timestamp_ms": 1772911811396,
  "source": "remoteid",
  "data": {
    "contact_id": "rid:ui_ws_1772911810",
    "basic_id": "ui_ws_1772911810",
    "lat": 22.306,
    "lon": 70.805,
    "alt_m": 123.0,
    "speed_mps": 14.0,
    "heading_deg": 178.0,
    "first_seen_ms": 1772911811396,
    "last_seen_ms": 1772911811396
  }
}
```

### CONTACT_UPDATE
```json
{
  "type": "CONTACT_UPDATE",
  "timestamp_ms": 1772911811478,
  "source": "fusion",
  "data": {
    "contact_id": "fusion:ui_ws_1772911810",
    "type": "remoteid",
    "remoteid_id": "ui_ws_1772911810",
    "rf_sources": [
      "antsdr"
    ],
    "video_sources": [],
    "first_seen_ms": 1772911811396,
    "last_seen_ms": 1772911811478,
    "threat_score": 2.0
  }
}
```

### ALERT_NEW
```json
{
  "type": "ALERT_NEW",
  "timestamp_ms": 1772911811396,
  "source": "alerts",
  "data": {
    "alert_id": "alert:fusion:ui_ws_1772911810",
    "contact_id": "fusion:ui_ws_1772911810",
    "threat_score": 2,
    "severity": "medium",
    "first_seen_ms": 1772911811396,
    "last_seen_ms": 1772911811396,
    "state": "active"
  }
}
```

### ALERT_UPDATE
```json
{
  "type": "ALERT_UPDATE",
  "timestamp_ms": 1772911811478,
  "source": "alerts",
  "data": {
    "alert_id": "alert:fusion:ui_ws_1772911810",
    "contact_id": "fusion:ui_ws_1772911810",
    "threat_score": 3,
    "severity": "high",
    "first_seen_ms": 1772911811396,
    "last_seen_ms": 1772911811478,
    "state": "active"
  }
}
```

### RF_SCAN_STATE
Not observed within 12s.

## Step 3 — REST after live inject

### /api/v1/contacts type,length
"array"
0

### /api/v1/contacts first item
null

### /api/v1/alerts type,length
"array"
0

### /api/v1/alerts first item
null


## Step 3 — REST immediate after inject

### /api/v1/contacts type,length
"array"
1

### /api/v1/contacts first item
{
  "contact_id": "fusion:ui_rest_1772911850",
  "type": "remoteid",
  "remoteid_id": "ui_rest_1772911850",
  "rf_sources": [
    "antsdr"
  ],
  "video_sources": [],
  "first_seen_ms": 1772911851406,
  "last_seen_ms": 1772911852799,
  "threat_score": 2.0
}

### /api/v1/alerts type,length
"array"
1

### /api/v1/alerts first item
{
  "alert_id": "alert:fusion:ui_rest_1772911850",
  "contact_id": "fusion:ui_rest_1772911850",
  "threat_score": 3,
  "severity": "high",
  "first_seen_ms": 1772911851406,
  "last_seen_ms": 1772911852799,
  "state": "active"
}


## Step 3 — TELEMETRY_UPDATE capture attempt (30s)

### HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772911874168,
  "source": "core",
  "data": {}
}
```

### TELEMETRY_UPDATE
Not observed within 30s.

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0

## Step 4 — Command Flow Validation (BEFORE)

### status.modules.esp32
{
  "ok": true,
  "last_update_ms": 1772907985102,
  "last_error": null,
  "connected": true,
  "firmware_version": null,
  "device_uptime_ms": null,
  "seq": null,
  "rssi_dbm": null,
  "supply_voltage_v": null,
  "temperature_c": null
}

### status.modules.antsdr
{
  "ok": true,
  "last_update_ms": 1772912491360,
  "last_error": null,
  "device_present": true,
  "driver_ok": true,
  "center_freq_hz": 5805000000,
  "sample_rate_hz": 2000000,
  "rf_bw_hz": 2000000,
  "gain_db": null,
  "rf_power_dbm": null,
  "noise_floor_dbm": null,
  "stream_active": true
}

### WS HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772912498096,
  "source": "core",
  "data": {}
}
```


## Step 4 — Command runtime validation

### WS HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772912512620,
  "source": "core",
  "data": {}
}
```

### Command: video/select
**Request**
```json
{
  "command": "video/select",
  "payload": {
    "sel": 1
  },
  "confirm": false
}
```
**HTTP Response**
```json
{
  "status": 200,
  "body": {
    "ok": true
  }
}
```
**WS COMMAND_ACK**
```json
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 1772912512771,
  "source": "esp32",
  "data": {
    "command": "video/select",
    "ok": true,
    "code": "OK",
    "detail": "ok",
    "timestamp_ms": 1772912512626
  }
}
```

### Command: antsdr/start
**Request**
```json
{
  "command": "antsdr/start",
  "payload": {},
  "confirm": false
}
```
**HTTP Response**
```json
{
  "status": 200,
  "body": {
    "ok": true
  }
}
```
**WS COMMAND_ACK**
```json
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 1772912512774,
  "source": "antsdr",
  "data": {
    "command": "antsdr/start",
    "ok": true,
    "code": "OK",
    "detail": "ok",
    "timestamp_ms": 1772912512774
  }
}
```
**AntSDR status after command**
```json
{
  "ok": true,
  "last_update_ms": 1772912512363,
  "last_error": null,
  "device_present": true,
  "driver_ok": true,
  "center_freq_hz": 5805000000,
  "sample_rate_hz": 2000000,
  "rf_bw_hz": 2000000,
  "gain_db": null,
  "rf_power_dbm": null,
  "noise_floor_dbm": null,
  "stream_active": true
}
```

### Command: antsdr/stop
**Request**
```json
{
  "command": "antsdr/stop",
  "payload": {},
  "confirm": false
}
```
**HTTP Response**
```json
{
  "status": 200,
  "body": {
    "ok": true
  }
}
```
**WS COMMAND_ACK**
```json
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 1772912512900,
  "source": "antsdr",
  "data": {
    "command": "antsdr/stop",
    "ok": true,
    "code": "OK",
    "detail": "ok",
    "timestamp_ms": 1772912512900
  }
}
```
**AntSDR status after command**
```json
{
  "ok": true,
  "last_update_ms": 1772912512363,
  "last_error": null,
  "device_present": true,
  "driver_ok": true,
  "center_freq_hz": 5805000000,
  "sample_rate_hz": 2000000,
  "rf_bw_hz": 2000000,
  "gain_db": null,
  "rf_power_dbm": null,
  "noise_floor_dbm": null,
  "stream_active": true
}
```


## Step 4 — AntSDR start/stop status verification

### antsdr/start
**Request**
```json
{
  "command": "antsdr/start",
  "payload": {},
  "confirm": false
}
```
**HTTP Response**
```json
{
  "status": 200,
  "body": {
    "ok": true
  }
}
```
**Status after start**
```json
{
  "ok": true,
  "last_update_ms": 1772912538367,
  "last_error": null,
  "device_present": true,
  "driver_ok": true,
  "center_freq_hz": 5845000000,
  "sample_rate_hz": 2000000,
  "rf_bw_hz": 2000000,
  "gain_db": null,
  "rf_power_dbm": null,
  "noise_floor_dbm": null,
  "stream_active": false
}
```

### antsdr/stop
**Request**
```json
{
  "command": "antsdr/stop",
  "payload": {},
  "confirm": false
}
```
**HTTP Response**
```json
{
  "status": 200,
  "body": {
    "ok": true
  }
}
```
**Status after stop**
```json
{
  "ok": true,
  "last_update_ms": 1772912538367,
  "last_error": null,
  "device_present": true,
  "driver_ok": true,
  "center_freq_hz": 5845000000,
  "sample_rate_hz": 2000000,
  "rf_bw_hz": 2000000,
  "gain_db": null,
  "rf_power_dbm": null,
  "noise_floor_dbm": null,
  "stream_active": false
}
```


## Step 4 — Command flow with WS + status (timed)

### WS HELLO
```json
{
  "type": "HELLO",
  "timestamp_ms": 1772912586595,
  "source": "core",
  "data": {}
}
```

### Command: antsdr/start (timed)
**Request**
```json
{
  "command": "antsdr/start",
  "payload": {},
  "confirm": false
}
```
**HTTP Response**
```json
{
  "status": 200,
  "body": {
    "ok": true
  }
}
```
**WS COMMAND_ACK**
```json
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 1772912586607,
  "source": "antsdr",
  "data": {
    "command": "antsdr/start",
    "ok": true,
    "code": "OK",
    "detail": "ok",
    "timestamp_ms": 1772912586606
  }
}
```
**WS RF_SCAN_STATE**
Not observed within 2s.
**Status after start (1s)**
```json
{
  "ok": true,
  "last_update_ms": 1772912590380,
  "last_error": null,
  "device_present": true,
  "driver_ok": true,
  "center_freq_hz": 5845000000,
  "sample_rate_hz": 2000000,
  "rf_bw_hz": 2000000,
  "gain_db": null,
  "rf_power_dbm": null,
  "noise_floor_dbm": null,
  "stream_active": true
}
```

### Command: antsdr/stop (timed)
**Request**
```json
{
  "command": "antsdr/stop",
  "payload": {},
  "confirm": false
}
```
**HTTP Response**
```json
{
  "status": 200,
  "body": {
    "ok": true
  }
}
```
**WS COMMAND_ACK**
```json
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 1772912590978,
  "source": "antsdr",
  "data": {
    "command": "antsdr/stop",
    "ok": true,
    "code": "OK",
    "detail": "ok",
    "timestamp_ms": 1772912590978
  }
}
```
**WS RF_SCAN_STATE**
Not observed within 2s.
**Status after stop (1s)**
```json
{
  "ok": true,
  "last_update_ms": 1772912594380,
  "last_error": null,
  "device_present": true,
  "driver_ok": true,
  "center_freq_hz": 5645000000,
  "sample_rate_hz": 2000000,
  "rf_bw_hz": 2000000,
  "gain_db": null,
  "rf_power_dbm": null,
  "noise_floor_dbm": null,
  "stream_active": false
}
```

### Command: video/select (timed)
**Request**
```json
{
  "command": "video/select",
  "payload": {
    "sel": 1
  },
  "confirm": false
}
```
**HTTP Response**
```json
{
  "status": 200,
  "body": {
    "ok": true
  }
}
```
**WS COMMAND_ACK**
```json
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 1772912595923,
  "source": "esp32",
  "data": {
    "command": "video/select",
    "ok": true,
    "code": "OK",
    "detail": "ok",
    "timestamp_ms": 1772912594430
  }
}
```

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=21 PASS=21 FAIL=0 SKIP=0

## Step 5 — GPS Integration (BEFORE)

### /dev/serial0
lrwxrwxrwx 1 root root 7 Mar  7 01:17 /dev/serial0 -> ttyAMA0

### /dev/ttyAMA0
crw-rw---- 1 root dialout 204, 64 Mar  7 02:01 /dev/ttyAMA0

### gpsd status
○ gpsd.service - GPS (Global Positioning System) Daemon
     Loaded: loaded (/lib/systemd/system/gpsd.service; disabled; preset: enabled)
     Active: inactive (dead)
TriggeredBy: ● gpsd.socket

## Step 5 — gpsd live output

### gpspipe -w -n 5
{"class":"VERSION","release":"3.22","rev":"3.22","proto_major":3,"proto_minor":14}
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/serial0","activated":"2026-03-07T20:06:30.467Z","native":0,"bps":115200,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}

### gpspipe -w -n 5 (timeout 5s)
{"class":"VERSION","release":"3.22","rev":"3.22","proto_major":3,"proto_minor":14}
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/serial0","activated":"2026-03-07T20:06:30.467Z","native":0,"bps":115200,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}

## PHASE STEP 5 — GPS STEP 0 BEFORE

### ls -l /dev/serial0
```
lrwxrwxrwx 1 root root 7 Mar  7 01:17 /dev/serial0 -> ttyAMA0
```

### ls -l /dev/ttyAMA0
```
crw-rw---- 1 root dialout 204, 64 Mar  8 01:36 /dev/ttyAMA0
```

### systemctl status gpsd --no-pager
```
● gpsd.service - GPS (Global Positioning System) Daemon
     Loaded: loaded (/lib/systemd/system/gpsd.service; disabled; preset: enabled)
     Active: active (running) since Sun 2026-03-08 01:36:26 IST; 4min 24s ago
TriggeredBy: ● gpsd.socket
    Process: 18769 ExecStart=/usr/sbin/gpsd $GPSD_OPTIONS $OPTIONS $DEVICES (code=exited, status=0/SUCCESS)
   Main PID: 18770 (gpsd)
      Tasks: 2 (limit: 19359)
        CPU: 393ms
     CGroup: /system.slice/gpsd.service
             └─18770 /usr/sbin/gpsd -n -s 115200 /dev/serial0
```

### gpspipe -w -n 5 (timeout 5s)
```
{"class":"VERSION","release":"3.22","rev":"3.22","proto_major":3,"proto_minor":14}
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/serial0","activated":"2026-03-07T20:06:30.467Z","native":0,"bps":115200,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}
```

### gpspipe -R -n 5 (timeout 5s)
```
{"class":"VERSION","release":"3.22","rev":"3.22","proto_major":3,"proto_minor":14}
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/serial0","activated":"2026-03-07T20:06:30.467Z","native":0,"bps":115200,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":false,"nmea":false,"raw":2,"scaled":false,"timing":false,"split24":false,"pps":false}
```

# Test Results 2026-03-08
- status_keys: FAIL (missing_modules=['gps'])
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- gps_status: FAIL (gps_ok_not_false)
- placeholders_status: PASS (ok)
- health_keys: FAIL (missing_modules=['gps'])
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- gps_health: FAIL (gps_health_ok_not_false)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=23 PASS=19 FAIL=4 SKIP=0

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- gps_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- gps_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=23 PASS=23 FAIL=0 SKIP=0

## PHASE STEP 5 — GPS CONFIG + VALIDATION

### /etc/default/gpsd
```
START_DAEMON="true"
GPSD_OPTIONS="-n -s 115200"
DEVICES="/dev/serial0"
USBAUTO="false"
```

### configure_ublox_gnss.py (attempt)
```
Using port: /dev/serial0 @ 115200
ERROR: No CFG-GNSS response from receiver
```

### gpspipe -w -n 10 (timeout 8s)
```
{"class":"VERSION","release":"3.22","rev":"3.22","proto_major":3,"proto_minor":14}
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/serial0","activated":"2026-03-07T20:16:51.747Z","native":0,"bps":115200,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}
```

### gpspipe -R -n 10 (timeout 8s)
```
{"class":"VERSION","release":"3.22","rev":"3.22","proto_major":3,"proto_minor":14}
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/serial0","activated":"2026-03-07T20:16:51.747Z","native":0,"bps":115200,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":false,"nmea":false,"raw":2,"scaled":false,"timing":false,"split24":false,"pps":false}
```

### /api/v1/status gps module
```
{
  "ok": false,
  "last_update_ms": null,
  "last_error": "GPS_NO_DATA",
  "latitude": null,
  "longitude": null,
  "altitude_m": null,
  "speed_mps": null,
  "heading_deg": null,
  "fix_mode": null
}
```

### pytest -q
```
24 passed, 2 warnings in 3.11s
```

### scripts/run_evidence.py
```
SUMMARY Total=23 PASS=23 FAIL=0 SKIP=0
```

# Test Results 2026-03-08
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: PASS (ok)
- gps_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: PASS (ok)
- gps_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- alerts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=23 PASS=23 FAIL=0 SKIP=0
