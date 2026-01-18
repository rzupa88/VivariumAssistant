from __future__ import annotations

from datetime import datetime

from vivariumassistant.packages.core.device_state import DeviceState
from vivariumassistant.packages.engine.lighting import compute_daylight_level
from vivariumassistant.packages.core.config_schema import LightingProfile  # adjust import if your type lives elsewhere


def desired_daylight_state(
    *,
    now: datetime,
    timezone: str,
    lighting: LightingProfile,
    device_id: str = "light_day",
) -> DeviceState:
    """
    V1 lighting rule: compute desired state for the primary daylight light.

    Deterministic: depends only on inputs.
    Hardware-agnostic: returns DeviceState only.
    """
    level = compute_daylight_level(now, timezone, lighting).level

    # Normalize to a clean on/off threshold and clamp noise
    if level <= 0.001:
        return DeviceState(device_id=device_id, on=False, level=0.0)

    return DeviceState(device_id=device_id, on=True, level=level)