from pydantic import BaseModel

class Nutrition(BaseModel):
    calories: str | None = None
    carbohydrates: str | None = None
    cholesterol: str | None = None
    fat: str | None = None
    fiber: str | None = None
    protein: str | None = None
    saturated_fat: str | None = None
    sodium: str | None = None
    sugar: str | None = None
    trans_fat: str | None = None
    unsaturated_fat: str | None = None