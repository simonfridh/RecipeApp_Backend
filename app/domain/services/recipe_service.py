from uuid import UUID

from app.domain.interfaces.repositories.ai_repository import AiRepository
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.interfaces.repositories.parser_repository import ParserRepository
from app.domain.models.recipe import Recipe
from app.domain.models.recipe_comparison import RecipeComparison


class RecipeService:
    def __init__(
            self,
            parser_repository: ParserRepository,
            recipe_repository: DbRepository,
            ai_repository: AiRepository
    ):
        self.parser_repository = parser_repository
        self.recipe_repository = recipe_repository
        self.ai_repository = ai_repository

    def get_recipe(self, uuid: UUID) -> Recipe | None:
        return self.recipe_repository.get_generated_recipe_by_id(uuid)

    def get_recipe_comparison(self, uuid: UUID) -> RecipeComparison | None:
        generated_recipe = self.recipe_repository.get_generated_recipe_by_id(uuid)
        original_recipe = self.recipe_repository.get_original_recipe_by_id(uuid)

        if generated_recipe is not None and original_recipe is not None:
            return RecipeComparison(
                generated_recipe=generated_recipe,
                original_recipe=original_recipe
            )
        else:
            return None

    def optimize_recipe(self, url: str) -> UUID:
        # Check if recipe already has been generated for this page
        existing_recipe_uuid = self.recipe_repository.get_uuid_by_url(url)
        if existing_recipe_uuid is not None:
            print("Using existing recipe uuid")
            return existing_recipe_uuid

        # If not create new recipe
        else:
            print("Fetching recipe from: " + url)
            original_recipe = self.parser_repository.parse(url)

            # TODO Generate a new recipe from original_recipe with AI
            generated_recipe = self.ai_repository.generate_new_recipe(original_recipe)

            uuid = self.recipe_repository.save(generated_recipe,original_recipe)
            return uuid