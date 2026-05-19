from uuid import UUID

from app.data.parsers.fetch_html import fetch_html
from app.domain.interfaces.i_parser import IParser
from app.domain.interfaces.i_recipe_repository import IRecipeRepository
from app.domain.models.recipe import Recipe


class RecipeService:
    def __init__(
            self,
            parser: IParser,
            recipe_repository: IRecipeRepository
    ):
        self.parser = parser
        self.recipe_repository = recipe_repository

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
            html = fetch_html(url)
            print("Fetching recipe html from: " + url)
            parsed_recipe = self.parser.parse(html,url)
            # TODO Generate a new recipe from parsed_recipe with AI
            uuid = self.recipe_repository.save(parsed_recipe)
            return uuid