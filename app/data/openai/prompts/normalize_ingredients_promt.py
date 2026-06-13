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
                    - "name" may not include alternative ingredients for example "chicken or turkey"
                    - Translate to English.
                    - Use lowercase USDA-friendly search names, not display names.
                    - For fresh whole produce use USDA-style plural names and append ", raw". Examples:
                      onion -> onions, raw
                      tomato -> tomatoes, raw
                      potato -> potatoes, raw
                      carrot -> carrots, raw
                    - Do not add "raw" to spices, condiments, dairy, legumes, processed foods or branded foods.
                    
                    "name" examples:
                    - "5 cherry tomatoes" -> "tomatoes, raw"
                    - "2 garlic cloves, minced" -> "garlic, raw"
                    - "1 large onion, diced" -> "onions, raw"
                    - "2 carrots, chopped" -> "carrots, raw"
                    - "500g ground beef" -> "ground beef"
                    - "2 dl greek yoghurt" -> "greek yoghurt"
                    - "1 cup rice" -> "rice"
                    - "1 cup brown rice" -> "brown rice"
                    - "2 chicken breasts" -> "chicken breast"
                    - "1 tbsp olive oil" -> "olive oil"
                    - "4 portions whole wheat spaghetti" -> "whole wheat spaghetti"
                    - "250g lentils" -> "lentils"

                    Rules for "quantity":
                    - Normalize number words and fractions to numeric values.
    
                    Rules for "unit":
                    - Standardize to common English units such as:
                      g, kg, ml, l, dl, tsp, tbsp, cup, clove, slice, can, bunch
                    - If the ingredient has no clear unit the field should be set to null
    
                    Rules for "grams_estimate":
                    - Estimate the ingredient weight in grams.
                    - Use realistic estimates based on the recipe context.
                    - If no quantity is present estimate weight based on recipe context.
                    - Ingredients with no impact on nutritional values should be set to null.
                    Examples of low impact ingredients:
                        - Water
                        - Spices with no quantity like salt or black pepper.
                """
            ).strip()
        },
        {
            "role": "user",
            "content": ingredients.model_dump_json(indent=2)
        }
    ]
