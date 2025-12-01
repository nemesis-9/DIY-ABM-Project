from fastapi import APIRouter
from ..core.simulation import start_sim, stop_sim

router = APIRouter()


@router.post('/start')
async def start():
    return start_sim()


@router.post('/stop')
async def stop():
    return await stop_sim()
