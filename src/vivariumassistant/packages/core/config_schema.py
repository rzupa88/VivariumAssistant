from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional

DeviceKind = Literal["light", "uvb", "mist", "pump", "heat", "fan"]
ControlMode = Literal["pwm", "relay"]
DriverKey = str

class DeviceConfig(BaseModel):
    id: str
    name: str
    kind: DeviceKind
    driver: DriverKey
    params: dict[str, Any] = Field(default_factory=dict)

SensorKind = Literal["temp_humidity", "temp", "humidity"]

class SensorConfig(BaseModel):
    id: str
    kind: SensorKind
    driver: DriverKey
    params: dict[str, Any] = Field(default_factory=dict)

class EnclosureConfig(BaseModel):
    id:str
    name: str
    timezone: str = "America/New_York"
    devices: list[DeviceConfig] = Field(default_factory=list)
    sensors: list[SensorConfig] = Field(default_factory=list)

class LightingProfile(BaseModel):
    day_start: str  # "HH:MM" format
    day_end: str  # "HH:MM" format
    sunrise_minutes: int = 45
    sunset_minutes: int = 45
    max_brightness: float = 1.0

class UVBProfile(BaseModel):
    start: str  # "HH:MM" format
    end: str  # "HH:MM" format

class MistBurst(BaseModel):
    at: str
    seconds: int

class MistSafety(BaseModel):
    min_minutes_between: int = 120
    max_seconds_per_day: int = 240

class MistWindow(BaseModel):
    start: str  # "HH:MM"
    end: str    # "HH:MM"
    every_minutes: int
    seconds: int

class MistProfile(BaseModel):
    # Mode A: fixed bursts (existing)
    bursts: list[MistBurst] = Field(default_factory=list)
    # Mode B: window schedule (new)
    windows: list[MistWindow] = Field(default_factory=list)
    safety: MistSafety = Field(default_factory=MistSafety)

class ProfileConfig(BaseModel):
    id: str
    lighting: LightingProfile
    uvb: Optional[UVBProfile] = None
    mist: Optional[MistProfile] = None