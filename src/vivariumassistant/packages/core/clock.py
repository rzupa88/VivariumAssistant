from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class Clock(ABC):
    @abstractmethod
    def now(self) -> datetime:
        """Return the current timezone-aware datetime."""


class RealClock(Clock):
    def __init__(self, timezone: str):
        self._tz = ZoneInfo(timezone)

    def now(self) -> datetime:
        return datetime.now(tz=self._tz)


class SimClock(Clock):
    def __init__(self, start: datetime):
        if start.tzinfo is None:
            raise ValueError("SimClock start datetime must be timezone-aware")
        self._now = start

    def now(self) -> datetime:
        return self._now

    def advance(self, seconds: int) -> None:
        self._now = self._now + timedelta(seconds=seconds)