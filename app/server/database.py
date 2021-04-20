import os
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder

MONGO_DETAILS = os.getenv("COSMOSDB_PRIMARY_CONNECTION_STRING")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.drops


async def add_event(drop_id: int, event_data: dict) -> int:
    """Add a new event into the database"""
    collection = database.get_collection(event_data["type"])
    event_data["drop"] = drop_id
    event = await collection.insert_one(jsonable_encoder(event_data))
    return event.inserted_id
