import pytest

from .testing_utils import do_find_one, do_find


@pytest.mark.parametrize(
    "drop, data",
    [
        ("test_drop", [{"time": 1618844678, "type": "PowerON"}]),
        (
            "test_drop",
            [{"time": 1618844900 + i, "type": "PowerON" + str(i)} for i in range(100)],
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
    nb_inserted = resp.json()
    assert nb_inserted == len(data)
    from_db = [e for e in do_find(collection, {"drop": drop})]  # noqa
    assert nb_inserted == len(from_db)
    for event in from_db:
        event.pop("_id")
        event.pop("drop")
    assert sorted(from_db, key=lambda x: x["time"]) == sorted(
        [{k: str(v) for k, v in d.items()} for d in data], key=lambda x: x["time"]
    )


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
    """Current behaviour: Insert every thing, even if malformed event"""
    collection = db.get_collection("events")
    tag = f"missing_field_{missing_field}"
    body = dict(drop="test_drop", data=[{"time": tag, "type": tag}])
    body["data"][0].pop(missing_field)
    resp = client.post("/events/", json=body)
    assert resp.status_code == 200
    assert (
        do_find_one(collection, {"type" if missing_field == "time" else "time": tag})
        is not None
    )


@pytest.mark.parametrize("missing_field", ["time", "type"])
def test_best_effort(client, db, caplog, missing_field):
    """
    Test that when one of the events is not valid,
    all of the events are correctly saved in DB
    NOTE: Looks like a duplicate of the previous one, but it is actually
    intended to be reused when in real prod situation we want to discard
    malformed events (if...)
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
    # Best Effort: 3 documents are created
    assert resp.json() == 3
    # Invalid entry is saved, and the two valid entries are
    assert (
        do_find_one(collection, {"type" if missing_field == "time" else "time": tag})
        is not None
    )
    assert do_find_one(collection, {"type": "CorrectBefore"}) is not None
    assert do_find_one(collection, {"type": "CorrectAfter"}) is not None
    # A Warning log has been emitted with the event content
    assert str(incorrect_event)[1:-2] in caplog.text
