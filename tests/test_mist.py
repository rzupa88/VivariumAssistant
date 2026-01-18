from datetime import datetime
from zoneinfo import ZoneInfo

from vivariumassistant.packages.core.config_schema import MistProfile, MistBurst, MistSafety, MistWindow
from vivariumassistant.packages.engine.mist import MistRuntime, mist_burst_due


TZ = "America/New_York"


def dt(y, m, d, hh, mm):
    return datetime(y, m, d, hh, mm, tzinfo=ZoneInfo(TZ))


def test_fixed_burst_triggers_on_exact_time():
    prof = MistProfile(
        bursts=[MistBurst(at="07:30", seconds=20)],
        safety=MistSafety(min_minutes_between=0, max_seconds_per_day=240),
    )
    rt = MistRuntime()
    assert mist_burst_due(dt(2026, 1, 18, 7, 30), TZ, prof, rt) == 20


def test_fixed_burst_no_trigger_other_time():
    prof = MistProfile(
        bursts=[MistBurst(at="07:30", seconds=20)],
        safety=MistSafety(min_minutes_between=0, max_seconds_per_day=240),
    )
    rt = MistRuntime()
    assert mist_burst_due(dt(2026, 1, 18, 7, 31), TZ, prof, rt) is None


def test_spacing_blocks_burst():
    prof = MistProfile(
        bursts=[MistBurst(at="07:30", seconds=20)],
        safety=MistSafety(min_minutes_between=120, max_seconds_per_day=240),
    )
    rt = MistRuntime()
    rt.last_burst_at = dt(2026, 1, 18, 6, 31)
    assert mist_burst_due(dt(2026, 1, 18, 7, 30), TZ, prof, rt) is None


def test_daily_cap_clamps_burst():
    prof = MistProfile(
        bursts=[MistBurst(at="07:30", seconds=50)],
        safety=MistSafety(min_minutes_between=0, max_seconds_per_day=240),
    )
    rt = MistRuntime()
    rt.daily_seconds_used["2026-01-18"] = 230
    assert mist_burst_due(dt(2026, 1, 18, 7, 30), TZ, prof, rt) == 10


def test_window_schedule_triggers_on_interval_inside_window():
    prof = MistProfile(
        windows=[MistWindow(start="07:00", end="08:00", every_minutes=15, seconds=12)],
        safety=MistSafety(min_minutes_between=0, max_seconds_per_day=240),
    )
    rt = MistRuntime()
    assert mist_burst_due(dt(2026, 1, 18, 7, 30), TZ, prof, rt) == 12
    assert mist_burst_due(dt(2026, 1, 18, 7, 31), TZ, prof, rt) is None