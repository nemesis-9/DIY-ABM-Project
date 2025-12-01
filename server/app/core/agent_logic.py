from ..db.mongo import agents


async def update_agent(agent):
    # hunger increase every tick
    agent["hunger"] += 2

    # eat if hungry
    if agent["hunger"] > 60 and agent["inventory"].get("food", 0) > 0:
        agent["inventory"]["food"] -= 1
        agent["hunger"] -= 50

    # death check
    if agent["hunger"] >= 120:
        agent["state"] = "dead"
        agent["hp"] = 0

    await agents.update_one({"_id": agent["_id"]}, {"$set": agent})
