from motor.motor_asyncio import AsyncIOMotorDatabase as DataBase  # noqa
from fastapi import APIRouter, Depends


from ..database import get_db
from ..models.versions import VersionsRespSchema

versions_router = APIRouter()


@versions_router.get("/", status_code=200, response_model=VersionsRespSchema)
async def add_events_data(drop: str, db: DataBase = Depends(get_db)):
    collection = db.get_collection("drops")
    # Get the generic versions
    default_versions = await collection.find_one({"drop": "generic"})
    if default_versions is None:
        default_versions = {"drop": "generic", "config": "0", "firmware": "0"}
    # Try to retrieve specific versions if they exist
    versions = await collection.find_one({"drop": drop})
    if versions is None:
        versions = default_versions
    else:
        for field, value in versions.items():
            versions[field] = default_versions[field] if value is None else value
    return VersionsRespSchema(**versions)
