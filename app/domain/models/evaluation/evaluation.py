from pydantic import BaseModel

from app.domain.models.evaluation.nutrition_search_result import NutritionSearchResult
from app.domain.models.recipe.nutrition import Nutrition


class Evaluation(BaseModel):
    original_recipe_nutrition: Nutrition
    generated_recipe_nutrition: Nutrition

    original_calculated_nutrition: Nutrition
    generated_calculated_nutrition: Nutrition

    cosine_similarity: float

    original_search_result: NutritionSearchResult
    generated_search_result: NutritionSearchResult


    #Relative nutrition recipe (%)
    #Relative nutrition calculated (%)


