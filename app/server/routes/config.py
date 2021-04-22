from motor.motor_asyncio import AsyncIOMotorDatabase as DataBase  # noqa
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.logger import logger
from fastapi.encoders import jsonable_encoder


from ..database import get_db, DEFAULT_CONFIG, DEFAULT_CONFIG_NAME
from ..models.config import ConfigPostSchema, ConfigRespSchema

config_router = APIRouter()


@config_router.post("/")
async def add_config(
    body: ConfigPostSchema = Body(...), db: DataBase = Depends(get_db)
):
    response = {}
    """User Endpoint: Push a config for one, several or all of the drops"""
    # Create or replace config
    config_collection = db.get_collection("configs")
    config = body.config
    await config_collection.delete_many({"version": config.version})
    result = await config_collection.insert_one(jsonable_encoder(config))
    response["config"] = str(result.inserted_id)

    # Update or create drop entries with config version
    response["drops"] = []
    drop_collection = db.get_collection("drops")
    for drop in body.target_drops:
        result = await drop_collection.update_many(
            {"drop": drop},
            {
                "$set": {"config": config.version},
                "$setOnInsert": {"firmware": None, "drop": drop},
            },
            upsert=True,
        )
        if result.raw_result["ok"]:
            response["drops"].append(drop)
    return response


@config_router.get("/", response_model=ConfigRespSchema)
async def get_config(drop: str, db: DataBase = Depends(get_db)):
    drop_collection = db.get_collection("drops")
    versions = await drop_collection.find_one({"drop": drop})
    # TODO: clean this cascade
    if versions is None:
        versions = await drop_collection.find_one({"drop": DEFAULT_CONFIG_NAME})
        if versions is None:
            versions = DEFAULT_CONFIG
    config_version = versions["config"]

    config_collection = db.get_collection("configs")
    config_res = await config_collection.find_one({"version": config_version})
    if config_res is None:
        message = f"Configuration {config_version} for drop {drop} not found"
        logger.error(message)
        raise HTTPException(status_code=404, detail=message)

    return ConfigRespSchema(config=config_res["config"])
