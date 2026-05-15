import json
from typing import Any
from bs4 import BeautifulSoup

from app.data.parsers.json_ld.mapper import schema_org_recipe_mapper
from app.domain.interfaces.i_parser import IParser
from app.domain.models.recipe import Recipe


class JsonLdParser(IParser):
    def parse(self, html: str) -> Recipe:
        recipe_json: dict[str, Any] | None = None
        soup = BeautifulSoup(html, "html.parser")

        scripts = soup.find_all("script", type="application/ld+json")
        print(scripts)
        for script in scripts:

            jsonld = json.loads(script.text)
            if isinstance(jsonld, dict):
                recipe_type = jsonld.get("@type")

                if ((isinstance(recipe_type, str) and recipe_type == "Recipe")
                        or isinstance(recipe_type, list) and "Recipe" in recipe_type):
                    recipe_json = jsonld
                    break

        if recipe_json is None:
            raise Exception("No recipe-json found")

        return schema_org_recipe_mapper(recipe_json)