import pytest

from .testing_utils import do_find_one, do_insert_one


@pytest.mark.parametrize(
    "drops",
    [[], ["test-drop"], ["test1", "test2", "test3"], ["generic"], ["generic", "test1"]],
    ids=["nothing", "one", "three", "generic", "gen+spec"],
)
def test_post_config_nominal(client, db, drops):
    config_name = "test-config"
    resp = client.post(
        "/versions/", json={"target_drops": drops, "config": config_name}
    )
    assert resp.status_code == 200
    ack_drops = resp.json()["data"]
    assert sorted(ack_drops) == sorted(drops)
    collection = db.get_collection("drops")
    for drop in ack_drops:
        from_db = do_find_one(collection, {"drop": drop})
        assert from_db is not None
        assert from_db["config"] == config_name
        assert from_db["firmware"] is None


@pytest.mark.parametrize(
    "fields",
    [["config"], ["config", "firmware"], ["firmware"]],
    ids=["config", "both", "firmware"],
)
def test_post_config_firm_optional(client, db, fields):
    names = {"config": "test-config", "firmware": "test-firmware"}
    data = {"target_drops": ["test-drop"]}
    for field in fields:
        data[field] = names[field]
    resp = client.post("/versions/", json=data)
    assert resp.status_code == 200
    ack_drops = resp.json()["data"]
    collection = db.get_collection("drops")
    for drop in ack_drops:
        from_db = do_find_one(collection, {"drop": drop})
        for field in fields:
            assert from_db[field] == names[field]
        for field in set(names.keys()) - set(fields):
            assert from_db[field] is None


@pytest.mark.parametrize(
    "data",
    [
        {"config": "test-config", "firmware": "test-firmware"},
        {"firmware": "test-firmware"},
        {"config": "test-config"},
    ],
    ids=["config", "both", "firmware"],
)
def test_post_missing_drops(client, data):
    resp = client.post("/versions/", json=data)
    assert resp.status_code == 422


def test_post_neither(client):
    resp = client.post("/versions/", json={"target_drops": ["test"]})
    assert resp.status_code == 422


@pytest.mark.parametrize("has_generic", [True, False], ids=["generic", "no_generic"])
@pytest.mark.parametrize(
    "cfg, firm",
    [("1.1", "0.9.2"), (None, "0.9.2"), ("1.1", None)],
    ids=["ok", "missing_cfg", "missing_firm"],
)
def test_get_nominal(client, db, has_generic, cfg, firm):
    data = {"drop": "test", "config": cfg, "firmware": firm}
    collection = db.get_collection("drops")
    do_insert_one(collection, data)
    default = "0" if has_generic else "2.2"
    if has_generic:
        do_insert_one(
            collection, {"drop": "generic", "config": default, "firmware": default}
        )
    resp = client.get("/versions/", params={"drop": "test"})
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["config"] == cfg if cfg else default
    assert resp_data["firmware"] == firm if firm else default


def test_get_missing_drop_param(client):
    resp = client.get("/versions/")
    assert resp.status_code == 422
