from fastapi import Depends
from functools import lru_cache

from app.data.parsers.json_ld.json_ld_parser import JsonLdParser
from app.domain.interfaces.i_parser import IParser
from app.domain.services.recipe_service import RecipeService


def get_parser() -> IParser:
    return JsonLdParser()

def get_recipe_service(
    parser: IParser = Depends(get_parser),
):
    return RecipeService(parser)


