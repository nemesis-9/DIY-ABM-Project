from fastapi import FastAPI
from .api.routes_sim import router as sim_routes
from .api.routes_worlds import router as world_routes
from .api.routes_agents import router as agent_routes
from .core.world_init import init_world, wipe_database

app = FastAPI(title="Inari Okami")


@app.on_event("startup")
async def startup_event():
    print("Initializing world data...")

    # TODO: For fresh database
    await wipe_database()

    # Await the asynchronous database initialization
    await init_world()

    print("World initialization complete.")


app.include_router(sim_routes, prefix="/sim")
app.include_router(world_routes)
app.include_router(agent_routes)
