from datetime import datetime
from zoneinfo import ZoneInfo

from packages.core.config_loader import load_enclosure, load_profile
from packages.engine.lighting import compute_daylight_level

enc = load_enclosure("enclosure_1")
prof = load_profile("crested_gecko")

now = datetime.now(tz=ZoneInfo(enc.timezone))
decision = compute_daylight_level(now, enc.timezone, prof.lighting)

print("Now:", now.isoformat())
print("Target daylight level:", decision.level)