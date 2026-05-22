from uuid import UUID, uuid4

from sqlalchemy import JSON
from sqlalchemy.orm import Session

from app.data.database.tables.recipe_db import RecipeDB
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.models.recipe import Recipe


class SQLiteRepository(DbRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, uuid: UUID) -> Recipe | None:
        recipe_db = self.db.query(RecipeDB).filter(RecipeDB.uuid == str(uuid)).first()
        if recipe_db is None: return None
        return Recipe.model_validate(recipe_db.generated_recipe)


    def get_uuid_by_url(self, url: str) -> UUID | None:
        recipe_db = self.db.query(RecipeDB).filter(RecipeDB.url == url).first()
        if recipe_db is None: return None
        uuid_string = str(recipe_db.uuid)
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