# Mist Scheduling Logic (v1)

## Goal
Decide whether misting should run *now* and for how long, based on time + mist profile + runtime, producing deterministic desired device states (SIM-first).

## Inputs
- now (datetime; provided by clock abstraction)
- timezone (IANA string)
- MistProfile (schedule + limits)
- MistRuntime (tracks last burst + daily usage)

## Output
- burst_seconds: int (0 means no burst due)

## Rules (v1)
1. Mist bursts may only occur inside configured schedule windows.
2. A burst is due when:
   - `now` is inside a window, AND
   - cooldown since last burst has elapsed (or no burst has run yet today), AND
   - daily cap has remaining seconds.
3. Burst duration is clamped:
   `burst_seconds = min(profile.burst_seconds, remaining_daily_seconds)`
4. When a burst runs, runtime updates:
   - `last_burst_at = now`
   - `daily_seconds_used[YYYY-MM-DD] += burst_seconds`

## Edge Cases
- Multiple windows per day
- Daily cap reached
- Crossing midnight resets usage key naturally via date key
- Timezone correctness is required (ZoneInfo-based)

## Non-goals (v1)
- Sensor feedback (humidity-based)
- Adaptive scheduling
- Hardware retries/fault handling