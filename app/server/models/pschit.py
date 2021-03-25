from typing import Optional

from pydantic import BaseModel, Field


class PschitSchema(BaseModel):
    drop_id: str = Field(...)
    timestamp: str = Field(...)
    location: str = Field(...)
    count: int = Field(ge=0.0)

    class Config:
        schema_extra = {
            "example": {
                "drop_id": "c23a-bd22-ff89",
                "timestamp": "Mon Mar 15 14:16:39 UTC 2021",
                "location": "Boutique Galleries Lafayette",
                "count": 2,
            }
        }


class UpdatePschitModel(BaseModel):
    drop_id: Optional[str]
    timestamp: Optional[str]
    location: Optional[str]
    count: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "drop_id": "c23a-bd22-ff89",
                "timestamp": "Mon Mar 15 14:16:39 UTC 2021",
                "location": "Boutique Galleries Lafayette",
                "count": 2,
            }
        }


def ResponseModel(data, message):
    return {"data": [data], "code": 200, "message": message}


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
