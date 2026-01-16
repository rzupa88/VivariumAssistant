from __future__ import annotations
from vivariumassistant.packages.drivers.base import RelayDriver

class SimRelayDriver(RelayDriver):
    def __init__(self):
        self._on: dict[int, bool] = {}

    async def set_on(self, channel: int, on: bool) -> None:
        self._on[channel] = bool(on)

    async def get_on(self, channel: int) -> bool:
        return bool(self._on.get(channel, False))