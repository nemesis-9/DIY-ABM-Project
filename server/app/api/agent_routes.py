from fastapi import APIRouter, HTTPException
from ..db.mongo import agents
from ..schemas.agent_schema import SchemaAgent

router = APIRouter()


@router.get("/agents")
async def all_agents():
    try:
        data = await agents.find({}).to_list(None)
        return [SchemaAgent(**agent) for agent in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{name}")
async def get_agent(name: str):
    agent = await agents.find_one({"name": name})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return SchemaAgent(**agent)
