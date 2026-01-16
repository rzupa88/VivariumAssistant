from __future__ import annotations
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from vivariumassistant.packages.core.config_schema import UVBProfile

def _parse_hhmm(s: str) -> time:
    hh, mm = s.split(":")
    return time(hour=int(hh), minute=int(mm))

def uvb_should_be_on(now: datetime, tz: str, prof: UVBProfile) -> bool:
    zone = ZoneInfo(tz)
    now = now.astimezone(zone) if now.tzinfo else now.replace(tzinfo=zone)

    start_t = _parse_hhmm(prof.start)
    end_t = _parse_hhmm(prof.end)

    today = now.date()
    start = datetime.combine(today, start_t, tzinfo=zone)
    end = datetime.combine(today, end_t, tzinfo=zone)

    if end <= start:  # overnight support
        end += timedelta(days=1)
        if now < start:
            start -= timedelta(days=1)

    return start <= now < end