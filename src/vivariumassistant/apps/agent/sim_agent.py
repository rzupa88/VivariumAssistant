from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from vivariumassistant.packages.core.config_loader import load_enclosure, load_profile
from vivariumassistant.packages.core.device_state import DeviceState
from vivariumassistant.packages.engine.lighting import compute_daylight_level
from vivariumassistant.packages.engine.uvb import uvb_should_be_on
from vivariumassistant.packages.engine.mist import MistRuntime, mist_burst_due

from vivariumassistant.packages.simulator.pwm import SimPWMDriver
from vivariumassistant.packages.simulator.relay import SimRelayDriver


logger = logging.getLogger("vivariumassistant.agent.sim")


class SimAgent:
    def __init__(self, enclosure_id: str, profile_id: str):
        self.enc = load_enclosure(enclosure_id)
        self.prof = load_profile(profile_id)

        self.pwm = SimPWMDriver()
        self.relay = SimRelayDriver()
        self.mist_rt = MistRuntime()

        # index devices by id for quick access
        self.devices = {d.id: d for d in self.enc.devices}

    async def tick(self) -> dict[str, DeviceState]:
        now = datetime.now(tz=ZoneInfo(self.enc.timezone))
        desired: dict[str, DeviceState] = {}

        # LIGHT (PWM)
        if "light_day" in self.devices:
            light = self.devices["light_day"]
            level = compute_daylight_level(
                now, self.enc.timezone, self.prof.lighting
            ).level
            ch = int(light.params.get("channel", 0))
            await self.pwm.set_level(ch, level)
            desired["light_day"] = DeviceState(
                device_id="light_day",
                on=(level > 0.001),
                level=level,
            )

        # UVB (relay)
        if self.prof.uvb and "uvb" in self.devices:
            uvb = self.devices["uvb"]
            ch = int(uvb.params.get("channel", 1))
            on = uvb_should_be_on(now, self.enc.timezone, self.prof.uvb)
            await self.relay.set_on(ch, on)
            desired["uvb"] = DeviceState(device_id="uvb", on=on)

        # MIST (relay bursts)
        if self.prof.mist and "mister" in self.devices:
            mister = self.devices["mister"]
            ch = int(mister.params.get("channel", 2))
            seconds = mist_burst_due(
                now, self.enc.timezone, self.prof.mist, self.mist_rt
            )

            if seconds:
                await self.relay.set_on(ch, True)
                desired["mister"] = DeviceState(
                    device_id="mister",
                    on=True,
                    meta={"burst_seconds": seconds},
                )

                # simulate burst duration without blocking loop too long
                await asyncio.sleep(min(seconds, 5))

                await self.relay.set_on(ch, False)

                self.mist_rt.last_burst_at = now
                key = now.date().isoformat()
                self.mist_rt.daily_seconds_used[key] = (
                    self.mist_rt.daily_seconds_used.get(key, 0) + int(seconds)
                )
            else:
                await self.relay.set_on(ch, False)
                desired["mister"] = DeviceState(device_id="mister", on=False)

        # WATERFALL (OFF in v1 SIM)
        if "waterfall" in self.devices:
            wf = self.devices["waterfall"]
            ch = int(wf.params.get("channel", 3))
            await self.relay.set_on(ch, False)
            desired["waterfall"] = DeviceState(device_id="waterfall", on=False)

        return desired

    async def run(self, interval_seconds: int = 5):
        while True:
            desired = await self.tick()

            logger.info(
                "control_tick",
                extra={
                    "event": "control_tick",
                    "enclosure_id": self.enc.id,
                    "profile_id": self.prof.id,
                    "now": datetime.now(
                        tz=ZoneInfo(self.enc.timezone)
                    ).isoformat(),
                    "desired": {k: v.model_dump() for k, v in desired.items()},
                },
            )

            await asyncio.sleep(interval_seconds)