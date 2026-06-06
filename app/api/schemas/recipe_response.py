from pydantic import BaseModel

from app.domain.models.recipe.recipe import Recipe

class RecipeResponse(BaseModel):
    generated_recipe: Recipe
    similarity: float