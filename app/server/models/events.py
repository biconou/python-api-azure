from typing import List
from pydantic import BaseModel, Field


class EventsSchema(BaseModel):
    drop: str = Field(...)
    data: List[dict] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "drop": "c23a-bd22-ff89",
                "data": [
                    {"time": 1618844678, "type": "PowerON"},
                    {
                        "time": 1618844679,
                        "type": "Battery",
                        "Battery1State": "Empty",
                        "Battery2State": "Active",
                    },
                    {
                        "time": 1618844696,
                        "type": "DeliveredDrop",
                        "NbDelivered": 3,
                        "DropQtyToDeliver": 3,
                    },
                    {"time": 1618844706, "type": "StartTransmission"},
                    {"time": 1618844706, "type": "WiFiRSSI", "RSSI": -68},
                ],
            }
        }
