from typing import Protocol

from app.domain.models.recipe import Recipe


class IParser(Protocol):
    def parseable(self,html:str) -> bool:
        ...

    def parse(self, html: str) -> Recipe:
        ...