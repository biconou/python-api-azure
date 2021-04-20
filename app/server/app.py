from fastapi import FastAPI

from server.routes.events import router as EventsRouter

app = FastAPI()

app.include_router(EventsRouter, tags=["Events"], prefix="/events")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
