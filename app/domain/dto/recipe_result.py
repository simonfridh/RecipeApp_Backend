from pydantic import BaseModel

from app.domain.models.recipe import Recipe

class RecipeResult(BaseModel):
    generated_recipe: Recipe
    similarity: float