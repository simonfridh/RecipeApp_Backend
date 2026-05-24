from pydantic import BaseModel

from app.domain.models.recipe import Recipe


class RecipeComparison(BaseModel):
    generated_recipe: Recipe
    original_recipe: Recipe