from fastapi import APIRouter, HTTPException
from ..db.mongo import agents, inventories
from ..schemas.agent_schema import AgentSchema

router = APIRouter()


async def combine_agent_inventories(agent_data: dict) -> dict:
    if not agent_data or '_id' not in agent_data:
        return agent_data
    agent_id = agent_data['_id']
    inventory = await inventories.find_one({'agent': agent_id})
    inventory_items = inventory.get("items", {}) if inventory else {}
    merged_data = {**agent_data, "inventory": inventory_items}
    return merged_data


@router.get("/agents")
async def all_agents():
    try:
        agent_list = await agents.find({}).to_list(None)
        response_list = []
        for agent in agent_list:
            merged_agent = await combine_agent_inventories(agent)
            response_list.append(AgentSchema(**merged_agent))
        return response_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{name}")
async def get_agent(name: str):
    agent = await agents.find_one({"name": name})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    merged_agent = await combine_agent_inventories(agent)
    return AgentSchema(**merged_agent)
