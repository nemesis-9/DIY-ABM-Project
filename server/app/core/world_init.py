import random
from ..db.mongo import worlds, agents, inventories, buildings
from ..models.world import world_template
from ..models.agent import default_agent
from ..models.inventory import default_inventory
from ..models.building import house


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

    # seed 10 agents
    for i in range(10):
        await agents.insert_one(default_agent(
            f"A{i + 1}",
            random_value(20, 60),
            random_value(0, 200),
            random_value(0, 200),
            0,
            random_value(60, 80),
            random_value(30, 50),
            random_value(80, 150)
        ))

    # seed 10 inventory records
    people = await agents.find({}).to_list(None)
    for person in people:
        await inventories.insert_one(default_inventory(
            person["_id"],
            {
                "food": random_value(1, 5),
                "water": random_value(1, 5)
            },
            random_value(0, 200),
            random_value(0, 200),
            0,
            True
        ))

    # add 2 houses
    await buildings.insert_one(house("H1", 250, 5, 5, 0))
    await buildings.insert_one(house("H2", 300, 8, 5, 0))
