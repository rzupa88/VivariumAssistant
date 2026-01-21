from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from typing import Any

from vivariumassistant.packages.core.config_schema import EnclosureConfig
from vivariumassistant.packages.drivers.base import PWMDriver, RelayDriver
from vivariumassistant.packages.simulator.pwm import SimPWMDriver
from vivariumassistant.packages.simulator.relay import SimRelayDriver

VA_GPIOZERO_MODULE = "gpiozero"


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

        importlib.import_module(VA_GPIOZERO_MODULE)
    except Exception as e:
        raise RuntimeError(
            f"REAL mode requires the '{VA_GPIOZERO_MODULE}' dependency. "
            "Install it (on Pi) with: poetry add gpiozero"
        ) from e


def _get_int_param(params: dict[str, Any], key: str) -> int:
    val = params.get(key)
    if val is None:
        raise RuntimeError(f"Missing required device param: {key}")
    try:
        return int(val)
    except Exception as e:
        raise RuntimeError(f"Invalid int for device param '{key}': {val!r}") from e


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

        # IMPORTANT: names here must match your class names exactly.
        from vivariumassistant.packages.drivers.real_pwm_gpiozero import RealPWMDriverGpioZero
        from vivariumassistant.packages.drivers.real_relay_gpiozero import RealRelayDriverGpioZero

        # Conservative mapping for now:
        # - light -> PWM
        # - uvb/mist/pump -> relay
        pwm_kinds = {"light"}
        relay_kinds = {"uvb", "mist", "pump"}

        pwm_pin_by_channel: dict[int, int] = {}
        relay_pin_by_channel: dict[int, int] = {}

        for d in enc.devices:
            params: dict[str, Any] = d.params
            gpio_pin = params.get("gpio_pin")
            if gpio_pin is None:
                continue

            ch = _get_int_param(params, "channel")
            pin = _get_int_param(params, "gpio_pin")

            if d.kind in pwm_kinds:
                pwm_pin_by_channel[ch] = pin
            elif d.kind in relay_kinds:
                relay_pin_by_channel[ch] = pin

        # Allow REAL mode with only relay, only pwm, or both.
        pwm: PWMDriver = (
            RealPWMDriverGpioZero(pin_by_channel=pwm_pin_by_channel)
            if pwm_pin_by_channel
            else SimPWMDriver()
        )
        relay: RelayDriver = (
            RealRelayDriverGpioZero(pin_by_channel=relay_pin_by_channel)
            if relay_pin_by_channel
            else SimRelayDriver()
        )

        # Safety note: REAL drivers should default OFF / 0.0 on creation.
        return DriverBundle(pwm=pwm, relay=relay, mode="real")

    # Default: SIM drivers
    return DriverBundle(pwm=SimPWMDriver(), relay=SimRelayDriver(), mode="sim")