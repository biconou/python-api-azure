from fastapi import FastAPI

from .routes.events import events_router
from .routes.versions import versions_router

app = FastAPI()

app.include_router(events_router, tags=["Events"], prefix="/events")
app.include_router(versions_router, tags=["Versions"], prefix="/versions")


@app.get("/", tags=["Root"])
async def read_root():
    """Default route to avoid a 404 after login on browser"""
    return {"message": "ok"}
