from typing import Protocol
from uuid import UUID

from app.domain.models.recipe import Recipe


class DbRepository(Protocol):
    def get_by_id(self, uuid: UUID) -> Recipe | None:
        ...
    def get_uuid_by_url(self, url: str) -> UUID| None:
        ...
    def save(self, recipe: Recipe) -> UUID:
        ...