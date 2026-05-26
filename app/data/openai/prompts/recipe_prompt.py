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
                
                Ingredient requirements:
                - Preserve "raw_string" as a human-readable ingredient line.
                - Preserve original language for "raw_string"
                - "name" must be English, lowercase, singular, and contain only the core ingredient.
                - Keep ingredient naming consistent.
                - Include "grams_estimate" when reasonably possible.
                - Use null for uncertain values.
                
                Nutrition requirements:
                - Estimate nutrition values for the generated recipe.
                - Use realistic nutritional estimates based on the ingredients.
                """
            ).strip()
        },
        {
            "role": "user",
            "content": recipe.model_dump_json(indent=2)
        }
    ]

