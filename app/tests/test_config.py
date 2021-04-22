import pytest

from .testing_utils import do_find_one


@pytest.mark.parametrize(
    "drops, version, config",
    [
        (["generic"], "0", {"DropQtyToDeliver": "4"}),
        (["test1"], "0", {"DropQtyToDeliver": "4"}),
        (["test1", "test2"], "test-version1.0", {"DropQtyToDeliver": "4"}),
        ([], "0", {"DropQtyToDeliver": "4"}),
        (["test1"], "0", {"0": "4", "a": "a", "b": "b", "c": 3000}),
    ],
    ids=["generic", "one", "two", "config_only", "any_fields"],
)
def test_post_nominal(client, db, drops, version, config):
    resp = client.post(
        "/config/",
        json={"target_drops": drops, "config": {"version": version, "config": config}},
    )
    assert resp.status_code == 200
    resp_dict = resp.json()
    ids = resp_dict["drops"]
    assert len(ids) == len(drops)
    assert "config" in resp_dict
    config_collection = db.get_collection("configs")
    config_from_db = do_find_one(config_collection, {"version": version})
    assert config_from_db["config"] == config
    drops_collection = db.get_collection("drops")
    for drop in drops:
        from_db = do_find_one(drops_collection, {"drop": drop})
        assert from_db is not None
        assert from_db["config"] == version


@pytest.mark.parametrize("missing", ["target_drops", "config", "_version", "_config"])
def test_post_missing_field(client, missing):
    data = {
        "target_drops": ["drop1"],
        "config": {"version": "version", "config": {"a": "a"}},
    }
    if missing.startswith("_"):
        data["config"].pop(missing[1:])
    else:
        data.pop(missing)
    resp = client.post("/config/", json=data)
    assert resp.status_code == 422


# TODO: test for get nominal (with/without generic) / error
