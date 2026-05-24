from typing import Protocol
from uuid import UUID

from app.domain.models.recipe import Recipe


class DbRepository(Protocol):
    def get_generated_recipe_by_id(self, uuid: UUID) -> Recipe | None:
        ...
    def get_original_recipe_by_id(self, uuid: UUID) -> Recipe | None:
        ...
    def get_uuid_by_url(self, url: str) -> UUID| None:
        ...
    def save(self, generated_recipe: Recipe, original_recipe: Recipe) -> UUID:
        ...