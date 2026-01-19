from __future__ import annotations

import os
import platform
from dataclasses import dataclass

from vivariumassistant.packages.core.config_schema import EnclosureConfig
from vivariumassistant.packages.drivers.base import PWMDriver, RelayDriver
from vivariumassistant.packages.simulator.pwm import SimPWMDriver
from vivariumassistant.packages.simulator.relay import SimRelayDriver


@dataclass(frozen=True)
class DriverBundle:
    pwm: PWMDriver
    relay: RelayDriver
    mode: str  # "sim" | "real"


def _real_mode_enabled() -> bool:
    """
    Hard safety gate: REAL drivers require explicit opt-in.
    This prevents accidentally toggling GPIO on a dev machine.
    """
    return os.getenv("VA_ENABLE_REAL", "").strip().lower() in {"1", "true", "yes", "on"}


def _assert_supported_real_platform() -> None:
    """
    REAL mode is intended for Raspberry Pi class devices.
    Keep this strict for safety; relax later if you intentionally support more platforms.
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Typical Pi: Linux + arm/arm64 (aarch64)
    is_linux = system == "linux"
    is_arm = any(x in machine for x in ("arm", "aarch64"))

    if not (is_linux and is_arm):
        raise RuntimeError(
            "REAL mode is only supported on Raspberry Pi-style Linux ARM devices. "
            f"Detected system={platform.system()} machine={platform.machine()}. "
            "Use runtime.mode=sim on non-Pi machines."
        )


def _assert_real_deps_available() -> None:
    """
    Ensure the expected GPIO dependency is installed.
    Import is intentionally local so SIM/dev environments do not require it.
    """
    try:
        import importlib
        importlib.import_module("gpiozero")
    except Exception as e:
        raise RuntimeError(
            "REAL mode requires the 'gpiozero' dependency. "
            "Install it (on Pi) with: poetry add gpiozero"
        ) from e

def build_drivers(enc: EnclosureConfig) -> DriverBundle:
    mode = getattr(getattr(enc, "runtime", None), "mode", "sim")

    if mode == "real":
        if not _real_mode_enabled():
            raise RuntimeError(
                "Refusing to start in REAL mode. "
                "Set VA_ENABLE_REAL=1 to explicitly allow hardware drivers."
            )

        # Provide clear, actionable errors before we ever touch GPIO.
        _assert_supported_real_platform()
        _assert_real_deps_available()

        # Placeholder until you implement real drivers:
        # from vivariumassistant.packages.drivers.real_pwm import RealPWMDriver
        # from vivariumassistant.packages.drivers.real_relay import RealRelayDriver
        # return DriverBundle(pwm=RealPWMDriver(enc), relay=RealRelayDriver(enc), mode="real")

        raise RuntimeError(
            "REAL mode is selected but real drivers are not implemented yet. "
            "Use runtime.mode=sim (default) or implement hardware drivers."
        )

    # Default: SIM drivers
    return DriverBundle(pwm=SimPWMDriver(), relay=SimRelayDriver(), mode="sim")