# Logging & Observability

Logging is intentionally minimal in v0.1 but consistent across SIM and real modes.

## Log levels
- DEBUG: verbose development details
- INFO: standard operational events
- WARNING: unusual but recoverable situations
- ERROR: failures that prevent expected behavior

## Standard events

### `control_tick`
Emitted once per loop tick.

Fields (baseline):
- `event`: `"control_tick"`
- `enclosure_id`
- `profile_id`
- `now` (ISO timestamp)
- `desired` (map of `device_id -> DeviceState`)

## Log format
Set using `VA_LOG_FORMAT`:
- `text` (default): human-friendly
- `json`: structured output (better for parsing later)