from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from app.models import UpsHealth, UpsStatus, now_ms


I2C_ADDR = 0x2D


def _import_smbus():
    try:
        import smbus2 as smbus  # type: ignore

        return smbus
    except Exception:
        import smbus  # type: ignore

        return smbus


@dataclass
class UpsReading:
    state: str
    vbus_voltage_mv: int
    vbus_current_ma: int
    vbus_power_mw: int
    battery_voltage_mv: int
    battery_current_ma: int
    battery_percent: float
    remaining_capacity_mah: float
    runtime_min: float
    cell_voltages_mv: List[int]


class UpsHatEReader:
    def __init__(self, bus_id: int = 1, address: int = I2C_ADDR) -> None:
        self.bus_id = bus_id
        self.address = address
        self._bus = None
        self._last_update_ms: Optional[int] = None

    def _get_bus(self):
        if self._bus is None:
            smbus = _import_smbus()
            self._bus = smbus.SMBus(self.bus_id)
        return self._bus

    def _read_block(self, register: int, length: int) -> List[int]:
        bus = self._get_bus()
        return bus.read_i2c_block_data(self.address, register, length)

    def _read_state(self) -> str:
        data = self._read_block(0x02, 0x01)
        value = data[0]
        if value & 0x20:
            return "discharging"
        if value & 0x40 or value & 0x80:
            return "charging"
        return "idle"

    def _read_vbus(self) -> Tuple[int, int, int]:
        data = self._read_block(0x10, 0x06)
        vbus_voltage = data[0] | (data[1] << 8)
        vbus_current = data[2] | (data[3] << 8)
        vbus_power = data[4] | (data[5] << 8)
        return vbus_voltage, vbus_current, vbus_power

    def _read_battery(self) -> Tuple[int, int, float, float, float]:
        data = self._read_block(0x20, 0x0C)
        battery_voltage = data[0] | (data[1] << 8)
        current_raw = data[2] | (data[3] << 8)
        if current_raw > 0x7FFF:
            current_raw -= 0x10000
        battery_percent = float(int(data[4] | (data[5] << 8)))
        remaining_capacity = float(data[6] | (data[7] << 8))

        if current_raw < 0:
            runtime_min = float(data[8] | (data[9] << 8))
        else:
            runtime_min = float(data[10] | (data[11] << 8))

        return battery_voltage, current_raw, battery_percent, remaining_capacity, runtime_min

    def _read_cells(self) -> List[int]:
        data = self._read_block(0x30, 0x08)
        return [
            data[0] | (data[1] << 8),
            data[2] | (data[3] << 8),
            data[4] | (data[5] << 8),
            data[6] | (data[7] << 8),
        ]

    def read(self) -> UpsReading:
        state = self._read_state()
        vbus_voltage, vbus_current, vbus_power = self._read_vbus()
        battery_voltage, battery_current, battery_percent, remaining_capacity, runtime_min = (
            self._read_battery()
        )
        cell_voltages = self._read_cells()
        return UpsReading(
            state=state,
            vbus_voltage_mv=vbus_voltage,
            vbus_current_ma=vbus_current,
            vbus_power_mw=vbus_power,
            battery_voltage_mv=battery_voltage,
            battery_current_ma=battery_current,
            battery_percent=battery_percent,
            remaining_capacity_mah=remaining_capacity,
            runtime_min=runtime_min,
            cell_voltages_mv=cell_voltages,
        )

    def poll(self) -> Tuple[UpsStatus, UpsHealth]:
        try:
            reading = self.read()
            ts = now_ms()
            self._last_update_ms = ts

            if reading.vbus_voltage_mv is None:
                on_battery = None
            else:
                on_battery = (reading.vbus_voltage_mv / 1000.0) <= 1.0

            status = UpsStatus(
                ok=True,
                last_update_ms=ts,
                last_error=None,
                battery_percent=reading.battery_percent,
                battery_voltage_v=reading.battery_voltage_mv / 1000.0,
                battery_current_a=reading.battery_current_ma / 1000.0,
                current_a=reading.battery_current_ma / 1000.0,
                remaining_capacity_mah=reading.remaining_capacity_mah,
                runtime_s=reading.runtime_min * 60.0,
                cell_voltages_v=[v / 1000.0 for v in reading.cell_voltages_mv],
                vbus_voltage_v=reading.vbus_voltage_mv / 1000.0,
                vbus_current_a=reading.vbus_current_ma / 1000.0,
                vbus_power_w=reading.vbus_power_mw / 1000.0,
                state=reading.state,
                input_voltage_v=reading.vbus_voltage_mv / 1000.0,
                output_voltage_v=reading.battery_voltage_mv / 1000.0,
                on_battery=on_battery,
            )

            health = UpsHealth(
                ok=True,
                last_update_ms=ts,
                last_error=None,
                comms_ok=True,
                model="Waveshare UPS HAT (E)",
            )
            return status, health
        except Exception as exc:  # pragma: no cover - exercised in integration
            ts = self._last_update_ms or now_ms()
            err = _classify_error(exc)
            status = UpsStatus(
                ok=False,
                last_update_ms=ts,
                last_error=err,
                battery_percent=None,
                battery_voltage_v=None,
                battery_current_a=None,
                current_a=None,
                remaining_capacity_mah=None,
                runtime_s=None,
                cell_voltages_v=None,
                vbus_voltage_v=None,
                vbus_current_a=None,
                vbus_power_w=None,
                state="unknown",
                input_voltage_v=None,
                output_voltage_v=None,
                on_battery=None,
            )
            health = UpsHealth(
                ok=False,
                last_update_ms=ts,
                last_error=err,
                comms_ok=False,
                model="Waveshare UPS HAT (E)",
            )
            return status, health


def _classify_error(exc: Exception) -> str:
    if isinstance(exc, OSError):
        if getattr(exc, "errno", None) in (2, 5, 6, 121):
            return "UPS_NOT_DETECTED"
    return f"UPS_READ_FAILED:{exc}"


class FakeUpsHatEReader(UpsHatEReader):
    def __init__(self) -> None:
        super().__init__(bus_id=1, address=I2C_ADDR)

    def read(self) -> UpsReading:  # pragma: no cover - test helper
        return UpsReading(
            state="charging",
            vbus_voltage_mv=15000,
            vbus_current_ma=1800,
            vbus_power_mw=27000,
            battery_voltage_mv=16400,
            battery_current_ma=700,
            battery_percent=85.0,
            remaining_capacity_mah=4000.0,
            runtime_min=60.0,
            cell_voltages_mv=[4100, 4100, 4100, 4100],
        )
