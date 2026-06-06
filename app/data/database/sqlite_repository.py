from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.data.database.tables.evaluation_db import EvaluationDb
from app.data.database.tables.recipe_db import RecipeDB
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.models.evaluation.Evaluation import Evaluation
from app.domain.models.recipe.recipe import Recipe


class SQLiteRepository(DbRepository):
    def __init__(self, db: Session):
        self.db = db


    #Recipes
    def get_generated_recipe_by_id(self, uuid: UUID) -> Recipe | None:
        generated_recipe = self.db.query(RecipeDB.generated_recipe).filter(RecipeDB.uuid == str(uuid)).scalar()
        if generated_recipe is None: return None
        return Recipe.model_validate(generated_recipe)

    def get_original_recipe_by_id(self, uuid: UUID) -> Recipe | None:
        original_recipe = self.db.query(RecipeDB.original_recipe).filter(RecipeDB.uuid == str(uuid)).scalar()
        if original_recipe is None: return None
        return Recipe.model_validate(original_recipe)

    def get_similarity_by_id(self, uuid: UUID) -> float | None:
        similarity = self.db.query(RecipeDB.similarity).filter(RecipeDB.uuid == str(uuid)).scalar()
        if similarity is None: return None
        return float(similarity)

    def get_uuid_by_url(self, url: str) -> UUID | None:
        recipe_uuid = self.db.query(RecipeDB.uuid).filter(RecipeDB.url == url).scalar()
        if recipe_uuid is None: return None
        return UUID(recipe_uuid)

    def save_recipe(self, generated_recipe: Recipe, original_recipe: Recipe, similarity: float) -> UUID:
        uuid = uuid4()
        recipe_db = RecipeDB(
            uuid = str(uuid),
            url = original_recipe.url,
            generated_recipe = generated_recipe.model_dump(mode="json"),
            original_recipe = original_recipe.model_dump(mode="json"),
            similarity = similarity
        )
        self.db.add(recipe_db)
        self.db.commit()
        return uuid

    #Evaluation
    def get_evaluation_by_id(self, uuid: UUID) -> Evaluation | None:
        evaluation = self.db.query(EvaluationDb.evaluation).filter(EvaluationDb.uuid == str(uuid)).scalar()
        if evaluation is None: return None
        return Evaluation.model_validate(evaluation)

    def get_evaluation_by_url(self, url: str) -> Evaluation | None:
        evaluation = self.db.query(EvaluationDb.evaluation).filter(EvaluationDb.url == url).scalar()
        if evaluation is None: return None
        return Evaluation.model_validate(evaluation)

    def save_evaluation(self, recipe_uuid: UUID, recipe_url: str, evaluation: Evaluation) -> UUID:
        evaluation_db = EvaluationDb(
            uuid = str(recipe_uuid),
            url = recipe_url,
            evaluation = evaluation.model_dump(mode="json"),
        )
        self.db.add(evaluation_db)
        self.db.commit()
        return recipe_uuid
