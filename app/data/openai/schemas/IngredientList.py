from pydantic import BaseModel

from app.domain.models.ingredient import Ingredient


class IngredientList(BaseModel):
    ingredients: list[Ingredient]