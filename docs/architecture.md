# Architecture

VivariumAssistant is built around a **deterministic control loop** that separates
decision-making from hardware execution.

---

## Big Picture

**Configuration + time + observations + overrides → desired device states**

A runtime (simulation or real hardware) applies those desired states via drivers.

This separation ensures that simulation behavior exactly mirrors real hardware
behavior when given the same inputs.

---

## Core Design Principles

- **Determinism**: same inputs always produce the same outputs
- **Hardware agnostic logic**: no GPIO, filesystem, or network access in the engine
- **Simulation parity**: SIM and real modes share the same control logic
- **Clear boundaries**: each layer has a single responsibility

---

## Key Concepts

- **EnclosureConfig**  
  Describes the physical setup: devices, sensors, and timezone.

- **ProfileConfig**  
  Describes behavioral rules: lighting schedules, UVB windows, mist schedules, etc.

- **Engine**  
  Pure, deterministic logic that converts inputs into desired `DeviceState` values.

- **Agent**  
  Orchestrates the control loop on an interval and calls drivers to apply results.

- **Drivers**  
  Hardware interfaces (SIM drivers today; GPIO/I2C drivers in the future).

---

## Codebase Boundaries

### `src/vivariumassistant/packages/core/`
Shared foundational models and helpers:
- configuration schema and loader
- clock abstraction
- logging helpers
- device state model
- manual override model

---

### `src/vivariumassistant/packages/engine/`
Deterministic “brain” of the system:
- lighting logic
- UVB logic
- mist scheduling logic
- manual override resolution

**Rules for this layer:**
- Must not read the system clock directly
- Must not access hardware, filesystem, or network
- Must be fully deterministic

---

### `src/vivariumassistant/packages/simulator/`
Simulation-only drivers:
- relay simulation
- PWM simulation

Used to validate behavior before running on real hardware.

---

### `src/vivariumassistant/packages/drivers/`
Real hardware drivers (future):
- GPIO interfaces
- I2C devices
- PWM controllers

This layer applies desired states to physical hardware.

---

### `src/vivariumassistant/apps/`
Application entry points:
- `apps/agent/` contains the simulation agent runner
- `apps/api/` reserved for a future API layer

---

## Determinism Rule

Given the same:
- configuration
- time input
- observations
- overrides

the engine **must** produce the same desired device states.

This guarantees that simulation and real hardware behave identically.

---

## Non-Goals (v0.1)

- closed-loop PID control
- hardware fault recovery
- advanced telemetry or alerting