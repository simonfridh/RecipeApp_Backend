from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.data.database.database import session_local
from app.data.database.sqlite_repository import SQLiteRepository
from app.data.parsers.html.html_fetcher import HTMLFetcher
from app.data.parsers.json_ld.json_ld_parser import JsonLdParser
from app.data.parsers.multi_parser_repository import MultiParserRepository
from app.domain.interfaces.repositories.db_repository import DbRepository
from app.domain.interfaces.repositories.parser_repository import ParserRepository
from app.domain.services.recipe_service import RecipeService

#Database (should not be singleton)
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

def get_recipe_repository(
        db: Session = Depends(get_db),
) -> DbRepository:
    return SQLiteRepository(db)


#Parsers (singleton)
@lru_cache
def get_multi_parser_repository() -> ParserRepository:
    return MultiParserRepository(
        html_fetcher = HTMLFetcher(),
        parsers=[JsonLdParser()]
    )

#Service (should not be singleton, since it depends on db)
def get_recipe_service(
    parser_repository: ParserRepository = Depends(get_multi_parser_repository),
    recipe_repository: DbRepository = Depends(get_recipe_repository)
):
    return RecipeService(parser_repository,recipe_repository)


