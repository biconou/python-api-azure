import bson
import io
import os
import pytest

from .testing_utils import do_find_one, do_insert_one


@pytest.mark.parametrize(
    "content",
    [
        b"test_file",
        bytes(("a" * 100000).encode()),
        os.urandom(100000),
        os.urandom(10_000_000),
    ],
    ids=["simple_string", "100k_string", "100k_bytes", "10M_bytes"],
)
def test_post_nominal(client, db, content):
    name = "test-firmware.txt"
    file = io.BytesIO(content)
    resp = client.post("/firmware/", data={"name": name}, files={"file": file})
    assert resp.status_code == 200
    config_collection = db.get_collection("firmwares")
    from_db = do_find_one(config_collection, {"name": name})
    assert from_db["name"] == name
    assert from_db["firmware"] == content


@pytest.mark.parametrize("data", [dict(filename="test")], ids=["missing_name"])
def test_post_bad_from(client, data):
    file = io.BytesIO(b"content")
    resp = client.post("/firmware/", data=data, files={"file": file})
    assert resp.status_code == 422


def test_post_bad_file_field(client):
    name = "test-firmware.txt"
    file = io.BytesIO(b"content")
    resp = client.post("/firmware/", data={"name": name}, files={"firmware": file})
    assert resp.status_code == 422


@pytest.mark.slow
@pytest.mark.parametrize(
    "content",
    [
        b"test_file",
        bytes(("a" * 100000).encode()),
        os.urandom(100000),
        os.urandom(10_000_000),
    ],
    ids=["simple_string", "100k_string", "100k_bytes", "10M_bytes"],
)
def test_get_nominal(client, db, content):
    name = "test-firmware"
    firmware = {"name": name, "firmware": bson.binary.Binary(content)}
    do_insert_one(db.get_collection("firmwares"), firmware)
    resp = client.get("/firmware/", params={"name": name})
    assert resp.status_code == 200
    assert resp.content == content
