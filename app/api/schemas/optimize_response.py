from uuid import UUID

from pydantic import BaseModel

class OptimizeResponse(BaseModel):
    uuid: UUID