from __future__ import annotations
from abc import ABC, abstractmethod

class PWMDriver(ABC):
    @abstractmethod
    async def set_level(self, channel: int, level: float) -> None: ...
    @abstractmethod
    async def get_level(self, channel: int) -> float: ...

class RelayDriver(ABC):
    @abstractmethod
    async def set_on(self, channel: int, on: bool) -> None: ...
    @abstractmethod
    async def get_on(self, channel: int) -> bool: ...