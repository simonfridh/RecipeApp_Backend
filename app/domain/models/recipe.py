from pydantic import BaseModel

from app.domain.models.ingredient import Ingredient
from app.domain.models.instruction import Instruction
from app.domain.models.nutrition import Nutrition


class Recipe(BaseModel):
    name: str
    description: str | None = None
    url: str | None = None

    ingredients: list[Ingredient]
    instructions: list[Instruction]

    nutrition: Nutrition | None = None
