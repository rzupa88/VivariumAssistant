# Control Loop Contract

## Goal
Define a deterministic, hardware-agnostic control loop that converts configuration + time + observations into desired device states.

## Inputs
- EnclosureConfig
- ProfileConfig
- now (datetime)
- observations (sensor readings; simulated in v0.1)
- overrides (optional; manual override with timeout)
- previous_state (optional; last desired state)

## Outputs
A list of DeviceState records:
- device_id: str
- on: bool
- level: Optional[float] (0.0–1.0)
- meta: dict (optional reasoning/debug context)

## Determinism
Same inputs => same outputs. No direct reading from:
- system clock
- filesystem
- network
- hardware APIs

## Conflict Resolution
Priority order:
1. Safety constraints (future)
2. Manual overrides (active, not expired)
3. Profile-derived rules
4. Defaults/off

## Timing Model
The loop runs on a fixed interval but uses only `now` provided by the clock abstraction. Simulation and real execution must behave identically given the same inputs.

## Failure Behavior
Config validation happens before the loop. Missing sensors should fall back to safe defaults for v0.1.

## Non-Goals (v0.1)
- GPIO/I2C interactions
- retries / hardware fault recovery
- advanced environmental feedback control (PID, etc.)