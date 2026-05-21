from app.data.parsers.html.html_fetcher import HTMLFetcher
from app.domain.interfaces.parsers.recipe_parser import RecipeParser
from app.domain.interfaces.repositories.parser_repository import ParserRepository
from app.domain.models.recipe import Recipe


class MultiParserRepository(ParserRepository):
    def __init__(self, html_fetcher:HTMLFetcher, parsers: list[RecipeParser]):
        self.html_fetcher = html_fetcher
        self.parsers = parsers

    def parse(self, url: str) -> Recipe:
        html = self.html_fetcher.fetch(url)

        errors = []
        for parser in self.parsers:
            try:
                recipe = parser.parse(html,url)
                if recipe is not None:
                    return recipe
            except Exception as e:
                errors.append(e)
                continue

        #All parsers failed
        raise Exception(f"All parsers failed. Errors: ${errors}")

