from typing import Protocol

from app.domain.models.recipe.recipe import Recipe


class RecipeParser(Protocol):
    def parse(self, html: str, url:str) -> Recipe:
        ...