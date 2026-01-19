# Architecture Decisions

This directory contains **Architecture Decision Records (ADRs)** for VivariumAssistant.

An ADR documents a **significant technical or architectural choice** that affects the structure, behavior, or future direction of the system.

Decisions are written once, reviewed, and then treated as **historical record** — not rewritten later to match new opinions.

---

## Why decisions exist

VivariumAssistant is intentionally:
- deterministic
- hardware-agnostic
- simulation-first
- safety-oriented

These constraints require **explicit tradeoffs**.

Decisions help us:
- avoid re-litigating past discussions
- onboard new contributors faster
- keep architecture consistent over time
- understand *why* something was built a certain way

---

## What should be a decision?

Create a decision when:
- multiple reasonable options exist
- the choice impacts more than one module
- the decision affects future extensibility
- reversing the decision later would be costly

Examples:
- Agent vs runtime responsibilities
- Hardware driver abstraction design
- Logging architecture
- Override precedence rules
- Simulation vs real-hardware parity guarantees

Non-examples:
- naming variables
- formatting choices
- small refactors

---

## Decision lifecycle

Each decision has a **status**:

- **Proposed** — under discussion, not yet accepted
- **Accepted** — agreed upon and implemented
- **Superseded** — replaced by a newer decision (link required)

Decisions are **never deleted**.

---

## File naming convention

Decisions use a numeric prefix to preserve ordering: