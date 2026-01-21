from __future__ import annotations

from typing import Protocol, cast

from vivariumassistant.packages.drivers.base import PWMDriver

# Guarded import so Codespaces/laptops don’t require gpiozero.
try:
    from gpiozero import PWMOutputDevice  # type: ignore[import-untyped]
except Exception:  # pragma: no cover
    PWMOutputDevice = None  # type: ignore[assignment]


class _PWMDevice(Protocol):
    """Minimum interface we need from a PWM output device."""
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, v: float) -> None: ...
    def off(self) -> None: ...
    def close(self) -> None: ...


class RealPWMDriverGpioZero(PWMDriver):
    """
    Real PWM driver using gpiozero. Channels map to BCM GPIO pins.

    Safety:
    - Outputs default to 0.0 on creation.
    - This driver should only be constructed behind REAL-mode safety gate.
    """

    def __init__(self, pin_by_channel: dict[int, int]) -> None:
        if PWMOutputDevice is None:
            raise RuntimeError(
                "gpiozero is not available. Install it on the Raspberry Pi environment "
                "(e.g., `poetry add gpiozero`) and run with REAL mode enabled."
            )

        self._channels: dict[int, _PWMDevice] = {}
        self._levels: dict[int, float] = {}

        for ch, bcm_pin in pin_by_channel.items():
            dev = PWMOutputDevice(bcm_pin, initial_value=0.0)  # type: ignore[misc]
            self._channels[ch] = cast(_PWMDevice, dev)
            self._levels[ch] = 0.0

    async def set_level(self, channel: int, level: float) -> None:
        lvl = max(0.0, min(1.0, float(level)))
        dev = self._channels[channel]
        dev.value = lvl
        self._levels[channel] = lvl

    async def get_level(self, channel: int) -> float:
        return float(self._levels.get(channel, 0.0))

    def close(self) -> None:
        """Best-effort safe shutdown."""
        for dev in self._channels.values():
            try:
                dev.off()
            except Exception:
                pass
            try:
                dev.close()
            except Exception:
                pass
        self._channels.clear()
        self._levels.clear()