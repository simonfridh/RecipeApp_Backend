from pydantic import BaseModel

class Instruction(BaseModel):
    step: int
    text: str