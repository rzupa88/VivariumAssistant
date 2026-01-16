import asyncio
from apps.agent.sim_agent import SimAgent

async def main():
    agent = SimAgent(enclosure_id="enclosure_1", profile_id="crested_gecko")
    await agent.run(interval_seconds=5)

if __name__ == "__main__":
    asyncio.run(main())