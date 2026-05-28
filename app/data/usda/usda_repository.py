from app.data.usda.mapper import usda_mapper
from app.data.usda.usda_client import UsdaClient
from app.domain.interfaces.repositories.nutrition_repository import NutritionRepository
from app.domain.models.ingredient import Ingredient
from app.domain.models.nutrition import Nutrition


class UsdaRepository(NutritionRepository):
    def __init__(self, api_key: str):
        self.client = UsdaClient(api_key)

    def fetch_nutrition(self, ingredient: Ingredient) -> Nutrition:
        if ingredient.name is None or ingredient.grams_estimate is None or ingredient.name.lower() == "water":
            return Nutrition()

        usda_json = self.client.fetch(ingredient.name)

        try:
            return usda_mapper(usda_json, ingredient)
        except ValueError as e:
            print(f"failed to fetch: {ingredient.name}")
            return Nutrition()
