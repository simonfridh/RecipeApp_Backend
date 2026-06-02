from uuid import UUID

from app.domain.interfaces.repositories.ai_repository import AiRepository
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.interfaces.repositories.nutrition_repository import NutritionRepository
from app.domain.math.nutrition_per_serving import nutrition_per_serving
from app.domain.models.evaluation.Evaluation import Evaluation
from app.domain.models.nutrition import Nutrition
from app.domain.models.recipe import Recipe


class EvaluationService:
    def __init__(
            self,
            db_repository: DbRepository,
            ai_repository: AiRepository,
            nutrition_repository: NutritionRepository
    ):
        self.db_repository = db_repository
        self.ai_repository = ai_repository
        self.nutrition_repository = nutrition_repository

    def create_evaluation(self, url):

        uuid = self.db_repository.get_uuid_by_url(url)
        if uuid is None: return None
        cached_evaluation = self.db_repository.get_evaluation_by_id(uuid)
        if cached_evaluation is not None:
            print("Cached evaluation")
            return cached_evaluation

        # Retrieve all needed data from db
        generated_recipe = self.db_repository.get_generated_recipe_by_id(uuid)
        original_recipe = self.db_repository.get_original_recipe_by_id(uuid)
        cosine_similarity = self.db_repository.get_similarity_by_id(uuid)
        if generated_recipe is None or original_recipe is None or cosine_similarity is None: return None

        #Evaluation
        original_recipe_nutrition = original_recipe.nutrition
        generated_recipe_nutrition = generated_recipe.nutrition
        if original_recipe_nutrition is None or generated_recipe_nutrition is None: return None

        generated_calculated_nutrition = self._calculate_calories(generated_recipe)
        original_calculated_nutrition = self._calculate_calories(original_recipe)
        if generated_calculated_nutrition is None or original_calculated_nutrition is None: return None

        evaluation = Evaluation(
            original_recipe_nutrition=original_recipe_nutrition,
            generated_recipe_nutrition=generated_recipe_nutrition,
            original_calculated_nutrition=original_calculated_nutrition,
            generated_calculated_nutrition=generated_calculated_nutrition,
            cosine_similarity=cosine_similarity
        )

        self.db_repository.save_evaluation(uuid, url, evaluation)
        return evaluation

    def _calculate_calories(self,recipe: Recipe | None) -> Nutrition | None:
        if recipe is None: return None
        nutrition_list:list[Nutrition] = []
        for ingredient in recipe.ingredients:
            nutrition_list.append(self.nutrition_repository.fetch_nutrition(ingredient))
        return nutrition_per_serving(nutrition_list, recipe.recipe_yield)