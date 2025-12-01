from ..db.mongo import worlds, agents, buildings
from ..models.world import world_template
from ..models.agent import default_agent
from ..models.building import house


async def init_world():
    # wipe old data
    await worlds.delete_many({})
    await agents.delete_many({})
    await buildings.delete_many({})

    await worlds.insert_one(world_template)

    # seed 5 agents
    for i in range(5):
        agents.insert_one(default_agent(f"A{i + 1}", i + 30, i * 3 + 4, i * 2 + 5, 0))

    # add 2 houses
    await buildings.insert_one(house("H1", 250, 5, 5, 0))
    await buildings.insert_one(house("H2", 300, 8, 5, 0))
