# Test Results 2026-03-06
- status_keys: PASS (ok)
- os_populated: PASS (ok)
- ups_populated: PASS (ok)
- esp32_status: PASS (ok)
- antsdr_status: PASS (ok)
- placeholders_status: PASS (ok)
- health_keys: PASS (ok)
- os_health: PASS (ok)
- ups_health: PASS (ok)
- esp32_health: PASS (ok)
- antsdr_health: PASS (ok)
- placeholders_health: PASS (ok)
- contacts_keys: PASS (ok)
- ws_hello: PASS (ok)

SUMMARY Total=14 PASS=14 FAIL=0 SKIP=0

# PHASE C.5 STEP 0 BEFORE
- `git log -1 --oneline`
```
5d2a634 docs: lock esp32 module
```
- `systemctl status ndefender-unified --no-pager || true`
```
● ndefender-unified.service - N-Defender Unified Backend (FastAPI)
     Loaded: loaded (/etc/systemd/system/ndefender-unified.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-03-06 02:52:50 IST; 5min ago
   Main PID: 18850 (python)
      Tasks: 5 (limit: 19359)
        CPU: 1.636s
     CGroup: /system.slice/ndefender-unified.service
             └─18850 /home/toybook/ndefender-unified-backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

Mar 06 02:53:55 ndefender-pi python[18850]: INFO:     127.0.0.1:47524 - "GET /api/v1/contacts HTTP/1.1" 200 OK
Mar 06 02:53:55 ndefender-pi python[18850]: INFO:     127.0.0.1:47526 - "WebSocket /api/v1/ws" [accepted]
Mar 06 02:53:55 ndefender-pi python[18850]: INFO:     connection open
Mar 06 02:53:55 ndefender-pi python[18850]: INFO:     connection closed
Mar 06 02:54:29 ndefender-pi python[18850]: INFO:     127.0.0.1:43130 - "GET /api/v1/status HTTP/1.1" 200 OK
Mar 06 02:54:29 ndefender-pi python[18850]: INFO:     127.0.0.1:43130 - "GET /api/v1/health HTTP/1.1" 200 OK
Mar 06 02:54:29 ndefender-pi python[18850]: INFO:     127.0.0.1:43130 - "GET /api/v1/contacts HTTP/1.1" 200 OK
Mar 06 02:54:29 ndefender-pi python[18850]: INFO:     127.0.0.1:43142 - "WebSocket /api/v1/ws" [accepted]
Mar 06 02:54:29 ndefender-pi python[18850]: INFO:     connection open
Mar 06 02:54:29 ndefender-pi python[18850]: INFO:     connection closed
```
- `ip a | head -n 120`
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
3: wlan0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 28:0c:50:a3:1d:da brd ff:ff:ff:ff:ff:ff
4: wlan1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 88:a2:9e:0c:5a:23 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.35/24 brd 192.168.1.255 scope global noprefixroute wlan1
       valid_lft forever preferred_lft forever
    inet6 2401:4900:8fed:57cb:84:5db1:6c9f:c868/64 scope global deprecated dynamic noprefixroute 
       valid_lft 31937sec preferred_lft 0sec
    inet6 2401:4900:8fee:f593:2290:d377:4376:2372/64 scope global deprecated dynamic noprefixroute 
       valid_lft 33888sec preferred_lft 0sec
    inet6 2401:4900:8fee:ffd9:d86:5c76:2bb3:48e6/64 scope global deprecated dynamic noprefixroute 
       valid_lft 49143sec preferred_lft 0sec
    inet6 2401:4900:8fef:3eea:a668:4bfa:465b:24df/64 scope global dynamic noprefixroute 
       valid_lft 86275sec preferred_lft 86275sec
    inet6 fe80::ca6b:3cbc:d1bb:efe6/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
5: tailscale0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1280 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 100.99.78.121/32 scope global tailscale0
       valid_lft forever preferred_lft forever
    inet6 fd7a:115c:a1e0::6001:4e8f/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::c3f1:acd4:f05a:d9aa/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
```
- `ip r`
```
default via 192.168.1.1 dev wlan1 proto static metric 600 
192.168.1.0/24 dev wlan1 proto kernel scope link src 192.168.1.35 metric 600 
192.168.10.0/24 dev eth0 proto kernel scope link src 192.168.10.1 metric 100 
```
- `ls -la /dev/iio* 2>/dev/null || true`
```
```
- `python3 -c "import adi,sys; print('pyadi-iio ok')" || echo "pyadi-iio missing"`
```
pyadi-iio ok
```
- `ping -c 1 192.168.10.2 || true`
```
PING 192.168.10.2 (192.168.10.2) 56(84) bytes of data.
64 bytes from 192.168.10.2: icmp_seq=1 ttl=64 time=0.414 ms

--- 192.168.10.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.414/0.414/0.414/0.000 ms
```
- `curl -sS http://127.0.0.1:8000/api/v1/status | jq '.modules.antsdr'`
```
{
  "ok": false,
  "last_update_ms": null,
  "last_error": "not_implemented",
  "center_freq_hz": null,
  "sample_rate_hz": null,
  "gain_db": null,
  "rf_power_dbm": null,
  "stream_active": null
}
```
- `curl -sS http://127.0.0.1:8000/api/v1/health | jq '.modules.antsdr'`
```
{
  "ok": false,
  "last_update_ms": null,
  "last_error": "not_implemented",
  "device_present": null,
  "driver_ok": null
}
```

# PHASE C.5 STEP 3 GATES
- `pytest -q`
```
..........                                                            [100%]
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
13 passed, 2 warnings in 1.62s
```
- `python3 scripts/run_evidence.py`
```
SUMMARY Total=14 PASS=14 FAIL=0 SKIP=0
```
