import os
import asyncio
from ..db.mongo import worlds, agents
from ..core.agent_logic import update_agent
from dotenv import load_dotenv

load_dotenv()

TICK_TIME = float(os.getenv("TICK_TIME", 0.6))
sim_task = None


async def tick():
    world = await worlds.find_one({'_id': "world"})
    if not world:
        print("World not found. Skipping tick.")
        return

    world["tick"] += 1

    # update agents
    # 'find' returns an AsyncIOMotorCursor, which needs 'to_list' and 'await' to get all results
    people = await agents.find({"state": {"$ne": "dead"}}).to_list(length=None)

    # Run agent updates concurrently using asyncio.gather
    await asyncio.gather(*(update_agent(person) for person in people))

    # save world
    await worlds.update_one({"_id": "world"}, {"$set": world})


async def sim_loop():
    print("simulation started")
    while True:
        try:
            if not sim_task or sim_task.done():
                break
            await tick()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error during simulation tick: {e}")
            break
        await asyncio.sleep(TICK_TIME)
    print("simulation stopped")


def start_sim():
    global sim_task
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return {"status": "Error: Not running inside an asyncio event loop."}

    if sim_task and not sim_task.done():
        return {"status": "simulation already running"}

    sim_task = loop.create_task(sim_loop())
    return {"status": "simulation started"}


async def stop_sim():
    global sim_task
    if sim_task and not sim_task.done():
        sim_task.cancel()

        try:
            await sim_task
        except asyncio.CancelledError:
            pass  # Expected
        except Exception:
            pass  # Handle other exceptions during cancellation

        sim_task = None
        return {"status": "simulation stopped"}
    return {"status": "simulation is not running"}
