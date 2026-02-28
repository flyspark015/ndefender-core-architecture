#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/home/toybook/ndefender-unified-backend"
UNIT_PATH="/etc/systemd/system/ndefender-unified.service"

sudo tee "$UNIT_PATH" >/dev/null <<'UNIT'
[Unit]
Description=N-Defender Unified Backend (FastAPI)
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/toybook/ndefender-unified-backend
ExecStart=/home/toybook/ndefender-unified-backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=2
User=toybook
Group=toybook

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl daemon-reload
