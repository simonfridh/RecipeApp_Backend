from pydantic import BaseModel


class NutritionSearchResult(BaseModel):
    matched_ingredients: list[str] = []
    failed_ingredients: list[str] = []
    skipped_ingredients: list[str] = []