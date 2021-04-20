from fastapi import APIRouter, Body

from app.server.database import add_event
from app.server.models.events import EventsSchema
from app.server.models.common import ResponseModel

router = APIRouter()


@router.post("/", response_description="Events data added into the database")
async def add_events_data(events_struct: EventsSchema = Body(...)):
    event_ids = []
    for event in events_struct.data:
        event_id = await add_event(events_struct.drop, event)
        event_ids.append(str(event_id))
    resp = ResponseModel(event_ids, f"{len(event_ids)} events added successfully.")
    return resp
