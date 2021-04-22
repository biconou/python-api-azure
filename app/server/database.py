import os

import motor.motor_asyncio

MONGO_DETAILS = os.getenv("COSMOSDB_PRIMARY_CONNECTION_STRING")
DEFAULT_CONFIG_NAME = "generic"
DEFAULT_VERSION = "0"
DEFAULT_CONFIG = {
    "drop": DEFAULT_CONFIG_NAME,
    "config": DEFAULT_VERSION,
    "firmware": DEFAULT_VERSION,
}


async def get_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    yield client.drops
