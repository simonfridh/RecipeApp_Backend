from pydantic import BaseModel

class Nutrition(BaseModel):
    calories_kcal: int | None = None
    fat_g: float | None = None
    carbs_g: float | None = None
    proteins_g: float | None = None