from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Dict, Any

class DeviceState(BaseModel):
    on: bool
    level: Optional[float] = None   # for PWM devices 0..1
    meta: Dict[str, Any] = {}