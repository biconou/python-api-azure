from pydantic import BaseModel, Field


class VersionsRespSchema(BaseModel):
    config: str = Field(...)
    firmware: str = Field(...)

    class Config:
        schema_extra = {
            "example": {"config": "drops-client1_v1.2", "firmware": "0.9.2"}
        }
