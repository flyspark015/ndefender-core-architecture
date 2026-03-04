from __future__ import annotations

import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from .bus import EventBus
from .events import EVENT_HUB
from .models import CommandRequest, DeepHealth, EventEnvelope, StatusSnapshot, now_ms
from .state import STATE

app = FastAPI(title="N-Defender Unified Backend", version="0.1.0")
BUS = EventBus()

SUPPORTED_COMMANDS = {
    "video/select",
    "scan/start",
    "scan/stop",
    "vrx/tune",
}

@app.on_event("startup")
def _startup() -> None:
    STATE.start_pollers()

@app.get("/api/v1/status", response_model=StatusSnapshot)
def get_status() -> StatusSnapshot:
    STATE.start_pollers()
    STATE.refresh_os()
    return StatusSnapshot(**STATE.snapshot())


@app.get("/api/v1/health", response_model=DeepHealth)
def get_health() -> DeepHealth:
    STATE.start_pollers()
    STATE.refresh_os()
    return DeepHealth(**STATE.health())


@app.get("/api/v1/contacts")
def get_contacts():
    return STATE.contacts_snapshot()


@app.post("/api/v1/commands")
def post_commands(_req: CommandRequest):
    ts = _req.timestamp_ms or now_ms()
    command = _req.command
    payload = _req.payload or {}

    def emit_ack(ok: bool, code: str, detail: str) -> None:
        event = EventEnvelope(
            type="COMMAND_ACK",
            timestamp_ms=now_ms(),
            source="esp32",
            data={
                "command": command,
                "ok": ok,
                "code": code,
                "detail": detail,
                "timestamp_ms": ts,
            },
        )
        EVENT_HUB.publish(event.model_dump())

    if command not in SUPPORTED_COMMANDS:
        emit_ack(False, "NOT_IMPLEMENTED", "precondition_failed")
        return JSONResponse(
            status_code=409,
            content={"detail": "precondition_failed", "code": "NOT_IMPLEMENTED"},
        )

    if not STATE.esp32_connected():
        emit_ack(False, "ESP32_SERIAL_NOT_CONNECTED", "precondition_failed")
        return JSONResponse(
            status_code=409,
            content={"detail": "precondition_failed", "code": "ESP32_SERIAL_NOT_CONNECTED"},
        )

    try:
        STATE.esp32_send_command(command, payload, ts)
        emit_ack(True, "OK", "ok")
        return {"ok": True}
    except Exception:
        emit_ack(False, "ESP32_SERIAL_NOT_CONNECTED", "precondition_failed")
        return JSONResponse(
            status_code=409,
            content={"detail": "precondition_failed", "code": "ESP32_SERIAL_NOT_CONNECTED"},
        )


@app.websocket("/api/v1/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    hello = EventEnvelope(
        type="HELLO",
        timestamp_ms=now_ms(),
        source="core",
        data={},
    )
    queue = EVENT_HUB.subscribe()
    await websocket.send_json(hello.model_dump())

    async def sender() -> None:
        while True:
            event = await asyncio.to_thread(queue.get)
            if event is None:
                return
            try:
                await websocket.send_json(event)
            except WebSocketDisconnect:
                return
            except Exception:
                return

    sender_task = asyncio.create_task(sender())
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        return
    finally:
        EVENT_HUB.unsubscribe(queue)
        queue.put(None)
        try:
            await sender_task
        except Exception:
            return
