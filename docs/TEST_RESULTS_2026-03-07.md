# Test Results 2026-03-07
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0

# Test Results 2026-03-07
- status_keys: FAIL (missing_fields=antsdr:['driver_ok', 'device_present', 'rf_bw_hz', 'noise_floor_dbm'])
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: FAIL (antsdr_device_present_not_false)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=18 PASS=16 FAIL=2 SKIP=0

# Test Results 2026-03-07
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0

# Test Results 2026-03-07
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0

# PHASE C.6 STEP 3 GATES

$ . .venv/bin/activate && pytest -q
.....................                                                    [100%]
=============================== warnings summary ===============================
app/main.py:25
  /home/toybook/ndefender-unified-backend/app/main.py:25: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    @app.on_event("startup")

.venv/lib/python3.11/site-packages/fastapi/applications.py:4599
  /home/toybook/ndefender-unified-backend/.venv/lib/python3.11/site-packages/fastapi/applications.py:4599: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    return self.router.on_event(event_type)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
21 passed, 2 warnings in 0.63s

$ . .venv/bin/activate && python3 scripts/run_evidence.py
SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0

# PHASE C.6 STEP 5 AFTER (ANTS DR LIVE)

$ systemctl status ndefender-unified --no-pager
● ndefender-unified.service - N-Defender Unified Backend (FastAPI)
     Loaded: loaded (/etc/systemd/system/ndefender-unified.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-03-07 00:49:10 IST; 33s ago
   Main PID: 4323 (python)
      Tasks: 8 (limit: 19359)
        CPU: 745ms
     CGroup: /system.slice/ndefender-unified.service
             └─4323 /home/toybook/ndefender-unified-backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

Mar 07 00:49:10 ndefender-pi python[4323]: INFO:     Waiting for application startup.
Mar 07 00:49:10 ndefender-pi python[4323]: esp32 serial candidates: ['/dev/serial/by-id/usb-1a86_USB_Single_Serial_58FB009763-if00']
Mar 07 00:49:10 ndefender-pi python[4323]: INFO:     Application startup complete.
Mar 07 00:49:10 ndefender-pi python[4323]: INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
Mar 07 00:49:14 ndefender-pi python[4323]: INFO:     127.0.0.1:58644 - "GET /api/v1/status HTTP/1.1" 200 OK
Mar 07 00:49:14 ndefender-pi python[4323]: INFO:     127.0.0.1:58644 - "GET /api/v1/health HTTP/1.1" 200 OK
Mar 07 00:49:14 ndefender-pi python[4323]: INFO:     127.0.0.1:58644 - "GET /api/v1/contacts HTTP/1.1" 200 OK
Mar 07 00:49:14 ndefender-pi python[4323]: INFO:     127.0.0.1:58652 - "WebSocket /api/v1/ws" [accepted]
Mar 07 00:49:14 ndefender-pi python[4323]: INFO:     connection open
Mar 07 00:49:14 ndefender-pi python[4323]: INFO:     connection closed

$ curl -sS http://127.0.0.1:8000/api/v1/health | jq '.modules.antsdr'
{
  "ok": true,
  "last_update_ms": 1772824824354,
  "last_error": null,
  "device_present": true,
  "driver_ok": true
}

$ curl -sS http://127.0.0.1:8000/api/v1/status | jq '.modules.antsdr'
{
  "ok": true,
  "last_update_ms": 1772824882363,
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

$ python3 - <<'PY'
import asyncio
import httpx
import websockets

WS_URL = "ws://127.0.0.1:8000/api/v1/ws"
CMD_URL = "http://127.0.0.1:8000/api/v1/commands"

async def main():
    async with websockets.connect(WS_URL) as ws:
        print(await ws.recv())
        async with httpx.AsyncClient() as client:
            r = await client.post(CMD_URL, json={"command": "antsdr/start", "payload": {}, "confirm": False})
            print(f"start_status {r.status_code} {r.text}")
        for _ in range(6):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=3)
            except Exception as exc:
                print(f"timeout {exc}")
                break
            print(msg)

asyncio.run(main())
PY
{"type":"HELLO","timestamp_ms":1772824865948,"source":"core","data":{}}
start_status 200 {"ok":true}
{"type":"RF_SCAN_STATE","timestamp_ms":1772824866031,"source":"antsdr","data":{"active":true}}
{"type":"COMMAND_ACK","timestamp_ms":1772824866031,"source":"antsdr","data":{"command":"antsdr/start","ok":true,"code":"OK","detail":"ok","timestamp_ms":1772824866031}}
{"type":"TELEMETRY_UPDATE","timestamp_ms":1772824866200,"source":"esp32","data":{"device_uptime_ms":869363,"seq":870,"fw_version":"0.3.0","sel":1,"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":641},{"id":2,"freq_hz":5800000000,"rssi_raw":246},{"id":3,"freq_hz":5860000000,"rssi_raw":198}],"video":{"selected":1},"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":869363,"heap":337544},"raw":{"type":"telemetry","timestamp_ms":869363,"seq":870,"fw_version":"0.3.0","sel":1,"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":641},{"id":2,"freq_hz":5800000000,"rssi_raw":246},{"id":3,"freq_hz":5860000000,"rssi_raw":198}],"video":{"selected":1},"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":869363,"heap":337544}}}}
{"type":"RF_CONTACT_UPDATE","timestamp_ms":1772824866594,"source":"antsdr","data":{"contact_id":"rf:5645000000","center_freq_hz":5645000000,"last_seen_ms":1772824866594,"first_seen_ms":1772824844750,"peak_dbm":63.27059396787152,"snr_db":null,"band":"5.8g","timestamp_ms":1772824866594}}
{"type":"RF_CONTACT_LOST","timestamp_ms":1772824866594,"source":"antsdr","data":{"contact_id":"rf:5725000000","last_seen_ms":1772824850772}}
{"type":"RF_CONTACT_LOST","timestamp_ms":1772824866594,"source":"antsdr","data":{"contact_id":"rf:5765000000","last_seen_ms":1772824851362}}

# Test Results 2026-03-07
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0

# Test Results 2026-03-07
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0

# PHASE D.3 STEP 0 BEFORE

$ curl -sS http://127.0.0.1:8000/api/v1/status | jq '.modules'
{
  "ups": {
    "ok": true,
    "last_update_ms": 1772825296755,
    "last_error": null,
    "battery_percent": 92,
    "battery_voltage_v": 16.127,
    "battery_current_a": -0.858,
    "current_a": -0.858,
    "remaining_capacity_mah": 4398,
    "cell_voltages_v": [
      4.026,
      4.035,
      4.035,
      4.03
    ],
    "vbus_voltage_v": 15.161,
    "vbus_current_a": 0.002,
    "vbus_power_w": 0.038,
    "state": "discharging",
    "input_voltage_v": 15.161,
    "output_voltage_v": 16.127,
    "load_percent": null,
    "temperature_c": null,
    "runtime_s": 18480,
    "on_battery": false
  },
  "os": {
    "ok": true,
    "last_update_ms": 1772825296007,
    "last_error": null,
    "cpu_temp_c": 33.65,
    "cpu_percent": 0.6,
    "mem_used_mb": 1042,
    "mem_total_mb": 16215.046875,
    "disk_used_mb": 65049.30078125,
    "disk_total_mb": 119404.86328125,
    "uptime_s": 1283
  },
  "esp32": {
    "ok": true,
    "last_update_ms": 1772825296242,
    "last_error": null,
    "connected": true,
    "firmware_version": "0.3.0",
    "device_uptime_ms": 1299399,
    "seq": 1300,
    "rssi_dbm": null,
    "supply_voltage_v": null,
    "temperature_c": null
  },
  "antsdr": {
    "ok": true,
    "last_update_ms": 1772825296435,
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
  },
  "remoteid": {
    "ok": false,
    "last_update_ms": null,
    "last_error": "REMOTEID_NO_DATA",
    "active_contacts": 0
  },
  "fusion": {
    "ok": true,
    "last_update_ms": 1772825296242,
    "last_error": null,
    "active_contacts": 0
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

$ curl -sS http://127.0.0.1:8000/api/v1/contacts | jq '.[0:3]'
[]

# Test Results 2026-03-07
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0

# Test Results 2026-03-07
- status_keys: FAIL (missing_modules=['alerts'])
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- remoteid_status: PASS (ok)
- fusion_status: PASS (ok)
- alerts_status: FAIL (alerts_ok_not_true)
- placeholders_status: PASS (ok)
- health_keys: FAIL (missing_modules=['alerts'])
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- remoteid_health: PASS (ok)
- fusion_health: PASS (ok)
- alerts_health: FAIL (alerts_health_ok_not_true)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=20 PASS=16 FAIL=4 SKIP=0

# Test Results 2026-03-07
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
- ws_hello: PASS (ok)

SUMMARY Total=20 PASS=20 FAIL=0 SKIP=0

# PHASE D.3 STEP 2 GATES

$ . .venv/bin/activate && pytest -q
.................                                                  [100%]
=============================== warnings summary ===============================
app/main.py:25
  /home/toybook/ndefender-unified-backend/app/main.py:25: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    @app.on_event("startup")

.venv/lib/python3.11/site-packages/fastapi/applications.py:4599
  /home/toybook/ndefender-unified-backend/.venv/lib/python3.11/site-packages/fastapi/applications.py:4599: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    return self.router.on_event(event_type)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
23 passed, 2 warnings in 1.83s

$ . .venv/bin/activate && python3 scripts/run_evidence.py
SUMMARY Total=20 PASS=20 FAIL=0 SKIP=0

# PHASE D.3 STEP 3 AFTER

$ curl -sS http://127.0.0.1:8000/api/v1/status | jq '.modules.alerts'
{
  "ok": true,
  "active_alerts": 1,
  "last_update_ms": 1772825457236,
  "last_error": null
}

$ curl -sS http://127.0.0.1:8000/api/v1/alerts | jq '.[0:5]'
[
  {
    "alert_id": "alert:fusion:drone999",
    "contact_id": "fusion:drone999",
    "threat_score": 3,
    "severity": "high",
    "first_seen_ms": 1772825448462,
    "last_seen_ms": 1772825461236,
    "state": "active"
  }
]

$ python3 - <<'PY'
import asyncio
import json
import time
import websockets

WS_URL = "ws://127.0.0.1:8000/api/v1/ws"
PATH = "/opt/ndefender/logs/odid_wifi_sample.ek.jsonl"

async def main():
    async with websockets.connect(WS_URL) as ws:
        print(await ws.recv())
        payload = {
            "basic_id": "drone999",
            "lat": 22.304,
            "lon": 70.803,
            "alt": 121,
            "speed": 16,
            "heading": 181,
            "timestamp": int(time.time() * 1000),
        }
        with open(PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
        print("appended", payload)
        for _ in range(8):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=3)
            except Exception as exc:
                print(f"timeout {exc}")
                break
            print(msg)

asyncio.run(main())
PY
{"type":"HELLO","timestamp_ms":1772825447811,"source":"core","data":{}}
appended {'basic_id': 'drone999', 'lat': 22.304, 'lon': 70.803, 'alt': 121, 'speed': 16, 'heading': 181, 'timestamp': 1772825447812}
{"type":"TELEMETRY_UPDATE","timestamp_ms":1772825448237,"source":"esp32","data":{"device_uptime_ms":1451399,"seq":1452,"fw_version":"0.3.0","sel":1,"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":552},{"id":2,"freq_hz":5800000000,"rssi_raw":249},{"id":3,"freq_hz":5860000000,"rssi_raw":214}],"video":{"selected":1},"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":1451399,"heap":337544},"raw":{"type":"telemetry","timestamp_ms":1451399,"seq":1452,"fw_version":"0.3.0","sel":1,"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":552},{"id":2,"freq_hz":5800000000,"rssi_raw":249},{"id":3,"freq_hz":5860000000,"rssi_raw":214}],"video":{"selected":1},"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":1451399,"heap":337544}}}}
{"type":"CONTACT_UPDATE","timestamp_ms":1772825448237,"source":"fusion","data":{"contact_id":"fusion:drone123","type":"remoteid","remoteid_id":"drone123","rf_sources":[],"video_sources":["esp32"],"first_seen_ms":1772825427458,"last_seen_ms":1772825448237,"threat_score":2.0}}
{"type":"ALERT_UPDATE","timestamp_ms":1772825448237,"source":"alerts","data":{"alert_id":"alert:fusion:drone123","contact_id":"fusion:drone123","threat_score":3,"severity":"high","first_seen_ms":1772825427458,"last_seen_ms":1772825448237,"state":"active"}}
{"type":"CONTACT_NEW","timestamp_ms":1772825448462,"source":"remoteid","data":{"contact_id":"rid:drone999","basic_id":"drone999","lat":22.304,"lon":70.803,"alt_m":121.0,"speed_mps":16.0,"heading_deg":181.0,"first_seen_ms":1772825448462,"last_seen_ms":1772825448462}}
{"type":"CONTACT_NEW","timestamp_ms":1772825448462,"source":"fusion","data":{"contact_id":"fusion:drone999","type":"remoteid","remoteid_id":"drone999","rf_sources":[],"video_sources":[],"first_seen_ms":1772825448462,"last_seen_ms":1772825448462,"threat_score":1.0}}
{"type":"ALERT_NEW","timestamp_ms":1772825448462,"source":"alerts","data":{"alert_id":"alert:fusion:drone999","contact_id":"fusion:drone999","threat_score":2,"severity":"medium","first_seen_ms":1772825448462,"last_seen_ms":1772825448462,"state":"active"}}
{"type":"TELEMETRY_UPDATE","timestamp_ms":1772825449237,"source":"esp32","data":{"device_uptime_ms":1452399,"seq":1453,"fw_version":"0.3.0","sel":1,"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":549},{"id":2,"freq_hz":5800000000,"rssi_raw":246},{"id":3,"freq_hz":5860000000,"rssi_raw":211}],"video":{"selected":1},"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":1452399,"heap":337544},"raw":{"type":"telemetry","timestamp_ms":1452399,"seq":1453,"fw_version":"0.3.0","sel":1,"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":549},{"id":2,"freq_hz":5800000000,"rssi_raw":246},{"id":3,"freq_hz":5860000000,"rssi_raw":211}],"video":{"selected":1},"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":1452399,"heap":337544}}}}
{"type":"CONTACT_UPDATE","timestamp_ms":1772825449237,"source":"fusion","data":{"contact_id":"fusion:drone999","type":"remoteid","remoteid_id":"drone999","rf_sources":[],"video_sources":["esp32"],"first_seen_ms":1772825448462,"last_seen_ms":1772825449237,"threat_score":2.0}}

# Test Results 2026-03-07
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
- ws_hello: PASS (ok)

SUMMARY Total=20 PASS=20 FAIL=0 SKIP=0
