import os

import pytest
from fastapi.testclient import TestClient

from ..server.app import app
from ..server.database import get_db

import motor.motor_asyncio

MONGO_DETAILS = os.getenv("COSMOSDB_PRIMARY_CONNECTION_STRING")


def override_get_db():
    try:
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        print("hello")
        yield mongo_client.test_drops
    finally:
        pass


client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db


import time


@pytest.mark.parametrize(
    "drop, data",
    [
        (
            "test_drop",
            [{"time": 1618844678, "type": "PowerON", "_time": str(time.time())}],
        ),
        # ("test_drop", [{"time": 1618844900+i, "type": "PowerON"} for i in range(100)]),
        # ("test_drop", [{"time": "1618844678", "type": "RandomType"}]),
        # ("test_drop", [{"time": "1618844678", "type": "PowerON", "a": "a", "b": "b"}]),
    ],
)
def test_nominal(drop, data):
    resp = client.post("/events/", json={"drop": drop, "data": data})
    assert resp.status_code == 200
    print(resp)
