# Configuration

VivariumAssistant reads YAML from the `config/` directory.

## Folder layout
- `config/enclosures/` → physical setup (devices, timezone)
- `config/profiles/` → behavior profile (lighting, UVB, mist schedules)

## Enclosure config
Example: `config/enclosures/enclosure_1.yaml`

Defines:
- `timezone` (used for schedules)
- devices (id, kind, driver, parameters like channel)

## Profile config
Example: `config/profiles/crested_gecko.yaml`

Defines:
- `lighting` schedule + brightness curve settings
- optional `uvb` schedule
- optional `mist` bursts + safety caps

## Tips
- Prefer stable device IDs (these become keys throughout logs and state).
- Keep “behavior” in profiles and “wiring/channel mapping” in enclosures.