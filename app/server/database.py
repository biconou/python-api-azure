import os

import motor.motor_asyncio

MONGO_DETAILS = os.getenv("COSMOSDB_PRIMARY_CONNECTION_STRING")


async def get_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    yield client.drops


# def find_one(collection, query, schema=None, default=None, **kwargs):
#     result = collection.find_one(query, **kwargs)
#     if schema is None:
#         return result
#     if result is None and default is not None:
#
#     result.pop("_id", None)
#     return cls(**dict(data, id=id))
