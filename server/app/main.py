from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.sim_routes import router as sim_routes
from .api.world_routes import router as world_routes
from .api.agent_routes import router as agent_routes
from .core.world_init import init_world, wipe_database

app = FastAPI(title="Inari Okami")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
