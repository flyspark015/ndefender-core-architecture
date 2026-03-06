from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from threading import Event, Lock, Thread
from typing import Any, Callable, Dict, List, Optional, Tuple

from app.models import AntsdrHealth, AntsdrStatus, now_ms


def _import_adi():
    import adi  # type: ignore

    return adi


def _safe_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return None


def _rms_db(value: float) -> Optional[float]:
    if value <= 0:
        return None
    return 20.0 * math.log10(value)


DEFAULT_VTX_58 = [
    5645000000,
    5685000000,
    5725000000,
    5765000000,
    5805000000,
    5845000000,
    5885000000,
]


@dataclass
class RfContact:
    contact_id: str
    center_freq_hz: int
    last_seen_ms: int
    first_seen_ms: int
    peak_dbm: Optional[float] = None
    snr_db: Optional[float] = None
    band: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contact_id": self.contact_id,
            "center_freq_hz": self.center_freq_hz,
            "last_seen_ms": self.last_seen_ms,
            "first_seen_ms": self.first_seen_ms,
            "peak_dbm": self.peak_dbm,
            "snr_db": self.snr_db,
            "band": self.band,
            "timestamp_ms": self.last_seen_ms,
        }


class AntsdrController:
    def __init__(
        self,
        *,
        uri: str,
        enabled: bool,
        sample_rate_hz: int,
        rf_bw_hz: int,
        sweep_plan: str,
        step_hz: int,
        on_event: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ) -> None:
        self._uri = uri.strip()
        self._enabled = enabled
        self._sample_rate_hz = sample_rate_hz
        self._rf_bw_hz = rf_bw_hz
        self._step_hz = step_hz
        self._sweep_plan = sweep_plan
        self._on_event = on_event
        self._device = None
        self._last_error: Optional[str] = "ANTSDR_NOT_CONNECTED"
        self._last_update_ms: Optional[int] = None
        self._device_present = False
        self._driver_ok = False
        self._stream_active: Optional[bool] = None
        self._center_freq_hz: Optional[int] = None
        self._gain_db: Optional[float] = None
        self._noise_floor_dbm: Optional[float] = None
        self._contacts: Dict[str, RfContact] = {}
        self._scan_thread: Optional[Thread] = None
        self._scan_stop = Event()
        self._lock = Lock()
        self._last_emit_ms: int = 0

    def _emit(self, event_type: str, data: Dict[str, Any]) -> None:
        if not self._on_event:
            return
        self._on_event(event_type, data)

    def _build_plan(self) -> List[int]:
        if self._sweep_plan.upper() == "VTX_58":
            return list(DEFAULT_VTX_58)
        # fallback to single center if unknown
        return list(DEFAULT_VTX_58)

    def _status(self) -> AntsdrStatus:
        return AntsdrStatus(
            ok=self._device_present and self._driver_ok,
            last_update_ms=self._last_update_ms,
            last_error=self._last_error if not (self._device_present and self._driver_ok) else None,
            device_present=self._device_present,
            driver_ok=self._driver_ok,
            center_freq_hz=self._center_freq_hz,
            sample_rate_hz=self._sample_rate_hz,
            rf_bw_hz=self._rf_bw_hz,
            gain_db=self._gain_db,
            rf_power_dbm=None,
            noise_floor_dbm=self._noise_floor_dbm,
            stream_active=self._stream_active,
        )

    def _health(self) -> AntsdrHealth:
        return AntsdrHealth(
            ok=self._device_present and self._driver_ok,
            last_update_ms=self._last_update_ms,
            last_error=self._last_error if not (self._device_present and self._driver_ok) else None,
            device_present=self._device_present,
            driver_ok=self._driver_ok,
        )

    def _ensure_device(self) -> Tuple[bool, Optional[str]]:
        if not self._enabled:
            self._device = None
            self._device_present = False
            self._driver_ok = False
            self._last_error = "ANTSDR_DISABLED"
            self._last_update_ms = None
            return False, "ANTSDR_NOT_CONNECTED"
        if not self._uri:
            self._device = None
            self._device_present = False
            self._driver_ok = False
            self._last_error = "ANTSDR_NOT_CONNECTED"
            self._last_update_ms = None
            return False, "ANTSDR_NOT_CONNECTED"
        try:
            adi = _import_adi()
        except Exception:
            self._device = None
            self._device_present = False
            self._driver_ok = False
            self._last_error = "ANTSDR_LIB_MISSING"
            self._last_update_ms = None
            return False, "ANTSDR_DRIVER_UNAVAILABLE"

        try:
            if self._device is None:
                self._device = adi.ad9364(uri=self._uri)
            self._device_present = True
            self._driver_ok = True
            self._last_error = None
            self._last_update_ms = now_ms()
            return True, None
        except Exception:
            self._device = None
            self._device_present = False
            self._driver_ok = False
            self._last_error = "ANTSDR_INIT_FAILED"
            self._last_update_ms = None
            return False, "ANTSDR_NOT_CONNECTED"

    def poll(self) -> Tuple[AntsdrStatus, AntsdrHealth]:
        with self._lock:
            self._ensure_device()
            return self._status(), self._health()

    def start_scan(self) -> Tuple[bool, Optional[str]]:
        with self._lock:
            ok, err = self._ensure_device()
            if not ok:
                return False, err
            if self._scan_thread and self._scan_thread.is_alive():
                self._stream_active = True
                return True, None
            self._scan_stop.clear()
            self._scan_thread = Thread(target=self._scan_loop, daemon=True)
            self._stream_active = True
            self._emit("RF_SCAN_STATE", {"active": True})
            self._scan_thread.start()
            return True, None

    def stop_scan(self) -> None:
        with self._lock:
            self._scan_stop.set()
            self._stream_active = False
            self._emit("RF_SCAN_STATE", {"active": False})

    def _read_samples(self, freq_hz: int) -> Optional[List[complex]]:
        if self._device is None:
            return None
        sdr = self._device
        try:
            sdr.sample_rate = int(self._sample_rate_hz)
            sdr.rx_rf_bandwidth = int(self._rf_bw_hz)
            sdr.rx_lo = int(freq_hz)
            sdr.rx_enabled_channels = [0]
            sdr.rx_buffer_size = 1024
            self._center_freq_hz = int(freq_hz)
            try:
                self._gain_db = _safe_float(getattr(sdr, "rx_hardwaregain", None))
            except Exception:
                self._gain_db = None
            data = sdr.rx()
            if data is None:
                return None
            return list(data)
        except Exception:
            self._last_error = "ANTSDR_READ_FAILED"
            return None

    def _process_contact(self, freq_hz: int, samples: List[complex], now_ms_val: int) -> None:
        if not samples:
            return
        power = sum((abs(x) ** 2 for x in samples)) / max(len(samples), 1)
        peak_dbm = _rms_db(power)
        contact_id = f"rf:{freq_hz}"
        contact = self._contacts.get(contact_id)
        if contact is None:
            contact = RfContact(
                contact_id=contact_id,
                center_freq_hz=freq_hz,
                last_seen_ms=now_ms_val,
                first_seen_ms=now_ms_val,
                peak_dbm=peak_dbm,
                snr_db=None,
                band="5.8g",
            )
            self._contacts[contact_id] = contact
            self._emit("RF_CONTACT_NEW", contact.to_dict())
        else:
            contact.last_seen_ms = now_ms_val
            contact.peak_dbm = peak_dbm
            self._emit("RF_CONTACT_UPDATE", contact.to_dict())

    def _expire_contacts(self, now_ms_val: int) -> None:
        ttl_ms = 15000
        for key in list(self._contacts.keys()):
            contact = self._contacts[key]
            if now_ms_val - contact.last_seen_ms > ttl_ms:
                self._emit(
                    "RF_CONTACT_LOST",
                    {
                        "contact_id": contact.contact_id,
                        "last_seen_ms": contact.last_seen_ms,
                    },
                )
                del self._contacts[key]

    def _scan_loop(self) -> None:
        plan = self._build_plan()
        while not self._scan_stop.is_set():
            for freq in plan:
                if self._scan_stop.is_set():
                    break
                samples = self._read_samples(freq)
                now_ms_val = now_ms()
                self._last_update_ms = now_ms_val
                if samples:
                    if now_ms_val - self._last_emit_ms >= 200:
                        self._process_contact(freq, samples, now_ms_val)
                        self._last_emit_ms = now_ms_val
                self._expire_contacts(now_ms_val)
                time.sleep(0.05)
