from app.domain.interfaces.repositories.ai_repository import AiRepository
from openai import OpenAI

from app.domain.models.recipe import Recipe


class OpenAiRepository(AiRepository):
    def __init__(self, api_key: str):
        self.api_key = api_key


    def generate_new_recipe(self, recipe: Recipe):
        print("this key will be used: " + self.api_key)