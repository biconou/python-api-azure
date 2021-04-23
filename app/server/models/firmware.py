import bson
from pydantic import BaseModel, Field


class FirmwareDBSchema(BaseModel):
    """Only Informative"""

    name: str = Field(..., min_length=1)
    firmware: bson.binary.Binary = Field(...)
