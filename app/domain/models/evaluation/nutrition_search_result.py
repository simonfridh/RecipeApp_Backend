from pydantic import BaseModel

from app.domain.models.evaluation.ingredient_query_info import IngredientQueryInfo


class NutritionSearchResult(BaseModel):
    matched_ingredients: list[IngredientQueryInfo] = []
    failed_ingredients: list[str] = []
    skipped_ingredients: list[str] = []