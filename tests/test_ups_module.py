from app.modules.ups_hat_e import UpsHatEReader


class FakeBus:
    def read_i2c_block_data(self, addr, register, length):
        if register == 0x02:
            return [0x20]
        if register == 0x10:
            # vbus voltage 15000mV, current 1800mA, power 27000mW
            return [0x98, 0x3A, 0x08, 0x07, 0x78, 0x69]
        if register == 0x20:
            # battery voltage 16400mV, current -500mA, percent 85, remaining 4000mAh
            # runtime (discharge) 120 min
            return [
                0x10,
                0x40,
                0x0C,
                0xFE,
                0x55,
                0x00,
                0xA0,
                0x0F,
                0x78,
                0x00,
                0x00,
                0x00,
            ]
        if register == 0x30:
            # 4x 4100mV
            return [0x04, 0x10, 0x04, 0x10, 0x04, 0x10, 0x04, 0x10]
        raise ValueError("unknown register")


class FakeSmbusModule:
    def SMBus(self, bus_id):
        return FakeBus()


def test_ups_hat_e_reader(monkeypatch):
    monkeypatch.setattr("app.modules.ups_hat_e._import_smbus", lambda: FakeSmbusModule())
    reader = UpsHatEReader()
    status, health = reader.poll()

    assert status.ok is True
    assert status.last_error is None
    assert status.battery_voltage_v == 16.4
    assert status.battery_current_a == -0.5
    assert status.battery_percent == 85.0
    assert status.remaining_capacity_mah == 4000.0
    assert status.runtime_s == 7200.0
    assert status.cell_voltages_v == [4.1, 4.1, 4.1, 4.1]
    assert status.vbus_voltage_v == 15.0
    assert status.vbus_current_a == 1.8
    assert status.vbus_power_w == 27.0
    assert status.state == "discharging"

    assert health.ok is True
    assert health.comms_ok is True
    assert health.model == "Waveshare UPS HAT (E)"
