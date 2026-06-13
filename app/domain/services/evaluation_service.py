from uuid import UUID

from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.interfaces.repositories.nutrition_repository import NutritionRepository
from app.domain.math.calculate_percentage_point_error import calculate_percentage_point_error
from app.domain.math.jaccard_similarity import jaccard_similarity
from app.domain.math.calculate_nutrition_change import calculate_nutrition_change
from app.domain.math.nutrition_per_serving import nutrition_per_serving
from app.domain.models.evaluation.evaluation import Evaluation
from app.domain.models.evaluation.nutrition_search_info import NutritionSearchInfo
from app.domain.models.recipe.nutrition import Nutrition
from app.domain.models.recipe.recipe import Recipe


class EvaluationService:
    def __init__(
            self,
            db_repository: DbRepository,
            nutrition_repository: NutritionRepository
    ):
        self.db_repository = db_repository
        self.nutrition_repository = nutrition_repository

    def get_evaluation(self, uuid: UUID) -> Evaluation:
        evaluation = self.db_repository.get_evaluation_by_id(uuid)
        if evaluation is None: raise ValueError("Evaluation could not be retrieved")
        return evaluation

    def create_evaluation(self, uuid: UUID):
        print("Starting background job for evaluation")
        # Check database for already created evaluations.
        if self.db_repository.get_evaluation_by_id(uuid) is not None:
            print("Evaluation already exists")
            return

        # Retrieve all needed data from db
        generated_recipe = self.db_repository.get_generated_recipe_by_id(uuid)
        original_recipe = self.db_repository.get_original_recipe_by_id(uuid)
        cosine_similarity = self.db_repository.get_similarity_by_id(uuid)
        if generated_recipe is None or original_recipe is None or cosine_similarity is None:
            print("evaluation could not be created: recipe is none")
            return
        if original_recipe.nutrition is None or generated_recipe.nutrition is None:
            print("evaluation could not be created: nutrition within recipe is none")
            return

        ingredient_overlap = jaccard_similarity(generated_recipe.ingredients, original_recipe.ingredients)
        original_calculated_nutrition, original_search_info = self._calculate_calories(original_recipe)
        generated_calculated_nutrition, generated_search_info = self._calculate_calories(generated_recipe)
        recipe_nutrition_changes = calculate_nutrition_change(generated_recipe.nutrition, original_recipe.nutrition)
        calculated_nutrition_changes = calculate_nutrition_change(generated_calculated_nutrition,original_calculated_nutrition)
        percentage_point_error = calculate_percentage_point_error(calculated_nutrition_changes, recipe_nutrition_changes)

        evaluation = Evaluation(
            original_recipe_nutrition=original_recipe.nutrition,
            generated_recipe_nutrition=generated_recipe.nutrition,
            original_calculated_nutrition=original_calculated_nutrition,
            generated_calculated_nutrition=generated_calculated_nutrition,
            recipe_nutrition_changes=recipe_nutrition_changes,
            calculated_nutrition_changes=calculated_nutrition_changes,
            percentage_point_error=percentage_point_error,
            cosine_similarity=cosine_similarity,
            ingredient_overlap=ingredient_overlap,
            original_search_info= original_search_info,
            generated_search_info= generated_search_info
        )
        self.db_repository.save_evaluation(uuid, original_recipe.url, evaluation)
        print("successfully created evaluation")
        return

    def _calculate_calories(self,recipe: Recipe) -> tuple[Nutrition, NutritionSearchInfo]:
        nutrition_list: list[Nutrition] = []
        search_result: NutritionSearchInfo = NutritionSearchInfo()
        for ingredient in recipe.ingredients:
            try:
                fetch_result = self.nutrition_repository.fetch_nutrition(ingredient)
                if fetch_result is not None:
                    nutrition, ingredient_query_info = fetch_result
                    nutrition_list.append(nutrition)
                    search_result.matched_ingredients.append(ingredient_query_info)
                else:
                    search_result.skipped_ingredients.append(ingredient.name or ingredient.raw_string)
            except ValueError:
                search_result.failed_ingredients.append(ingredient.name or ingredient.raw_string)
        return nutrition_per_serving(nutrition_list, recipe.recipe_yield), search_result