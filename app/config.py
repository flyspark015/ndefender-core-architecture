from __future__ import annotations

import os

HOST = os.getenv("NDEFENDER_HOST", "127.0.0.1")
PORT = int(os.getenv("NDEFENDER_PORT", "8000"))
UPS_POLL_INTERVAL_S = float(os.getenv("NDEFENDER_UPS_POLL_INTERVAL_S", "1.5"))
UPS_FAKE = os.getenv("NDEFENDER_UPS_FAKE", "0") == "1"
ESP32_PORT = os.getenv("NDEFENDER_ESP32_PORT", "auto")
ESP32_BAUD = int(os.getenv("NDEFENDER_ESP32_BAUD", "115200"))
ESP32_READ_TIMEOUT_S = float(os.getenv("NDEFENDER_ESP32_READ_TIMEOUT_S", "1.0"))
ESP32_RECONNECT_S = float(os.getenv("NDEFENDER_ESP32_RECONNECT_S", "1.0"))
ANTSDR_URI = os.getenv("NDEFENDER_ANTSDR_URI", "").strip()
ANTSDR_POLL_INTERVAL_S = float(os.getenv("NDEFENDER_ANTSDR_POLL_INTERVAL_S", "2.0"))
