from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from vivariumassistant.packages.core.config_schema import LightingProfile


def _parse_hhmm(s: str) -> time:
    hh, mm = s.split(":")
    return time(hour=int(hh), minute=int(mm))


@dataclass(frozen=True)
class LightingDecision:
    level: float  # 0..1


def compute_daylight_level(now: datetime, tz: str, profile: LightingProfile) -> LightingDecision:
    zone = ZoneInfo(tz)
    now = now.astimezone(zone) if now.tzinfo else now.replace(tzinfo=zone)

    day_start_t = _parse_hhmm(profile.day_start)
    day_end_t = _parse_hhmm(profile.day_end)

    today = now.date()
    day_start = datetime.combine(today, day_start_t, tzinfo=zone)
    day_end = datetime.combine(today, day_end_t, tzinfo=zone)

    # Support overnight windows (rare, but safe)
    if day_end <= day_start:
        day_end += timedelta(days=1)
        if now < day_start:
            day_start -= timedelta(days=1)

    sunrise = timedelta(minutes=max(profile.sunrise_minutes, 0))
    sunset = timedelta(minutes=max(profile.sunset_minutes, 0))
    max_b = float(profile.max_brightness)

    if now <= day_start:
        return LightingDecision(level=0.0)

    if sunrise.total_seconds() > 0 and day_start < now < (day_start + sunrise):
        frac = (now - day_start) / sunrise
        return LightingDecision(level=max(0.0, min(max_b, max_b * float(frac))))

    ramp_down_start = day_end - sunset if sunset.total_seconds() > 0 else day_end
    if now < ramp_down_start:
        return LightingDecision(level=max_b)

    if sunset.total_seconds() > 0 and ramp_down_start <= now < day_end:
        frac = (day_end - now) / sunset
        return LightingDecision(level=max(0.0, min(max_b, max_b * float(frac))))

    return LightingDecision(level=0.0)