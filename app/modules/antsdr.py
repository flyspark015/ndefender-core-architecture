from __future__ import annotations

from typing import Optional, Tuple

from app.models import AntsdrHealth, AntsdrStatus, now_ms


def _import_adi():
    import adi  # type: ignore

    return adi


class AntsdrReader:
    def __init__(self, uri: str) -> None:
        self._uri = uri.strip()
        self._device = None
        self._last_error: Optional[str] = "ANTSDR_NOT_CONNECTED"
        self._last_update_ms: Optional[int] = None

    def _status(self, ok: bool, last_error: Optional[str], device_present: Optional[bool], driver_ok: Optional[bool]) -> Tuple[AntsdrStatus, AntsdrHealth]:
        status = AntsdrStatus(
            ok=ok,
            last_update_ms=self._last_update_ms if ok else None,
            last_error=last_error,
            center_freq_hz=None,
            sample_rate_hz=None,
            gain_db=None,
            rf_power_dbm=None,
            stream_active=None,
        )
        health = AntsdrHealth(
            ok=ok,
            last_update_ms=self._last_update_ms if ok else None,
            last_error=last_error,
            device_present=device_present,
            driver_ok=driver_ok,
        )
        return status, health

    def poll(self) -> Tuple[AntsdrStatus, AntsdrHealth]:
        if not self._uri:
            self._device = None
            self._last_error = "ANTSDR_NOT_CONNECTED"
            self._last_update_ms = None
            return self._status(False, self._last_error, False, False)

        try:
            adi = _import_adi()
        except Exception:
            self._device = None
            self._last_error = "ANTSDR_LIB_MISSING"
            self._last_update_ms = None
            return self._status(False, self._last_error, False, False)

        try:
            if self._device is None:
                self._device = adi.ad9364(uri=self._uri)
            self._last_error = None
            self._last_update_ms = now_ms()
            return self._status(True, None, True, True)
        except Exception:
            self._device = None
            self._last_error = "ANTSDR_INIT_FAILED"
            self._last_update_ms = None
            return self._status(False, self._last_error, False, False)
