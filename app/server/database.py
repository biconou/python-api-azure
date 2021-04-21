import os

import motor.motor_asyncio

MONGO_DETAILS = os.getenv("COSMOSDB_PRIMARY_CONNECTION_STRING")


async def get_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    yield client.drops
