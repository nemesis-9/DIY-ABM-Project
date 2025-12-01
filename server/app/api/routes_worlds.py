from fastapi import APIRouter
from ..db.mongo import worlds

router = APIRouter()


@router.get("/world")
async def get_world():
    return await worlds.find_one({"_id": "world"})
