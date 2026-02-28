# N-Defender Unified Backend Contract v1 (Phase A)

## Event Envelope
All events follow:

```
{ "type": "...", "timestamp_ms": 0, "source": "...", "data": {} }
```

## REST API
Base: `/api/v1`

### GET `/status`
Always 200.

Response:
```
{
  "timestamp_ms": 0,
  "overall_ok": false,
  "system": {},
  "modules": {
    "ups": {"ok": false, "last_update_ms": null, "detail": null},
    "os": {"ok": false, "last_update_ms": null, "detail": null},
    "esp32": {"ok": false, "last_update_ms": null, "detail": null},
    "antsdr": {"ok": false, "last_update_ms": null, "detail": null},
    "remoteid": {"ok": false, "last_update_ms": null, "detail": null},
    "video": {"ok": false, "last_update_ms": null, "detail": null}
  }
}
```

### GET `/health`
Always 200. Same module keys as `/status`.

```
{
  "timestamp_ms": 0,
  "overall_ok": false,
  "modules": { ... }
}
```

### GET `/contacts`
Always 200.

```
{ "contacts": [] }
```

### POST `/commands`
Accepts:
```
{ "timestamp_ms": 0, "command": "...", "confirm": false, "payload": {} }
```

Phase A behavior:
- Always returns HTTP 409
```
{ "detail": "precondition_failed", "code": "NOT_IMPLEMENTED" }
```

## WebSocket
### WS `/ws`
On connect, immediately sends a `HELLO` event envelope.
