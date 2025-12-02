from ...db.mongo import agents, inventories


async def food_chain(agent):
    # inventory of agent
    inventory = await inventories.find_one({"agent": agent["_id"]})

    # hunger increase every tick
    agent["hunger"] += 2

    # eat if hungry
    if agent["hunger"] > agent["hunger_max"] and inventory["items"].get("food", 0) > 0:
        inventory["items"]["food"] -= 1
        agent["hunger"] -= agent["metabolism"]

    # death check
    if agent["hunger"] >= agent["hunger_max"]*2:
        agent["state"] = "dead"
        agent["hp"] = 0

    await agents.update_one({"_id": agent["_id"]}, {"$set": agent})
    await inventories.update_one({"_id": inventory["_id"]}, {"$set": inventory})


async def update_agent(agent):
    await food_chain(agent)
