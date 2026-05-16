from fastapi import Depends
from sqlalchemy.orm import Session
from functools import lru_cache

from app.data.database.database import session_local
from app.data.database.recipe_repository import RecipeRepository
from app.data.parsers.json_ld.json_ld_parser import JsonLdParser
from app.domain.interfaces.i_parser import IParser
from app.domain.interfaces.i_recipe_repository import IRecipeRepository
from app.domain.services.recipe_service import RecipeService

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

def get_recipe_repository(
        db: Session = Depends(get_db),
) -> IRecipeRepository:
    return RecipeRepository(db)

def get_parser() -> IParser:
    return JsonLdParser()

def get_recipe_service(
    parser: IParser = Depends(get_parser),
    recipe_repository: IRecipeRepository = Depends(get_recipe_repository)
):
    return RecipeService(parser,recipe_repository)


