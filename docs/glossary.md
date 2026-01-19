# Glossary

- **Agent**: runs the control loop on a schedule and applies outputs to drivers.
- **Control loop / tick**: one evaluation cycle producing desired device states.
- **Desired state**: what the system *wants* devices to be set to (not necessarily what hardware is doing).
- **DeviceState**: `{ device_id, on, level, meta }` output record for one device.
- **Enclosure**: the physical vivarium setup (devices + timezone).
- **Profile**: species/setup behavior rules (lighting/uvb/mist).
- **Override**: manual instruction that temporarily supersedes profile behavior.
- **SIM**: simulator mode (no hardware; drivers are mocked).