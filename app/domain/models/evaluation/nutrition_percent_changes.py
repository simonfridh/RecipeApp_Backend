from pydantic import BaseModel


class NutritionPercentChanges(BaseModel):
    calories: float | None = None
    carbohydrates: float | None = None
    cholesterol: float | None = None
    fat: float | None = None
    fiber: float | None = None
    protein: float | None = None
    saturated_fat: float | None = None
    sodium: float | None = None
    sugar: float | None = None
    trans_fat: float | None = None
    unsaturated_fat: float | None = None