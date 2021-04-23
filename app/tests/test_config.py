import pytest

from .testing_utils import do_find_one, do_insert_one


@pytest.mark.parametrize(
    "name, config",
    [
        ("test-config", {"DropQtyToDeliver": "4"}),
        ("test-config", {"0": "4", "a": "a", "b": "b", "c": 3000}),
    ],
    ids=["one", "any_fields"],
)
def test_post_nominal(client, db, name, config):
    resp = client.post("/config/", json={"name": name, "config": config})
    assert resp.status_code == 200
    config_collection = db.get_collection("configs")
    config_from_db = do_find_one(config_collection, {"name": name})
    assert config_from_db["config"] == config


@pytest.mark.parametrize("missing", ["name", "config"])
def test_post_missing_field(client, missing):
    data = {"name": "version", "config": {"a": "a"}}
    data.pop(missing)
    resp = client.post("/config/", json=data)
    assert resp.status_code == 422


def test_get_nominal(client, db):
    config = {"name": "test-config", "config": {"a": "a"}}
    do_insert_one(db.get_collection("configs"), config)
    resp = client.get("/config/", params={"name": "test-config"})
    assert resp.status_code == 200
    assert resp.json()["config"] == config["config"]


def test_missing_param(client):
    resp = client.get("/config/")
    assert resp.status_code == 422


def test_missing_config(client):
    resp = client.get("/config/", params={"name": "test-config"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Configuration test-config not found"
