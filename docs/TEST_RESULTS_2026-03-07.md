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
