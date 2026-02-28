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
