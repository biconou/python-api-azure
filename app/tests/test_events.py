import pytest
from bson.objectid import ObjectId

from .testing_utils import do_find_one


@pytest.mark.parametrize(
    "drop, data",
    [
        ("test_drop", [{"time": 1618844678, "type": "PowerON"}]),
        (
            "test_drop",
            [{"time": 1618844900 + i, "type": "PowerON"} for i in range(100)],
        ),
        ("test_drop", [{"time": "1618844678", "type": "RandomType"}]),
        ("test_drop", [{"time": "1618844678", "type": "PowerON", "a": "a", "b": "b"}]),
        ("test_drop", []),
    ],
    ids=["simple", "multiples", "randType", "randFields", "empty"],
)
def test_nominal(client, db, drop, data):
    collection = db.get_collection("events")
    resp = client.post("/events/", json={"drop": drop, "data": data})
    assert resp.status_code == 200
    ids = resp.json()["data"]
    assert len(ids) == len(data)
    for _id, event in zip(ids, data):
        from_db = do_find_one(collection, {"_id": ObjectId(_id)})
        assert from_db is not None
        assert from_db["drop"] == drop
        assert from_db["time"] == str(event["time"])
        for field in event.keys():
            assert field in from_db


@pytest.mark.parametrize("missing_field", ["drop", "data"])
def test_missing_field(client, db, missing_field):
    collection = db.get_collection("events")
    tag = f"missing_field_{missing_field}"
    body = dict(drop="test_drop", data=[{"time": "1618844678", "type": tag}])
    body.pop(missing_field)
    resp = client.post("/events/", json=body)
    assert resp.status_code == 422
    assert do_find_one(collection, {"type": tag}) is None


@pytest.mark.parametrize("missing_field", ["time", "type"])
def test_missing_field_in_event(client, db, missing_field):
    collection = db.get_collection("events")
    tag = f"missing_field_{missing_field}"
    body = dict(drop="test_drop", data=[{"time": tag, "type": tag}])
    body["data"][0].pop(missing_field)
    resp = client.post("/events/", json=body)
    assert resp.status_code == 200
    assert (
        do_find_one(collection, {"type" if missing_field == "time" else "time": tag})
        is None
    )


@pytest.mark.parametrize("missing_field", ["time", "type"])
def test_best_effort(client, db, caplog, missing_field):
    """
    Test that when one of the events is not valid,
    all of the other events are correctly saved in DB
    """
    collection = db.get_collection("events")
    tag = f"missing_field_{missing_field}"
    incorrect_event = {"time": tag, "type": tag}
    incorrect_event.pop(missing_field)
    body = dict(
        drop="test_drop",
        data=[
            {"time": "1618844678", "type": "CorrectBefore"},
            incorrect_event,
            {"time": "1618844678", "type": "CorrectAfter"},
        ],
    )
    resp = client.post("/events/", json=body)
    # Request is successful
    assert resp.status_code == 200
    # Best Effort: 2 documents are created
    assert len(resp.json()["data"]) == 2
    # Invalid entry is not saved, but the two valid entries are
    assert (
        do_find_one(collection, {"type" if missing_field == "time" else "time": tag})
        is None
    )
    assert do_find_one(collection, {"type": "CorrectBefore"}) is not None
    assert do_find_one(collection, {"type": "CorrectAfter"}) is not None
    # A Warning log has been emitted with the event content
    assert str(incorrect_event)[1:-2] in caplog.text
