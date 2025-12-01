from ..db.mongo import agents


async def food_chain(agent):
    # hunger increase every tick
    agent["hunger"] += 2

    # eat if hungry
    if agent["hunger"] > agent["hunger_max"] and agent["inventory"].get("food", 0) > 0:
        agent["inventory"]["food"] -= 1
        agent["hunger"] -= agent["metabolism"]

    # death check
    if agent["hunger"] >= agent["hunger_max"]*2:
        agent["state"] = "dead"
        agent["hp"] = 0

    await agents.update_one({"_id": agent["_id"]}, {"$set": agent})


async def update_agent(agent):
    await food_chain(agent)
