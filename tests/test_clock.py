from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from vivariumassistant.packages.core.clock import SimClock


def test_sim_clock_requires_timezone():
    with pytest.raises(ValueError):
        SimClock(datetime(2025, 1, 1))  # naive datetime


def test_sim_clock_advances():
    start = datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC"))
    clock = SimClock(start)

    assert clock.now() == start
    clock.advance(60)
    assert clock.now() == start + timedelta(seconds=60)