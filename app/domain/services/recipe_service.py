from uuid import UUID

from app.domain.interfaces.repositories import ai_repository
from app.domain.interfaces.repositories.ai_repository import AiRepository
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.interfaces.repositories.parser_repository import ParserRepository
from app.domain.models.recipe import Recipe


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
        return self.recipe_repository.get_by_id(uuid)

    def optimize_recipe(self, url: str) -> UUID:
        # Check if recipe already has been generated for this page
        existing_recipe_uuid = self.recipe_repository.get_uuid_by_url(url)
        if existing_recipe_uuid is not None:
            print("Using existing recipe uuid")
            return existing_recipe_uuid

        # If not create new recipe
        else:
            print("Fetching recipe from: " + url)
            parsed_recipe = self.parser_repository.parse(url)

            # TODO Generate a new recipe from parsed_recipe with AI
            self.ai_repository.generate_new_recipe(parsed_recipe)

            uuid = self.recipe_repository.save(parsed_recipe)
            return uuid