from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.data.database.database import session_local
from app.data.database.sqlite_repository import SQLiteRepository
from app.data.openai.openai_repository import OpenAiRepository
from app.data.parsers.html.html_fetcher import HTMLFetcher
from app.data.parsers.json_ld.json_ld_parser import JsonLdParser
from app.data.parsers.multi_parser_repository import MultiParserRepository
from app.data.usda.usda_repository import UsdaRepository
from app.domain.interfaces.repositories.ai_repository import AiRepository
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.interfaces.repositories.nutrition_repository import NutritionRepository
from app.domain.interfaces.repositories.parser_repository import ParserRepository
from app.domain.services.evaluation_service import EvaluationService
from app.domain.services.recipe_service import RecipeService
from app.settings import Settings


#Settings (singleton)
@lru_cache
def get_settings() -> Settings:
    return Settings()


#Ai repository (singleton)
@lru_cache
def get_ai_repository() -> AiRepository:
    settings = get_settings()
    return OpenAiRepository(settings.openai_api_key)


#Nutrition Repository (singleton)
@lru_cache
def get_nutrition_repository() -> NutritionRepository:
    settings = get_settings()
    return UsdaRepository(settings.usda_api_key)


#Parsers (singleton) TODO: Add fallback parsers if Json+Ld Fails
@lru_cache
def get_multi_parser_repository() -> ParserRepository:
    return MultiParserRepository(
        html_fetcher = HTMLFetcher(),
        parsers=[JsonLdParser()]
    )


#Database (should not be singleton because of transactions and sessions)
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

def get_db_repository(
        db: Session = Depends(get_db),
) -> DbRepository:
    return SQLiteRepository(db)


#Recipe Generation Service (should not be singleton, since it depends on db)
def get_recipe_service(
    parser_repository: ParserRepository = Depends(get_multi_parser_repository),
    db_repository: DbRepository = Depends(get_db_repository),
    ai_repository: AiRepository = Depends(get_ai_repository),
    nutrition_repository: NutritionRepository = Depends(get_nutrition_repository)
):
    return RecipeService(parser_repository, db_repository, ai_repository, nutrition_repository)


#Evaluation service (same here, uses db)
def get_evaluation_service(
        db_repository: DbRepository = Depends(get_db_repository),
        nutrition_repository: NutritionRepository = Depends(get_nutrition_repository)
):
    return EvaluationService(db_repository,nutrition_repository)


