from __future__ import annotations

import os

HOST = os.getenv("NDEFENDER_HOST", "127.0.0.1")
PORT = int(os.getenv("NDEFENDER_PORT", "8000"))
UPS_POLL_INTERVAL_S = float(os.getenv("NDEFENDER_UPS_POLL_INTERVAL_S", "1.5"))
UPS_FAKE = os.getenv("NDEFENDER_UPS_FAKE", "0") == "1"
