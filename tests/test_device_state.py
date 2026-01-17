import pytest
from vivariumassistant.packages.core.device_state import DeviceState


def test_device_state_accepts_basic_fields():
    s = DeviceState(device_id="light_day", on=True, level=0.5, meta={"reason": "daylight"})
    assert s.device_id == "light_day"
    assert s.on is True
    assert s.level == 0.5
    assert s.meta["reason"] == "daylight"


def test_device_state_level_bounds():
    with pytest.raises(ValueError):
        DeviceState(device_id="light_day", on=True, level=-0.1)
    with pytest.raises(ValueError):
        DeviceState(device_id="light_day", on=True, level=1.1)


def test_device_state_level_optional():
    s = DeviceState(device_id="mister", on=False)
    assert s.level is None