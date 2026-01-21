from __future__ import annotations

from typing import Protocol, cast

from vivariumassistant.packages.drivers.base import RelayDriver

# Guarded import so non-Pi dev environments don't require gpiozero.
try:
    from gpiozero import DigitalOutputDevice  # type: ignore[import-untyped]
except Exception:  # pragma: no cover
    DigitalOutputDevice = None  # type: ignore[assignment]


class _RelayDevice(Protocol):
    """Minimum interface we need from a relay output device."""
    def on(self) -> None: ...
    def off(self) -> None: ...
    def close(self) -> None: ...


class RealRelayDriverGpioZero(RelayDriver):
    """
    Real relay driver using gpiozero. Channels map to BCM GPIO pins.

    Safety:
    - Outputs default OFF on creation (initial_value=False).
    - This driver should only be constructed behind REAL-mode safety gate.
    """

    def __init__(self, pin_by_channel: dict[int, int]) -> None:
        if DigitalOutputDevice is None:
            raise RuntimeError(
                "gpiozero is not available. Install it on the Raspberry Pi environment "
                "(e.g., `poetry add gpiozero`) and run with REAL mode enabled."
            )

        self._channels: dict[int, _RelayDevice] = {}
        self._state: dict[int, bool] = {}

        for ch, bcm_pin in pin_by_channel.items():
            dev = DigitalOutputDevice(bcm_pin, initial_value=False)  # type: ignore[misc]
            self._channels[ch] = cast(_RelayDevice, dev)
            self._state[ch] = False

    async def set_on(self, channel: int, on: bool) -> None:
        dev = self._channels[channel]
        if on:
            dev.on()
        else:
            dev.off()
        self._state[channel] = on

    async def get_on(self, channel: int) -> bool:
        return bool(self._state.get(channel, False))

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
        self._state.clear()