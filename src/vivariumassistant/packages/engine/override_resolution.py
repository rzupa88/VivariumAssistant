from __future__ import annotations

from datetime import datetime
from typing import Mapping

from vivariumassistant.packages.core.device_state import DeviceState
from vivariumassistant.packages.core.manual_override import ManualOverride


def apply_manual_overrides(
    now: datetime,
    desired: Mapping[str, DeviceState],
    overrides: Mapping[str, ManualOverride],
) -> dict[str, DeviceState]:
    resolved = dict(desired)

    for device_id, ovr in overrides.items():
        if ovr.is_active(now):
            resolved[device_id] = ovr.state

    return resolved