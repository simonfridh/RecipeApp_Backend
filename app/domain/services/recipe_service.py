from app.data.fetch_html import fetch_html
from app.domain.interfaces.i_parser import IParser


class RecipeService:
    def __init__(
            self,
            parser: IParser
    ):
        self.parser = parser

    def get_recipe(self, recipe_id):
        if recipe_id == "1": return {
            "title": "hello world",
            "ingredients": [
                {
                    "name": "ingrediens A",
                    "amount": 1
                },
                {
                    "name": "ingrediens B",
                    "amount": 2
                }
            ],
            "instructions": [
                "cook food",
                "eat food",
                "???",
                "profit"
            ]
        }
        return {
            "title": "NYI",
            "ingredients": [],
            "instructions": [],
        }

    def optimize_recipe(self, url):
        html = fetch_html(url)
        return self.parser.parse(html, url)

