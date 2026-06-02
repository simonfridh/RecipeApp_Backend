from pydantic import BaseModel

from app.domain.models.nutrition import Nutrition


class Evaluation(BaseModel):
    original_recipe_nutrition: Nutrition
    generated_recipe_nutrition: Nutrition

    original_calculated_nutrition: Nutrition
    generated_calculated_nutrition: Nutrition

    cosine_similarity: float

    #Relative nutrition recipe (%)
    #Relative nutrition calculated (%)


