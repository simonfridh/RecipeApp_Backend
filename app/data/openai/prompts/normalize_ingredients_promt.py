from textwrap import dedent
from openai.types.responses import EasyInputMessageParam

from app.data.openai.schemas.IngredientList import IngredientList


def normalize_ingredients_prompt(ingredients: IngredientList) -> list[EasyInputMessageParam]:
    return [
        {
            "role": "developer",
            "content": dedent(
                """
                Normalize this ingredient list.
                
                Rules:
                - Preserve "raw_string" exactly.
                - Translate "name" to English.
                - Make "name" lowercase, singular, and only the core ingredient.
                - Remove prep words from "name".
                - Keep existing "quantity" and "unit" unless clearly wrong.
                - Estimate the ingredient weight in grams in "grams_estimate".
                - "grams_estimate" should represent the total ingredient amount in grams.
                - Use reasonable cooking estimates.
                - If estimation is highly uncertain, approximate the amount based on the context the ingredient is used in.
                """
            ).strip()
        },
        {
            "role": "user",
            "content": ingredients.model_dump_json(indent=2)
        }
    ]
