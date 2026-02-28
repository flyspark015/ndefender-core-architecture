from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from .bus import EventBus
from .models import CommandRequest, DeepHealth, EventEnvelope, StatusSnapshot, now_ms
from .state import STATE

app = FastAPI(title="N-Defender Unified Backend", version="0.1.0")
BUS = EventBus()

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
    return JSONResponse(
        status_code=409,
        content={"detail": "precondition_failed", "code": "NOT_IMPLEMENTED"},
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
    await websocket.send_json(hello.model_dump())
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        return
