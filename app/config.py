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
ANTSDR_URI = os.getenv("NDEFENDER_ANTSDR_URI", "ip:192.168.10.2").strip()
ANTSDR_ENABLED = os.getenv("NDEFENDER_ANTSDR_ENABLED", "1").lower() in ("1", "true", "yes", "on")
ANTSDR_SWEEP_PLAN = os.getenv("NDEFENDER_ANTSDR_SWEEP_PLAN", "VTX_58").strip()
ANTSDR_STEP_HZ = int(os.getenv("NDEFENDER_ANTSDR_STEP_HZ", "2000000"))
ANTSDR_SAMPLE_RATE_HZ = int(os.getenv("NDEFENDER_ANTSDR_SAMPLE_RATE_HZ", "2000000"))
ANTSDR_RF_BW_HZ = int(os.getenv("NDEFENDER_ANTSDR_RF_BW_HZ", "2000000"))
ANTSDR_POLL_INTERVAL_S = float(os.getenv("NDEFENDER_ANTSDR_POLL_INTERVAL_S", "1.0"))
REMOTEID_EK_PATH = os.getenv(
    "NDEFENDER_REMOTEID_EK_PATH", "/opt/ndefender/logs/odid_wifi_sample.ek.jsonl"
).strip()
REMOTEID_TTL_S = float(os.getenv("NDEFENDER_REMOTEID_TTL_S", "15.0"))
REMOTEID_POLL_INTERVAL_S = float(os.getenv("NDEFENDER_REMOTEID_POLL_INTERVAL_S", "1.0"))
