from typing import List
from pydantic import BaseModel, Field


class ConfigDBSchema(BaseModel):
    version: str = Field(..., min_length=1)
    config: dict = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "version": "drops-client1_v1.2",
                "config": {
                    "DropQtyToDeliver": "4",
                    "MaxDeliveryDelay": "3",
                    "TransmissionPeriod": "2000",
                },
            }
        }


class ConfigPostSchema(BaseModel):
    target_drops: List[str] = Field(...)
    config: ConfigDBSchema = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "target_drops": ["test-drop1", "test-drop2"],
                "config": {
                    "version": "drops-client1_v1.2",
                    "config": {
                        "DropQtyToDeliver": "4",
                        "MaxDeliveryDelay": "3",
                        "TransmissionPeriod": "2000",
                    },
                },
            }
        }


class ConfigRespSchema(BaseModel):
    config: dict = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "config": {
                    "DropQtyToDeliver": "4",
                    "MaxDeliveryDelay": "3",
                    "TransmissionPeriod": "2000",
                }
            }
        }
