import json
from bs4 import BeautifulSoup

from app.domain.interfaces.i_parser import IParser
from app.domain.models.ingredient import Ingredient
from app.domain.models.recipe import Recipe


class JsonLdParser(IParser):
    def parse(self, html: str) -> Recipe:


        return Recipe(
            name="test",
            ingredients=[],
            instructions=[],
        )
