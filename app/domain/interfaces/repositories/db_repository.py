from typing import Protocol
from uuid import UUID

from app.domain.models.evaluation.evaluation import Evaluation
from app.domain.models.recipe.recipe import Recipe


class DbRepository(Protocol):
    def get_generated_recipe_by_id(self, uuid: UUID) -> Recipe | None:
        ...
    def get_original_recipe_by_id(self, uuid: UUID) -> Recipe | None:
        ...

    def get_similarity_by_id(self, uuid: UUID) -> float | None:
        ...
    def get_uuid_by_url(self, url: str) -> UUID| None:
        ...

    def save_recipe(self, generated_recipe: Recipe, original_recipe: Recipe, similarity: float) -> UUID:
        ...

    def get_evaluation_by_id(self, uuid: UUID) -> Evaluation | None:
        ...

    def save_evaluation(self, recipe_uuid: UUID, recipe_url: str, evaluation: Evaluation) -> UUID:
        ...