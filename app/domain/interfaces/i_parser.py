from typing import Protocol

from app.domain.models.recipe import Recipe


class IParser(Protocol):
    def parse(self, html: str, url:str) -> Recipe:
        ...