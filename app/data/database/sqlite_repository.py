from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.data.database.tables.recipe_db import RecipeDB
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.models.recipe import Recipe


class SQLiteRepository(DbRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_generated_recipe_by_id(self, uuid: UUID) -> Recipe | None:
        generated_recipe = self.db.query(RecipeDB.generated_recipe).filter(RecipeDB.uuid == str(uuid)).scalar()
        if generated_recipe is None: return None
        return Recipe.model_validate(generated_recipe)

    def get_original_recipe_by_id(self, uuid: UUID) -> Recipe | None:
        original_recipe = self.db.query(RecipeDB.original_recipe).filter(RecipeDB.uuid == str(uuid)).scalar()
        if original_recipe is None: return None
        return Recipe.model_validate(original_recipe)

    def get_uuid_by_url(self, url: str) -> UUID | None:
        recipe_uuid = self.db.query(RecipeDB.uuid).filter(RecipeDB.url == url).scalar()
        if recipe_uuid is None: return None
        uuid_string = str(recipe_uuid.uuid)
        return UUID(uuid_string)

    def save(self, generated_recipe: Recipe, original_recipe: Recipe) -> UUID:
        uuid = uuid4()
        recipe_db = RecipeDB(
            uuid = str(uuid),
            url = original_recipe.url,
            generated_recipe = generated_recipe.model_dump(mode="json"),
            original_recipe = original_recipe.model_dump(mode="json")
        )
        self.db.add(recipe_db)
        self.db.commit()
        return uuid