from typing import List
from pydantic import BaseModel, Field


class DropDBSchema(BaseModel):
    """Only Informative"""

    drop: str = Field(...)
    config: str = Field(None)
    firmware: str = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "drop": "test-drop",
                "config": "drops-client1_v1.2",
                "firmware": None,
            }
        }


class DropPostSchema(BaseModel):
    target_drops: List[str] = Field(...)
    config: str = Field(None, min_length=1)
    firmware: str = Field(None, min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "target_drops": ["test-drop", "test-drop2"],
                "config": "drops-client1_v1.2",
                "firmware": None,
            }
        }
