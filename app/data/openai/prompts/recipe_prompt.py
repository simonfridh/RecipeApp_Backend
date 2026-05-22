from textwrap import dedent

from openai.types.responses import EasyInputMessageParam

from app.domain.models.recipe import Recipe


def create_recipe_prompt(recipe: Recipe) -> list[EasyInputMessageParam]:
    return [
        {
            "role": "developer",
            "content": dedent(
                """
                You are a professional nutritionist and chef.
                Create a healthier version of the provided recipe.

                Requirements:
                - Retain similar taste and texture to the original recipe.
                - Improve nutritional quality.
                - Keep ingredient substitutions practical.
                - Keep preparation realistic for home cooking.
                - Preserve the original recipe URL.
                """
            ).strip()
        },
        {
            "role": "user",
            "content": recipe.model_dump_json(indent=2)
        }
    ]

