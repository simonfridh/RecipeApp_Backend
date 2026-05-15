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

        for script in scripts: # loop through results since there could be more scripts of type LD+JSON
            recipe_json = _find_recipe_json(json.loads(script.text))
            if recipe_json is not None: break # stop after finding first recipe json

        if recipe_json is None:
            raise Exception("No recipe-json found")

        return schema_org_recipe_mapper(recipe_json)


# this function handles some variations of json structure i have found
def _find_recipe_json(item: Any) -> dict | None:
    if isinstance(item, dict):
        # recipe json found
        if has_type(item, "Recipe"):
            return item

        # @graph found that contains other nested schema.org jsons
        graph = item.get("@graph")
        if graph is not None:
            return _find_recipe_json(graph)

    elif isinstance(item, list):
        for list_item in item:
            # check if any item in the list contains a recipe json
            recipe_json = _find_recipe_json(list_item)

            if recipe_json is not None:
                return recipe_json

    return None

# private function to check for schema.org type in a ld+json
# this function also checks for lists of types which appear on some websites. for example: @type: ["recipe","article"]
def has_type(item: dict[str, Any], schema_type: str) -> bool:
    item_type = item.get("@type")
    if isinstance(item_type, str):
        return item_type == schema_type
    if isinstance(item_type, list):
        return schema_type in item_type
    return False