from app.data.openai.prompts.embeddingprompt import create_embedding_prompt
from app.data.openai.prompts.normalize_ingredients_promt import normalize_ingredients_prompt
from app.data.openai.prompts.recipe_prompt import create_recipe_prompt
from app.data.openai.schemas.IngredientList import IngredientList
from app.domain.interfaces.repositories.ai_repository import AiRepository
from openai import OpenAI

from app.domain.models.recipe.recipe import Recipe


class OpenAiRepository(AiRepository):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)


    def generate_new_recipe(self, recipe: Recipe) -> Recipe:
        prompt = create_recipe_prompt(recipe)

        response = self.client.responses.parse(
            model="gpt-5.4-mini",
            input=prompt,
            text_format=Recipe
        )

        generated_recipe = response.output_parsed
        if generated_recipe is None:
            raise ValueError("No recipe returned from OpenAI")

        return generated_recipe

    def create_embedding(self, recipe: Recipe) -> list[float]:
        prompt = create_embedding_prompt(recipe)
        embedding_response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=prompt,
        )
        return embedding_response.data[0].embedding


    def normalize_ingredients(self, recipe:Recipe) -> Recipe:
        prompt = normalize_ingredients_prompt(IngredientList(ingredients=recipe.ingredients))
        response = self.client.responses.parse(
            model="gpt-5.4-mini",
            input=prompt,
            text_format=IngredientList
        )
        normalized_ingredients = response.output_parsed
        if normalized_ingredients is None:
            raise ValueError("No ingredients returned from OpenAI")

        return recipe.model_copy(
            update={"ingredients": normalized_ingredients.ingredients}
        )
