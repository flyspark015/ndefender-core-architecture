# Progress

## Phase A
- Created new unified backend repo and Python venv
- Implemented event envelope, in-process bus, and in-memory state store
- Implemented REST and WS endpoints
- Added evidence runner and pytest coverage
- Added Phase A contract documentation
- Evidence runner PASS; Phase A locked on 2026-02-28

## Phase A.2
Before:
- No systemd unit for unified backend

After:
- Added systemd unit + installer script
- Commands:
  sudo systemctl enable --now ndefender-unified.service
  sudo systemctl restart ndefender-unified.service
  systemctl status ndefender-unified --no-pager

Proof:
- `systemctl status ndefender-unified --no-pager`
- `curl http://127.0.0.1:8000/api/v1/health`
- `pytest -q`
- `python3 scripts/run_evidence.py`

## Phase B
Before:
- Contract only defined basic Phase A endpoints
- Status/health modules had minimal schema checks

After:
- Expanded CONTRACT_V1 with per-module TX/RX contracts
- Added explicit per-module status/health models
- Strengthened tests and evidence schema checks

Proof:
- `pytest -q`
- `python3 scripts/run_evidence.py`

## Phase C.1
Before:
- system status was empty
- os module fields were null placeholders only

After:
- OS module uses real Pi telemetry (cpu/mem/disk/uptime/temp)
- system status populated from OS telemetry
- OS health populated (hostname/os/kernel/time sync)
- Evidence runner adds OS populated check

Proof:
- `pytest -q`
- `python3 scripts/run_evidence.py`
- `curl -sS http://127.0.0.1:8000/api/v1/status | head`
- `curl -sS http://127.0.0.1:8000/api/v1/health | head`

## Phase C.2 (UPS HAT E)
Before:
- UPS module placeholders only (ok=false, last_error=not_implemented)
- No UPS I2C polling in backend

Change:
- Added UPS HAT (E) I2C reader and poll loop (1.5s)
- UPS status/health populated with real values
- Evidence/test assertions enforce UPS health + real readings

After:
- `/api/v1/status` reports UPS measurements and ok=true
- `/api/v1/health` reports UPS comms_ok=true and model

Proof:
- `pytest -q`
- `python3 scripts/run_evidence.py`
- `curl -sS http://127.0.0.1:8000/api/v1/status | head -c 800 ; echo`
- `curl -sS http://127.0.0.1:8000/api/v1/health | head -c 800 ; echo`

Before:
- PASS could still show placeholder modules without explanation

After:
- Non-OS modules return deterministic `last_error=not_implemented`
- Evidence/tests assert OS ok=true and placeholders ok=false

Proof:
- `pytest -q`
- `python3 scripts/run_evidence.py`
- `curl -sS http://127.0.0.1:8000/api/v1/status | head`
- `curl -sS http://127.0.0.1:8000/api/v1/health | head`

## Next
- Phase C.2 module implementations (ups/esp32/antsdr/remoteid/video)

## Phase C.3 (ESP32 Module)
### STEP 0 — BEFORE
A) Repo check:
```
/home/toybook/ndefender-unified-backend
total 40
drwxr-xr-x  9 toybook toybook 4096 Feb 28 23:50 .
drwx------ 30 toybook toybook 4096 Mar  5 03:51 ..
drwxr-xr-x  8 toybook toybook 4096 Mar  1 00:57 .git
-rw-r--r--  1 toybook toybook   51 Feb 28 23:50 .gitignore
drwxr-xr-x  3 toybook toybook 4096 Feb 28 23:50 .pytest_cache
drwxr-xr-x  5 toybook toybook 4096 Feb 28 23:48 .venv
drwxr-xr-x  4 toybook toybook 4096 Mar  1 00:06 app
drwxr-xr-x  2 toybook toybook 4096 Mar  1 00:01 docs
drwxr-xr-x  2 toybook toybook 4096 Feb 28 23:58 scripts
drwxr-xr-x  3 toybook toybook 4096 Mar  1 00:42 tests
```

B) Service + endpoints:
```
● ndefender-unified.service - N-Defender Unified Backend (FastAPI)
     Loaded: loaded (/etc/systemd/system/ndefender-unified.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-03-04 20:11:26 IST; 7h ago
   Main PID: 938 (python)
      Tasks: 3 (limit: 19359)
        CPU: 2.093s
     CGroup: /system.slice/ndefender-unified.service
             └─938 /home/toybook/ndefender-unified-backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

Mar 05 03:29:57 ndefender-pi python[938]: INFO:     127.0.0.1:48590 - "GET /?kiosk=1 HTTP/1.1" 404 Not Found
Mar 05 03:29:57 ndefender-pi python[938]: INFO:     127.0.0.1:48590 - "GET /favicon.ico HTTP/1.1" 404 Not Found
Mar 05 03:49:49 ndefender-pi python[938]: INFO:     127.0.0.1:49200 - "GET /api/v1/status HTTP/1.1" 200 OK
Mar 05 03:49:59 ndefender-pi python[938]: INFO:     127.0.0.1:47442 - "GET /api/v1/status HTTP/1.1" 200 OK
Mar 05 03:50:07 ndefender-pi python[938]: INFO:     127.0.0.1:51904 - "GET /api/v1/health HTTP/1.1" 200 OK
Mar 05 03:50:15 ndefender-pi python[938]: INFO:     127.0.0.1:34070 - "WebSocket /api/v1/ws" [accepted]
Mar 05 03:50:15 ndefender-pi python[938]: INFO:     connection open
Mar 05 03:50:26 ndefender-pi python[938]: INFO:     connection closed
Mar 05 03:50:27 ndefender-pi python[938]: INFO:     127.0.0.1:46100 - "POST /api/v1/commands HTTP/1.1" 422 Unprocessable Entity
Mar 05 03:50:36 ndefender-pi python[938]: INFO:     127.0.0.1:40566 - "GET /api/v1/status HTTP/1.1" 200 OK
```

`/api/v1/health`:
```
{"timestamp_ms":1772663586189,"overall_ok":false,"modules":{"ups":{"ok":true,"last_update_ms":1772663586007,"last_error":null,"comms_ok":true,"model":"Waveshare UPS HAT (E)","serial":null,"firmware_version":null},"os":{"ok":true,"last_update_ms":1772663586189,"last_error":null,"hostname":"ndefender-pi","os_version":"Debian GNU/Linux 12 (bookworm)","kernel_version":"6.12.62+rpt-rpi-2712","time_sync_ok":null},"esp32":{"ok":false,"last_update_ms":null,"last_error":"not_implemented","comms_ok":null},"antsdr":{"ok":false,"last_update_ms":null,"last_error":"not_implemented","device_present":null,"driver_ok":null},"remoteid":{"ok":false,"last_update_ms":null,"last_error":"not_implemented","receiver_ok":null,"gps_ok":null},"video":{"ok":false,"last_update_ms":null,"last_error":"not_implemented","encoder_ok":null,"camera_ok":null}}}
HTTP_STATUS:200
```

`/api/v1/status` (head -c 800):
```
{"timestamp_ms":1772663586407,"overall_ok":false,"system":{"timestamp_ms":1772663586200,"cpu_temp_c":37.5,"cpu_percent":11.4,"mem_used_mb":1027.859375,"mem_total_mb":16215.046875,"disk_used_mb":64951.68359375,"disk_total_mb":119404.86328125,"uptime_s":2142},"modules":{"ups":{"ok":true,"last_update_ms":1772663586007,"last_error":null,"battery_percent":95.0,"battery_voltage_v":16.562,"battery_current_a":0.604,"remaining_capacity_mah":4518.0,"cell_voltages_v":[4.145,4.14,4.135,4.141],"vbus_voltage_v":14.959,"vbus_current_a":1.718,"vbus_power_w":25.754,"state":"discharging","input_voltage_v":null,"output_voltage_v":null,"load_percent":null,"temperature_c":null,"runtime_s":1440.0,"on_battery":null},"os":{"ok":true,"last_update_ms":1772663586200,"last_error":null,"cpu_temp_c":37.5,"cpu_percent":
```

C) Serial detection:
```
lrwxrwxrwx 1 root root 7 Mar  4 19:17 /dev/serial0 -> ttyAMA0
```

D) Evidence runner:
```
total 24
drwxr-xr-x 2 toybook toybook  4096 Feb 28 23:58 .
drwxr-xr-x 9 toybook toybook  4096 Feb 28 23:50 ..
-rwxr-xr-x 1 toybook toybook   597 Feb 28 23:58 install_systemd.sh
-rw-r--r-- 1 toybook toybook 11514 Mar  1 00:42 run_evidence.py
Traceback (most recent call last):
  File "/home/toybook/ndefender-unified-backend/scripts/run_evidence.py", line 10, in <module>
    import httpx
ModuleNotFoundError: No module named 'httpx'
```

### STEP 1 — ESP32 Module Baseline
Change:
- Added ESP32 serial reader + background poller
- ESP32 status/health now report deterministic "ESP32_SERIAL_NOT_CONNECTED" when missing
- Evidence/tests updated to assert ESP32 missing state

After (proof):
- `pytest -q`
```
4 passed, 2 warnings in 0.49s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=12 PASS=12 FAIL=0 SKIP=0
```
- `/api/v1/health` (head -c 600):
```
{"timestamp_ms":1772663927444,"overall_ok":false,"modules":{"ups":{"ok":true,"last_update_ms":1772663926430,"last_error":null,"comms_ok":true,"model":"Waveshare UPS HAT (E)","serial":null,"firmware_version":null},"os":{"ok":true,"last_update_ms":1772663927444,"last_error":null,"hostname":"ndefender-pi","os_version":"Debian GNU/Linux 12 (bookworm)","kernel_version":"6.12.62+rpt-rpi-2712","time_sync_ok":true},"esp32":{"ok":false,"last_update_ms":null,"last_error":"ESP32_SERIAL_NOT_CONNECTED","comms_ok":false},"antsdr":{"ok":false,"last_update_ms":null,"last_error":"not_implemented","device_prese
```
- `/api/v1/status` (head -c 600):
```
{"timestamp_ms":1772663927507,"overall_ok":false,"system":{"timestamp_ms":1772663927456,"cpu_temp_c":40.25,"cpu_percent":18.2,"mem_used_mb":1049.15625,"mem_total_mb":16215.046875,"disk_used_mb":64953.05078125,"disk_total_mb":119404.86328125,"uptime_s":2483},"modules":{"ups":{"ok":true,"last_update_ms":1772663926430,"last_error":null,"battery_percent":96.0,"battery_voltage_v":16.658,"battery_current_a":0.681,"remaining_capacity_mah":4581.0,"cell_voltages_v":[4.17,4.164,4.158,4.166],"vbus_voltage_v":14.953,"vbus_current_a":1.728,"vbus_power_w":25.908,"state":"discharging","input_voltage_v":null,
```

### STEP 2 — Commands + WS COMMAND_ACK
Change:
- /api/v1/commands accepts missing timestamp_ms (server fills)
- COMMAND_ACK events emitted on command attempts
- WebSocket sender handles clean close

After (proof):
- `pytest -q`
```
4 passed, 2 warnings in 1.61s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=12 PASS=12 FAIL=0 SKIP=0
```

### STEP 3 — WS Telemetry Events
Change:
- ESP32 telemetry now emits TELEMETRY_UPDATE events

After (proof):
- `pytest -q`
```
4 passed, 2 warnings in 0.48s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=12 PASS=12 FAIL=0 SKIP=0
```

### STEP 4 — ESP32 Tests (No Hardware)
Change:
- Added unit tests for missing serial and COMMAND_ACK behavior

After (proof):
- `pytest -q`
```
6 passed, 2 warnings in 0.48s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=12 PASS=12 FAIL=0 SKIP=0
```

### STEP 5 — After Proof
- `pytest -q`
```
6 passed, 2 warnings in 0.49s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=12 PASS=12 FAIL=0 SKIP=0
```
- `/api/v1/status` (head -c 900):
```
{"timestamp_ms":1772664329237,"overall_ok":false,"system":{"timestamp_ms":1772664329181,"cpu_temp_c":39.15,"cpu_percent":1.2,"mem_used_mb":1130.703125,"mem_total_mb":16215.046875,"disk_used_mb":64953.46875,"disk_total_mb":119404.86328125,"uptime_s":2885},"modules":{"ups":{"ok":true,"last_update_ms":1772664327798,"last_error":null,"battery_percent":97.0,"battery_voltage_v":16.703,"battery_current_a":0.38,"remaining_capacity_mah":4643.0,"cell_voltages_v":[4.179,4.176,4.17,4.177],"vbus_voltage_v":14.985,"vbus_current_a":1.392,"vbus_power_w":20.912,"state":"discharging","input_voltage_v":null,"output_voltage_v":null,"load_percent":null,"temperature_c":null,"runtime_s":660.0,"on_battery":null},"os":{"ok":true,"last_update_ms":1772664329181,"last_error":null,"cpu_temp_c":39.15,"cpu_percent":1.2,"mem_used_mb":1130.703125,"mem_total_mb":16215.046875,"disk_used_mb":64953.46875,"disk_total_mb":119
```
- `/api/v1/health` (head -c 900):
```
{"timestamp_ms":1772664329301,"overall_ok":false,"modules":{"ups":{"ok":true,"last_update_ms":1772664327798,"last_error":null,"comms_ok":true,"model":"Waveshare UPS HAT (E)","serial":null,"firmware_version":null},"os":{"ok":true,"last_update_ms":1772664329301,"last_error":null,"hostname":"ndefender-pi","os_version":"Debian GNU/Linux 12 (bookworm)","kernel_version":"6.12.62+rpt-rpi-2712","time_sync_ok":true},"esp32":{"ok":false,"last_update_ms":null,"last_error":"ESP32_SERIAL_NOT_CONNECTED","comms_ok":false},"antsdr":{"ok":false,"last_update_ms":null,"last_error":"not_implemented","device_present":null,"driver_ok":null},"remoteid":{"ok":false,"last_update_ms":null,"last_error":"not_implemented","receiver_ok":null,"gps_ok":null},"video":{"ok":false,"last_update_ms":null,"last_error":"not_implemented","encoder_ok":null,"camera_ok":null}}}
```
- ESP32 precondition command:
```
{"detail":"precondition_failed","code":"ESP32_SERIAL_NOT_CONNECTED"}
HTTP_STATUS:409
```

## Phase C.3.1 — ESP32 Auto Port Detect
### BEFORE
```
BYID []
ACM []
USB []
```

### CHANGE
- Added ESP32 auto port detection (by-id -> ttyACM -> ttyUSB)
- Added throttled logging for port selection/failures
- Added tests for auto-detect preference

### AFTER (proof)
- `pytest -q`
```
7 passed, 2 warnings in 1.64s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=12 PASS=12 FAIL=0 SKIP=0
```
- `curl -sS http://127.0.0.1:8000/api/v1/status | jq '.modules.esp32'`
```
{
  "ok": false,
  "last_update_ms": null,
  "last_error": "ESP32_SERIAL_NOT_CONNECTED",
  "connected": false,
  "firmware_version": null,
  "rssi_dbm": null,
  "supply_voltage_v": null,
  "temperature_c": null
}
```

### Future Firmware Update (not implemented)
- Preferred: `esptool.py` or PlatformIO
- Firmware repo: `ndefender-esp32` (external, not in this repo)
