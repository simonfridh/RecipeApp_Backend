from pydantic import BaseModel

class OptimizeRequest(BaseModel):
    url: str