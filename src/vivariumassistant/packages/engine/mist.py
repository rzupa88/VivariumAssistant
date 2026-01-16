from __future__ import annotations
from datetime import datetime, time
from zoneinfo import ZoneInfo

from vivariumassistant.packages.core.config_schema import MistProfile

def _parse_hhmm(s: str) -> time:
    hh, mm = s.split(":")
    return time(hour=int(hh), minute=int(mm))

class MistRuntime:
    def __init__(self):
        self.last_burst_at: datetime | None = None
        self.daily_seconds_used: dict[str, int] = {}  # YYYY-MM-DD -> seconds

def mist_burst_due(now: datetime, tz: str, prof: MistProfile, rt: MistRuntime) -> int | None:
    """
    Returns burst seconds if a burst should trigger now, else None.
    Rule: trigger when current minute matches a burst 'at' minute.
    Safety: min spacing + daily cap.
    """
    zone = ZoneInfo(tz)
    now = now.astimezone(zone) if now.tzinfo else now.replace(tzinfo=zone)

    today_key = now.date().isoformat()
    used = rt.daily_seconds_used.get(today_key, 0)

    # daily cap
    if used >= prof.safety.max_seconds_per_day:
        return None

    # min spacing
    if rt.last_burst_at is not None:
        delta_min = (now - rt.last_burst_at).total_seconds() / 60.0
        if delta_min < prof.safety.min_minutes_between:
            return None

    # minute match
    now_hhmm = now.strftime("%H:%M")
    for b in prof.bursts:
        if b.at == now_hhmm:
            seconds = int(b.seconds)
            if used + seconds > prof.safety.max_seconds_per_day:
                seconds = prof.safety.max_seconds_per_day - used
            return max(0, seconds) or None

    return None