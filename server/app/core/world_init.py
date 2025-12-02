import os
import random
from dotenv import load_dotenv
from ..db.mongo import worlds, agents, inventories, buildings
from ..models.world import world_template
from ..models.agent import default_agent
from ..models.inventory import default_inventory
from ..models.building import house

load_dotenv()
AGENT_COUNT = int(os.getenv('AGENT_COUNT', 10))


def random_value(min=0, max=1):
    return random.randint(min, max)


async def wipe_database():
    print("Wiping all collections...")
    await worlds.delete_many({})
    await agents.delete_many({})
    await buildings.delete_many({})
    await inventories.delete_many({})
    print("Database wipe complete.")


async def init_world():
    # wipe old data
    # await wipe_database()

    await worlds.insert_one(world_template)

    # seed agents
    for i in range(AGENT_COUNT):
        await agents.insert_one(default_agent(
            f"A{i + 1}",
            random_value(20, 60),
            "M" if (i + 1) % 2 == 0 else "F",
            random_value(0, 200),
            random_value(0, 200),
            0,
            random_value(35, 100) * 1.5,
            random_value(70, 100) * 0.02,
            random_value(80, 100)
        ))

    # seed inventory records
    people = await agents.find({}).to_list(None)
    for person in people:
        await inventories.insert_one(default_inventory(
            person["_id"],
            [
                {"count": random_value(2, 6), "cal": random_value(50, 150)},
                {"count": random_value(1, 3), "cal": random_value(300, 550)},
            ],
            [
                {"count": random_value(5, 15), "litres": random_value(500, 2000)/1000, "cal": random_value(0, 5)},
                {"count": random_value(3, 6), "litres": random_value(300, 1000)/1000, "cal": random_value(100, 250)},
            ],
            random_value(0, 200),
            random_value(0, 200),
            0,
            True
        ))

    # add 2 houses
    await buildings.insert_one(house("H1", 250, 5, 5, 0))
    await buildings.insert_one(house("H2", 300, 8, 5, 0))
