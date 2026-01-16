from datetime import datetime
from zoneinfo import ZoneInfo
from packages.engine.lighting import compute_daylight_level
from packages.core.config_schema import LightingProfile

def test_daylight_level_bounds():
    prof = LightingProfile(
        day_start="08:00",
        day_end="20:00",
        sunrise_minutes=30,
        sunset_minutes=30,
        max_brightness=0.8,
    )
    now = datetime(2026, 1, 15, 12, 0, tzinfo=ZoneInfo("America/New_York"))
    lvl = compute_daylight_level(now, "America/New_York", prof).level
    assert 0.0 <= lvl <= 0.8