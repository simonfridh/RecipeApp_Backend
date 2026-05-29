import json
from uuid import UUID

from app.domain.dto.recipe_comparison_result import RecipeComparisonResult
from app.domain.dto.recipe_result import RecipeResult
from app.domain.interfaces.repositories.ai_repository import AiRepository
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.interfaces.repositories.nutrition_repository import NutritionRepository
from app.domain.interfaces.repositories.parser_repository import ParserRepository
from app.domain.math.cosine_similarity import cosine_similarity
from app.domain.math.nutrition_per_serving import nutrition_per_serving
from app.domain.models.nutrition import Nutrition
from app.domain.models.recipe import Recipe


class RecipeService:
    def __init__(
            self,
            parser_repository: ParserRepository,
            db_repository: DbRepository,
            ai_repository: AiRepository,
            nutrition_repository: NutritionRepository
    ):
        self.parser_repository = parser_repository
        self.db_repository = db_repository
        self.ai_repository = ai_repository
        self.nutrition_repository = nutrition_repository

    def get_recipe(self, uuid: UUID) -> RecipeResult | None:
        generated_recipe = self.db_repository.get_generated_recipe_by_id(uuid)
        similarity = self.db_repository.get_similarity_by_id(uuid)
        if generated_recipe is None or similarity is None: return None
        return RecipeResult(
            generated_recipe=generated_recipe,
            similarity=similarity
        )

    def get_recipe_comparison(self, uuid: UUID) -> RecipeComparisonResult | None:
        generated_recipe = self.db_repository.get_generated_recipe_by_id(uuid)
        original_recipe = self.db_repository.get_original_recipe_by_id(uuid)
        similarity = self.db_repository.get_similarity_by_id(uuid)

        if generated_recipe is None or original_recipe is None or similarity is None:
            return None
        return RecipeComparisonResult(
            generated_recipe=generated_recipe,
            original_recipe=original_recipe,
            similarity = similarity
        )


    def optimize_recipe(self, url: str) -> UUID:
        # Check if recipe already has been generated for this page
        existing_recipe_uuid = self.db_repository.get_uuid_by_url(url)
        if existing_recipe_uuid is not None:
            print("Using existing recipe uuid")
            return existing_recipe_uuid

        # If not create new recipe
        else:
            #Retrieve recipe from web and generate new recipe inspired by it
            web_recipe = self.parser_repository.parse(url)
            original_recipe = self.ai_repository.normalize_ingredients(web_recipe)
            generated_recipe = self.ai_repository.generate_new_recipe(original_recipe)

            #Calculate similarity through embeddings and cosine similarity
            original_embedding = self.ai_repository.create_embedding(original_recipe)
            generated_embedding = self.ai_repository.create_embedding(generated_recipe)
            similarity = cosine_similarity(original_embedding,generated_embedding)

            #Save results to DB and return UUID to user
            uuid = self.db_repository.save(generated_recipe, original_recipe,similarity)
            return uuid

    def test_similarity(self, first_recipe_url:str, second_recipe_url) -> float:
        first_recipe = self.parser_repository.parse(first_recipe_url)
        second_recipe = self.parser_repository.parse(second_recipe_url)

        first_embedding = self.ai_repository.create_embedding(first_recipe)
        second_embedding = self.ai_repository.create_embedding(second_recipe)
        similarity = cosine_similarity(first_embedding,second_embedding)
        return similarity

    def test_calorie_calculation(self,uuid: UUID):
        generated_recipe = self.db_repository.get_generated_recipe_by_id(uuid)
        generated_nutrition = self._calculate_calories(generated_recipe)
        if generated_nutrition is not None:
            print(f"generated_nutrition: {generated_nutrition.model_dump_json(indent=2)}")

        original_recipe = self.db_repository.get_original_recipe_by_id(uuid)
        original_nutrition = self._calculate_calories(original_recipe)
        if original_nutrition is not None:
            print(f"generated_nutrition: {original_nutrition.model_dump_json(indent=2)}")

        return uuid

    def _calculate_calories(self,recipe: Recipe | None) -> Nutrition | None:
        if recipe is None: return None
        nutrition_list:list[Nutrition] = []
        for ingredient in recipe.ingredients:
            nutrition_list.append(self.nutrition_repository.fetch_nutrition(ingredient))
        return nutrition_per_serving(nutrition_list, recipe.recipe_yield)
