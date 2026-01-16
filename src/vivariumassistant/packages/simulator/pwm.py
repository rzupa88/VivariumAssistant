from __future__ import annotations
from vivariumassistant.packages.drivers.base import PWMDriver

class SimPWMDriver(PWMDriver):
    def __init__(self):
        self._levels: dict[int, float] = {}

    async def set_level(self, channel: int, level: float) -> None:
        level = max(0.0, min(1.0, float(level)))
        self._levels[channel] = level

    async def get_level(self, channel: int) -> float:
        return float(self._levels.get(channel, 0.0))