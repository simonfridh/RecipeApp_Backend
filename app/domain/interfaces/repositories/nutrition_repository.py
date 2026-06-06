from typing import Protocol

from app.domain.models.evaluation.ingredient_query_info import IngredientQueryInfo
from app.domain.models.recipe.ingredient import Ingredient
from app.domain.models.recipe.nutrition import Nutrition


class NutritionRepository(Protocol):
    def fetch_nutrition(self, ingredient: Ingredient) -> tuple[Nutrition, IngredientQueryInfo] | None:
        ...