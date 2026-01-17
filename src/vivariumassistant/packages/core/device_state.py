from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class DeviceState(BaseModel):
    """
    Hardware-agnostic desired state for a single device.

    This is produced by the engine and consumed by drivers (SIM or real).
    """

    device_id: str = Field(..., min_length=1)
    on: bool
    level: Optional[float] = None
    meta: dict[str, Any] = Field(default_factory=dict)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return v
        if not (0.0 <= v <= 1.0):
            raise ValueError("level must be between 0.0 and 1.0 inclusive")
        return v