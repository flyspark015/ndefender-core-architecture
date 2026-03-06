# Test Results 2026-03-06
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

# PHASE C.6 STEP 0 BEFORE
- `systemctl status ndefender-unified --no-pager`
```
● ndefender-unified.service - N-Defender Unified Backend (FastAPI)
     Loaded: loaded (/etc/systemd/system/ndefender-unified.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-03-06 16:13:50 IST; 8h ago
   Main PID: 948 (python)
      Tasks: 6 (limit: 19359)
        CPU: 1.405s
     CGroup: /system.slice/ndefender-unified.service
             └─948 /home/toybook/ndefender-unified-backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

Mar 06 16:13:53 ndefender-pi python[948]: INFO:     Started server process [948]
Mar 06 16:13:53 ndefender-pi python[948]: INFO:     Waiting for application startup.
Mar 06 16:13:53 ndefender-pi python[948]: esp32 serial candidates: ['/dev/serial/by-id/usb-1a86_USB_Single_Serial_58FB009763-if00']
Mar 06 16:13:53 ndefender-pi python[948]: INFO:     Application startup complete.
Mar 06 16:13:53 ndefender-pi python[948]: INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
- `curl -sS http://127.0.0.1:8000/api/v1/health | jq '.modules.antsdr'`
```
{
  "ok": false,
  "last_update_ms": null,
  "last_error": "ANTSDR_NOT_CONNECTED",
  "device_present": false,
  "driver_ok": false
}
```
- `iio_info -s`
```
Unable to create Local IIO context : No such file or directory (2)
Library version: 0.24 (git tag: v0.24)
Compiled with backends: local xml ip usb
Available contexts:
	0: 192.168.10.2 (Analog Devices ANTSDR Rev.C (Z7020-AD9364)), serial= [ip:ant.local]
```
- `python3 - <<'PY' ...` (iio context check)
```
iio_ctx_ok network
devices 5
```
- `ip addr show | head -n 80`
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 88:a2:9e:0c:5a:22 brd ff:ff:ff:ff:ff:ff
    inet 192.168.10.1/24 brd 192.168.10.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::8aa2:9eff:fe0c:5a22/64 scope link 
       valid_lft forever preferred_lft forever
3: wlan0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN group default qlen 1000
    link/ether 88:a2:9e:0c:5a:23 brd ff:ff:ff:ff:ff:ff
4: wlan1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 28:0c:50:a3:1d:da brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.35/24 brd 192.168.1.255 scope global noprefixroute wlan1
       valid_lft forever preferred_lft forever
    inet6 2401:4900:8fef:3eea:a668:4bfa:465b:24df/64 scope global dynamic noprefixroute 
       valid_lft 86143sec preferred_lft 86143sec
    inet6 fe80::ca6b:3cbc:d1bb:efe6/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
5: tailscale0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1280 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 100.99.78.121/32 scope global tailscale0
       valid_lft forever preferred_lft forever
    inet6 fd7a:115c:a1e0::6001:4e8f/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::f73e:843a:837b:7c28/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
```
- `ls -la /dev/iio* /sys/bus/iio/devices || true`
```
ls: cannot access '/dev/iio*': No such file or directory
ls: cannot access '/sys/bus/iio/devices': No such file or directory
```
# PHASE D.2 STEP 3 GATES (latest)
- `pytest -q`
```
...................                                                      [100%]
=============================== warnings summary ===============================
app/main.py:23
  /home/toybook/ndefender-unified-backend/app/main.py:23: DeprecationWarning: 
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
19 passed, 2 warnings in 0.52s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0
```

# PHASE D.1 STEP 3 GATES (latest)
- `pytest -q`
```
...............                                                       [100%]
=============================== warnings summary ===============================
app/main.py:23
  /home/toybook/ndefender-unified-backend/app/main.py:23: DeprecationWarning: 
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
18 passed, 2 warnings in 1.67s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0
```

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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
- contacts_keys: FAIL (contacts_not_list)
- ws_hello: PASS (ok)

SUMMARY Total=18 PASS=17 FAIL=1 SKIP=0

# PHASE D.2 STEP 3 GATES
- `pytest -q`
```
................                                                      [100%]
=============================== warnings summary ===============================
app/main.py:23
  /home/toybook/ndefender-unified-backend/app/main.py:23: DeprecationWarning: 
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
19 passed, 2 warnings in 1.71s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=18 PASS=18 FAIL=0 SKIP=0
```

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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

# Test Results 2026-03-06
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
