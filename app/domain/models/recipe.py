from pydantic import BaseModel

from app.domain.models.ingredient import Ingredient
from app.domain.models.instruction import Instruction
from app.domain.models.nutrition import Nutrition


class Recipe(BaseModel):
    name: str
    url: str

    total_time: str | None = None
    cooking_method: str | None = None
    recipe_category: str | None = None
    recipe_cuisine: str | None = None
    recipe_yield: str | None = None

    ingredients: list[Ingredient]
    instructions: list[Instruction]

    nutrition: Nutrition | None = None
