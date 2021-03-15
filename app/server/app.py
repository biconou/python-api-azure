from fastapi import FastAPI

from app.server.routes.pschit import router as PschitRouter

app = FastAPI()

app.include_router(PschitRouter, tags=["Pschit"], prefix="/pschit")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
