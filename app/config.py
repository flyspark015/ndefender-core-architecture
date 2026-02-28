from __future__ import annotations

import os

HOST = os.getenv("NDEFENDER_HOST", "127.0.0.1")
PORT = int(os.getenv("NDEFENDER_PORT", "8000"))
