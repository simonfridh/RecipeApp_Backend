from pydantic import BaseModel

from app.domain.models.recipe.ingredient import Ingredient


class IngredientList(BaseModel):
    ingredients: list[Ingredient]