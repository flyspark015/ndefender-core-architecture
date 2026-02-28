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

## Next
- Phase B contract expansion + module scaffolding
