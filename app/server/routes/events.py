from motor.motor_asyncio import AsyncIOMotorDatabase as DataBase  # noqa
from fastapi import APIRouter, Body, Depends
from fastapi.logger import logger
from fastapi.encoders import jsonable_encoder


from ..database import get_db
from ..models.events import EventsSchema, EventDBSchema
from ..models.common import response_model

events_router = APIRouter()


@events_router.post("/", summary="Send multiple events for a given drop")
async def add_events_data(
    events_struct: EventsSchema = Body(...), db: DataBase = Depends(get_db)
):
    event_ids = []
    collection = db.get_collection("events")
    for event in events_struct.data:
        if event.type is None or event.time is None:
            logger.warning(
                f"[drop={events_struct.drop}] Ignoring event: "
                f"missing 'time' or 'type' field in event {event.dict()}"
            )
            continue
        db_event = EventDBSchema.from_event(event, events_struct.drop)
        inserted_event = await collection.insert_one(jsonable_encoder(db_event))
        event_ids.append(str(inserted_event.inserted_id))
    resp = response_model(event_ids, f"{len(event_ids)} events added successfully.")
    return resp
