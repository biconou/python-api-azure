import os

import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder

MONGO_DETAILS = os.getenv("COSMOSDB_PRIMARY_CONNECTION_STRING")


def get_db():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        print(type(client.drops))
        yield client.drops
    finally:
        pass


async def add_event(db, drop_id: int, event_data: dict) -> int:
    """Add a new event into the database"""
    collection = db.get_collection("events")
    event_data["drop"] = drop_id
    event = await collection.insert_one(jsonable_encoder(event_data))
    return event.inserted_id
