from __future__ import annotations

import asyncio
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple

import httpx
import websockets

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import HOST, PORT  # noqa: E402

BASE_URL = f"http://{HOST}:{PORT}"
WS_URL = f"ws://{HOST}:{PORT}/api/v1/ws"


def _check_keys(obj: Dict[str, Any], keys: List[str]) -> Tuple[bool, str]:
    missing = [k for k in keys if k not in obj]
    if missing:
        return False, f"missing_keys={missing}"
    return True, "ok"


def _check_modules(obj: Dict[str, Any]) -> Tuple[bool, str]:
    modules = obj.get("modules", {})
    required = ["ups", "os", "esp32", "antsdr", "remoteid", "video"]
    missing = [m for m in required if m not in modules]
    if missing:
        return False, f"missing_modules={missing}"
    return True, "ok"


async def _ws_hello_check() -> Tuple[bool, str]:
    try:
        async with websockets.connect(WS_URL, open_timeout=1, close_timeout=1) as ws:
            msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
            data = json.loads(msg)
            ok, detail = _check_keys(data, ["type", "timestamp_ms", "source", "data"])
            if not ok:
                return False, detail
            if data.get("type") != "HELLO":
                return False, f"type={data.get('type')}"
            return True, "ok"
    except Exception as exc:
        return False, f"error={exc}"


def run() -> int:
    results: List[Tuple[str, bool, str]] = []

    with httpx.Client(timeout=2.0) as client:
        try:
            r = client.get(f"{BASE_URL}/api/v1/status")
            ok, detail = _check_keys(r.json(), ["timestamp_ms", "overall_ok", "system", "modules"])
            if ok:
                ok, detail = _check_modules(r.json())
            results.append(("status_keys", ok, detail))
        except Exception as exc:
            results.append(("status_keys", False, f"error={exc}"))

        try:
            r = client.get(f"{BASE_URL}/api/v1/health")
            ok, detail = _check_keys(r.json(), ["timestamp_ms", "overall_ok", "modules"])
            if ok:
                ok, detail = _check_modules(r.json())
            results.append(("health_keys", ok, detail))
        except Exception as exc:
            results.append(("health_keys", False, f"error={exc}"))

        try:
            r = client.get(f"{BASE_URL}/api/v1/contacts")
            ok, detail = _check_keys(r.json(), ["contacts"])
            results.append(("contacts_keys", ok, detail))
        except Exception as exc:
            results.append(("contacts_keys", False, f"error={exc}"))

    ws_ok, ws_detail = asyncio.run(_ws_hello_check())
    results.append(("ws_hello", ws_ok, ws_detail))

    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    skipped = 0

    summary = f"SUMMARY Total={total} PASS={passed} FAIL={failed} SKIP={skipped}"

    report_lines = [f"# Test Results {date.today().isoformat()}"]
    for name, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        report_lines.append(f"- {name}: {status} ({detail})")
    report_lines.append("")
    report_lines.append(summary)

    report_path = Path("docs") / f"TEST_RESULTS_{date.today().isoformat()}.md"
    report_path.write_text("\n".join(report_lines) + "\n")

    print(summary)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run())
