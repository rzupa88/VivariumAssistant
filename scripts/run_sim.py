import asyncio
from vivariumassistant.apps.agent.sim_agent import SimAgent
from vivariumassistant.packages.core.logging import setup_logging

async def main():
    setup_logging()
    agent = SimAgent(enclosure_id="enclosure_1", profile_id="crested_gecko")
    await agent.run(interval_seconds=5)

if __name__ == "__main__":
    asyncio.run(main())