from pydantic import BaseModel

from app.domain.models.recipe.recipe import Recipe

class RecipeComparisonResult(BaseModel):
    generated_recipe: Recipe
    original_recipe: Recipe
    similarity: float
