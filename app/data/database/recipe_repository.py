from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.data.database.tables.recipe_db import RecipeDB
from app.domain.interfaces.i_recipe_repository import IRecipeRepository
from app.domain.models.recipe import Recipe


class RecipeRepository(IRecipeRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, uuid: UUID) -> Recipe | None:
        recipe_db = self.db.query(RecipeDB).filter(RecipeDB.uuid == str(uuid)).first()
        if recipe_db is None: return None
        return Recipe.model_validate(recipe_db.recipe)


    def get_uuid_by_url(self, url: str) -> UUID | None:
        recipe_db = self.db.query(RecipeDB).filter(RecipeDB.url == url).first()
        if recipe_db is None: return None
        uuid_string = str(recipe_db.uuid)
        return UUID(uuid_string)

    def save(self, recipe: Recipe) -> UUID:
        uuid = uuid4()
        recipe_db = RecipeDB(
            uuid = str(uuid),
            url = recipe.url,
            recipe = recipe.model_dump(mode="json")
        )
        self.db.add(recipe_db)
        self.db.commit()
        return uuid