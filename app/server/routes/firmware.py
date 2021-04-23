import bson
import io
from fastapi import APIRouter, File, Form, Depends, HTTPException
from fastapi.logger import logger
from fastapi.responses import HTMLResponse, StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase as DataBase  # noqa


from ..database import get_db

firmware_router = APIRouter()


@firmware_router.get("/upload_form/")
async def get_firmware_upload_form():
    content = """
        <body>
        <form action="/firmware/" enctype="multipart/form-data" method="post">
        <input name="name" type="text">
        <input name="file" type="file">
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)


@firmware_router.post("/")
async def add_firmware(
    file: bytes = File(...), name: str = Form(...), db: DataBase = Depends(get_db)
):
    """User Endpoint: Push a firmware"""
    # Create or replace firmware
    config_collection = db.get_collection("firmwares")
    await config_collection.delete_many({"name": name})
    result = await config_collection.insert_one(
        {"name": name, "firmware": bson.binary.Binary(file)}
    )
    return str(result)


@firmware_router.get("/")
async def get_firmware(name: str, db: DataBase = Depends(get_db)):
    firmwares_collection = db.get_collection("firmwares")
    firmware = await firmwares_collection.find_one({"name": name})
    if firmware is None:
        logger.error(f"No Firmware named {name}")
        return HTTPException(404, detail=f"No Firmware named {name}")
    firmware_file = io.BytesIO(firmware["firmware"])
    firmware_file.name = firmware["name"]

    return StreamingResponse(firmware_file)
