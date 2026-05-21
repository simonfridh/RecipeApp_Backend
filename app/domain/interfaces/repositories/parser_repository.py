from typing import Protocol

from app.domain.models.recipe import Recipe


class ParserRepository(Protocol):
    def parse(self, url:str) -> Recipe:
        ...