import pytest

from .testing_utils import do_insert_one


@pytest.mark.parametrize("has_generic", [True, False], ids=["generic", "no_generic"])
@pytest.mark.parametrize(
    "cfg, firm",
    [("1.1", "0.9.2"), (None, "0.9.2"), ("1.1", None)],
    ids=["ok", "missing_cfg", "missing_firm"],
)
def test_nominal(client, db, has_generic, cfg, firm):
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


def test_missing_drop_param(client):
    resp = client.get("/versions/")
    assert resp.status_code == 422
