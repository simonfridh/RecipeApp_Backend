from pydantic import BaseModel

from app.domain.models.evaluation.nutrition_search_info import NutritionSearchInfo
from app.domain.models.recipe.nutrition import Nutrition


class Evaluation(BaseModel):
    original_recipe_nutrition: Nutrition
    generated_recipe_nutrition: Nutrition

    original_calculated_nutrition: Nutrition
    generated_calculated_nutrition: Nutrition

    cosine_similarity: float

    original_search_info: NutritionSearchInfo
    generated_search_info: NutritionSearchInfo


    #Relative nutrition recipe (%)
    #Relative nutrition calculated (%)


