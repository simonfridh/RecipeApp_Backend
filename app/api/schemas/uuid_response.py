from pydantic import BaseModel


class UuidResponse(BaseModel):
    uuid: str