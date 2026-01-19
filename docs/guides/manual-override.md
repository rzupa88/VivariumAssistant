Manual Override with Timeout (v1)

Status

Proposed

Motivation

The control loop computes desired device states based on schedules, profiles, and environmental rules.
However, operators must be able to temporarily override automated behavior (e.g. force a light on, disable misting) without permanently disabling the system.

A manual override provides a time-bounded, explicit mechanism to supersede engine-derived behavior while preserving safety and automatic recovery.

⸻

Definition

A manual override is an explicit, user-initiated directive applied to a specific device that:
	•	Forces a desired device state
	•	Takes precedence over engine-computed logic
	•	Automatically expires after a defined timeout
	•	Reverts control back to the engine once expired

Overrides are device-scoped, not global.

⸻

Priority Rules

Device state resolution follows this precedence order:
	1.	Safety constraints (future work; always highest priority)
	2.	Active manual override (not expired)
	3.	Engine-computed desired state
	4.	Default/off state

Manual overrides MUST NOT bypass safety constraints.

⸻

Timeout Semantics
	•	Every override has an explicit expiration timestamp
	•	When the override expires:
	•	It is automatically ignored
	•	Control returns to engine logic on the next control loop tick
	•	If a new override is applied before expiration:
	•	The previous override is replaced
	•	The timeout resets

⸻

Data Model (v1)

Manual overrides are represented as immutable records.

Proposed shape:

ManualOverride:
  device_id: str
  state: DeviceState
  expires_at: datetime

Overrides are stored in a runtime map keyed by device_id.

⸻

Engine Interaction

During each control loop tick:
	1.	Engine computes desired states normally
	2.	Manual override map is consulted
	3.	For each device:
	•	If an active override exists → override wins
	•	If expired → override is ignored
	4.	Final desired state map is emitted

Overrides do not directly actuate hardware — they influence the desired state layer only.

⸻

Clock & Testability

All override expiration logic must depend on the system clock abstraction (Clock.now()).

This enables:
	•	Deterministic simulation
	•	Fast-forward testing
	•	Consistent behavior across SIM and real hardware

⸻

Non-Goals (v1)

The following are explicitly out of scope:
	•	Persistence across restarts
	•	Multi-device or group overrides
	•	Partial field overrides (e.g. override on but not level)
	•	User authentication / permissions
	•	UI/API exposure

⸻

Acceptance Criteria
	•	Manual override supersedes engine logic
	•	Override expires automatically without manual cleanup
	•	Expired overrides do not affect device state
	•	Behavior is deterministic under simulated time
	•	Unit tests cover:
	•	Active override
	•	Expired override
	•	Override replacement
	•	Engine fallback after expiry

⸻

Future Extensions
	•	Persistent overrides
	•	Safety-aware overrides
	•	UI/API control surface
	•	Group overrides
	•	Override audit logging