from motor.motor_asyncio import AsyncIOMotorDatabase as DataBase  # noqa
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.logger import logger
from fastapi.encoders import jsonable_encoder


from ..database import get_db
from ..models.config import ConfigDBSchema, ConfigRespSchema

config_router = APIRouter()


@config_router.post("/")
async def add_config(
    config: ConfigDBSchema = Body(...), db: DataBase = Depends(get_db)
):
    """User Endpoint: Push a config for one, several or all of the drops"""
    # Create or replace config
    config_collection = db.get_collection("configs")
    await config_collection.delete_many({"name": config.name})
    result = await config_collection.insert_one(jsonable_encoder(config))

    return str(result.inserted_id)


@config_router.get("/", response_model=ConfigRespSchema)
async def get_config(name: str, db: DataBase = Depends(get_db)):
    config_collection = db.get_collection("configs")
    config_res = await config_collection.find_one({"name": name})
    if config_res is None:
        message = f"Configuration {name} not found"
        logger.error(message)
        raise HTTPException(status_code=404, detail=message)

    return ConfigRespSchema(config=config_res["config"])
