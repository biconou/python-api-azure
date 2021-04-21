import os

import pytest
import motor.motor_asyncio
from fastapi.testclient import TestClient

from ..server.app import app
from ..server.database import get_db


MONGO_DETAILS = os.getenv("COSMOSDB_PRIMARY_CONNECTION_STRING")


@pytest.fixture(scope="function")
def client():
    """
    Global fixture to instantiate the db connection,
    the app and the testing client
    """

    async def override_get_db():
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        yield mongo_client.testing

    client = TestClient(app)
    app.dependency_overrides[get_db] = override_get_db
    return client


@pytest.fixture()
def db():
    """Global fixture to retrieve the database to use it to check directly what has been done"""
    return motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS).testing


@pytest.fixture(scope="function", autouse=True)
def clean_db(db):
    """Cleans the testing database after each test"""
    yield
    db.client.drop_database("testing")
