from motor.motor_asyncio import AsyncIOMotorDatabase as DataBase  # noqa
from fastapi import APIRouter, Depends


from ..database import get_db, DEFAULT_CONFIG, DEFAULT_CONFIG_NAME
from ..models.versions import VersionsRespSchema

versions_router = APIRouter()


@versions_router.get("/", status_code=200, response_model=VersionsRespSchema)
async def get_versions(drop: str, db: DataBase = Depends(get_db)):
    collection = db.get_collection("drops")
    # Get the generic versions
    # TODO: clean this (factorize)
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
