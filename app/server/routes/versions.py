from motor.motor_asyncio import AsyncIOMotorDatabase as DataBase  # noqa
from fastapi import APIRouter, Body, Depends, HTTPException


from ..database import get_db, DEFAULT_CONFIG, DEFAULT_CONFIG_NAME
from ..models.versions import VersionsRespSchema
from ..models.drop import DropPostSchema
from ..models.common import response_model

versions_router = APIRouter()


@versions_router.get("/", status_code=200, response_model=VersionsRespSchema)
async def get_versions(drop: str, db: DataBase = Depends(get_db)):
    collection = db.get_collection("drops")
    # Get the generic versions
    default_versions = await collection.find_one({"drop": DEFAULT_CONFIG_NAME})
    if default_versions is None:
        default_versions = DEFAULT_CONFIG
    # Try to retrieve specific versions if they exist
    versions = await collection.find_one({"drop": drop})
    if versions is None:
        versions = default_versions
    else:
        for field, value in versions.items():
            versions[field] = default_versions[field] if value is None else value
    return VersionsRespSchema(**versions)


@versions_router.post("/")
async def set_versions(
    body: DropPostSchema = Body(...), db: DataBase = Depends(get_db)
):
    """Set versions for several drops"""
    # Over-quality
    # if body.config is not None:
    #     config_collection = db.get_collection("configs")
    #     result = await config_collection.find_one({"name": body.config})
    #     if result is None:
    #         raise HTTPException(
    #             status_code=428, detail=f"Referenced config {body.config} not found"
    #         )
    # if body.firmware is not None:
    #     firmware_collection = db.get_collection("firmwares")
    #     result = await firmware_collection.find_one({"name": body.firmware})
    #     if result is None:
    #         raise HTTPException(
    #             status_code=428, detail=f"Referenced firmware {body.firmware} not found"
    #         )

    drops = []
    drop_collection = db.get_collection("drops")
    fields = {"config": body.config, "firmware": body.firmware}
    set_dict = {f: value for f, value in fields.items() if value is not None}
    if not set_dict:
        raise HTTPException(
            status_code=422, detail="Either config or firmware must be set"
        )
    insert_dict = {f: value for f, value in fields.items() if value is None}
    for drop in body.target_drops:
        result = await drop_collection.update_many(
            {"drop": drop},
            {"$set": set_dict, "$setOnInsert": {**insert_dict, "drop": drop}},
            upsert=True,
        )
        if result.raw_result["ok"]:
            drops.append(drop)
    return response_model(
        drops, f"{len(drops)} config/firmware versions set successfully."
    )
