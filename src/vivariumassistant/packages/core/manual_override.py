from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .device_state import DeviceState


@dataclass(frozen=True, slots=True)
class ManualOverride:
    device_id: str
    state: DeviceState
    expires_at: datetime

    def is_active(self, now: datetime) -> bool:
        return now < self.expires_at