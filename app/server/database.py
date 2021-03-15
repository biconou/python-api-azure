import motor.motor_asyncio
from bson.objectid import ObjectId

# MONGO_URL = "mongodb://cdb-everie-ycoteststartup-script.mongo.cosmos.azure.com:10255?ssl=true"
# MONGO_USERNAME = "cdb-everie-ycoteststartup-script"
# MONGO_PASSWORD = "drUKspy5OUB7IBWzNFirZax71kLHaUDQvwVuBNawz6TMld7smtXEEBEQdgHOsgjdNa3AKCOSbN5Q2SrAnQtrXQ=="


MONGO_DETAILS = (
    "mongodb://cdb-everie-ycoteststartup-script"
    ":drUKspy5OUB7IBWzNFirZax71kLHaUDQvwVuBNawz6TMld7smtXEEBEQdgHOsgjdNa3AKCOSbN5Q2SrAnQtrXQ=="
    "@cdb-everie-ycoteststartup-script.mongo.cosmos.azure.com:10255"
    "/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "&appName=@cdb-everie-ycoteststartup-script@"
)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.drops
pschit_collection = database.get_collection("pschit")


def pschit_helper(pschit) -> dict:
    return {
        "id": str(pschit["_id"]),
        "drop_id": pschit["drop_id"],
        "timestamp": pschit["timestamp"],
        "location": pschit["location"],
        "count": pschit.get("count"),
    }


async def retrieve_pschits():
    """Retrieve all students present in the database"""
    pschits = []
    async for pschit in pschit_collection.find():
        pschits.append(pschit_helper(pschit))
    return pschits


async def add_pschit(pschit_data: dict) -> dict:
    """Add a new pschit into to the database"""
    pschit = await pschit_collection.insert_one(pschit_data)
    new_pschit = await pschit_collection.find_one({"_id": pschit.inserted_id})
    return pschit_helper(new_pschit)


async def retrieve_pschit(id: str) -> dict:
    """Retrieve a pschit with a matching ID"""
    pschit = await pschit_collection.find_one({"_id": ObjectId(id)})
    if pschit:
        return pschit_helper(pschit)


async def update_pschit(id: str, data: dict):
    """Update a pschit with a matching ID"""
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    pschit = await pschit_collection.find_one({"_id": ObjectId(id)})
    if pschit:
        updated_pschit = await pschit_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_pschit:
            return True
        return False


async def delete_pschit(id: str):
    """Delete a pschit from the database"""
    pschit = await pschit_collection.find_one({"_id": ObjectId(id)})
    if pschit:
        await pschit_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
