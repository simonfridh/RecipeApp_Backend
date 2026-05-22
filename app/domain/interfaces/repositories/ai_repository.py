from typing import Protocol

from app.domain.models.recipe import Recipe


class AiRepository(Protocol):
    def generate_new_recipe(self, recipe: Recipe) -> Recipe:
        ...