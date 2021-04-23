from pydantic import BaseModel, Field


class ConfigDBSchema(BaseModel):
    name: str = Field(..., min_length=1)
    config: dict = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "drops-client1_v1.2",
                "config": {
                    "DropQtyToDeliver": "4",
                    "MaxDeliveryDelay": "3",
                    "TransmissionPeriod": "2000",
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
