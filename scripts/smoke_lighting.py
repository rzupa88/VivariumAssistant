from datetime import datetime
from zoneinfo import ZoneInfo


from vivariumassistant.apps.agent.sim_agent import SimAgent
from vivariumassistant.packages.core.config_loader import ...
enc = load_enclosure("enclosure_1")
prof = load_profile("crested_gecko")

now = datetime.now(tz=ZoneInfo(enc.timezone))
decision = compute_daylight_level(now, enc.timezone, prof.lighting)

print("Now:", now.isoformat())
print("Target daylight level:", decision.level)