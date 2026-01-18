from __future__ import annotations

from datetime import datetime, timedelta, timezone

from vivariumassistant.packages.core.device_state import DeviceState
from vivariumassistant.packages.core.manual_override import ManualOverride
from vivariumassistant.packages.engine.override_resolution import apply_manual_overrides


def test_active_override_wins() -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    desired = {"light_day": DeviceState(device_id="light_day", on=False, level=0.0)}
    overrides = {
        "light_day": ManualOverride(
            device_id="light_day",
            state=DeviceState(device_id="light_day", on=True, level=0.85),
            expires_at=now + timedelta(minutes=10),
        )
    }

    resolved = apply_manual_overrides(now, desired, overrides)
    assert resolved["light_day"].on is True
    assert resolved["light_day"].level == 0.85


def test_expired_override_is_ignored() -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    desired = {"uvb": DeviceState(device_id="uvb", on=False)}
    overrides = {
        "uvb": ManualOverride(
            device_id="uvb",
            state=DeviceState(device_id="uvb", on=True),
            expires_at=now - timedelta(seconds=1),
        )
    }

    resolved = apply_manual_overrides(now, desired, overrides)
    assert resolved["uvb"].on is False