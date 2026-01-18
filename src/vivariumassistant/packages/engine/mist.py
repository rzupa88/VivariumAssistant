from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo

from vivariumassistant.packages.core.config_schema import MistProfile


def _parse_hhmm(s: str) -> time:
    hh, mm = s.split(":")
    return time(hour=int(hh), minute=int(mm))


def _localize(now: datetime, tz: str) -> datetime:
    zone = ZoneInfo(tz)
    return now.astimezone(zone) if now.tzinfo else now.replace(tzinfo=zone)


def _in_window(local: datetime, start: str, end: str) -> bool:
    t = local.time()
    s = _parse_hhmm(start)
    e = _parse_hhmm(end)

    # normal same-day window
    if s <= e:
        return s <= t <= e

    # overnight window (e.g. 22:00 -> 02:00)
    return t >= s or t <= e


class MistRuntime:
    def __init__(self):
        self.last_burst_at: datetime | None = None
        self.daily_seconds_used: dict[str, int] = {}  # YYYY-MM-DD -> seconds


def mist_burst_due(now: datetime, tz: str, prof: MistProfile, rt: MistRuntime) -> int | None:
    """
    Returns burst seconds if a burst should trigger now, else None.

    Supports:
      - Fixed bursts: prof.bursts (exact HH:MM match)
      - Window schedule: prof.windows (start/end + every_minutes)
    Enforces:
      - min spacing (minutes)
      - daily cap (seconds)
    """
    local = _localize(now, tz)
    today_key = local.date().isoformat()
    used = rt.daily_seconds_used.get(today_key, 0)

    # daily cap
    if used >= prof.safety.max_seconds_per_day:
        return None

    # min spacing
    if rt.last_burst_at is not None:
        last_local = _localize(rt.last_burst_at, tz)
        delta_min = (local - last_local).total_seconds() / 60.0
        if delta_min < prof.safety.min_minutes_between:
            return None

    # --- Mode A: fixed bursts (existing behavior) ---
    now_hhmm = local.strftime("%H:%M")
    for b in prof.bursts:
        if b.at == now_hhmm:
            seconds = int(b.seconds)
            remaining = prof.safety.max_seconds_per_day - used
            seconds = min(seconds, remaining)
            return seconds if seconds > 0 else None

    # --- Mode B: window schedule (new) ---
    for w in prof.windows:
        if not _in_window(local, w.start, w.end):
            continue

        # trigger when minute aligns with interval
        # Example: every 180 minutes -> trigger at 00, 03:00, 06:00, etc.
        total_minutes = local.hour * 60 + local.minute
        if w.every_minutes <= 0:
            continue
        if total_minutes % int(w.every_minutes) != 0:
            continue

        seconds = int(w.seconds)
        remaining = prof.safety.max_seconds_per_day - used
        seconds = min(seconds, remaining)
        return seconds if seconds > 0 else None

    return None