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
