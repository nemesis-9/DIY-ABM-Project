from fastapi import APIRouter
from ..db.mongo import agents

router = APIRouter()


@router.get("/agents")
async def all_agents():
    return await agents.find({}).to_list(length=None)


@router.get("/agents/{name}")
async def get_agent(name: str):
    return await agents.find_one({"name": name})
