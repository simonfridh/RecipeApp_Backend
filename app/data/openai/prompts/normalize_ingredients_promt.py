from textwrap import dedent
from openai.types.responses import EasyInputMessageParam

from app.data.openai.schemas.IngredientList import IngredientList


def normalize_ingredients_prompt(ingredients: IngredientList) -> list[EasyInputMessageParam]:
    return [
        {
            "role": "developer",
            "content": dedent(
                """
                Normalize this ingredient list for nutrition database lookup.

                Rules for "raw_string":
                    - Preserve "raw_string" exactly.

                Rules for "name":
                    - "name" must be optimized for USDA FoodData Central lookup.
                    - "name" should be a canonical name for the ingredient.
                    - Translate to English.
                    - Use lowercase USDA-friendly search names, not display names.
                    - For fresh whole produce use USDA-style plural names and append ", raw". Examples:
                      onion -> onions, raw
                      tomato -> tomatoes, raw
                      potato -> potatoes, raw
                      carrot -> carrots, raw
                      mushroom -> mushrooms, raw
                      strawberry -> strawberries, raw
                    - Do not add "raw" to spices, condiments, dairy, or branded/processed foods.
                    - Keep meaningful descriptors that affect nutrition/matching:
                    
                "name" examples:
                - "2 garlic cloves, minced" -> "garlic, raw"
                - "1 large onion, diced" -> "onions, raw"
                - "2 carrots, chopped" -> "carrots, raw"
                - "400g canned tomatoes" -> "tomatoes, canned"
                - "500g ground beef" -> "ground beef"
                - "2 dl greek yoghurt" -> "greek yoghurt"
                - "1 cup rice" -> "rice"
                - "1 cup brown rice" -> "brown rice"
                - "2 chicken breasts" -> "chicken breast"
                - "1 tbsp olive oil" -> "olive oil"

                Rules for "quantity":
                    - Keep existing "quantity" unless clearly wrong.
                    - If missing, extract it from "raw_string".
                    - Normalize number words and fractions to numeric values when possible.

                Rules for "unit":
                    - Keep existing "unit" unless clearly wrong.
                    - If missing, extract it from "raw_string".
                    - Standardize to common English units such as:
                      g, kg, ml, l, dl, tsp, tbsp, cup, clove, slice, can, bunch
                    - If the ingredient has no clear unit the field should be set to null.

                Rules for "grams_estimate":
                    - Estimate the total edible ingredient weight in grams.
                    - Use realistic cooking estimates.
                    - If highly uncertain, approximate the amount based on recipe context.
                """
            ).strip()
        },
        {
            "role": "user",
            "content": ingredients.model_dump_json(indent=2)
        }
    ]
