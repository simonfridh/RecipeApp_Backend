from typing import Protocol

from app.domain.models.ingredient import Ingredient
from app.domain.models.nutrition import Nutrition


class NutritionRepository(Protocol):
    def fetch_nutrition(self, ingredient: Ingredient) -> Nutrition:
        ...