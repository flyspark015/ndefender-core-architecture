import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("NDEFENDER_UPS_FAKE", "1")
os.environ.setdefault("NDEFENDER_ESP32_PORTS", "/dev/ttyFAKE0")
