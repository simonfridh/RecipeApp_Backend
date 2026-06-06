from pydantic import BaseModel

class Ingredient(BaseModel):
    raw_string: str
    name: str | None = None
    quantity: str | None = None
    unit: str | None = None
    grams_estimate: float | None = None
