from app.data.usda.mapper import usda_mapper
from app.data.usda.usda_client import UsdaClient
from app.domain.interfaces.repositories.nutrition_repository import NutritionRepository
from app.domain.models.recipe.ingredient import Ingredient
from app.domain.models.recipe.nutrition import Nutrition


class UsdaRepository(NutritionRepository):
    def __init__(self, api_key: str):
        self.client = UsdaClient(api_key)

    def fetch_nutrition(self, ingredient: Ingredient) -> Nutrition | None:
        if ingredient.name is None: raise ValueError("ingredient could not be parsed")
        if ingredient.name.lower() == "water" or ingredient.grams_estimate is None:
            #skipping water and ingredients estimated to be weightless or near 0g
            return None

        usda_json = self.client.fetch(ingredient.name)
        return usda_mapper(usda_json, ingredient)