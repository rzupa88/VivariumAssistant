# VivariumAssistant

VivariumAssistant is an automated vivarium control system designed to run on Raspberry Pi hardware.  
It manages lighting, misting, and other enclosure systems using species-specific profiles and a deterministic control loop.

The project is developed **SIM-first**, with all logic validated in simulation before being applied to real hardware.

---

## Project Status

**Current phase:** MVP (v0.1)

The current focus is on:
- Stable configuration schemas
- Deterministic control logic
- Simulation-based validation
- Hardware abstraction boundaries

Real hardware integration will follow once the core engine is proven in simulation.

---

## What This Is (and Is Not)

**This is:**
- A deterministic control engine for vivarium environments
- Config-driven (species + enclosure profiles)
- Designed for safety, testability, and extensibility

**This is not (yet):**
- A UI or dashboard
- A cloud service
- A finalized hardware implementation

---

## Running the Simulation

The simulation allows you to observe desired device states over time without physical hardware.

```bash
poetry install
poetry run python scripts/run_sim.py
